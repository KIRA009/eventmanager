from django.db import models

from utils.base_model_mixin import AutoCreatedUpdatedMixin
from event_app.models import User


class Marketeer(AutoCreatedUpdatedMixin):
    STATUS_CHOICES = (
        ('INTERESTED', 'Interested'),
        ('MAILED', 'Mailed'),
        ('NOT_INTERESTED', 'Not Interested'),
        ('DID_NOT_REPLY', 'Did not reply'),
        ('CONTACTED', 'Contacted')
    )
    insta_username = models.TextField(blank=False)
    signed_up = models.BooleanField(default=False)
    bought_pro_pack = models.BooleanField(default=False)
    added_link_in_insta = models.BooleanField(default=False)
    followed_myweblink_on_insta = models.BooleanField(default=False)
    status = models.TextField(blank=True, choices=STATUS_CHOICES)
    marketeer = models.ForeignKey(User, on_delete=models.CASCADE)
