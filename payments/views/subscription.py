from django.views import View

from utils.tasks import cancel_subscription
from utils.exceptions import AccessDenied


class SubscriptionView(View):
    def post(self, request):
        data = request.json
        if request.User.user_type == 'pro':
            raise AccessDenied("User is already a pro user")
        return dict(payment_url='abc')


class CancelSubscriptionView(View):
    def post(self, request):
        data = request.json
        cancel_subscription(request.User.id, data['sub_id'])
        return dict(message="Cancelled successfully")
