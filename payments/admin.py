from django.contrib import admin

from .models import *
from utils.base_admin import BaseAdmin


class OrderItemAdmin(BaseAdmin):
	list_display = ['content_type', 'order']


class OrderAdmin(BaseAdmin):
	def item_count(self, obj):
		return obj.items.count()

	list_display = ['user', 'amount', 'paid', 'item_count']


class SubscriptionAdmin(BaseAdmin):
	list_display = ['user', 'start_date', 'end_date', 'test']


admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
