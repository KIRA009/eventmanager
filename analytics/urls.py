from django.urls import path

from .views import *
from utils.decorators import login_required

unauth_urls = list(
    map(lambda x: path(x[0], x[1].as_view()), [
        ("click/", AddClickView),
        ("view/", AddViewView),
    ])
)

auth_urls = list(
    map(lambda x: path(x[0], login_required(x[1].as_view())), [
        ("get_clicks/", GetLinkData),
        ("get_views/", GetProfileViewData)
    ])
)

urlpatterns = unauth_urls + auth_urls
