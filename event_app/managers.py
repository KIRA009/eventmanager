from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth import get_user_model

from utils.base_manager import BaseManager
from utils.exceptions import NotFound


class UserManager(BaseUserManager):

    def create_user(self, details):
        model = get_user_model()
        if details.get('phone'):
            phone = details.get('phone')
            if model.objects.filter(phone=phone).exists():
                raise NotFound("Phone number already registered")
            if not phone.isdigit():
                raise NotFound("Phone number should contain only digits")
            if len(phone) != 10:
                raise NotFound("Phone number should be 10 digits long")
        if model.objects.filter(email=details['email']).exists():
            raise NotFound("Email already registered")
        from .models import College
        details["college"] = College.objects.get(id=details["college"])
        if model.objects.filter(username=details['username']).exists():
            raise NotFound('Username already exists')
        details["is_staff"] = details["is_superuser"] = False
        user = self.model(**details)
        user.set_password(details['password'])
        try:
            user.save(using=self._db)
            return user
        except Exception as e:
            raise NotFound(str(e))

    def create_superuser(self, email, password):
        user = self.model(email=email.lower(), is_superuser=True, is_staff=True)
        user.set_password(password)
        user.save(using=self._db)
        return user


class LinkManager(BaseManager):
    def all(self):
        return super(LinkManager, self).order_by("index").all()
