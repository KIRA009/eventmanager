from django.views import View

from notifications.models import Notification
from notifications.validators import *


class GetNotificationsView(View):
	def get(self, request):
		page_no = int(request.GET.get('pageNo', 1))
		num_pages, notifications = Notification.objects.filter(user=request.User).paginate(page_no)
		return dict(num_pages=num_pages, notifications=notifications.detail())


class ReadNotificationView(View):
	@read_notification_schema
	def post(self, request):
		data = request.json
		Notification.objects.get(id=data['notif_id'], user=request.User).read()
		return dict(message="Read")
