import django.conf.global_settings as settings
import os

from .default_settings import *


AUTH_USER_MODEL = "event_app.User"

AUTHENTICATION_BACKENDS = settings.AUTHENTICATION_BACKENDS + [
    "event_app.backend.AuthBackend"
]


STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_URL = "/event_manager/static/"

CORS_ORIGIN_ALLOW_ALL = True
STATIC_ROOT = os.path.join(BASE_DIR, "static_root")
