from django.db import models
from django.utils import timezone as tz


class AutoCreatedUpdatedMixin(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    objects = models.Manager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = tz.now()
            self.updated_at = self.created_at
        else:
            auto_updated_at_is_disabled = kwargs.pop("disable_auto_updated_at", False)
            if not auto_updated_at_is_disabled:
                self.updated_at = tz.now()
        super(AutoCreatedUpdatedMixin, self).save(*args, **kwargs)

    def detail(self):
        ret = self.__dict__
        del ret["_state"]
        return ret
