from django.db import models
from .exceptions import NotFound


class BaseManager(models.Manager):
    def get(self, **kwargs):
        try:
            return super(BaseManager, self).get(**kwargs)
        except self.model.DoesNotExist:
            raise NotFound(f'The {self.model._meta.model_name} requested for does not exist')
