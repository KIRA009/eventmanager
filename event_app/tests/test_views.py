from mixer.backend.django import mixer
import pytest

from utils.base_test_case import BaseTestCase
from event_app.models import User


pytestmark = pytest.mark.django_db


class TestUnAuth(BaseTestCase):
    def setUp(self):
        print('here')
        self.user = mixer.blend('event_app.user')

    def test_register(self):
        data = self.post('register', dict(
            college=1,
            name="name",
            email="abc@gmail.com",
            password="pass"
        ))
        user = User.objects.get(email="abc@gmail.com")
        self.assertEqual(data, user.detail())
