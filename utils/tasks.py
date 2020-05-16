import utils.email as email
import event_app.utils as event_app_utils
import payments.utils as payment_utils
from .periodic_tasks import *


def send_email(emails, subject, message):
    email.send_email.delay(emails, subject, message)


def delete_file(url):
    event_app_utils.delete_file.delay(url)


def cancel_subscription(user_id, sub_id):
    payment_utils.cancel_subscription.delay(user_id, sub_id)


def create_invoice(order_id, seller_id):
    payment_utils.create_invoice.delay(order_id, seller_id)
