"""Module contains tests for the bucketlist service"""
import json
from app.models import User
from .base import BaseTestCase


class TestBucketlist(BaseTestCase):
    """class contains tests for the bucketlist service"""

    def register_user(
            self,
            firstname='Innocent',
            lastname='Asiimwe',
            username='inno',
            password='pass',
            email='a@a.com'):
        """Helper method to register a user"""
        data = {
            'firstname': firstname,
            'lastname': lastname,
            'username': username,
            'password': password,
            'email': email
        }
        response = self.client.post(
            '/auth/register',
            data=json.dumps(data),
            content_type='application/json')
        return response

    def login_user(self, username='inno', password='pass'):
        """Helper method to login a user"""
        data = dict(
            username=username,
            password=password
        )
        response = self.client.post(
            '/auth/login',
            data=json.dumps(data),
            content_type='application/json'
            )
        return response

    def test_create_bucketlist_success(self):
        """Tests successful creation of bucketlist"""

        with self.client:
            res_register = self.register_user()
            res_login = self.login_user()
            user_id = User.query.filter_by(username='inno').first().id
            access_token = json.loads(res_login.data.decode())['auth_token']
            response = self.client.post(
                '/bucketlists/',
                headers=dict(Authorization="Bearer " + access_token),
                data=json.dumps(dict(
                    name='before 30',
                    description='Things to do before I am 30 years',
                    owner=user_id
                )),
                content_type='application/json'
                )
            data = json.loads(response.data.decode())
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(response.status_code, 201)
            self.assertIn('before 30', data['name'])

    def test_create_bucketlist_duplicate(self):
        """Tests API doesnot create bucketlists with duplicate"""

        with self.client:
            res_register = self.register_user()
            res_login = self.login_user()
            user_id = User.query.filter_by(username='inno').first().id
            access_token = json.loads(res_login.data.decode())['auth_token']
            response1 = self.client.post(
                '/bucketlists/',
                headers=dict(Authorization="Bearer " + access_token),
                data=json.dumps(dict(
                    name='before 30',
                    description='Things to do before I am 30 years',
                    owner=user_id
                )),
                content_type='application/json'
            )
            response2 = self.client.post(
                '/bucketlists/',
                headers=dict(Authorization="Bearer " + access_token),
                data=json.dumps(dict(
                    name='before 30',
                    description='Places to visit before I am 30 years',
                    owner=user_id
                )),
                content_type='application/json'
            )
            data1 = json.loads(response1.data.decode())
            data2 = json.loads(response2.data.decode())
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(response1.status_code, 201)
            self.assertEqual(response2.status_code, 202)
            self.assertIn('before 30', data1['name'])
            self.assertIn('Failed', data2['status'])

