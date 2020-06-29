from django.contrib import admin
from django.db.models import Q

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
        stack = [request.user.id]
        users = []
        while len(stack) > 0:
            temp = stack.pop()
            temp1 = Onboard.objects.filter(marketeer__id=temp).values_list('onboarder_id', flat=True)
            if temp1:
                users.append(temp)
                stack += temp1
        return Onboard.objects.filter(marketeer_id__in=users)

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        if request.user.is_superuser:
            return True
        return obj.marketeer == request.user

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)

    def onboarder__username(self, inst):
        return inst.onboarder.username

    def onboarder__products__count(self, inst):
        return inst.onboarder.products.count()

    list_display = ['marketeer', 'onboarder', 'onboarder__username', 'onboarder__products__count', 'amount']
    fields = ['onboarder']


admin.site.register(ContactedAccount, MarketeerAdmin)
admin.site.register(Onboard, OnboardAdmin)
