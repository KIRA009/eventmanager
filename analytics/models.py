from django.db import models

from utils.base_model_mixin import AutoCreatedUpdatedMixin
from event_app.models import Link, User
from .managers import ClickManager, ProfileViewManager


class Click(AutoCreatedUpdatedMixin):
    clicks = models.BigIntegerField(default=0)
    day = models.DateField()
    link = models.ForeignKey(Link, on_delete=models.CASCADE, related_name="clicks")

    objects = ClickManager()


class ProfileView(AutoCreatedUpdatedMixin):
    views = models.BigIntegerField(default=0)
    day = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="views")

    objects = ProfileViewManager()


class LifeTimeClick(AutoCreatedUpdatedMixin):
    clicks = models.BigIntegerField(default=0)
    link = models.OneToOneField(Link, on_delete=models.CASCADE, related_name="total_clicks")


class LifeTimeView(AutoCreatedUpdatedMixin):
    views = models.BigIntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="total_views")
