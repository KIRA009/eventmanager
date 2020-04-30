from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth import get_user_model
import re
from utils import BaseManager


class UserManager(BaseUserManager):

    def create_user(self, details):
        model = get_user_model()
        if details.get('phone'):
            if model.objects.filter(phone=details['phone']).exists():
                return False, "Phone number already registered"

        if model.objects.filter(email=details['email']).exists():
            return False, "Email already registered"
        from .models import College
        details["college"] = College.objects.get(id=details["college"])
        if not details['college']:
            return False, 'College does not exist'
        details['username'] = details['email']
        details["is_staff"] = details["is_superuser"] = False
        user = self.model(**details)
        user.set_password(details['password'])
        try:
            user.save(using=self._db)
            return True, user
        except Exception as e:
            return False, str(e)

    def create_superuser(self, email, password):
        user = self.model(email=email.lower(), is_superuser=True, is_staff=True)
        user.set_password(password)
        user.save(using=self._db)
        return user


class LinkManager(BaseManager):
    def all(self):
        return super(LinkManager, self).order_by("index").all()
