from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
import json

from utils import AutoCreatedUpdatedMixin


User = get_user_model()


class OrderItem(AutoCreatedUpdatedMixin):
    order = GenericForeignKey()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    meta_data = models.TextField(default="")
    index = models.IntegerField(default=0)
    order_id = models.ForeignKey(
        "Order", on_delete=models.CASCADE, related_name="items"
    )

    def detail(self):
        det = super(OrderItem, self).detail()
        det["meta_data"] = json.loads(det["meta_data"])
        return det


class Order(AutoCreatedUpdatedMixin):
    order_id = models.TextField(default="")
    amount = models.BigIntegerField(default=0)
    payment_id = models.TextField(default="")
    signature = models.TextField(default="")
    meta_data = models.TextField(default="")
    paid = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")

    def detail(self):
        det = super(Order, self).detail()
        det["meta_data"] = json.loads(det["meta_data"])
        return det
