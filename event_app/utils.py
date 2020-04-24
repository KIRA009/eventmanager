from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import re
import uuid
import azure.core.exceptions as azure_exc

from event_manager.settings import (
    SENDGRIDAPIKEY,
    EMAIL_FROM,
    STORAGE_CLIENT,
)
from utils import decorator


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
    if file is None:
        return None
    file_name = request.User.username + str(uuid.uuid4()) + file.name
    blob_client = STORAGE_CLIENT.get_blob_client(container=container, blob=file_name)
    blob_client.upload_blob(file.read())
    return f"https://storageeventmanager.blob.core.windows.net/{container}/{file_name}"


def delete_file(url):
    if url is None:
        return
    container, file_name = get_container_and_name(url)
    blob_client = STORAGE_CLIENT.get_blob_client(container=container, blob=file_name)
    try:
        blob_client.delete_blob(delete_snapshots="include")
    except azure_exc.ResourceNotFoundError:
        pass


def get_container_and_name(url):
    pat = re.compile(r"https://storageeventmanager\.blob\.core\.windows\.net/(.*)/(.*)")
    return pat.findall(url)[0]


def pro_required(func):
    return decorator(func, lambda u: u.user_type == "pro")