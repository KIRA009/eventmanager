from django.views import View
import django.utils.timezone as tz

from analytics.models import Click
from event_app.models import Link


class AddClickView(View):
    def post(self, request):
        data = request.json
        link = Link.objects.get(id=data["link_id"])
        link, _ = Click.objects.get_or_create(link=link, day=tz.now().date())
        link.clicks += 1
        link.save()
        return dict(message="Click added successfully")


class AddView(View):
    def post(self, request):
        data = request.json
        link = Link.objects.get(id=data["link_id"])
        link, _ = Click.objects.get_or_create(link=link, day=tz.now().date())
        link.clicks += 1
        link.save()
        return dict(message="Click added successfully")
