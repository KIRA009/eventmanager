import requests
from celery.task import task

from event_manager.settings import MSG91AUTHKEY


@task(name='send_message')
def send_message(phone, message):
    param_dict = dict(
        sms=[dict(message=message, to=phone.split(","))],
        route="4",
        sender="MYWBLK",
        country="91",
    )
    headers = {"authkey": MSG91AUTHKEY, "Content-Type": "application/json"}
    url = "https://api.msg91.com/api/v2/sendsms"
    requests.post(url, json=param_dict, headers=headers)
