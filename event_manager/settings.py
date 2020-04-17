import django.conf.global_settings as settings
from azure.storage.blob import BlobServiceClient
from corsheaders.defaults import default_headers

from .default_settings import *


AUTH_USER_MODEL = "event_app.User"

AUTHENTICATION_BACKENDS = settings.AUTHENTICATION_BACKENDS + [
    "event_app.backend.AuthBackend"
]


STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static_root")

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = list(default_headers) + ["Token"]

SENDGRIDAPIKEY = os.getenv("SENDGRIDAPIKEY")
EMAIL_FROM = os.getenv("EMAIL_FROM")

if DEBUG:
    PROFILECONTAINER = "eventmanagerprofiledebug"
    ICONCONTAINER = "eventmanagericondebug"
else:
    PROFILECONTAINER = "eventmanagerprofile"
    ICONCONTAINER = "eventmanagericon"
STORAGE_CLIENT = BlobServiceClient.from_connection_string(
    os.getenv("CONNECTION_STRING")
)
