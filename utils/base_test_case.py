from django.test import TestCase
from django.shortcuts import resolve_url
from json import loads


class BaseTestCase(TestCase):
	def get(self, url):
		url = resolve_url(url)
		return loads(self.client.get(url)._container[0].decode())

	def post(self, url, data, content_type='json'):
		url = resolve_url(url)
		if content_type == 'json':
			return loads(self.client.post(url, data=data, content_type='application/json')._container[0].decode())
