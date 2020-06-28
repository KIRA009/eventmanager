from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.timezone import now

from utils.base_model_mixin import AutoCreatedUpdatedMixin


class Notification(AutoCreatedUpdatedMixin):
	header = models.TextField(blank=True)
	description = models.TextField(blank=True)
	meta_data = JSONField(default=dict, blank=True)
	read_at = models.DateTimeField(default=None, blank=True, null=True)
	user = models.ForeignKey('event_app.User', on_delete=models.CASCADE, related_name='notifications')

	def read(self):
		self.read_at = now()
		self.save()