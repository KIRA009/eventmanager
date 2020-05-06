from django.urls import path

from utils.decorators import login_required
from .views import *

unauth_urls = list(
    map(
        lambda x: path(x[0], x[1].as_view()),
        [
            ("register/", RegisterView),
            ("colleges/", CollegeView),
            ("login/", LoginView),
            ("validate-email/", SendValidateEmailView),
            ("validate/<int:user_id>/<uuid:secret>/", CompleteValidateEmailView),
            ("user/", GetUserView),
            ('packs/', GetPacksView),
            ("check/", CheckAuthView)
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
