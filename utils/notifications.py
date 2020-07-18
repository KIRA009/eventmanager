from exponent_server_sdk import PushClient
from exponent_server_sdk import PushMessage
from exponent_server_sdk import PushServerError
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError
from celery.task import task

from .exceptions import AccessDenied


@task(name='send_push_message')
def send_push_message(notifs):
    try:
        responses = PushClient().publish_multiple(
            [
                PushMessage(
                    to=notif['token'], body=notif['description'], title=notif['title'], priority='high',
                    data=dict(id=notif['id']), badge=notif['unread_notifs']
                ) for notif in notifs
            ]
        )
    except PushServerError as exc:
        pass
    except (ConnectionError, HTTPError) as exc:
        pass
    except Exception as exc:
        pass
