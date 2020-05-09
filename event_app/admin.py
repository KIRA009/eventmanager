from django.contrib import admin
from django.contrib.auth.admin import Group, GroupAdmin

from .models import *
from payments.models import Subscription
from payments.utils import update_subscription
from utils.base_admin import CustomAdmin, BaseAdmin


admin.site = CustomAdmin()


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
    list_display = ['username', 'email', 'phone', 'is_validated']
    list_filter = ['is_validated']


class LinkAdmin(BaseAdmin):
    list_display = ['title', 'url', 'visible', 'user']
    list_filter = ['visible']
    search_fields = ['user']


class CollegeAdmin(BaseAdmin):
    def attendees(self, instance):
        return instance.students.count()
    list_display = ['name', 'state', 'has_college_email', 'attendees']
    list_filter = ['has_college_email']
    search_fields = ['name', 'state']


admin.site.register(College, CollegeAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
