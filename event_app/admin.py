from django.contrib import admin
from django.contrib.auth.admin import Group, GroupAdmin

from .models import *
from payments.models import Subscription
from payments.utils import update_subscription
from utils.base_admin import CustomAdmin


admin.site = CustomAdmin()


class BaseAdmin(admin.ModelAdmin):
    exclude = ['created_at', 'updated_at']
    show_full_result_count = True
    view_on_site = False
    date_hierarchy = 'created_at'
    list_per_page = 30


class UserAdmin(BaseAdmin):
    def create_pro(self, request, queryset):
        for user in queryset:
            if user.user_type == 'normal':
                sub = Subscription(sub_id=str(uuid4()), sub_type=Subscription.PROPACK, user=user)
                update_subscription(sub)
        self.message_user(request, 'The selected users were made pro users for a month')
    create_pro.short_description = 'Create a monthly pro pack for selected users'

    actions = ['create_pro']
    search_fields = ['username', 'email']


class ProPackAdmin(BaseAdmin):
    exclude = BaseAdmin.exclude + ['plan_id']


admin.site.register([College, Link, ProModeFeature], BaseAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(ProPack, ProPackAdmin)
admin.site.register(Group, GroupAdmin)