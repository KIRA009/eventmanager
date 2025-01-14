from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate


class CustomLogin(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username').lower()
        password = self.cleaned_data.get('password').lower()

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data


class CustomAdmin(admin.AdminSite):
    login_form = CustomLogin


class BaseAdmin(admin.ModelAdmin):
    exclude = ['created_at', 'updated_at']
    show_full_result_count = True
    view_on_site = False
    date_hierarchy = 'created_at'
    list_per_page = 30
