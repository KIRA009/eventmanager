from django.views import View

from utils.tasks import cancel_subscription
from payments.utils import create_subscription
from utils.exceptions import AccessDenied


class SubscriptionView(View):
    def post(self, request):
        data = request.json
        if request.User.user_type == 'pro':
            raise AccessDenied("User is already a pro user")
        sub = create_subscription(
            data['plan_id'], data['total_count'], user=request.User, meta_data={'notes[sub_type]': data['sub_type']}
        )
        return dict(payment_url=sub.payment_url)


class CancelSubscriptionView(View):
    def post(self, request):
        data = request.json
        cancel_subscription(request.User.id, data['sub_id'])
        return dict(message="Cancelled successfully")
