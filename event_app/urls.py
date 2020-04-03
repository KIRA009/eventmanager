from django.urls import path

from .views import *
from utils import is_admin

unauth_urls = list(
    map(
        lambda x: path(x[0], x[1].as_view()),
        [
            ("register/", RegisterView),
            ("update/", UpdateView),
            ("colleges/", CollegeView),
            ("login/", LoginView),
            ("check/", CheckView),
        ],
    )
)

admin_urls = list(map(lambda x: path(x[0], is_admin(x[1].as_view())), []))

urlpatterns = unauth_urls + admin_urls
