import django.contrib.admin as admin

from .models import *


@admin.register(Tracker)
class TrackerAdmin(admin.ModelAdmin):
    def mark_as_resolved(self, request, queryset):
        queryset.update(resolved=True)
        self.message_user(request, 'The selected issues have been resolved')
    mark_as_resolved.short_description = 'Mark selected issues as resolved'

    search_fields = ['user__email', 'user__username']
    actions = ['mark_as_resolved']
    list_display = ['user', 'msg', 'resolved', 'url']
