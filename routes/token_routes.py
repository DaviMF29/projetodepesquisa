from flask import request, jsonify, Blueprint
from controllers.token_controller import *
from flask_jwt_extended import jwt_required

token_app = Blueprint("token_app", __name__)

@token_app.route('/api/token/<user_id>', methods=['DELETE'])
def delete_token_route(user_id):
    return delete_token_controller(user_id)