from django_elasticsearch_dsl import (
	Index, fields, Document
)
from django_elasticsearch_dsl.registries import registry

from .models import Product, ProductCategory
from event_manager.settings import DEBUG


product_index = Index('products' if DEBUG else 'products_prod')
product_index.settings(
	number_of_shards=1,
	number_of_replicas=0
)


@registry.register_document
@product_index.doc_type
class ProductDocument(Document):
	name = fields.TextField(
		attr='name',
		fields={
			'suggest': fields.Completion()
		}
	)
	category = fields.ObjectField(
		attr='category',
		properties={
			'name': fields.TextField(
				attr='name',
				fields={
					'suggest': fields.Completion()
				}
			)
		}
	)
	description = fields.TextField(
		attr='description',
		fields={
			'suggest': fields.Completion()
		}
	)

	class Django:
		model = Product
		related_models = [ProductCategory]

	def get_instances_from_related(self, related_instance):
		if isinstance(related_instance, ProductCategory):
			return related_instance.products.all()
