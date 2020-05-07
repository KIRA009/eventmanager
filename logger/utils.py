import os

from utils.tasks import send_email
from event_manager.settings import ADMINS, BASE_DIR


def send_email_to_admins(template, subject, **kwargs):
    with open(os.path.join(BASE_DIR, 'logger', 'admin_templates', f'{template}.html')) as f:
        html = f.read()
    for k, v in kwargs.items():
        html = html.replace('{{' + k + '}}', v)
    send_email(ADMINS, subject, html)
