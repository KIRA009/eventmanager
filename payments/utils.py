import requests
from django.utils.timezone import now, localdate, datetime
from datetime import timedelta
import pytz
from celery.task import task
import stripe
from stripe.error import InvalidRequestError

from event_manager.settings import RAZORPAY_KEY, RAZORPAY_SECRET, TIME_ZONE, PAYMENT_TEST, PAYMENT_CALLBACK_URL, \
    PAYMENT_CANCEL_URL, STRIPE_KEY
from .models import Subscription, Order, OrderItem
from utils.exceptions import NotFound, AccessDenied

BASE_URL = "https://api.razorpay.com/v1"
auth = (RAZORPAY_KEY, RAZORPAY_SECRET)
tz = pytz.timezone(TIME_ZONE)
stripe.api_key = STRIPE_KEY


def create_order(items, user):
    try:
        res = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=items,
            customer_email=user.email,
            success_url=PAYMENT_CALLBACK_URL,
            cancel_url=PAYMENT_CANCEL_URL,
        )
        return res.id
    except InvalidRequestError as e:
        raise NotFound(e.user_message)


def get_payment_intent(payment_intent):
    return stripe.PaymentIntent.retrieve(
        payment_intent
    )


def get_order(order):
    ret = dict()
    res = requests.get(f"{BASE_URL}/orders/{order.order_id}", auth=auth).json()
    ret['order'] = res
    res = requests.get(f"{BASE_URL}/orders/{order.order_id}/payments", auth=auth).json()
    ret['payment'] = res["items"][0]
    ret['user_details'] = dict(
        name=order.user.name,
        email=order.user.email,
        phone=order.user.phone
    )
    return ret


def create_subscription(plan_id, total_count, user, meta_data):
    if meta_data is None:
        meta_data = dict()
    res = requests.post(f'{BASE_URL}/subscriptions', json=dict(
        plan_id=plan_id,
        total_count=total_count,
        customer_notify=0,
        **meta_data
    ), auth=auth).json()
    if "error" in res:
        raise AccessDenied(res["error"]['description'])
    sub = Subscription.objects.create(sub_id=res['id'], sub_type=meta_data['notes[sub_type]'],
                                      payment_url=res['short_url'], user=user)
    return sub


def update_subscription(sub, order=None, start_date=None, end_date=None):
    if sub is None:
        return None
    if isinstance(start_date, int):
        sub.start_date = datetime.fromtimestamp(start_date, tz).date()
        sub.end_date = datetime.fromtimestamp(end_date, tz).date()
    else:
        sub.start_date = localdate(now())
        sub.end_date = sub.start_date + timedelta(days=30)
    sub.save()
    if order:
        order = Order(order_id=order['order_id'], amount=int(order['amount']) / 100, paid=True, user=sub.user)
        order.meta_data = get_order(order)
        order.save()
        OrderItem.objects.create(order_id=order, index=0, order=sub)
    if PAYMENT_TEST:
        sub.test = True
    sub.save()


def renew_subscription(sub_id, sub_type, start_date, end_date, order):
    sub = Subscription.objects.get(sub_id=sub_id, sub_type=sub_type)
    sub.pk = None
    update_subscription(sub, order, start_date, end_date)


@task(name='cancel_subscription')
def cancel_subscription(user_id, sub_id):
    try:
        sub = Subscription.objects.get(sub_id=sub_id, user_id=user_id, is_unsubscribed=False)
        sub.is_unsubscribed = True
        sub.save()
        requests.post(f'{BASE_URL}/subscriptions/{sub_id}/cancel', auth=auth)
    except NotFound:
        pass
