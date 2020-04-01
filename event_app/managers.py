from django.contrib.auth.base_user import BaseUserManager
from django.db.models import Manager
from uuid import uuid4


class BaseManager(Manager):
    pass


class UserManager(BaseUserManager):
    def create_user(self, details):
        """
        Creates and saves a User with the given contact, password
        """
        from .models import College

        details["college"] = College.objects.get(name=details["college"])
        details["email"] = uuid4()
        user = self.model(**details)
        user.set_password(uuid4())
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
