from django.middleware.common import CommonMiddleware
import traceback

from .models import Tracker
from event_manager.settings import DEBUG
from .utils import send_email_to_admins


class ExceptionHandlerMiddleware(CommonMiddleware):
    def process_exception(self, request, exception):
        if not DEBUG:
            if 'User' in request.__dict__:
                user = request.User
            else:
                user = request.user
            _vars = {
                'route': request.path_info,
                'error': traceback.format_exc()
            }
            if user.is_authenticated:
                _vars['email'] = user.email
                _vars['phone'] = user.phone
            else:
                _vars['email'] = 'Anonymous'
                _vars['phone'] = 'nil'
            send_email_to_admins('error', 'Error', **_vars)
            Tracker.objects.create(trace=traceback.format_exc(), msg=exception, user=user, url=request.path_info)
        return dict(error="Server error", status_code=500)
