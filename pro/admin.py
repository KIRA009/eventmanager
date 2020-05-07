from django.contrib import admin

from .models import *
from utils.base_admin import BaseAdmin


class ProPackAdmin(BaseAdmin):
    exclude = BaseAdmin.exclude + ['plan_id']


admin.site.register(ProModeFeature, BaseAdmin)
admin.site.register(ProPack, ProPackAdmin)
