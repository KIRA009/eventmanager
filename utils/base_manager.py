from django.db import models


class BaseManager(models.Manager):
    def get(self, **kwargs):
        try:
            return super(BaseManager, self).get(**kwargs)
        except self.model.DoesNotExist:
            return None
