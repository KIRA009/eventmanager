from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField

from utils.base_model_mixin import AutoCreatedUpdatedMixin

User = get_user_model()


class ServerTracker(AutoCreatedUpdatedMixin):
    msg = models.TextField()
    trace = models.TextField(blank=True)
    url = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    request_body = JSONField(default=dict, blank=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        if self.user:
            return f'{self.user.username} --> {self.msg} -> {"resolved" if self.resolved else "not resolved"}'
        return f'anonymous -> {self.msg} -> {"resolved" if self.resolved else "not resolved"}'


class ClientTracker(AutoCreatedUpdatedMixin):
    url = models.TextField(blank=True)
    stack_trace = models.TextField(blank=True)
    resolved = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        if self.user:
            return f'{self.user.username} --> {"resolved" if self.resolved else "not resolved"}'
        return f'anonymous -> {"resolved" if self.resolved else "not resolved"}'
