from django.db import models
import django.utils.timezone as tz
import json
from django.core import serializers


from .base_manager import BaseManager


class AutoCreatedUpdatedMixin(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    objects = BaseManager()

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
        ret = json.loads(serializers.serialize('json', [self]))[0]
        ret['fields']['id'] = ret['pk']
        for i in self.Encoding.exclude_fields:
            del ret['fields'][i]
        for k, v in self.Encoding.process_fields.items():
            ret['fields'][k] = v(ret['fields'].get(k, self))
        return ret['fields']

    class Encoding:
        exclude_fields = ['created_at', 'updated_at']
        process_fields = {}
