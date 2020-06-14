from django.views import View

from notifications.models import Notification


class GetNotificationsView(View):
	def get(self, request):
		page_no = int(request.GET.get('pageNo', 0))
		num_pages, notifications = Notification.objects.filter(user=request.User).paginate(page_no)
		return dict(num_pages=num_pages, notifications=notifications.detail())
