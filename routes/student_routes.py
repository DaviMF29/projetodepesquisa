from bcrypt import gensalt, hashpw
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from controllers.student_controller import *

from models.Student import Student

user_app = Blueprint('user_app', __name__)

@user_app.route('/api/student', methods=['POST'])
def add_user_router():
    data = request.get_json()

    name = data.get('nameStudent').lower()
    email = data.get('emailStudent').lower()
    password = data.get('passwordStudent')

    if not all([name, email, password]):
        return jsonify({"message": "All fields are required"}), 400

    if len(password) < 6:
        return jsonify({"message": "Password must have at least 6 characters"}), 400
    
    if len(password) > 20:
        return jsonify({"message": "Password must not exceed 20 characters"})
    
    if "@" not in email:
        return jsonify({"message": "Invalid email"}), 400

    domain = email.split("@")[-1]
    allowed_domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "live.com", "aluno.uepb.edu.br"]
    if domain not in allowed_domains:
        return jsonify({"message": "Only specific email domains are allowed"}), 401

    hashed_password = hashpw(password.encode('utf-8'), gensalt())

    data['passwordStudent'] = hashed_password.decode('utf-8')  

    response, status_code = add_student_controller(data)
    return jsonify(response), status_code

@user_app.route("/api/student/<user_id>", methods=['PATCH'])
@jwt_required()
def update_user(user_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Dados inválidos"}), 400

    if len(data) == 0:
        return jsonify({"error": "Nenhum campo enviado para atualização"}), 400

    field, value = next(iter(data.items()))

    try:
        update_student_controller(user_id, field, value)
        return jsonify({"message": "Usuário atualizado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_app.route("/api/student/<user_id>", methods=["DELETE"])
@jwt_required()
def delete_users(user_id):
    current_user_id = get_jwt_identity()
    current_user_id = current_user_id['id']
    response, status_code = delete_student_controller(current_user_id,user_id)
    return jsonify(response), status_code

@user_app.route('/api/students', methods=['GET'])
def get_users_route():
    response = get_student_controller()
    return jsonify(response)


@user_app.route('/alterarNome', methods=['POST'])
def rename_table():
    data = request.get_json()

    current_name = data.get('current_name')
    new_name = data.get('new_name')

    if not all([current_name, new_name]):
        return jsonify({"message": "All fields are required"}), 400
    response = Student.rename_table(current_name, new_name)
    return jsonify(response)










'''from controllers.user_controller import (
    create_user_controller,update_user_controller,delete_user_controller)

from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity


users_app = Blueprint("users_app", __name__)

allowed_domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "live.com","aluno.uepb.edu.br"]

@users_app.route("/api/users", methods=["POST"])
def create_user_route():
    data = request.get_json()
    
    name = data["name"].lower()
    email = data["email"].lower()
    password = data["password"].lower()

    if len(password) < 6:
        return jsonify({"message": "Password must have at least 6 characters"}), 400

    if "@" not in email:
        return jsonify({"message": "Invalid email"}), 400

    domain = email.split("@")[-1]
    if domain not in allowed_domains:
        return jsonify({"message": "Only specific email domains are allowed"}), 401

    response, status_code = create_user_controller(email, name, password)
    return jsonify(response), status_code

@users_app.route("/api/users/<userId>", methods=["DELETE"])
@jwt_required()
def delete_user_route(userId):
    response, status_code = delete_user_controller(userId)
    return jsonify(response), status_code


@users_app.route("/api/users/<user_id>", methods=["PUT"])
@jwt_required()
def update_user_route(user_id):
    data = request.get_json()

    try:
        update_user_controller(user_id, data)
        return jsonify({"message": "User updated"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
'''