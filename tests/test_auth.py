"""The module contains tests for the authentication service"""
from .base import BaseTestCase
import json

class TestAuth(BaseTestCase):
    """Class contains tests to test the authentication service"""

    def test_register_success(self):
        """Tests successful registration, status code should be 201, with a success message"""
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    firstname='Innocent',
                    lastname='Asiimwe',
                    username='inno',
                    password='pass',
                    email='asiimwe@outlook.com'
                    )),
                content_type='application/json',
                )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('Successfully registered!', data['message'])
            self.assertIn('Success', data['status'])

    def test_register_duplicate(self):
        """Tests registration of a duplicate username, """
        with self.client:
            self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    firstname='Innocent',
                    lastname='Asiimwe',
                    username='inno',
                    password='pass',
                    email='asiimwe@outlook.com'
                    )),
                content_type='application/json'
                )
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    firstname='Jane',
                    lastname='Basemera',
                    username='inno',
                    password='yyy',
                    email='j@jane.com'
                )),
                content_type='application/json'
                )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 202)
            self.assertIn('Failed to register, duplicate user', data['message'])
            self.assertIn('Failed!!', data['status'])
    def test_login_success(self):
        """Tests a successful login"""
        with self.client:
            res = self.client.post(
                'auth/register',
                data=json.dumps(dict(
                    firstname='Innocent',
                    lastname='Asiimwe',
                    username='inno',
                    password='pass',
                    email='asiimwe@outlook.com'
                )),
                content_type='application/json'
            )
        self.assertEqual(res.status_code, 201)
        response = self.client.post(
            'auth/login',
            data=json.dumps(dict(
                username='inno',
                password='pass'
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('Succesfully logged in', data['message'])
        self.assertIn('Success', data['status'])
        self.assertTrue(data['auth_token'])

    def test_login_unregistered(self):
        """Tests an unregistered user cannot login"""
        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    username='unknown',
                    password='unknown'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertIn("Failed to login, unknown username or password", data['message'])
            self.assertIn('Failed', data['status'])
            

    def test_login_wrong_password(self):
        """Tests user cannot login in with wrong password"""
        with self.client:
            res= self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    firstname='Innocent',
                    lastname='Asiimwe',
                    username='inno',
                    password='pass',
                    email='asiimwe@outlook.com'
                    )),
                    content_type='application/json'
            )
            self.assertEqual(res.status_code, 201)
            response = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    username='inno',
                    password='wrongpass'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertIn("Failed to login, unknown username or password", data['message'])
            self.assertIn('Failed', data['status'])
