"""views for bucketlist_blueprint """
from flask import make_response, jsonify, request, abort
from app.utils import auth_required
from app.models import Bucketlist, Item
from . import bucketlist_blueprint

@bucketlist_blueprint.route('', methods=['POST', 'GET'])
@auth_required
def bucketlists(resp, auth_token):
    """create or retrieve bucketlist
    ---
    tags:
     - "bucketlists"
    parameters:
      - in: "header"
        name: "Authorization"
        description: "Token of logged in user"
        required: true
        type: string
      - in: "body"
        name: "body"
        description: "Name and description of bucketlist"
        schema:
         type: "object"
         required:
          - name
          - description
         properties:
          name:
           type: "string"
          description:
           type: "string"
    responses:
        202:
            description: "success"
        201:
            description: "Failed"
        200:
            description: "success"
     """
    q = request.args.get('q')
    limit = request.args.get('limit')
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
    elif limit:
        user_bucketlists = Bucketlist.query.filter_by(owner=resp).limit(int(limit))
        response = [bucketlist.to_json() for bucketlist in user_bucketlists]
        return make_response(jsonify(response)), 200
    elif q:
        user_bucketlists = Bucketlist.query.filter(
            Bucketlist.name.ilike("%" + q + "%"), Bucketlist.owner == resp
        ).all()
        response = [bucketlist.to_json() for bucketlist in user_bucketlists]
        return make_response(jsonify(response)), 200
    user_bucketlists = Bucketlist.get_all_bucketlists(resp)
    response = [bucketlist.to_json() for bucketlist in user_bucketlists]
    return make_response(jsonify(response)), 200

@bucketlist_blueprint.route('/<int:b_id>', methods=['GET'])
@auth_required
def get_bucketlist(resp, auth_token, b_id):
    """ Retrieve bucketlist
    ---
    tags:
     - "bucketlists"
    parameters:
     - in: "header"
       name: "Authorization"
       description: "Token of logged in user"
       required: true
       type: string
     - in: "body"
       name: "body"
       description: "Name and description of bucketlist"
       schema:
        type: "object"
        required:
         - name 
         - description
        properties:
         name:
            type: "string"
         description:
            type: "string"
    responses:
        404:
            description: "not found"
        200:
            description: "success"
     """
    my_bucketlist = Bucketlist.query.filter_by(id=b_id).first()
    if my_bucketlist:
        response = my_bucketlist.to_json()
        return make_response(jsonify(response)), 200
    abort(404)

@bucketlist_blueprint.route('/<int:b_id>', methods=['DELETE'])
@auth_required
def delete_bucketlist(resp, auth_token, b_id):
    """ Delete bucketlist
    ---
    tags:
     - "bucketlists"
    parameters:
     - in: "header"
       name: "Authorization"
       description: "Token of logged in user"
       required: true
       type: string
     - in: "body"
       name: "body"
       description: "Name and description of bucketlist"
       schema:
        type: "object"
        required:
         - name 
         - description
        properties:
         name:
            type: "string"
         description:
            type: "string"
    responses:
        404:
            description: "not found"
        200:
            description: "success"
     """

    my_bucketlist = Bucketlist.query.filter_by(id=b_id).first()
    if my_bucketlist:
        my_bucketlist.delete()
        response = {
            'status': 'Success'
        }
        return make_response(jsonify(response)), 200
    abort(404)

@bucketlist_blueprint.route('/<int:b_id>', methods=['PUT'])
@auth_required
def edit_bucketlist(resp, auth_token, b_id):
    """ Edit bucketlist
    ---
    tags:
     - "bucketlists"
    parameters:
     - in: "header"
       name: "Authorization"
       description: "Token of logged in user"
       required: true
       type: string
     - in: "body"
       name: "body"
       description: "Name and description of bucketlist"
       schema:
        type: "object"
        required:
         - description
        properties:
         name:
            type: "string"
         description:
            type: "string"
    responses:
        404:
            description: "not found"
        200:
            description: "success"
        409:
            description: "duplicates"
     """
    my_bucketlist = Bucketlist.query.filter_by(id=b_id).first()
    name = request.data['name']
    description =request.data['description']
    if my_bucketlist:
        if my_bucketlist.name != name:
            duplicate = Bucketlist.query.filter_by(name=name, owner=resp).first()
            if not duplicate:
                my_bucketlist.name = name
            else:
                return make_response(jsonify({'status': 'Failed'})), 409
        if my_bucketlist.description != description:
            my_bucketlist.description = description
        my_bucketlist.save()
        response = my_bucketlist.to_json()
        return make_response(jsonify(response)), 200
    abort(404)

@bucketlist_blueprint.route('/<int:b_id>/items', methods=['POST'])
@auth_required
def create_bucketlist_item(resp, auth_token, b_id):
    """Create a bucketlist item
    ---
    tags:
     - "bucketlists"
    parameters:
     - in: "header"
       name: "Authorization"
       required: true
       description: "Token of logged in user"
       type: string
     - in: "body"
       name: "body"
       required: true
       description: "Name and Description of bucketlist item"
       schema:
        type: "object"
        required:
         - name
         - description
        properties:
         name:
            type: "string"
         description:
            type: "string"
    responses:
        404:
            description: "resource not found"
        202:
            description: "Failed"
        201:
            description: "success"
    """
    if request.method == 'POST':
        my_bucketlist = Bucketlist.query.filter_by(id=b_id, owner=resp).first()
        if my_bucketlist:
            item = Item.query.filter_by(bucketlist_id=b_id, name=request.data['name']).first()
            if not item:
                try:
                    new_item = Item(
                        name=request.data['name'],
                        description=request.data['description'],
                        bucketlist_id=b_id)
                    new_item.save()
                except Exception as e:
                    response = {
                        'status': 'Failed',
                        'message': str(e)
                    }
                    return make_response(jsonify(response)), 202
                response = {
                    'status': 'Success',
                    'id': new_item.id,
                    'name': new_item.name,
                    'description': new_item.description,
                    'bucketlist_id': new_item.bucketlist_id
                }
                return make_response(jsonify(response)), 201
            response = {
                'status': 'Failed',
                'message': 'Item already exists'
            }
            return make_response(jsonify(response)), 202
        abort(404)

@bucketlist_blueprint.route('/<int:b_id>/items/<int:i_id>', methods=['PUT', 'DELETE'])
@auth_required
def edit_bucketlist_item(resp, auth_token, b_id, i_id):
    """"Edit and delete bucketlist item
    ---
    tags:
     - "bucketlists"
    parameters:
     - in: "headers"
       name: "Authorization"
       required: true
       type: string
       description: "Token of logged in user"
     - in: "body"
       name: "body"
       description: "Name and description of bucketlist item"
       schema:
        type: "object"
        required:
         - name
         - description
        properties:
            name:
                type: "string"
            description:
                type: "string"
    responses:
        200:
            description: "success"
        404:
            description: "Failed"
        409:
            description: "Duplicate name"
    """
    my_item = Item.query.filter_by(bucketlist_id=b_id, id=i_id).first()
    if my_item:
        if request.method == 'PUT':
            duplicate = Item.query.filter_by(name=request.data['name'], bucketlist_id=b_id).first()
            if not duplicate:
                my_item.name = request.data['name']
                my_item.description = request.data['description']
                my_item.save()
                response = {
                    'status':'Success',
                    'id': my_item.id,
                    'name': my_item.name,
                    'description':my_item.description,
                    'bucketlist_id': my_item.bucketlist_id
                }
                return make_response(jsonify(response)), 200
            response = {
                'status':'Failed'
            }
            return make_response(jsonify(response)), 409
        if request.method == 'DELETE':
            my_item.delete()
            response = {
                'status': 'Success'
            }
            return make_response(jsonify(response)), 200
    response = {
        'status': 'Failed',
        'message': 'Item not found'
    }
    return make_response((jsonify(response))), 404
     
    