from django.contrib import admin

from .models import *
from utils.base_admin import BaseAdmin


class ProPackAdmin(BaseAdmin):
    exclude = BaseAdmin.exclude + ['plan_id']


class ProductAdmin(BaseAdmin):
    list_display = ['name', 'description', 'price', 'disc_price', 'estimated_delivery', 'user']


admin.site.register(ProModeFeature, BaseAdmin)
admin.site.register(ProPack, ProPackAdmin)
admin.site.register(Product, ProductAdmin)
