from django.views import View
import json

from payments.utils import renew_subscription, update_subscription
from payments.models import Subscription, Order, Seller


class PaymentWebhookView(View):
    def post(self, request):
        data = request.json
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
                items = json.loads(data['payload']['payment']['entity']['notes']['items'])
                user_details = json.loads(data['payload']['payment']['entity']['notes']['user'])
                del data['payload']['payment']['entity']['notes']
                order.meta_data = dict(
                    payment=data['payload']['payment']['entity'],
                    order=data['payload']['order']['entity'],
                    user_details=user_details
                )
                seller = Seller.objects.get_or_create(user=order.items.first().order.user)[0]
                for item in order.items.all():
                    item.meta_data = items[item.index]['meta_data']
                    item.save()
                    seller.amount += int(0.97 * item.order.disc_price) - 5
                seller.save()
                order.save()
        return dict()
