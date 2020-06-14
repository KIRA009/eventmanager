from django.contrib import admin
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from utils.base_admin import BaseAdmin
from .models import Notification


class NotificationAdmin(BaseAdmin):
	class ReadFilter(admin.SimpleListFilter):
		title = _('Read')
		parameter_name = 'read'

		def lookups(self, request, model_admin):
			return (
				('1', 'Yes'),
				('0', 'No')
			)

		def queryset(self, request, queryset):
			if self.value() is None:
				return queryset
			if self.value() == '1':
				return queryset.exclude(read_at=None)
			return queryset.filter(read_at=None)

	list_display = ['user', 'header', 'read_at']
	list_filter = [ReadFilter]


admin.site.register(Notification, NotificationAdmin)

