from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.postgres.fields import JSONField
import json

from utils.base_model_mixin import AutoCreatedUpdatedMixin


User = get_user_model()


class Subscription(AutoCreatedUpdatedMixin):
    PROPACK = 'PROPACK'
    SUB_TYPES = [
        (PROPACK, 'propack'),
    ]
    sub_id = models.TextField(default='', blank=True)
    sub_type = models.TextField(default='PROPACK', choices=SUB_TYPES)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    payment_url = models.URLField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    test = models.BooleanField(default=False)
    order = GenericRelation("payments.OrderItem")

    def __str__(self):
        return f'{self.user.username} -> {self.sub_type} : {self.start_date} - {self.end_date}'


class OrderItem(AutoCreatedUpdatedMixin):
    order = GenericForeignKey()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    meta_data = JSONField(default=dict)
    index = models.IntegerField(default=0)
    order_id = models.ForeignKey(
        "Order", on_delete=models.CASCADE, related_name="items"
    )

    class Encoding(AutoCreatedUpdatedMixin.Encoding):
        process_fields = AutoCreatedUpdatedMixin.Encoding.process_fields.copy()
        process_fields.update(**dict(
            meta_data=lambda x: json.loads(x)
        ))


class Order(AutoCreatedUpdatedMixin):
    order_id = models.TextField(default="")
    amount = models.BigIntegerField(default=0)
    payment_id = models.TextField(default="")
    signature = models.TextField(default="")
    meta_data = JSONField(default=dict)
    paid = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")

    @staticmethod
    def process_meta(meta):
        if meta.get('notes'):
            meta['notes']['query'] = json.loads(meta['notes']['query'])
        return meta

    class Encoding(AutoCreatedUpdatedMixin.Encoding):
        process_fields = AutoCreatedUpdatedMixin.Encoding.process_fields.copy()
        process_fields.update(**dict(
            meta_data=lambda x: Order.process_meta(x),
        ))
