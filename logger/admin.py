import django.contrib.admin as admin

from .models import *


@admin.register(Tracker)
class TrackerAdmin(admin.ModelAdmin):
    search_fields = ['user__email', 'user__username']
