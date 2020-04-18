from django.urls import path

from .views import *

unauth_urls = list(
    map(lambda x: path(x[0], x[1].as_view()), [("click/", AddClickView)])
)

urlpatterns = unauth_urls
