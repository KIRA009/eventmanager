from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from uuid import uuid4

from .model_mixin import AutoCreatedUpdatedMixin
from .managers import UserManager, LinkManager


class User(AbstractBaseUser, PermissionsMixin, AutoCreatedUpdatedMixin):
    email = models.EmailField(max_length=256, unique=True)
    is_staff = models.BooleanField(default=False)
    phone = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=256)
    secret = models.UUIDField(default=uuid4)
    is_validated = models.BooleanField(default=False)
    username = models.TextField(unique=True)
    profile_pic = models.URLField(default="", null=True, blank=True)
    user_type = models.CharField(default="normal", max_length=256)
    college = models.ForeignKey(
        "College",
        related_name="students",
        on_delete=models.CASCADE,
        to_field="name",
        null=True,
    )
    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.email

    def detail(self):
        ret = super(User, self).detail()
        for i in ["password", "last_login", "is_superuser", "is_staff", "secret"]:
            del ret[i]
        ret["links"] = [link.detail() for link in self.links.all()]
        return ret

    def change_secret(self):
        self.secret = uuid4()
        self.save()

    def change_password(self, password):
        self.set_password(password)
        self.change_secret()


class College(AutoCreatedUpdatedMixin):
    name = models.TextField(unique=True)
    address = models.TextField()
    state = models.TextField()
    has_college_email = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Link(AutoCreatedUpdatedMixin):
    title = models.TextField(default="")
    url = models.URLField(default="", null=True)
    visible = models.BooleanField(default=False)
    index = models.IntegerField(default=0)
    icon = models.URLField(default="", null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="links", to_field="username"
    )

    objects = LinkManager()
