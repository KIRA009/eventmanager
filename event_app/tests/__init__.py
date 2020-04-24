from django.test import TestCase, Client
from json import loads


class BaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.loads = lambda x, y: loads(y.content.decode())
        cls.invalid_sc = 'Invalid status code'
        cls.invalid_resp = 'Invalid response'
        cls.maxDiff = None

    def post(self, url, data):
        return self.client.post(url, data, content_type='application/json')

    def get(self, url):
        return self.client.get(url)

    def setUp(self):
        print(f'Testing {self._testMethodName}')