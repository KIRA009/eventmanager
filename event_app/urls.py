from django.urls import path

from .views import *

unauth_urls = list(
    map(
        lambda x: path(x[0], x[1].as_view()),
        [
            ("register/", RegisterView),
            ("update/", UpdateView),
            ("colleges/", CollegeView),
            ("login/", LoginView),
        ],
    )
)

auth_urls = list(map(lambda x: path(x[0], x[1].as_view()), []))

urlpatterns = unauth_urls + auth_urls
