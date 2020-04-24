from event_app.models import College, User
from utils import create_token

from event_app.tests import BaseTestCase


class UnAuth(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        college = College.objects.create(name='name', address='address', state='state', has_college_email=False)
        cls.user = User.objects.create(college=college, phone='phone', name='name')

    def test_successful_register(self):
        res = self.post('/event_manager/api/register/', data=dict(
            name="Shohan",
            phone="8135026346",
            college=1
        ))
        self.assertEqual(res.status_code, 200, self.invalid_sc)
        self.assertIn('secret', self.loads(res), self.invalid_resp)

    def test_unsuccessful_register_due_to_existing_phone(self):
        res = self.post('/event_manager/api/register/', data=dict(
            name="Shohan",
            phone="phone",
            college=1
        ))
        self.assertEqual(res.status_code, 401, self.invalid_sc)
        self.assertIn('error', self.loads(res), self.invalid_resp)

    def test_successful_update(self):
        res = self.post('/event_manager/api/update/', data=dict(
            secret=self.user.secret,
            email='email@gmail.com',
            password='password'
        ))
        self.assertEqual(res.status_code, 200, self.invalid_sc)
        self.assertIn('message', self.loads(res), self.invalid_resp)

    def test_unsuccessful_update_due_to_invalid_email(self):
        res = self.post('/event_manager/api/update/', data=dict(
            secret=self.user.secret,
            email='abc',
            password='password'
        ))
        self.assertEqual(res.status_code, 404, self.invalid_sc)
        self.assertIn('error', self.loads(res), self.invalid_resp)

    def test_unsuccessful_update_due_to_duplicate_email(self):
        self.user.email = 'abc@gmail.com'
        self.user.save()
        user = User.objects.create(college=College.objects.get(), phone=self.user.phone + '1', name='name',
                                   username=self.user.username + '1')
        res = self.post('/event_manager/api/update/', data=dict(
            secret=user.secret,
            email=self.user.email,
            password='password'
        ))
        self.assertEqual(res.status_code, 404, self.invalid_sc)
        self.assertIn('error', self.loads(res), self.invalid_resp)

    def test_successful_get_colleges(self):
        res = self.get('/event_manager/api/colleges/')
        self.assertEqual(res.status_code, 200)
        data = self.loads(res)
        self.assertEqual(data, dict(colleges=[_.detail() for _ in College.objects.all()]))

    def test_successful_login(self):
        self.user.set_password('pass')
        self.user.save()
        res = self.post('/event_manager/api/login/', data=dict(
            username=self.user.email,
            password='pass'
        ))
        self.assertEqual(res.status_code, 200, self.invalid_sc)
        data = self.loads(res)
        self.assertEqual(data, dict(
            data="Successful",
            user=self.user.detail(),
            token=create_token(
                username=f"{self.user.email}$$${self.user.password}",
                len_email=len(self.user.email),
            )
        ))

    def test_unsuccessful_login_due_to_invalid_email(self):
        self.user.set_password('pass')
        self.user.save()
        res = self.post('/event_manager/api/login/', dict(
            username=self.user.email + '1',
            password='pass'
        ))
        self.assertEqual(res.status_code, 401)
        self.assertIn('error', self.loads(res))

    def test_unsuccessful_login_due_to_invalid_pwd(self):
        self.user.set_password('pass')
        self.user.save()
        res = self.post('/event_manager/api/login/', dict(
            username=self.user.email,
            password='passw'
        ))
        self.assertEqual(res.status_code, 401)
        self.assertIn('error', self.loads(res))
