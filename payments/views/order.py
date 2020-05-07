from django.views import View
import json
from django.shortcuts import redirect

from payments.models import Order, OrderItem
from payments.utils import create_order, is_signature_safe, get_order, handle_order, create_order_form
from event_manager.settings import PAYMENT_REDIRECT_URL


class OrderView(View):
    def get(self, request):
        return dict(orders=request.User.orders.all().detail())

    def post(self, request):
        data = request.json
        amount = 0
        items = []
        order_id = create_order(amount)
        order = Order.objects.create(
            order_id=order_id, amount=amount, user=request.User, meta_data=""
        )
        items = [OrderItem(order=item, order_id=order, index=i) for i, item in enumerate(items)]
        OrderItem.objects.bulk_create(items)
        return dict(
            form=create_order_form(order, json.dumps(data['items']))
        )


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
