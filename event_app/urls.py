from django.urls import path

from utils.decorators import login_required
from .views import *

unauth_urls = list(
    map(
        lambda x: path(x[0], x[1].as_view(), name=x[2]),
        [
            ("register/", RegisterView, 'register'),
            ("colleges/", CollegeView, 'college'),
            ("login/", LoginView, 'login'),
            ("validate-email/", SendValidateEmailView, 'send-validate-email'),
            ("validate/<int:user_id>/<uuid:secret>/", CompleteValidateEmailView, 'complete-valdiate-email'),
            ("user/", GetUserView, 'user'),
            ('packs/', GetPacksView, 'packs'),
            ("check/", CheckAuthView, 'auth')
        ],
    )
)

auth_urls = list(
    map(
        lambda x: path(x[0], login_required(x[1].as_view())),
        [
            ("upload/profile/", UploadProfilePicView),
            ("links/", UserLinkView),
            ("update-link-sequence/", UpdateLinkSequenceView),
            ("upload-icon/", UploadIconView),
            ("update/user/", UpdateUserDetailsView),
        ],
    )
)

urlpatterns = unauth_urls + auth_urls
