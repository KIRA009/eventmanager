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

if DEBUG:
    PROFILECONTAINER = "eventmanagerprofiledebug"
    ICONCONTAINER = "eventmanagericondebug"
else:
    PROFILECONTAINER = "eventmanagerprofile"
    ICONCONTAINER = "eventmanagericon"

STORAGE_CLIENT = BlobServiceClient.from_connection_string(
    os.getenv("CONNECTION_STRING")
)

RAZORPAY_MID = os.getenv("RAZORPAY_MID")
RAZORPAY_SECRET = os.getenv("RAZORPAY_SECRET")
RAZORPAY_KEY = os.getenv("RAZORPAY_KEY")
PAYMENT_CALLBACK_URL = os.getenv('PAYMENT_CALLBACK_URL')
PAYMENT_REDIRECT_URL = os.getenv('PAYMENT_REDIRECT_URL')

if DEBUG:
    ADMINS = ['shohanduttaroy99@gmail.com']
else:
    ADMINS = ['shohanduttaroy99@gmail.com', 'prasadyash549@yahoo.com', 'akashsurana119@gmail.com']

EMAIL_HOST = 'mail.privateemail.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
