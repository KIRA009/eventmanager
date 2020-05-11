from django.db.models import Q

from utils.base_manager import BaseManager


class OrderItemManager(BaseManager):
	def get_sold_products(self, user):
		query = (
				(
						Q(product__user=user) | Q(deleted_product__user=user)
				) &
				Q(content_type__model__in=['deletedbutusedproduct', 'product'])
		)
		return self.filter(query)
