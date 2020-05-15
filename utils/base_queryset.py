from django.db.models import QuerySet
import json
from django.core import serializers
from django.core.paginator import Paginator


class BaseQuerySet(QuerySet):
	def detail(self):
		query = self._chain()
		rows = json.loads(serializers.serialize('json', query))
		for index, row in enumerate(rows):
			row['fields']['id'] = row['pk']
			row = row['fields']
			for i in self.model.exclude_fields:
				del row[i]
			for k, v in self.model.process_fields.items():
				row[k] = v(row.get(k, query[index]))
			rows[index] = row
		return rows

	def paginate(self, page_no):
		paginator = Paginator(self._chain(), 10)
		if page_no > paginator.num_pages:
			return self.model.objects.none()
		return paginator.get_page(page_no).object_list
