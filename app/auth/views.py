from . import auth_blueprint
from flask import make_response, jsonify , request
from app.models import User

@auth_blueprint.route('/auth/register', methods=['POST'])
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
