from . import auth_blueprint
from flask import make_response, jsonify , request
from app.models import User, BlacklistToken
import jwt
from flask_bcrypt import Bcrypt
from app.utils import auth_required

@auth_blueprint.route('/register', methods=['POST'])
def register_user():
    """Registration of a new user
    ---
    tags:
      - "auth"
    parameters:
      - in: "body"
        name: "body"
        description: "firstname, lastname, username, password, email"
        required: true
        schema:
         type: "object"
         required:
         - "firstname"
         - "lastname"
         - "username"
         - "password"
         - "email"
         properties:
          firstname:
           type: "string"
          lastname:
           type: "string"
          username:
           type: "string"
          password:
           type: "string"
          email:
           type: "string"
    responses:
        201:
            description: "Successfully Registerd"
        202:
            description: "Failed to register"
    """
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
    """Loging in a user
    ---
    tags:
     - "auth"
    parameters:
        - in: "body"
          name: "body"
          description: "Username and password"
          required: true
          schema:
            type: "object"
            required:
            - "username"
            - "password"
            properties:
                username:
                    type: "string"
                password:
                    type: "string"
    responses:
        200:
            description: "Successfully logged in"
        401:
            description: "Failed to login"

    """
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
    """Reset User password
    ---
    tags:
     - "auth"
    parameters:
        - in: "header"
          name: "Authorization"
          description: "Token of logged in user"
          required: true
        - in: "body"
          name: "body"
          description: "Username, old password and new password"
          required: true
          schema:
            type: "object"
            required:
            - "username"
            - "old_password"
            - "new_password"
            properties:
                username:
                    type: "string"
                old_password:
                    type: "string"
                new_password:
                    type: "string"
    responses:
        200:
            description: "Successfully changed password"
        400:
            description: "Failed to reset password, bad username or password"
    """
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
@auth_required
def logout_user(resp, auth_token):
    """Log out a user
    ---
    tags:
     - "auth"
    parameters:
        - in : "header"
          name: "Authorization"
          description: "Token of logged in user"
          required: true
          type: "string"
    responses:
        200:
            description: "Success or Failed"
    """
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
