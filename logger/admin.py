import django.contrib.admin as admin

from .models import *


@admin.register(Logger)
class LoggerAdmin(admin.ModelAdmin):
    search_fields = ['user__email', 'user__username']
