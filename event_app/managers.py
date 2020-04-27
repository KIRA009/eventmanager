from django.contrib.auth.base_user import BaseUserManager
from django.db.models import Manager
from uuid import uuid4
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
import re


class BaseManager(Manager):
    pass


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
        is_present, username = self.get_username(details['email'])
        if is_present:
            details['username'] = username
        else:
            return False, username
        details["is_staff"] = details["is_superuser"] = False
        user = self.model(**details)
        user.set_password(uuid4())
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

    def get_username(self, email):
        pat = re.compile(r"(.*)@(.*)\..*")
        try:
            local, domain = pat.findall(email)[0]
        except IndexError:
            return False, 'Invalid email'
        if domain == "yahoo":
            return True, f"{local}!"
        elif domain == "gmail":
            return True, local
        else:
            return True, f"{local}&"


class LinkManager(BaseManager):
    def all(self):
        return super(LinkManager, self).order_by("index").all()
