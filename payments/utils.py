import requests
import sys
import hmac
import hashlib
from django.utils.timezone import now, localdate, datetime
from datetime import timedelta
import pytz
from celery.task import task
import stripe
from stripe.error import InvalidRequestError
import os
import json

from event_manager.settings import RAZORPAY_KEY, RAZORPAY_SECRET, TIME_ZONE, PAYMENT_TEST, PAYMENT_CALLBACK_URL, \
    PAYMENT_CANCEL_URL, BASE_DIR, RAZORPAY_WEBHOOK_SECRET
from .models import Subscription, Order, OrderItem, Seller
from utils.exceptions import NotFound, AccessDenied

BASE_URL = "https://api.razorpay.com/v1"
auth = (RAZORPAY_KEY, RAZORPAY_SECRET)
tz = pytz.timezone(TIME_ZONE)


def create_order(amount):
    res = requests.post(
        f"{BASE_URL}/orders",
        json={
            "amount": amount * 100,
            "currency": "INR",
            "receipt": "receipt",
            "payment_capture": 1,
        },
        auth=auth,
    ).json()
    if "error" in res:
        raise NotFound(res["error"]["description"])
    return res["id"]


def compare_string(expected_str, actual_str):
    if len(expected_str) != len(actual_str):
        return False
    result = 0
    for x, y in zip(expected_str, actual_str):
        result |= ord(x) ^ ord(y)
    return result == 0


def verify_webhook_signature(request):
    if sys.version_info[0] == 3:  # pragma: no cover
        key = bytes(RAZORPAY_WEBHOOK_SECRET, "utf-8")
        body = bytes(request.body.decode(), "utf-8")
    razorpay_signature = request.headers['x-razorpay-signature']
    dig = hmac.new(key=key, msg=body, digestmod=hashlib.sha256)

    generated_signature = dig.hexdigest()
    if sys.version_info[0:3] < (2, 7, 7):
        result = compare_string(generated_signature, razorpay_signature)
    else:
        result = hmac.compare_digest(generated_signature, razorpay_signature)

    if not result:
        return False
    return True


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


def get_plan(plan_id):
    res = requests.get(f"{BASE_URL}/plans/{plan_id}", auth=auth).json()
    if 'error' in res:
        return True, res['error']
    return False, res


def create_plan(pack):
    res = requests.post(f'{BASE_URL}/plans', auth=auth, json=dict(
        period=pack.period,
        interval=1,
        item=dict(
            name=f"Pro pack - {pack.period}",
            amount=pack.price * 100,
            currency=pack.currency,
        )
    )).json()
    return res


def handle_order(order, query):
    pass


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


def create_order_form(order_id, user):
    return {
        "url": "https://api.razorpay.com/v1/checkout/embedded",
        "fields": {
            "key_id": RAZORPAY_KEY,
            "order_id": order_id,
            "name": "MyWebLink",
            "prefill[name]": user.name,
            "prefill[contact]": user.phone,
            "prefill[email]": user.email,
            "callback_url": 'https://myweblink.store/payment/order/callback/',
            "cancel_url": 'https://myweblink.store/payment/order/cancel/'
        },
    }


@task(name='cancel_subscription')
def cancel_subscription(user_id, sub_id):
    try:
        sub = Subscription.objects.get(sub_id=sub_id, user_id=user_id, is_unsubscribed=False)
        sub.is_unsubscribed = True
        sub.save()
        requests.post(f'{BASE_URL}/subscriptions/{sub_id}/cancel', auth=auth)
    except NotFound:
        pass


@task(name='create_invoice')
def create_invoice(order_id, seller_id):
    from utils.tasks import send_email
    order = Order.objects.get(id=order_id)
    seller = Seller.objects.get(id=seller_id)
    with open(os.path.join(BASE_DIR, 'payments', 'invoice_templates', 'order_invoice.html')) as f:
        html = f.read()
    details = dict(
        order_id=order.id,
        created_at=order.created_at.isoformat().split('T')[0],
        name=order.meta_data['user_details']['name'],
        phone=order.meta_data['user_details']['number'],
        email=order.meta_data['user_details']['email'],
        receipt=order.meta_data['payment']['receipt'],
        total=order.amount
    )
    items = ''
    for item in order.items.all():
        items += f'''
                <tr>
                    <td>{item.order.name}</td>
                    <td>{item.meta_data['quantity']}</td>
                    <td>{item.meta_data['quantity'] * item.order.disc_price}</td>
                </tr>
                '''
    details['items'] = items.replace('\n', '')
    for k, v in details.items():
        html = html.replace('{' + k + '}', str(v))
    html = html.replace('\n', '')
    send_email([seller.user.email, order.meta_data['user_details']['email']], 'Invoice', html)
