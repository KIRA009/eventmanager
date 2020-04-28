import os

from utils import decorator, send_email
from event_manager.settings import ADMINS, BASE_DIR


def admin_required(func):
    return decorator(func, lambda u: u.is_superuser)


def send_email_to_admins(template, subject, **kwargs):
    with open(os.path.join(BASE_DIR, 'logger', 'admin_templates', f'{template}.html')) as f:
        html = f.read()
    for k, v in kwargs.items():
        html = html.replace('{{' + k + '}}', v)
    send_email(ADMINS, subject, html)
