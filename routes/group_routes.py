from flask import request, jsonify, Blueprint

from controllers.group_controller import *

from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

group_app = Blueprint("group_app", __name__)

@group_app.route("/api/group", methods=["POST"])
@jwt_required()
def create_group_route():
    data = request.get_json()
    id_teacher = get_jwt_identity()

    response, status_code = create_group_controller(id_teacher,data)
    return jsonify(response), status_code

@group_app.route("/api/group/<groupId>/<studentId>", methods=["DELETE"])
@jwt_required()
def delete_student_from_group_route(groupId, studentId):
    response, status_code = delete_student_from_group_controller(groupId, studentId)
    return jsonify(response), status_code

@group_app.route("/api/group/student/<groupId>/<studentId>", methods=["PUT"])
@jwt_required()
def add_student_to_group_route(groupId, studentId):
    response, status_code = add_student_to_group_controller(groupId, studentId)
    return jsonify(response), status_code

@group_app.route("/api/group/<groupId>", methods=["GET"])
@jwt_required()
def get_students_from_group_route(groupId):
    data = request.get_json()
    response, status_code = get_students_from_group_controller(data, groupId)
    return jsonify(response), status_code

@group_app.route("/api/group/<groupId>", methods=["DELETE"])
@jwt_required
def delete_student_from_group_routes(groupId):
    data = request.get_json()
    current_user_id = get_jwt_identity()    
    studentId = data["studentId"]
    response, status_code = delete_student_from_group_controller(current_user_id,groupId, studentId)
    return jsonify(response), status_code

