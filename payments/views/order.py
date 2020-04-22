from django.views import View
import json
from django.shortcuts import redirect

from payments.models import Order, OrderItem
from payments.utils import create_order, is_signature_safe, get_order
from event_manager.settings import RAZORPAY_MID
from event_app.models import ProPack


class OrderView(View):
    def post(self, request):
        pack = ProPack.objects.get()
        amount = pack.price
        created, order_id = create_order(amount)
        if created:
            order = Order.objects.create(
                order_id=order_id, amount=amount, user=request.User, meta_data=""
            )
        else:
            return dict(error=order_id["description"], status_code=404)
        OrderItem.objects.create(order=pack, order_id=order)
        return dict(
            form={
                "url": "https://api.razorpay.com/v1/checkout/embedded",
                "fields": {
                    "key_id": RAZORPAY_MID,
                    "order_id": order_id,
                    "name": "MyWork",
                    "image": "https://cdn.razorpay.com/logos/BUVwvgaqVByGp2_large.png",
                    "prefill[name]": order.user.name,
                    "prefill[contact]": order.user.phone,
                    "prefill[email]": order.user.email,
                    "callback_url": "https://extremist.team/event_manager/api/callback/",
                },
            }
        )


class OrderCallBackView(View):
    def post(self, request):
        data = request.POST.dict()
        order = Order.objects.get(order_id=data["razorpay_order_id"])
        if is_signature_safe(data):
            order.paid = True
            order.payment_id = data["razorpay_payment_id"]
            order.signature = data["razorpay_signature"]
            order.meta_data = json.dumps(get_order(order.order_id))
            order.user.user_type = "pro"
            order.user.save()
            order.save()
        return redirect("https://extremist.team/event_manager/")
