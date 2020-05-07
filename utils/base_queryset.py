from django.db.models import QuerySet
import json
from django.core import serializers


class BaseQuerySet(QuerySet):
	def detail(self):
		rows = json.loads(serializers.serialize('json', self._chain()))
		for index, row in enumerate(rows):
			row['fields']['id'] = row['pk']
			row = row['fields']
			for i in self.model.exclude_fields:
				del row[i]
			for k, v in self.model.process_fields.items():
				row[k] = v(row.get(k, self))
			rows[index] = row
		return rows