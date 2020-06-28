from django.db import models

from utils.base_model_mixin import AutoCreatedUpdatedMixin


class Shipment(AutoCreatedUpdatedMixin):
	courier_company_id = models.IntegerField()
	courier_name = models.TextField()
	awb_code = models.TextField()
	shipment_id = models.TextField()
	shipment_order_id = models.TextField()
	label_url = models.URLField()
	manifest_url = models.URLField()
	pickup_token_number = models.TextField()
	routing_code = models.TextField()
	applied_weight = models.FloatField()
	pickup_scheduled_date = models.DateTimeField()
	length = models.FloatField(default=0)
	height = models.FloatField(default=0)
	breadth = models.FloatField(default=0)
	weight = models.FloatField(default=0)
	order = models.OneToOneField('payments.Order', on_delete=models.CASCADE, related_name='shipment')
