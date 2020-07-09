from django.middleware.common import CommonMiddleware
import traceback

from .models import ServerTracker
from event_manager.settings import DEBUG
from .utils import send_email_to_admins


class ExceptionHandlerMiddleware(CommonMiddleware):
    def process_exception(self, request, exception):
        if 'User' in request.__dict__:
            user = request.User
        else:
            user = request.user if request.user.is_authenticated else None
        _vars = {
            'route': request.path_info,
            'error': traceback.format_exc()
        }
        if user:
            _vars['email'] = user.email
            _vars['phone'] = user.phone
        else:
            _vars['email'] = 'Anonymous'
            _vars['phone'] = 'nil'
        if 'status_code' in exception.__dict__:
            return dict(error=exception.message, status_code=exception.status_code)
        log = ServerTracker(trace=traceback.format_exc(), msg=exception, user=user, url=request.path_info)
        if 'json' in request.__dict__ and request.method not in 'GET':
            log.request_body = request.json
        log.save()
        if DEBUG:
            print(traceback.format_exc())
            try:
                print(request.json)
            except AttributeError:
                pass
        else:
            send_email_to_admins('error', 'Error', **_vars)
        return dict(error="Server error", status_code=500)
