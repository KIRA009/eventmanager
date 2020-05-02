from django.contrib import admin

from .models import Marketeer


@admin.register(Marketeer)
class MarketeerAdmin(admin.ModelAdmin):
    exclude = ['created_at', 'updated_at', 'user']

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Marketeer.objects.all()
        return Marketeer.objects.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        if request.user.is_superuser:
            return True
        return obj.user == request.user

    def has_delete_permission(self, request, obj=None):
        if not obj:
            return True
        if request.user.is_superuser:
            return True
        return obj.user == request.user

    list_display = ['username', 'registered']
