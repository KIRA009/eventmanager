import requests
import sys
import hmac
import hashlib
from django.utils.timezone import now, localdate, datetime
from datetime import timedelta
import pytz
from celery.task import task
import uuid
import os
from collections import namedtuple

from event_manager.settings import RAZORPAY_KEY, RAZORPAY_SECRET, TIME_ZONE, PAYMENT_TEST, BASE_DIR,\
    RAZORPAY_WEBHOOK_SECRET
from .models import Subscription, Order, OrderItem
from utils.exceptions import NotFound, AccessDenied
from pro.models import Product
from event_app.models import User
from marketing.models import Onboard
from notifications.utils import create_notification

BASE_URL = "https://api.razorpay.com/v1"
auth = (RAZORPAY_KEY, RAZORPAY_SECRET)
tz = pytz.timezone(TIME_ZONE)


def create_order_in_razorpay(amount):
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


def create_order(order_items, mode, user_details, seller):
    seller_orders = dict(items=[], amount=0, shipping_charges=0)
    reseller_orders = {}
    for item in order_items:
        if item["type"] == "product":
            prod = Product.objects.select_related('user__seller').get(id=item["id"])
            original_seller_id = prod.user.seller.id
            if prod.sizes_available:
                it = prod.sizes.get(size=item['meta_data']['size'])
            else:
                it = prod
            if it.stock < int(item['meta_data']['quantity']):
                if isinstance(it, Product):
                    raise AccessDenied(f'{it.name} has less stock than requested')
                raise AccessDenied(f'Size {it.size} of {prod.name} has less stock than requested')
            if original_seller_id != seller.id:
                seller.resell_product.get(product=prod)
                if original_seller_id not in reseller_orders:
                    reseller_orders[original_seller_id] = dict(
                        items=[], amount=0, shipping_charges=0, resell_margin=0
                    )
                reseller_orders[original_seller_id]['items'].append(
                    (prod, item['meta_data'])
                )
                reseller_orders[original_seller_id]['amount'] += it.disc_price
                reseller_orders[original_seller_id]['shipping_charges'] = max(
                    reseller_orders[original_seller_id]['shipping_charges'], prod.shipping_charges
                )
                reseller_orders[original_seller_id]['resell_margin'] += it.resell_margin
            else:
                seller_orders['items'].append(
                    (prod, item['meta_data'])
                )
                seller_orders['amount'] += it.disc_price
                seller_orders['shipping_charges'] = max(seller_orders['shipping_charges'], prod.shipping_charges)
    if seller_orders['amount'] == 0 and not reseller_orders:
        return None, None
    _User = namedtuple('_User', ['email', 'phone', 'name'])
    user = User.objects.filter(email=user_details['email']).first()
    if not user:
        user = _User(email=user_details['email'], phone=user_details['number'], name=user_details['name'])
    if mode == 'cod':
        order_id = str(uuid.uuid4())
    else:
        order_id = create_order_in_razorpay(seller_orders['amount'] +
                                            sum(i['amount'] for i in reseller_orders.values()))
    if seller_orders['items']:
        order = Order.objects.create(
            order_id=order_id, amount=seller_orders['amount'], user=user if isinstance(user, User) else None,
            meta_data=dict(user_details=user_details), cod=(mode == 'cod'),
            shipping_charges=seller_orders['shipping_charges'],
            seller=seller, resell_margin=0
        )
        items = [
            OrderItem(order=item[0], order_id=order, index=i, meta_data=item[1])
            for i, item in enumerate(seller_orders['items'])
        ]
        OrderItem.objects.bulk_create(items)
    for seller_id, order in reseller_orders.items():
        _order = Order.objects.create(
            order_id=order_id, amount=order['amount'], user=user if isinstance(user, User) else None,
            meta_data=dict(user_details=user_details), cod=(mode == 'cod'),
            shipping_charges=order['shipping_charges'],
            seller_id=seller_id, resell_margin=order['resell_margin'], reseller=seller
        )
        items = [
            OrderItem(order=item[0], order_id=_order, index=i, meta_data=item[1])
            for i, item in enumerate(order['items'])
        ]
        OrderItem.objects.bulk_create(items)
    return order_id, user


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


@task(name='handle_order')
def handle_order(data):
    orders = Order.objects.filter(order_id=data['payload']['order']['entity']['id'])
    if not orders:
        return
    for ind, order in enumerate(list(orders)):
        if not order.paid:
            order.paid = True
            order.status = Order.PROCESSED
            order.meta_data['payment'] = data['payload']['payment']['entity']
            order.meta_data['order'] = data['payload']['order']['entity']
            order.save()
            seller = order.seller
            for item in order.items.all():
                prod = item.order
                prod.update_last_interaction()
                if prod.sizes_available:
                    prod = prod.sizes.get(size=item.meta_data['size'])
                prod.stock -= int(item.meta_data['quantity'])
                prod.save()
            if order.cod:
                percent = seller.commission['online']['percent'] * 0.01
                extra = seller.commission['online']['extra']
                seller.amount -= int(percent * (order.amount - order.resell_margin)) + extra
            else:
                percent = (100 - seller.commission['online']['percent']) * 0.01
                extra = seller.commission['online']['extra']
                seller.amount += int(percent * (order.amount - order.resell_margin)) - extra
            seller.save()
            if order.reseller:
                order.reseller.amount += order.resell_margin
                order.reseller.save()
            send_invoice(order, seller)
            send_text_update(order)
            distribute_money_to_managers(seller, order.amount - order.resell_margin)
            item_nums = order.items.count() - 1
            create_notification(
                seller.user, f'New order placed on {order.created_at.isoformat().split("T")[1][:8]}, '
                             f'{order.created_at.isoformat().split("T")[0]}',
                f'An order for {order.items.first().order.name}'
                f' {"+ " + str(item_nums) + " others" if item_nums > 0 else ""} has been placed successfully. The total'
                f' amount is Rs. {order.amount}',
                dict(order_id=order.order_id)
            )


def distribute_money_to_managers(seller, amount):
    onboard = Onboard.objects.filter(onboarder=seller.user).first()
    amount = (seller.commission['online']['percent'] - 2) * 0.01 * amount + seller.commission['online']['extra']
    i = 0
    while onboard and i < 6:
        onboard.amount += 0.2 * amount / (2 ** i)
        onboard.save()
        onboard = Onboard.objects.filter(onboarder=onboard.marketeer).first()
        i += 1


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


def send_invoice(order, seller):
    from utils.tasks import send_email
    with open(os.path.join(BASE_DIR, 'payments', 'invoice_templates', 'order_invoice.html')) as f:
        html = f.read()
    details = dict(
        order_id=order.id,
        created_at=order.created_at.isoformat().split('T')[0],
        name=order.meta_data['user_details']['name'],
        phone=order.meta_data['user_details']['number'],
        email=order.meta_data['user_details']['email'],
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


def send_text_update(order):
    from utils.tasks import send_message
    status = {
        Order.PROCESSED: 'placed successfully and is being processed',
        Order.CONFIRMED: 'confirmed by the merchant',
        Order.SHIPPED: 'shipped',
        Order.DELIVERED: 'delivered',
        Order.REFUND_INITIATED: 'initiated for refund',
        Order.REFUNDED: 'refunded',
    }
    statuses = [
        Order.PROCESSED, Order.CONFIRMED, Order.SHIPPED, Order.DELIVERED, Order.REFUND_INITIATED, Order.REFUNDED
    ]
    item = order.items.first().order
    item_nums = order.items.count() - 1
    message = f'Hi! Your myweblink order for {item.name} ' \
              f'{"+ " + str(item_nums) + " others" if item_nums > 0 else ""} has been {status[order.status]}.'
    if order.status not in [Order.DELIVERED, Order.REFUNDED]:
        message += f" We will send you an update when your order is " \
                   f"{status[statuses[statuses.index(order.status) + 1]]}"
    send_message(order.meta_data['user_details']['number'], message)


@task(name='refund_order')
def refund_order(order_id, seller_id):
    order = Order.objects.get(order_id=order_id, seller_id=seller_id)
    if 'payment' not in order.meta_data:
        return
    res = requests.post(f'{BASE_URL}/payments/{order.meta_data["payment"]["id"]}/refund',
                        json={'amount': order.amount * 100, 'notes': dict(order_id=order_id)}, auth=auth).json()
    if 'error' not in res:
        order.update_status(Order.REFUND_INITIATED)
