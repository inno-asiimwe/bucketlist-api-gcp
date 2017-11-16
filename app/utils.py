"""Module for decorated functions"""
from functools import wraps
from flask import request, jsonify, make_response
from .models import User


def auth_required(f):
    """decorator for authenticating a user using token based authentication """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """ Decorated function for authenticating a user"""
        response = {
            'status': 'Failed',
            'message': 'Invalid token'
        }
        code = 401

        auth_header = request.headers.get('Authorization')
        if not auth_header:
            auth_token = ''
        else:
            auth_token = auth_header.split(" ")[1]
            resp = User.decode_auth_token(auth_token)
        if not auth_token or isinstance(resp, str):
            return make_response(jsonify(response)), code
        user = {'user_id': resp, 'auth_token': auth_token}
        return f(user, *args, **kwargs)
    return decorated_function
