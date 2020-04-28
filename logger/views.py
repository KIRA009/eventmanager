from django.views import View
from django.shortcuts import redirect, reverse
from django.utils.timezone import now, timedelta

from .models import Tracker


class DeleteLogsView(View):
    def get(self, request):
        last_date = now() - timedelta(days=30)
        Tracker.objects.filter(updated_at__lte=last_date, resolved=False).delete()
        return redirect('/admin-dashboard/logger/logger/')
