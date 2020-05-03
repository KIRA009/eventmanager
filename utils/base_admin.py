from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate


class CustomLogin(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
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
