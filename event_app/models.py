from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from uuid import uuid4

from .model_mixin import AutoCreatedUpdatedMixin
from .managers import UserManager, BaseManager


class User(AbstractBaseUser, PermissionsMixin, AutoCreatedUpdatedMixin):
    email = models.EmailField(max_length=256, unique=True)
    is_staff = models.BooleanField(default=False)
    phone = models.CharField(max_length=10)
    name = models.CharField(max_length=256)
    college = models.ForeignKey(
        "College",
        related_name="students",
        on_delete=models.CASCADE,
        to_field="name",
        null=True,
    )
    secret = models.UUIDField(default=uuid4)
    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.email


class College(AutoCreatedUpdatedMixin):
    name = models.TextField(unique=True)
    address = models.TextField()
    state = models.TextField()
    has_college_email = models.BooleanField(default=False)

    objects = BaseManager()

    def __str__(self):
        return self.name
