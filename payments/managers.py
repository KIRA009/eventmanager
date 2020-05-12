from django.db.models import Q

from utils.base_manager import BaseManager


class OrderManager(BaseManager):
	def get_sold_products(self, user):
		query = (
				(
						Q(items__product__user=user) | Q(items__deleted_product__user=user)
				) &
				Q(items__content_type__model__in=['deletedbutusedproduct', 'product'])
		)
		return self.filter(query).distinct()
