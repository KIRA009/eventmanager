from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.hashers import check_password


class AuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        model = get_user_model()
        try:
            user = model.objects.get(Q(email=username) | Q(phone=username))
            if user:
                is_valid = check_password(password, user.password)
                if is_valid:
                    return user
            return None
        except model.DoesNotExist:
            return None
