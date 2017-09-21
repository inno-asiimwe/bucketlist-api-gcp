"""views for bucketlist_blueprint """
from flask import make_response, jsonify, request, abort
from app.utils import auth_required
from app.models import Bucketlist
from . import bucketlist_blueprint

@bucketlist_blueprint.route('/', methods=['POST', 'GET'])
@auth_required
def bucketlists(resp, auth_token):
    """view function to handle /bucketlists endpoint """
    if request.method == 'POST':
        name = request.data['name']
        description = request.data['description']
        owner = resp

        try:
            new_bucketlist = Bucketlist(name, description, owner)
            new_bucketlist.save()
            response = {
                'status': 'Success',
                'id': new_bucketlist.id,
                'name': new_bucketlist.name,
                'description': new_bucketlist.description,
                'owner': new_bucketlist.owner
            }
            return make_response(jsonify(response)), 201
        except Exception as e:
            response = {
                'status': 'Failed',
                'message': str(e)
            }
            return make_response(jsonify(response)), 202
    user_bucketlists = Bucketlist.get_all_bucketlists(resp)
    response = []

    for bucketlist in user_bucketlists:
        obj = {
            'id': bucketlist.id,
            'name': bucketlist.name,
            'description': bucketlist.description,
            'owner' : bucketlist.owner
        }
        response.append(obj)
    return make_response(jsonify(response)), 200

@bucketlist_blueprint.route('/<int:b_id>', methods=['GET', 'PUT', 'DELETE'])
@auth_required
def  bucketlist(resp, auth_token, b_id):
    """ View function handles retrieval, editing and deleting of bucketlist of a given id """
    my_bucketlist = Bucketlist.query.filter_by(id=b_id).first()

    if not my_bucketlist:
        abort(404)
    elif request.method == 'DELETE':
        my_bucketlist.delete()
        response = {
            'status': 'Success'
        }
        return make_response(jsonify(response)), 200
    elif request.method == 'PUT':
        my_bucketlist.name = request.data['name']
        my_bucketlist.description = request.data['description']
        my_bucketlist.save()
        response = {
            'id': my_bucketlist.id,
            'name': my_bucketlist.name,
            'description': my_bucketlist.description,
            'owner': my_bucketlist.owner
        }
        return make_response(jsonify(response)), 200
    response = {
        'id': my_bucketlist.id,
        'name': my_bucketlist.name,
        'description': my_bucketlist.description,
        'owner': my_bucketlist.owner
    }
    return make_response(jsonify(response))

@bucketlist_blueprint.route('/<int:b_id>/items/', methods=['POST'])
@auth_required
def create_bucketlist_item(resp, auth_token, b_id):
    if request.method == 'POST':
        return make_response(jsonify({}))

@bucketlist_blueprint.route('/<int:b_id>/items/<int:i_id>', methods=['PUT', 'DELETE'])
@auth_required
def edit_bucketlist_item(resp, auth_token, b_id, i_id):
    if request.method == 'PUT':
        return make_response(jsonify({}))
    return make_response(jsonify({}))


    