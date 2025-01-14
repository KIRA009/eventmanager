from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.postgres.fields import JSONField
from django.utils.timezone import localdate, now
import json
import secrets

from utils.base_model_mixin import AutoCreatedUpdatedMixin
from payments.managers import OrderManager


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
    is_unsubscribed = models.BooleanField(default=False)
    test = models.BooleanField(default=False)
    order = GenericRelation("payments.OrderItem")

    def __str__(self):
        return f'{self.user.username} -> {self.sub_type} : {self.start_date} - {self.end_date}'

    def is_active(self):
        today = localdate(now())
        return self.start_date <= today <= self.end_date if self.start_date and self.end_date else True

    exclude_fields = AutoCreatedUpdatedMixin.get_exclude_fields_copy()
    exclude_fields += ['user']
    process_fields = AutoCreatedUpdatedMixin.get_process_fields_copy()
    process_fields.update(**dict(
        is_active=lambda x: x.is_active()
    ))


class OrderItem(AutoCreatedUpdatedMixin):
    order = GenericForeignKey()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    index = models.IntegerField(default=0)
    meta_data = JSONField(default=dict, blank=True)
    order_id = models.ForeignKey(
        "Order", on_delete=models.CASCADE, related_name="items"
    )

    exclude_fields = AutoCreatedUpdatedMixin.get_exclude_fields_copy()
    exclude_fields += ['object_id', 'order_id', 'content_type']
    process_fields = AutoCreatedUpdatedMixin.get_process_fields_copy()
    process_fields.update(**dict(
        order=lambda x: x.order.detail(),
        order_type=lambda x: x.content_type.model
    ))


class Order(AutoCreatedUpdatedMixin):
    INITIATED = "Order Initiated"
    PROCESSED = 'Order Processed'
    CONFIRMED = 'Order Confirmed'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
    REFUND_INITIATED = 'Refund initiated'
    REFUNDED = 'Refunded'
    CANCELLED = 'Cancelled'
    STATUS_CHOICES = (
        (INITIATED, "Order Initiated"),
        (PROCESSED, 'Order Processed'),
        (CONFIRMED, 'Order Confirmed'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (REFUND_INITIATED, 'Refund initiated'),
        (REFUNDED, 'Refunded'),
        (CANCELLED, 'Cancelled')
    )
    order_id = models.TextField(default="")
    amount = models.BigIntegerField(default=0)
    meta_data = JSONField(default=dict, blank=True)
    paid = models.BooleanField(default=False)
    cod = models.BooleanField(default=False)
    status = models.TextField(default=INITIATED, choices=STATUS_CHOICES)
    shipping_charges = models.IntegerField(default=0)
    resell_margin = models.IntegerField(default=0)
    cancel_reason = models.TextField(default='', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders", null=True, blank=True)
    seller = models.ForeignKey('payments.Seller', on_delete=models.CASCADE, related_name="orders", null=True)
    reseller = models.ForeignKey('payments.Seller', on_delete=models.CASCADE, related_name="resold_orders", null=True)

    @staticmethod
    def process_meta(meta):
        if meta.get('notes'):
            meta['notes']['query'] = json.loads(meta['notes']['query'])
        return meta

    def __str__(self):
        return f'{self.user.username if self.user else self.meta_data["user_details"]["name"]} -> {self.order_id}'

    exclude_fields = ['updated_at']
    process_fields = AutoCreatedUpdatedMixin.process_fields.copy()
    process_fields.update(**dict(
        meta_data=lambda x: Order.process_meta(x),
        items=lambda x: x.items.all().detail(),
        tracking_number=lambda x: x.shipment.awb_code if hasattr(x, 'shipment') else None
    ))

    objects = OrderManager()

    def update_status(self, new_status, send_update=True):
        from .utils import send_text_update
        if not self.paid:
            return
        if new_status == self.status:
            return
        self.status = new_status
        if new_status == self.DELIVERED:
            self.paid = True
        elif new_status == self.REFUNDED and not self.cod:
            seller = Seller.objects.get_or_create(user=self.items.first().order.user)[0]
            seller.amount -= int(0.02 * self.amount)
            seller.save()
        self.save()
        if send_update:
            send_text_update(self)

    class Meta:
        ordering = ['-created_at']


def create_base_commission():
    return dict(online=dict(percent=3, extra=5), cod=dict(percent=3, extra=5))


class Seller(AutoCreatedUpdatedMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller')
    amount = models.IntegerField(default=0)
    account_holder_name = models.TextField(default='', blank=True)
    account_number = models.TextField(default='', blank=True)
    ifsc_code = models.TextField(default='', blank=True)
    shipping_area = models.TextField(default='World Wide shipping')
    shop_address = models.TextField(blank=True, default='')
    city = models.TextField(default='', blank=True)
    state = models.TextField(default='', blank=True)
    country = models.TextField(default='', blank=True)
    pincode = models.TextField(default='', blank=True)
    is_category_view_enabled = models.BooleanField(default=False)
    has_free_delivery_above_amount = models.BooleanField(default=False)
    free_delivery_above_amount = models.IntegerField(default=0)
    pickup_location = models.TextField(max_length=8, default='')
    commission = JSONField(default=create_base_commission)

    def save(self, *args, **kwargs):
        if not self.pickup_location:
            self.pickup_location = secrets.token_hex(4)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} -> {self.amount}'


class RetrieveAmount(AutoCreatedUpdatedMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='retrieved')
    amount = models.IntegerField(default=0)
    paid = models.BooleanField(default=False)

    def __str__(self):
        if self.paid:
            return f'{self.user} wash paid {self.amount}'
        return f'{self.user} asked for {self.amount}'

    exclude_fields = ['updated_at']
