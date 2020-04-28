from django.db import models
from django.contrib.auth import get_user_model
from utils import AutoCreatedUpdatedMixin

User = get_user_model()


class Tracker(AutoCreatedUpdatedMixin):
    msg = models.TextField()
    trace = models.TextField(blank=True)
    url = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        if self.user.is_authenticated:
            return f'{self.user.username} --> {self.msg} -> {"resolved" if self.resolved else "not resolved"}'
        return f'anonymous -> {self.msg} -> {"resolved" if self.resolved else "not resolved"}'
