from django.contrib import admin


from .models import *


class BaseAdmin(admin.ModelAdmin):
    exclude = ['created_at', 'updated_at']
    show_full_result_count = True
    view_on_site = False
    date_hierarchy = 'created_at'
    list_per_page = 30


class ProPackAdmin(BaseAdmin):
    exclude = BaseAdmin.exclude + ['plan_id']


admin.site.register(ProModeFeature, BaseAdmin)
admin.site.register(ProPack, ProPackAdmin)
