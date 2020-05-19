from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

from payments.models import Order, Seller, Subscription
from utils.tasks import create_invoice
from payments.utils import renew_subscription, update_subscription, verify_webhook_signature


@method_decorator(csrf_exempt, name="dispatch")
class PaymentWebhookView(View):
    def post(self, request):
        data = request.json
        if not verify_webhook_signature(request):
            return dict()
        if data['event'] == 'subscription.charged':
            sub = data['payload']['subscription']['entity']
            order = data['payload']['payment']['entity']
            if sub['paid_count'] > 1:
                renew_subscription(sub['id'], sub['notes']['sub_type'], sub['current_start'], sub['current_end'], order)
            else:
                subscription = Subscription.objects.get(sub_type=sub['notes']['sub_type'], sub_id=sub['id'],
                                                        start_date=None, end_date=None)
                update_subscription(subscription, order, sub['current_start'], sub['current_end'])
        elif data['event'] == 'order.paid':
            order = Order.objects.filter(order_id=data['payload']['order']['entity']['id']).first()
            if not order:
                return dict()
            if order.items.filter(content_type__model='subscription').exists():
                return dict()
            if not order.paid:
                order.paid = True
                order.meta_data['payment'] = data['payload']['payment']['entity']
                order.meta_data['order'] = data['payload']['order']['entity']
                order.save()
                seller = Seller.objects.get_or_create(user=order.items.first().order.user)[0]
                percent = (100 - seller.commission['online']['percent']) * 0.01
                extra = seller.commission['online']['extra']
                for item in order.items.all():
                    seller.amount += max(0, int(percent * item.order.disc_price) - extra)
                    item.order.stock -= int(item.meta_data['quantity'])
                    item.order.save()
                seller.save()
                create_invoice(order.id, seller.id)
        return dict()
