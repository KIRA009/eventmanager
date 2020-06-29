from django.urls import path, register_converter
from django.utils.timezone import datetime

from utils.decorators import login_required
from .views import *


class DateConverter:
    regex = '[0-9]{2}-[0-9]{2}-[0-9]{4}'
    format = '%d-%m-%Y'

    def to_python(self, value):
        return datetime.strptime(value, DateConverter.format).date()

    def to_url(self, value):
        return value.strftime(self.format)


register_converter(DateConverter, 'date')
auth_urls = list(
    map(
        lambda x: path(x[0], login_required(x[1].as_view())),
        [
            ("get/<date:date>/", GetNotificationsView),
            ("read/", ReadNotificationView)
        ],
    )
)

urlpatterns = auth_urls
