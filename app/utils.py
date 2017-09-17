"""Module for decorated functions"""
from functools import wraps
from flask import request, jsonify, make_response
from .models import User

def @auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response  = {
            'status': 'Failed'
            'message': 'Invalid token'
        }
        code = 401

        auth_header = request.headers.get('Authorization')
        if not auth_header:
            auth_token = ''
        else:
            auth_token = auth_header.split(" ")[1]
        
        if not auth_token or isinstance(User.decode_auth_token(auth_token), str):
            return make_response(jsonify(response)), code
        return decorated_function
