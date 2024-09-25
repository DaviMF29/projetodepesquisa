from flask import request, jsonify, Blueprint

from controllers.activity_controller import *

from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

activity_app = Blueprint("activity_app", __name__)

@activity_app.route("/api/activity", methods=["POST"])
def create_activity_route():
    data = request.get_json()
    response, status_code = create_activity_controller(data)
    return jsonify(response), status_code

@activity_app.route("/api/activity", methods=["GET"])
def get_activity_route():
    id_content = request.args.get('id_content')
    id_group = request.args.get('id_group')
    
    data = {
        "id_content": id_content,
        "id_group": id_group
    }

    response, status_code = get_activity_controller(data)
    
    return jsonify(response), status_code