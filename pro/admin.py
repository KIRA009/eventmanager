from django.contrib import admin

from .models import *
from utils.base_admin import BaseAdmin


class ProPackAdmin(BaseAdmin):
    exclude = BaseAdmin.exclude + ['plan_id']
    list_display = ['price', 'currency', 'period']
    list_filter = ['currency', 'period']


class ProductAdmin(BaseAdmin):
    list_display = ['name', 'description', 'price', 'disc_price', 'estimated_delivery', 'user', 'cod_available']
    search_fields = ['user']
    list_filter = ['cod_available']


class ProModeFeatureAdmin(BaseAdmin):
    search_fields = ['user']
    list_display = ['header_icon', 'header_text', 'user']


admin.site.register(ProModeFeature, ProModeFeatureAdmin)
admin.site.register(ProPack, ProPackAdmin)
admin.site.register(Product, ProductAdmin)
