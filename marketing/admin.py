from django.contrib import admin

from .models import Marketeer
from utils.base_admin import BaseAdmin


class MarketeerAdmin(BaseAdmin):
    exclude = ['created_at', 'updated_at', 'marketeer']

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Marketeer.objects.all()
        return Marketeer.objects.filter(marketeer=request.user)

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
        if not obj:
            return True
        if request.user.is_superuser:
            return True
        return obj.marketeer == request.user

    list_display = ['insta_username', 'signed_up', 'bought_pro_pack', 'marketeer', 'status', 'added_link_in_insta',
                    'followed_myweblink_on_insta']


admin.site.register(Marketeer, MarketeerAdmin)
