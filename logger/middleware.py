from django.middleware.common import CommonMiddleware
import traceback

from .models import Logger
from event_manager.settings import DEBUG


class ExceptionHandlerMiddleware(CommonMiddleware):
    def process_exception(self, request, exception):
        if not DEBUG:
            if 'User' in request.__dict__:
                user = request.User
            else:
                user = request.user
            Logger.objects.create(trace=traceback.format_exc(), msg=exception, user=user)
        return dict(error="Server error", status_code=500)
