from django.contrib import admin

from .models import *
from utils.base_admin import BaseAdmin


class ProPackAdmin(BaseAdmin):
    exclude = BaseAdmin.exclude + ['plan_id']
    list_display = ['price', 'currency', 'period']
    list_filter = ['currency', 'period']


class ProductAdmin(BaseAdmin):
    list_display = ['name', 'description', 'price', 'disc_price', 'estimated_delivery', 'user', 'cod_available',
                    'opt_for_reselling', 'slug', 'sizes_available', 'online_available']
    search_fields = ['user']
    list_filter = ['cod_available', 'sizes_available', 'online_available']

    def delete_queryset(self, request, queryset):
        content_type = ContentType.objects.get_for_model(DeletedButUsedProduct)
        for i in queryset:
            i.delete(content_type=content_type)


class ProModeFeatureAdmin(BaseAdmin):
    search_fields = ['user']
    list_display = ['header_icon', 'header_text', 'user']


class ResellProductAdmin(BaseAdmin):
    def seller_count(self, obj):
        return obj.product.resell_products.count()

    list_display = ['product', 'seller_count', 'resell_margin']


class ProductSizeAdmin(BaseAdmin):
    list_display = ['size', 'price', 'disc_price', 'stock', 'product']


admin.site.register(ProModeFeature, ProModeFeatureAdmin)
admin.site.register(ProPack, ProPackAdmin)
admin.site.register([Product, DeletedButUsedProduct], ProductAdmin)
admin.site.register(ResellProduct, ResellProductAdmin)
admin.site.register(ProductSize, ProductSizeAdmin)
