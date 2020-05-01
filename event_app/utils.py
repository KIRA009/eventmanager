import re
import uuid
import azure.core.exceptions as azure_exc

from event_manager.settings import (
    STORAGE_CLIENT,
)
from utils.decorators import decorator


def upload_file(request, file, container):
    if file is None:
        return None
    file_name = request.User.username + str(uuid.uuid4()) + file.name.replace(' ', '')
    blob_client = STORAGE_CLIENT.get_blob_client(container=container, blob=file_name)
    blob_client.upload_blob(file.read())
    return f"https://storageeventmanager.blob.core.windows.net/{container}/{file_name}"


def delete_file(url):
    if url is None:
        return
    resolved, res = get_container_and_name(url)
    if resolved:
        blob_client = STORAGE_CLIENT.get_blob_client(container=res[0], blob=res[1])
        try:
            blob_client.delete_blob(delete_snapshots="include")
        except azure_exc.ResourceNotFoundError:
            pass


def get_container_and_name(url):
    pat = re.compile(r"https://storageeventmanager\.blob\.core\.windows\.net/(.*)/(.*)")
    try:
        return True, pat.findall(url)[0]
    except IndexError:
        return False, None, None


def pro_required(func):
    return decorator(func, lambda u: u.user_type == "pro")