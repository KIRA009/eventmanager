import utils.email as email
import utils.messaging
import event_app.utils as event_app_utils
import payments.utils as payment_utils
from .periodic_tasks import *


def send_email(emails, subject, message):
    email.send_email.delay(emails, subject, message)


def delete_file(url):
    event_app_utils.delete_file.delay(url)


def cancel_subscription(user_id, sub_id):
    payment_utils.cancel_subscription.delay(user_id, sub_id)


def handle_order(data):
    payment_utils.handle_order.delay(data)


def send_message(phone, message):
    utils.messaging.send_message.delay(phone, message)
