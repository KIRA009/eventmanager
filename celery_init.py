import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_manager.settings')
app = Celery('event_manager')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks([*settings.INSTALLED_APPS, 'utils'])
