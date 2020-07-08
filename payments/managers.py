from django.db.models import Q

from utils.base_manager import BaseManager


class OrderManager(BaseManager):
	def get_sold_products(self, user):
		return self.filter(Q(seller__user=user) | Q(reseller__user=user), paid=True)
