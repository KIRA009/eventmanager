from django.http import JsonResponse
import jwt
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import re
import azure.core.exceptions as azure_exc
from functools import wraps
import uuid

from event_manager.settings import (
    SECRET_KEY,
    SENDGRIDAPIKEY,
    EMAIL_FROM,
    STORAGE_CLIENT,
)


def jsonify(data):
    status_code = int(data.get("status_code", 200))
    if "status_code" in data:
        del data["status_code"]
    return JsonResponse(data, status=status_code)


def retrieve_token(token):
    try:
        return True, jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except Exception as e:
        return False, str(e)


def create_token(**kwargs):
    return jwt.encode(kwargs, SECRET_KEY, algorithm="HS256").decode()


def send_email(emails, subject, message):
    message = Mail(
        from_email=EMAIL_FROM, to_emails=emails, subject=subject, html_content=message
    )
    try:
        sg = SendGridAPIClient(SENDGRIDAPIKEY)
        sg.send(message)
    except Exception as e:
        pass


def upload_file(request, file, container):
    file_name = request.User.username + str(uuid.uuid4()) + file.name
    blob_client = STORAGE_CLIENT.get_blob_client(container=container, blob=file_name)
    blob_client.upload_blob(file.read())
    return f"https://storageeventmanager.blob.core.windows.net/{container}/{file_name}"


def delete_file(url):
    container, file_name = get_container_and_name(url)
    blob_client = STORAGE_CLIENT.get_blob_client(container=container, blob=file_name)
    try:
        blob_client.delete_blob(delete_snapshots="include")
    except azure_exc.ResourceNotFoundError:
        pass


def get_container_and_name(url):
    pat = re.compile(r"https://storageeventmanager\.blob\.core\.windows\.net/(.*)/(.*)")
    return pat.findall(url)[0]


def test(test_func, login_url=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if "User" not in request.__dict__:
                return jsonify(dict(error="Access denied", status_code=401))
            if test_func(request.User):
                return view_func(request, *args, **kwargs)
            return jsonify(dict(error="Access denied", status_code=401))

        return _wrapped_view

    return decorator


def login_required(function=None):
    actual_decorator = test(lambda u: u.is_authenticated)
    if function:
        return actual_decorator(function)
    return actual_decorator


def pro_required(function=None):
    actual_decorator = test(lambda u: u.user_type == "pro")
    if function:
        return actual_decorator(function)
    return actual_decorator
