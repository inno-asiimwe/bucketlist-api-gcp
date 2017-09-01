"""Module contains tests for the app configurations"""
import unittest
from flask import current_app
from flask_testing import TestCase
from app import create_app

class TestDevelopmentConfig(TestCase):
    """Class to test development configurations"""
    def create_app(self):
        """Creating a development app"""
        app = create_app(config_name='development')
        return app
    #app = create_app()

    def test_app_is_development(self):
        """
        Method ensures app is using development configurations
        Running in debug mode 
        Usiing the correct database_url and secret
        """
        self.assertTrue(self.app.config['SECRET'] == 'My-secret-a-long-string')
        self.assertTrue(self.app.config['DEBUG'])
        self.assertFalse(current_app is None)
        self.assertTrue(
            self.app.config['SQLALCHEMY_DATABASE_URI'] ==
            'postgresql://postgres:admin@localhost/bucketlist_api'
        )
