from django.contrib import admin
from django.utils.timezone import now

from utils.base_admin import BaseAdmin
from .models import *


class ShipmentAdmin(BaseAdmin):
	this_time = now()

	def picked_up(self, instance):
		return self.this_time > instance.pickup_scheduled_date
	picked_up.boolean = True

	list_display = ['order', 'courier_name', 'pickup_scheduled_date', 'applied_weight', 'picked_up']


admin.site.register(Shipment, ShipmentAdmin)
