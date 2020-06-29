from uuid import uuid4
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.timezone import localdate, now
from django.db.utils import IntegrityError

from utils.base_model_mixin import AutoCreatedUpdatedMixin
from .managers import UserManager
from utils.exceptions import AccessDenied


class User(AbstractBaseUser, PermissionsMixin, AutoCreatedUpdatedMixin):
    email = models.EmailField(max_length=256, unique=True)
    is_staff = models.BooleanField(default=False)
    phone = models.CharField(max_length=10, blank=True)
    name = models.CharField(max_length=256)
    secret = models.UUIDField(default=uuid4)
    is_validated = models.BooleanField(default=False)
    username = models.TextField(unique=True)
    profile_pic = models.URLField(default="", null=True, blank=True)
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

    @property
    def user_type(self):
        return 'pro'
        # from payments.models import Subscription
        # today = localdate(now())
        # return 'pro' if self.subscriptions.filter(sub_type=Subscription.PROPACK, start_date__lte=today,
        #                                           end_date__gte=today).exists() else 'normal'

    exclude_fields = AutoCreatedUpdatedMixin.get_exclude_fields_copy()
    exclude_fields += ["password", "last_login", "is_superuser", "is_staff", "secret"]
    process_fields = AutoCreatedUpdatedMixin.get_process_fields_copy()
    process_fields.update(**dict(
        links=lambda x: x.links.all().detail(),
        user_type=lambda x: x.user_type,
        is_profile_complete=lambda x: (
                x.feature.header_text not in ['', None] and
                x.feature.header_icon not in ['', None] and
                x.seller.shipping_area not in ['', None]
        ),
        unread_notifs=lambda x: x.notifications.filter(read_at=None).count()
    ))

    def change_secret(self):
        self.secret = uuid4()
        self.save()

    def change_password(self, password):
        self.set_password(password)
        self.change_secret()

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        self.username = self.username.lower()
        try:
            super().save(*args, **kwargs)
        except IntegrityError as e:
            raise AccessDenied(str(e))


class College(AutoCreatedUpdatedMixin):
    name = models.TextField(unique=True)
    address = models.TextField()
    state = models.TextField()
    has_college_email = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Link(AutoCreatedUpdatedMixin):
    title = models.TextField(default="")
    url = models.URLField(default="", null=True, blank=True)
    visible = models.BooleanField(default=False)
    index = models.IntegerField(default=0)
    icon = models.URLField(default="", null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="links"
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['index']
