from django.contrib import admin

from .models import *
from utils.base_admin import BaseAdmin


class ClickAdmin(BaseAdmin):
    def user(self, instance):
        return instance.link.user
    list_display = ['clicks', 'link', 'day', 'user']
    search_fields = ['link__user__username', 'link__user__email']


class LifeTimeClickAdmin(BaseAdmin):
    def user(self, instance):
        return instance.link.user

    list_display = ['clicks', 'link', 'user']
    search_fields = ['link__user__username', 'link__user__email', 'link__title']


class ViewAdmin(BaseAdmin):
    list_display = ['views', 'user', 'day']
    search_fields = ['user__username', 'user__email']


class LifeTimeViewAdmin(BaseAdmin):
    list_display = ['views', 'user']
    search_fields = ['user__username', 'user__email']


admin.site.register(Click, ClickAdmin)
admin.site.register(LifeTimeClick, LifeTimeClickAdmin)
admin.site.register(ProfileView, ViewAdmin)
admin.site.register(LifeTimeView, LifeTimeViewAdmin)
