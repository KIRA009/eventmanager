from django.urls import path

from utils.decorators import login_required
from .views import *

auth_urls = list(
    map(
        lambda x: path(x[0], login_required(x[1].as_view())),
        [
            ("get/", GetNotificationsView),
            ("read/", ReadNotificationView)
        ],
    )
)

urlpatterns = auth_urls
