from django.db import models

from utils.base_model_mixin import AutoCreatedUpdatedMixin
from event_app.models import Link, User
from .managers import ClickManager, ProfileViewManager


class Click(AutoCreatedUpdatedMixin):
    clicks = models.BigIntegerField(default=0)
    day = models.DateField(auto_now_add=True)
    link = models.ForeignKey(Link, on_delete=models.CASCADE, related_name="clicks")

    objects = ClickManager()


class ProfileView(AutoCreatedUpdatedMixin):
    views = models.BigIntegerField(default=0)
    day = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="views")

    objects = ProfileViewManager()
