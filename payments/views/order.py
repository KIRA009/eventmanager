from django.views import View
import json
from django.shortcuts import redirect

from payments.models import Order, OrderItem, Subscription
from payments.utils import create_order, is_signature_safe, get_order, handle_order, create_subscription,\
    update_subscription, renew_subscription
from event_manager.settings import RAZORPAY_MID, PAYMENT_CALLBACK_URL, PAYMENT_REDIRECT_URL
from event_app.models import ProPack


class OrderView(View):
    def post(self, request):
        data = request.json
        amount = 0
        items = []
        for _item in data['items']:
            if _item['type'] == 'pro_pack':
                item = ProPack.objects.get()
                if _item['meta_data']['pack_type'] == 'monthly':
                    amount += item.monthly_price
                else:
                    amount += item.yearly_price
            items.append(item)
        created, order_id = create_order(amount)
        if created:
            order = Order.objects.create(
                order_id=order_id, amount=amount, user=request.User, meta_data=""
            )
        else:
            return dict(error=order_id["description"], status_code=404)
        items = [OrderItem(order=item, order_id=order, index=i) for i, item in enumerate(items)]
        OrderItem.objects.bulk_create(items)
        return dict(
            form={
                "url": "https://api.razorpay.com/v1/checkout/embedded",
                "fields": {
                    "key_id": RAZORPAY_MID,
                    "order_id": order_id,
                    "name": "MyWork",
                    "image": "https://cdn.razorpay.com/logos/BUVwvgaqVByGp2_large.png",
                    "notes[query]": json.dumps(data['items']),
                    "prefill[name]": order.user.name,
                    "prefill[contact]": order.user.phone,
                    "prefill[email]": order.user.email,
                    "callback_url": PAYMENT_CALLBACK_URL
                },
            }
        )


class SubscriptionView(View):
    def post(self, request):
        data = request.json
        created, sub = create_subscription(data['plan_id'], data['total_count'], user=request.User,
                                           meta_data={'notes[sub_type]': data['sub_type']})
        if created:
            return dict(payment_url=sub.payment_url)
        else:
            return dict(error=sub, status_code=401)


class PaymentWebhookView(View):
    def post(self, request):
        data = request.json
        sub = data['payload']['subscription']['entity']
        order = data['payload']['payment']['entity']
        if sub['paid_count'] > 1:
            renew_subscription(sub['id'], sub['notes']['sub_type'], sub['current_start'], sub['current_end'], order)
        else:
            subscription = Subscription.objects.get(sub_type=sub['notes']['sub_type'], sub_id=sub['id'],
                                                    start_date=None, end_date=None)
            update_subscription(subscription, order, sub['current_start'], sub['current_end'])

        return dict()


class OrderCallBackView(View):
    def post(self, request):
        data = request.POST.dict()
        order = Order.objects.get(order_id=data["razorpay_order_id"])
        if is_signature_safe(data):
            order.paid = True
            order.payment_id = data["razorpay_payment_id"]
            order.signature = data["razorpay_signature"]
            order_details = get_order(order.order_id)[0]
            order.meta_data = json.dumps(order_details)
            notes = json.loads(order_details['notes']['query'])
            for item in order.items.all():
                handle_order(item, notes[item.index])
            order.save()
        return redirect(PAYMENT_REDIRECT_URL)
