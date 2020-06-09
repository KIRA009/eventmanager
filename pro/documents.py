from django_elasticsearch_dsl import (
	Index, fields, Document
)

from .models import Product, ProductCategory


product_index = Index('products')
product_index.settings(
	number_of_shards=1,
	number_of_replicas=0
)


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
