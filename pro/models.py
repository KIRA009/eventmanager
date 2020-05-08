from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from json import loads

from utils.base_model_mixin import AutoCreatedUpdatedMixin
from event_app.models import User


class ProModeFeature(AutoCreatedUpdatedMixin):
    header_icon = models.URLField(default="", null=True, blank=True)
    header_text = models.TextField(default="", null=True, blank=True)
    background_color = models.TextField(default=None, null=True, blank=True)
    background_image = models.URLField(default=None, null=True, blank=True)
    link_style = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feature")


class ProPack(AutoCreatedUpdatedMixin):
    INR = 'INR'
    USD = 'USD'
    CURRENCIES = (
        (INR, '₹'),
        (USD, '$')
    )
    MONTHLY = 'monthly'
    YEARLY = 'yearly'
    TYPES = (
        (MONTHLY, 'Monthly pack'),
        (YEARLY, 'Yearly pack'),
    )
    price = models.IntegerField(default=300)
    plan_id = models.TextField(blank=True, default='')
    period = models.CharField(max_length=256, default=MONTHLY, blank=True, choices=TYPES)
    currency = models.TextField(choices=CURRENCIES, default=INR)
    features = ArrayField(models.TextField(blank=True), default=list, blank=True)

    def save(self, *args, **kwargs):
        from payments.utils import get_plan, create_plan
        if self.plan_id:
            error, plan = get_plan(self.plan_id)
            if error:
                return
            if plan['item']['amount'] != 100 * self.price or plan['period'] != self.period:
                self.plan_id = create_plan(self)['id']
        super(ProPack, self).save()

    process_fields = AutoCreatedUpdatedMixin.get_process_fields_copy()
    process_fields.update(**{
        'features': lambda x: loads(x)
    })


class Product(AutoCreatedUpdatedMixin):
    name = models.TextField(blank=False, default='Product')
    description = models.TextField(blank=True, default='Description')
    disc_price = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    images = ArrayField(models.URLField(blank=True), blank=True, default=list)
    estimated_delivery = models.TextField(default='', blank=False)
    meta_data = JSONField(default=dict)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')

    process_fields = AutoCreatedUpdatedMixin.get_process_fields_copy()
    process_fields.update(**dict(
        images=lambda x: loads(x)
    ))
