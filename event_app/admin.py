from django.contrib import admin

from .models import *
from payments.models import Subscription
from payments.utils import update_subscription


@admin.register(College, Link, ProModeFeature, ProPack)
class BaseAdmin(admin.ModelAdmin):
    fields_exclude = ['created_at', 'updated_at']
    show_full_result_count = True
    view_on_site = False
    date_hierarchy = 'created_at'
    list_per_page = 30


@admin.register(User)
class UserAdmin(BaseAdmin):
    def create_pro(self, request, queryset):
        for user in queryset:
            if user.user_type == 'normal':
                sub = Subscription(sub_id=str(uuid4()), sub_type=Subscription.PROPACK, user=user, test=True)
                update_subscription(sub)
        self.message_user(request, 'The selected users were made pro users for a month')
    create_pro.short_description = 'Create a monthly pro pack for selected users'

    actions = ['create_pro']
    search_fields = ['username', 'email']
