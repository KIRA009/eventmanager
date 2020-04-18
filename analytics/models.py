from django.db import models

from utils import AutoCreatedUpdatedMixin
from event_app.models import Link


class Click(AutoCreatedUpdatedMixin):
    clicks = models.BigIntegerField(default=0)
    day = models.DateField(auto_now_add=True)
    link = models.ForeignKey(Link, on_delete=models.CASCADE, related_name="clicks")
