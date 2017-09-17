"""views for bucketlist_blueprint """
from app.utils import auth_required
from app.models import Bucketlist
from . import bucketlist_blueprint
from flask import make_response, jsonify, request

@bucketlist_blueprint.route('/', methods=['POST', 'GET'])
@auth_required
def bucketlists(resp, auth_token):
    """view function to handle /bucketlists endpoint """
    user_bucketlists = Bucketlist.get_all_bucketlists(resp)
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

    