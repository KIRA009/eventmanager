from django.db import models

from utils.base_model_mixin import AutoCreatedUpdatedMixin
from event_app.models import User


class Marketeer(AutoCreatedUpdatedMixin):
    username = models.TextField(unique=True)
    registered = models.BooleanField(default=False)
    status = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
