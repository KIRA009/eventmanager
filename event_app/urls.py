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
            ("validate-email/", SendValidateEmailView),
            ("validate/<int:user_id>/<uuid:secret>/", CompleteValidateEmailView),
            ("user/", GetUserView),
        ],
    )
)

auth_urls = list(
    map(
        lambda x: path(x[0], x[1].as_view()),
        [("upload/profile/", UploadProfilePicView), ("links/", UserLinkView)],
    )
)

urlpatterns = unauth_urls + auth_urls
