import utils.email as _email
import event_app.utils as _event_app_utils


def send_email(emails, subject, message):
    _email.send_email.delay(emails, subject, message)


def delete_file(url):
    _event_app_utils.delete_file.delay(url)

