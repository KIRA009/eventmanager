from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from payments.models import Subscription, Order
from utils.tasks import handle_order
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
            handle_order(data)
        elif data['event'] == 'refund.processed':
            orders = Order.objects.filter(order_id=data['payload']['refund']['entity']['notes']['order_id'])
            for ind, order in enumerate(list(orders)):
                order.update_status(Order.REFUNDED, ind == 0)
        return dict()
