from django.db import models
from django.contrib.auth import get_user_model
from utils import AutoCreatedUpdatedMixin

User = get_user_model()


class Logger(AutoCreatedUpdatedMixin):
    msg = models.TextField()
    trace = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        if self.user.is_authenticated:
            return f'{self.user.username} --> {self.msg}'
        return f'anonymous -> {self.msg}'
