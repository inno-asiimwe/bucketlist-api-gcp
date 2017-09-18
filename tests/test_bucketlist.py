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

    def test_create_bucketlist_duplicate_name(self):
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

    def test_get_bucketlists(self):
        """Tests api can get all bucketlists for a given user  """
        with self.client:
            res_register = self.register_user()
            res_login = self.login_user()
            user_id = User.query.filter_by(username='inno').first().id
            access_token = json.loads(res_login.data.decode())['auth_token']
            res_post = self.client.post(
                '/bucketlists/',
                headers=dict(Authorization="Bearer " + access_token),
                data=json.dumps(dict(
                    name='before 30',
                    description='Things to do before I am 30 years',
                    owner=user_id
                )),
                content_type='application/json'
                )
            response = self.client.get(
                '/bucketlists/',
                headers=dict(Authorization="Bearer "+ access_token),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(res_post.status_code, 201)
            self.assertEqual(response.status_code, 200)
            self.assertIn('before 30', data[0]['name'])
    
    def test_get_bucketlist(self):
        """Tests api can get a bucketlist by id """
        with self.client:
            res_register = self.register_user()
            res_login = self.login_user()
            user_id = User.query.filter_by(username='inno').first().id
            access_token = json.loads(res_login.data.decode())['auth_token']
            res_post = self.client.post(
                '/bucketlists/',
                headers=dict(Authorization="Bearer " + access_token),
                data=json.dumps(dict(
                    name='before 30',
                    description='Things to do before I am 30 years',
                    owner=user_id
                )),
                content_type='application/json'
                )
            result = json.loads(res_post.data.decode())
            response = self.client.get(
                '/bucketlists/{}'.format(result['id']),
                headers=dict(Authorization='Bearer ' + access_token),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(res_post.status_code, 201)
            self.assertEqual(response.status_code, 200)
            self.assertIn('before 30', data['name'])

    def test_get_bucketlist_invalid_id(self):
        """ Tests API returns 404 for an invalid id"""
        with self.client:
            res_register = self.register_user()
            res_login = self.login_user()
            access_token = json.loads(res_login.data.decode())['auth_token']
            response = self.client.get(
                '/bucketlists/1',
                headers=dict(Authorization='Bearer ' + access_token),
                content_type='application/json'
            )
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(response.status_code, 404)
            
    def test_put_bucketlist(self):
        """Tests API can update bucketlist"""
        with self.client:
            res_register = self.register_user()
            res_login = self.login_user()
            user_id = User.query.filter_by(username='inno').first().id
            access_token = json.loads(res_login.data.decode())['auth_token']
            res_post = self.client.post(
                '/bucketlists/',
                headers=dict(Authorization="Bearer " + access_token),
                data=json.dumps(dict(
                    name='before 30',
                    description='Things to do before I am 30 years',
                    owner=user_id
                )),
                content_type='application/json'
                )
            result = json.loads(res_post.data.decode())
            response = self.client.put(
                '/bucketlists/{}'.format(result['id']),
                headers=dict(Authorization="Bearer " + access_token),
                data=json.dumps(dict(
                    name='Before 30'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(res_post.status_code, 201)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Before 30', data['name'])

    def test_put_bucketlist_invalid_id(self):
        """Tests API returns 404 for an invalid id"""
        with self.client:
            res_register = self.register_user()
            res_login = self.login_user()
            access_token = json.loads(res_login.data.decode())['auth_token']
            response = self.client.put(
                '/bucketlists/1',
                headers=dict(Authorization='Bearer ' + access_token),
                data=dict(
                    name='before 30'
                ),
                content_type='application/json'
            )
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(response.status_code, 404)

    def test_delete_bucketlist(self):
        """ Tests API can delete bucketlist by id """
        with self.client:
            res_register = self.register_user()
            res_login = self.login_user()
            user_id = User.query.filter_by(username='inno').first().id
            access_token = json.loads(res_login.data.decode())['auth_token']
            res_post = self.client.post(
                '/bucketlists/',
                headers=dict(Authorization="Bearer " + access_token),
                data=json.dumps(dict(
                    name='before 30',
                    description='Things to do before I am 30 years',
                    owner=user_id
                )),
                content_type='application/json'
                )
            result = json.dumps(res_post.data.decode())
            response = self.client.delete(
                '/bucketlists/{}'.format(result['id']),
                headers=dict(Authorization='Bearer ' + access_token),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            res_get = self.client.get(
                '/bucketlists/{}' .format(result['id']),
                headers=dict(Authorization='Bearer ' + access_token),
                content_type='application/json'
            )

            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(res_post.status_code, 201)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Success', data['status'])
            self.assertEqual(res_get.status_code, 404)

    def test_delete_bucketlist_invalid_id(self):
        """Tests API returns 404 for an invalid id"""
        with self.client:
            res_register = self.register_user()
            res_login = self.login_user()
            access_token = json.loads(res_login.data.decode())['auth_token']
            response = self.client.delete(
                '/bucketlists/1',
                headers=dict(Authorization='Bearer ' + access_token),
                data=dict(
                    name='before 30'
                ),
                content_type='application/json'
            )
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(response.status_code, 404)
