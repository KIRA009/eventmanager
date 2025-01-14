from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import localdate, now

from .models import *
from utils.base_admin import BaseAdmin


class OrderItemAdmin(BaseAdmin):
	def get_model_name(self, instance):
		return instance.content_type.model

	class ContentListFilter(admin.SimpleListFilter):
		title = _('Content Type')
		parameter_name = 'content_type'

		def lookups(self, request, model_admin):
			return (
				('product', 'Product'),
				('subscription', 'Subscription')
			)

		def queryset(self, request, queryset):
			if self.value() is None:
				return queryset
			return queryset.filter(content_type__model=self.value())

	list_display = ['get_model_name', 'order', 'order_id']
	search_fields = ['order_id__user__username']
	list_filter = [ContentListFilter]


class OrderAdmin(BaseAdmin):
	def item_count(self, obj):
		return obj.items.count()

	list_display = ['user', 'amount', 'paid', 'item_count', 'status', 'seller']
	search_fields = ['user']
	list_filter = ['paid', 'status']


class SubscriptionAdmin(BaseAdmin):
	class ActiveListFilter(admin.SimpleListFilter):
		title = _('Active')
		parameter_name = 'active'

		def lookups(self, request, model_admin):
			return (
				(True, 'Yes'),
				(False, 'No')
			)

		def queryset(self, request, queryset):
			today = localdate(now())
			if self.value() is None:
				return queryset
			if self.value():
				return queryset.filter(start_date__lte=today, end_date__gte=today)
			return queryset.filter(end_date__lte=today)

	def active(self, instance):
		return instance.is_active()
	active.boolean = True

	list_display = ['user', 'start_date', 'end_date', 'test', 'is_unsubscribed', 'active']
	search_fields = ['user']
	list_filter = ['is_unsubscribed', 'test', ActiveListFilter]


class SellerAdmin(BaseAdmin):
	def pay_outstanding(self, request, queryset):
		queryset.update(amount=0)
		self.message_user(request, 'The selected sellers have been paid')

	pay_outstanding.short_description = "Pay outstanding debt"

	list_display = ['user', 'amount', 'has_free_delivery_above_amount', 'free_delivery_above_amount']
	actions = ['pay_outstanding']


class RetrievedAdmin(BaseAdmin):
	def mark_as_paid(self, request, queryset):
		queryset.update(paid=True)
		self.message_user(request, 'The selected requests were successfully marked as paid')
	mark_as_paid.short_description = 'Mark requests as paid'
	list_display = ['user', 'amount', 'paid']
	list_filter = ['paid']
	actions = ['mark_as_paid']


admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Seller, SellerAdmin)
admin.site.register(RetrieveAmount, RetrievedAdmin)
