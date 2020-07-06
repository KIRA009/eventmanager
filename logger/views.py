from django.views import View

from .validators import *
from event_app.models import User
from .models import ClientTracker


class LogClientErrorView(View):
	@log_client_error_schema
	def post(self, request):
		data = request.json
		try:
			data['user'] = User.objects.get(username=data['username'])
			del data['username']
			ClientTracker(**data).save()
		except User.DoesNotExist:
			pass
		return dict(message="Logged")
