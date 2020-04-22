from django.urls import path

from .views import *
from utils import login_required

auth_urls = list(
    map(lambda x: path(x[0], login_required(x[1].as_view())), [("order/", OrderView)])
)

unauth_urls = list(
    map(lambda x: path(x[0], x[1].as_view()), [("callback/", OrderCallBackView)])
)

urlpatterns = auth_urls + unauth_urls
