from django.views import View
from django.shortcuts import redirect, reverse
from django.utils.timezone import now, timedelta

from .models import Logger


class DeleteLogsView(View):
    def get(self, request):
        last_date = now() - timedelta(days=30)
        Logger.objects.filter(updated_at__lte=last_date).delete()
        return redirect('/admin-dashboard/logger/logger/')
