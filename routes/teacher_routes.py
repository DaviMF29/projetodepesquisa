from bcrypt import gensalt, hashpw
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from controllers.teacher_controller import *

from models.Teacher import Teacher

teacher_app = Blueprint('teacher_app', __name__)

@teacher_app.route('/api/teacher', methods=['POST'])
def add_user_router():
    data = request.get_json()

    name = data.get('nameTeacher').lower()
    email = data.get('emailTeacher').lower()
    birth = data.get('birthTeacher')
    password = data.get('passwordTeacher')
    confirm_password = data.get('confirm_password_Teacher')
    

    if not all([name, email, birth, password, confirm_password]):
        return jsonify({"message": "All fields are required"}), 400
    
    if password != confirm_password:
        return jsonify({"message": "Passwords do not match!"}), 400

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

    data['passwordTeacher'] = hashed_password.decode('utf-8')  

    response, status_code = add_teacher_controller(data)
    return jsonify(response), status_code

@teacher_app.route("/api/teacher/<user_id>", methods=['PATCH'])
@jwt_required()
def update_user(user_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Dados inválidos"}), 400

    if len(data) == 0:
        return jsonify({"error": "Nenhum campo enviado para atualização"}), 400

    field, value = next(iter(data.items()))  # Obtém o primeiro par chave-valor

    try:
        update_teacher_controller(user_id, field, value)
        return jsonify({"message": "Usuário atualizado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@teacher_app.route("/api/teacher/<user_id>", methods=["DELETE"])
@jwt_required()
def delete_users(user_id):
    current_user_id = get_jwt_identity()
    current_user_id = current_user_id['id']
    response, status_code = delete_teacher_controller(current_user_id,user_id)
    return jsonify(response), status_code

@teacher_app.route('/api/teacher', methods=['GET'])
def get_users_route():
    response = get_teacher_controller()
    return jsonify(response)


@teacher_app.route('/alterarNome', methods=['POST'])
def rename_table():
    data = request.get_json()

    current_name = data.get('current_name')
    new_name = data.get('new_name')

    if not all([current_name, new_name]):
        return jsonify({"message": "All fields are required"}), 400
    response = Teacher.rename_table(current_name, new_name)
    return jsonify(response)

@teacher_app.route('/api/teacher/<email>', methods=['GET'])
def get_user_by_id_email(email):
    user = get_teacher_by_id_email_controller(email)
    if user:
        return jsonify(user)
    else:
        return jsonify({"message": "Usuário não encontrado!"}), 404

@teacher_app.route('/api/teachers/', methods=['GET'])
def get_all_teachers():
    teachers = get_teacher_controller()
    return jsonify(teachers)