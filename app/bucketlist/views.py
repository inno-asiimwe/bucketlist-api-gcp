from . import bucketlist_blueprint
from flask import make_response, jsonify, request
from app.utils import auth_required

@bucketlist_blueprint.route('', methods=['POST', 'GET'])
@auth_required
def bucketlists(resp):
    """view function to handle /bucketlists endpoint """
    pass
