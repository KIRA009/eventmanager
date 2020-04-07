import django.conf.global_settings as settings
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

from .default_settings import *


AUTH_USER_MODEL = "event_app.User"

AUTHENTICATION_BACKENDS = settings.AUTHENTICATION_BACKENDS + [
    "event_app.backend.AuthBackend"
]


STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_URL = "/event_manager/static/"

CORS_ORIGIN_ALLOW_ALL = True
STATIC_ROOT = os.path.join(BASE_DIR, "static_root")

SENDGRIDAPIKEY = os.getenv("SENDGRIDAPIKEY")
EMAIL_FROM = os.getenv("EMAIL_FROM")

if DEBUG:
    PROFILECONTAINER = "eventmanagerprofiledebug"
else:
    PROFILECONTAINER = "eventmanagerprofile"
STORAGE_CLIENT = BlobServiceClient.from_connection_string(
    os.getenv("CONNECTION_STRING")
)
