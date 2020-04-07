from django.http import JsonResponse
import jwt
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import re
import azure.core.exceptions as azure_exc

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


def upload_file(file, file_name, container):
    blob_client = STORAGE_CLIENT.get_blob_client(container=container, blob=file_name)
    blob_client.upload_blob(file.read())


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
