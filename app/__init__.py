from flask_api import FlaskAPI 
from flask_sqlalchemy import SQLAlchemy 
from instance.config import app_config
from flasgger import Swagger




db = SQLAlchemy()
swagger = Swagger()

def create_app(config_name):
    """Method to create the flask-api app"""

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    swagger.init_app(app)

    #registering blueprints
    from .auth import auth_blueprint
    from .bucketlist import bucketlist_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(bucketlist_blueprint, url_prefix='/bucketlists')



    return app
