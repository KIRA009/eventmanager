from django.db.models import Q

from utils.base_manager import BaseManager


class ProductManager(BaseManager):
	def get_products(self, user):
		return self.select_related('category').filter(
			Q(user__username=user) | Q(resell_product__sellers__user__username=user)
		)
