from . import auth_blueprint
from flask import make_response, jsonify , request
from app.models import User, BlacklistToken
import jwt
from flask_bcrypt import Bcrypt

@auth_blueprint.route('/register', methods=['POST'])
def register_user():
    """Route handles registration of a new user"""
    user = User.query.filter_by(username=request.data['username']).first()

    if not user:
        post_data = request.data
        firstname = post_data['firstname']
        lastname = post_data['lastname']
        username = post_data['username']
        password = post_data['password']
        email = post_data['email']

        user = User(
            firstname=firstname,
            lastname=lastname,
            username=username,
            password=password,
            email=email)
        user.save()

        response = {
            'message':'Successfully registered!',
            'status':'Success'
        }
        return make_response(jsonify(response)), 201
    response = {
        'message': 'Failed to register, duplicate user',
        'status': 'Failed!!'
    }
    return make_response(jsonify(response)), 202

@auth_blueprint.route('/login', methods=['POST'])
def login_user():
    """Function handles logging in a user"""
    user = User.query.filter_by(username=request.data['username']).first()

    if user and user.password_is_valid(request.data['password']):
        auth_token = user.encode_auth_token(user.id)
        if auth_token:
            response = {
                'message': 'Succesfully logged in',
                'status': 'Success',
                'auth_token': auth_token.decode()
            }
            return make_response(jsonify(response)), 200
    response = {
        'message': 'Failed to login, unknown username or password',
        'status': 'Failed'
    }
    return make_response(jsonify(response)), 401

@auth_blueprint.route('/reset-password', methods=['POST'])
def reset_password():
    """Function handles resetting a password for a given user"""
    user = User.query.filter_by(username=request.data['username']).first()

    if user and user.password_is_valid(request.data['old_password']):
        user.password = Bcrypt().generate_password_hash(password=request.data['new_password'])
        user.save()
        response = {
            'message': 'Successfully changed password',
            'status': 'Success'
        }
        return make_response(jsonify(response)), 200
    response = {
        'message': 'Failed to reset password, bad username or password',
        'status': 'Failed'
    }
    return make_response(jsonify(response)), 400

@auth_blueprint.route('/logout', methods=['POST'])
def logout_user():
    """Functions logout out a user by blacklisting the authentication token"""
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''
    if auth_token and not isinstance(
        User.decode_auth_token(auth_token), str):
        blacklist_token = BlacklistToken(token=auth_token)
        try:
            blacklist_token.save()
            response = {
                'message':"Successfully logged out",
                'status':"Success"
            }
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {
                "message": e,
                "status": "Failed"
            }
            return make_response(jsonify(response)), 200

    response = {
        'message': "Failed to logout, Invalid token",
        'status': "Failed"
    }
    return make_response(jsonify(response)), 401
        
    
