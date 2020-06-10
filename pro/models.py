from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from json import loads
from django.contrib.contenttypes.fields import GenericRelation, ContentType

from utils.base_model_mixin import AutoCreatedUpdatedMixin
from event_app.models import User


class ProModeFeature(AutoCreatedUpdatedMixin):
    header_icon = models.URLField(default="", null=True, blank=True)
    header_text = models.TextField(default="", null=True, blank=True)
    background_color = models.TextField(default=None, null=True, blank=True)
    background_image = models.URLField(default=None, null=True, blank=True)
    link_style = models.TextField(blank=True, null=True)
    preview_image = models.TextField(default='', blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="feature")


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
        super().save()

    process_fields = AutoCreatedUpdatedMixin.get_process_fields_copy()
    process_fields.update(**{
        'features': lambda x: loads(x)
    })


class ProductCategory(AutoCreatedUpdatedMixin):
    name = models.TextField(blank=True)
    image = models.URLField(blank=True, default='')
    seller = models.ForeignKey('payments.Seller', on_delete=models.CASCADE, related_name='categories')


class Product(AutoCreatedUpdatedMixin):
    name = models.TextField(blank=False, default='Product')
    description = models.TextField(blank=True, default='Description')
    disc_price = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    images = ArrayField(models.URLField(blank=True), blank=True, default=list)
    estimated_delivery = models.TextField(default='', blank=False)
    meta_data = JSONField(default=dict, blank=True)
    preview_images = ArrayField(models.TextField(default='', blank=True), default=list, blank=True)
    cod_available = models.BooleanField(default=False)
    online_available = models.BooleanField(default=False)
    stock = models.IntegerField(default=1000)
    shipping_charges = models.IntegerField(default=0)
    opt_for_reselling = models.BooleanField(default=False)
    resell_margin = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, related_name='products', default=None,
                                 null=True)
    order = GenericRelation("payments.OrderItem", related_query_name='product')

    exclude_fields = AutoCreatedUpdatedMixin.get_exclude_fields_copy()
    exclude_fields += ['category']
    process_fields = AutoCreatedUpdatedMixin.get_process_fields_copy()
    process_fields.update(**dict(
        images=lambda x: loads(x),
        preview_images=lambda x: loads(x),
        category=lambda x: x.category.detail() if x.category else None
    ))

    def delete(self, using=None, keep_parents=False, content_type=None):
        if self.order.count() > 0:
            if content_type is None:
                content_type = ContentType.objects.get_for_model(DeletedButUsedProduct)
            _del = DeletedButUsedProduct.objects.create(name=self.name, description=self.description,
                                                        disc_price=self.disc_price, price=self.price,
                                                        images=self.images, estimated_delivery=self.estimated_delivery,
                                                        meta_data=self.meta_data, preview_images=self.preview_images,
                                                        cod_available=self.cod_available,
                                                        online_available=self.online_available, stock=self.stock,
                                                        shipping_charges=self.shipping_charges,
                                                        opt_for_reselling=self.opt_for_reselling,
                                                        resell_margin=self.resell_margin, user=self.user,
                                                        category=self.category)
            self.order.all().update(content_type=content_type, object_id=_del.id)
        super().delete(using, keep_parents=True)

    def __str__(self):
        return f'{self.name} -> {self.user}'


class DeletedButUsedProduct(AutoCreatedUpdatedMixin):
    name = models.TextField(blank=False, default='Product')
    description = models.TextField(blank=True, default='Description')
    disc_price = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    images = ArrayField(models.URLField(blank=True), blank=True, default=list)
    estimated_delivery = models.TextField(default='', blank=False)
    meta_data = JSONField(default=dict, blank=True)
    preview_images = ArrayField(models.TextField(default='', blank=True), default=list, blank=True)
    cod_available = models.BooleanField(default=False)
    online_available = models.BooleanField(default=False)
    stock = models.IntegerField(default=1000)
    shipping_charges = models.IntegerField(default=0)
    opt_for_reselling = models.BooleanField(default=False)
    resell_margin = models.IntegerField(default=0)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, related_name='deleted_products',
                                 default=None, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deleted_products')
    order = GenericRelation("payments.OrderItem", related_query_name='deleted_product')

    exclude_fields = AutoCreatedUpdatedMixin.get_exclude_fields_copy()
    exclude_fields += ['category']
    process_fields = AutoCreatedUpdatedMixin.get_process_fields_copy()
    process_fields.update(**dict(
        images=lambda x: loads(x),
        preview_images=lambda x: loads(x),
        category=lambda x: x.category.detail() if x.category else None
    ))

    def __str__(self):
        return f'{self.name} -> {self.user}'


class ResellProduct(AutoCreatedUpdatedMixin):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='resell_product', null=True)
    sellers = models.ManyToManyField('payments.Seller', related_name='resell_product')

    exclude_fields = AutoCreatedUpdatedMixin.get_exclude_fields_copy()
    exclude_fields += ["product", "sellers"]
    process_fields = AutoCreatedUpdatedMixin.get_process_fields_copy()
    process_fields.update(**dict(
        product=lambda x: x.product.detail(),
        seller=lambda x: dict(
            **x.product.user.feature.detail()
        )
    ))
