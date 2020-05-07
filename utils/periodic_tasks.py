from celery.task import task
from django.utils.timezone import timedelta, now, localdate

from logger.models import Tracker
from analytics.models import *


@task(name='delete_month_old_logs')
def delete_month_old_logs():
    last_date = localdate(now()) - timedelta(days=30)
    Tracker.objects.filter(updated_at__lte=last_date, resolved=False).delete()


@task(name="add_to_lifetime_analytics")
def add_to_lifetime_analytics():
    last_date = localdate(now()) - timedelta(days=29)
    for i in Click.objects.filter(day=last_date):
        total_clicks = LifeTimeClick.objects.get_or_create(link=i.link)[0]
        total_clicks.clicks += i.clicks
        total_clicks.save()
        i.delete()
    for i in ProfileView.objects.filter(day=last_date):
        total_views = LifeTimeView.objects.get_or_create(user=i.user)[0]
        total_views.views += i.views
        total_views.save()
        i.delete()
