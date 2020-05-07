from django.contrib import admin

from .models import *
from utils.base_admin import BaseAdmin


class ClickAdmin(BaseAdmin):
    list_display = ['clicks', 'link', 'day']


class LifeTimeClickAdmin(BaseAdmin):
    list_display = ['clicks', 'link']


class ViewAdmin(BaseAdmin):
    list_display = ['views', 'user', 'day']


class LifeTimeViewAdmin(BaseAdmin):
    list_display = ['views', 'user']


admin.site.register(Click, ClickAdmin)
admin.site.register(LifeTimeClick, LifeTimeClickAdmin)
admin.site.register(ProfileView, ViewAdmin)
admin.site.register(LifeTimeView, LifeTimeViewAdmin)
