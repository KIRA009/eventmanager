import utils.email as email
import utils.messaging
import event_app.utils as event_app_utils
import payments.utils as payment_utils
from event_manager.settings import DEBUG
from .periodic_tasks import *
import utils.notifications as notifications


def send_email(emails, subject, message):
    if DEBUG:
        email.send_email(emails, subject, message)
    else:
        email.send_email.delay(emails, subject, message)


def delete_file(url):
    if DEBUG:
        event_app_utils.delete_file(url)
    else:
        event_app_utils.delete_file.delay(url)


def cancel_subscription(user_id, sub_id):
    if DEBUG:
        payment_utils.cancel_subscription(user_id, sub_id)
    else:
        payment_utils.cancel_subscription.delay(user_id, sub_id)


def handle_order(data):
    if DEBUG:
        payment_utils.handle_order(data)
    else:
        payment_utils.handle_order.delay(data)


def send_message(phone, message):
    if DEBUG:
        utils.messaging.send_message(phone, message)
    else:
        utils.messaging.send_message.delay(phone, message)


def refund_order(order_id, seller_id):
    if DEBUG:
        payment_utils.refund_order(order_id, seller_id)
    else:
        payment_utils.refund_order.delay(order_id, seller_id)


def send_push_message(notifs):
    if DEBUG:
        utils.notifications.send_push_message(notifs)
    else:
        utils.notifications.send_push_message.delay(notifs)
