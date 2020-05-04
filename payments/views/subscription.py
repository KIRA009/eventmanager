from django.views import View

from payments.utils import create_subscription
from utils.tasks import cancel_subscription


class SubscriptionView(View):
    def post(self, request):
        data = request.json
        sub = create_subscription(data['plan_id'], data['total_count'], user=request.User,
                                  meta_data={'notes[sub_type]': data['sub_type']})
        return dict(payment_url=sub.payment_url)


class CancelSubscriptionView(View):
    def post(self, request):
        data = request.json
        cancel_subscription(request.User.id, data['sub_id'])
        return dict(message="Cancelled successfully")
