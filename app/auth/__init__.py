"""Initialising the auth_blueprint for all the authentication """
from flask import Blueprint

auth_blueprint = Blueprint('auth', __name__)

from . import views
