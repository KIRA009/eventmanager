from django.views import View

from payments.utils import renew_subscription, update_subscription
from payments.models import Subscription


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
