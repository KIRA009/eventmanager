import django.contrib.admin as admin

from .models import *
from utils.base_admin import BaseAdmin


class ServerTrackerAdmin(BaseAdmin):
    def mark_as_resolved(self, request, queryset):
        queryset.update(resolved=True)
        self.message_user(request, 'The selected issues have been resolved')
    mark_as_resolved.short_description = 'Mark selected issues as resolved'

    search_fields = ['user__email', 'user__username']
    actions = ['mark_as_resolved']
    list_display = ['user', 'msg', 'resolved', 'url']
    date_hierarchy = 'created_at'


class ClientTrackerAdmin(BaseAdmin):
    def mark_as_resolved(self, request, queryset):
        queryset.update(resolved=True)
        self.message_user(request, 'The selected issues have been resolved')
    mark_as_resolved.short_description = 'Mark selected issues as resolved'

    search_fields = ['user__email', 'user__username']
    actions = ['mark_as_resolved']
    list_display = ['user', 'resolved', 'url']
    date_hierarchy = 'created_at'


admin.site.register(ServerTracker, ServerTrackerAdmin)
admin.site.register(ClientTracker, ClientTrackerAdmin)
