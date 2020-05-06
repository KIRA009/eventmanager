from django.urls import path

from utils.decorators import login_required
from .utils import pro_required
from .views import *

unauth_urls = list(
    map(
        lambda x: path(x[0], x[1].as_view()),
        [
            ("feature/", ProModeView),
            ("background/get/", GetBgView),
        ],
    )
)

pro_urls = list(
    map(
        lambda x: path(x[0], pro_required(login_required(x[1].as_view()))),
        [
            ("feature/header/", ProModeHeaderView),
            ('background/set/', SetBgView),
        ],
    )
)

urlpatterns = unauth_urls + pro_urls
