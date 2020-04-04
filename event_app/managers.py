from django.contrib.auth.base_user import BaseUserManager
from django.db.models import Manager
from uuid import uuid4
from django.contrib.auth import get_user_model


class BaseManager(Manager):
    pass


class UserManager(BaseUserManager):
    def create_user(self, details):
        """
        Creates and saves a User with the given contact, password
        """
        model = get_user_model()
        try:
            model.objects.get(phone=details["phone"])
            return False, "Phone number already registered"
        except model.DoesNotExist:
            pass
        from .models import College

        details["college"] = College.objects.get(id=details["college"])
        details["email"] = uuid4()
        details["is_staff"] = details["is_superuser"] = False
        user = self.model(**details)
        user.set_password(uuid4())
        try:
            user.save(using=self._db)
            return True, user
        except Exception as e:
            return False, str(e)

    def create_superuser(self, email, password):
        """
        Creates and saves a User with the given contact, password
        """
        user = self.model(email=email, is_superuser=True, is_staff=True)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def update_user(self, details):
        try:
            user = self.get(secret=details["secret"])
            user.email = details["email"]
            user.set_password(details["password"])
            user.save(using=self._db)
            return True, user
        except self.model.DoesNotExist:
            return False, None
