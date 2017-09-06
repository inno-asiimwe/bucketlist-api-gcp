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
            self.assertEqual(response.status_code, 400)
