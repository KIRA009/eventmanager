from django.contrib import admin

from .models import *
from utils.base_admin import BaseAdmin


class MarketeerAdmin(BaseAdmin):
    exclude = ['created_at', 'updated_at', 'marketeer']

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.groups.filter(name='Marketeer').exists()

    def get_queryset(self, request):
        if request.user.is_superuser:
            return ContactedAccount.objects.all()
        return ContactedAccount.objects.filter(marketeer=request.user)

    def save_model(self, request, obj, form, change):
        obj.marketeer = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        if request.user.is_superuser:
            return True
        return obj.marketeer == request.user

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)

    list_display = ['insta_username', 'signed_up', 'bought_pro_pack', 'marketeer', 'status', 'added_link_in_insta',
                    'followed_myweblink_on_insta']


class OnboardAdmin(BaseAdmin):
    def get_queryset(self, request):
        if request.user.is_superuser:
            return Onboard.objects.all()
        return Onboard.objects.filter(marketeer=request.user)

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        if request.user.is_superuser:
            return True
        return obj.marketeer == request.user

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)

    list_display = ['onboarder']
    fields = ['onboarder']


admin.site.register(ContactedAccount, MarketeerAdmin)
admin.site.register(Onboard, OnboardAdmin)
