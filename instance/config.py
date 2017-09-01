"""Module contains configurations for the app"""
import os

class Config:
    """The Parent configurations for the app"""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = 'My-secret-a-long-string'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost/bucketlist_api'

class DevelopmentConfig(Config):
    """Class for development configurations"""
    DEBUG = True

class TestingConfig(Config):
    """Class for the testing configurations"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost/test_db'

class StagingConfig(Config):
    """Class for the staging configurations"""
    DEBUG = True

class ProductionConfig(Config):
    """Class for the Production configurations"""
    DEBUG = False
    TESTING = False

app_config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'staging':StagingConfig,
    'production':ProductionConfig
}
