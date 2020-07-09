from django.contrib import admin
from django.contrib.auth.admin import Group, GroupAdmin
from django.utils.translation import gettext_lazy as _
from django.db.models import Count

from .models import *
from payments.models import Subscription
from payments.utils import update_subscription
from utils.base_admin import CustomAdmin, BaseAdmin
from marketing.models import Onboard


admin.site = CustomAdmin()


class UserAdmin(BaseAdmin):
    def create_pro(self, request, queryset):
        if not request.user.is_superuser:
            return
        for user in queryset:
            if user.user_type == 'normal':
                sub = Subscription(sub_id=str(uuid4()), sub_type=Subscription.PROPACK, user=user)
                update_subscription(sub)
        self.message_user(request, 'The selected users were made pro users for a month')
    create_pro.short_description = 'Create a monthly pro pack for selected users'

    def onboard_user(self, request, queryset):
        if request.user.groups.filter(name='Marketeer').exists():
            queryset = queryset.exclude(username=request.user.username)
            queryset = queryset.annotate(board=Count('onboarding')).filter(board=0)
            onboarders = [Onboard(onboarder=i, marketeer=request.user) for i in queryset]
            Onboard.objects.bulk_create(onboarders)

    def is_onboarded(self, instance):
        return Onboard.objects.filter(onboarder=instance).exists()
    is_onboarded.boolean = True

    class OnBoardFilter(admin.SimpleListFilter):
        title = _('Onboarded')
        parameter_name = 'onboarded'

        def lookups(self, request, model_admin):
            return (
                (1, 'Yes'),
                (0, 'No')
            )

        def queryset(self, request, queryset):
            if self.value() is None:
                return queryset
            return queryset.annotate(board=Count('onboarding')).filter(board=self.value())

    def pro(self, instance):
        return instance.user_type == 'pro'
    pro.boolean = True

    def onboarding__marketeer__username(self, inst):
        return inst.onboarding.marketeer.username

    actions = ['create_pro', 'onboard_user']
    search_fields = ['username', 'email']
    list_display = ['username', 'email', 'phone', 'is_validated', 'is_onboarded', 'onboarding__marketeer__username']

    list_filter = ['is_validated', OnBoardFilter]


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
