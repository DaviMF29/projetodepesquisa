from bcrypt import gensalt, hashpw
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from controllers.student_controller import *
from werkzeug.utils import secure_filename
from db.firebase import delete_file_from_upload, handle_image_upload
from models.Student import Student

user_app = Blueprint('user_app', __name__)

@user_app.route('/api/student', methods=['POST'])
def add_user_router():
    data = request.get_json()

    name = data.get('nameStudent')
    email = data.get('emailStudent')
    birth = data.get('birthStudent')
    password = data.get('passwordStudent')
    confirm_password = data.get('confirm_password_Student')

    if not all([name, email, birth, password, confirm_password]):
        return jsonify({"message": "All fields are required"}), 400

    if password != confirm_password:
        return jsonify({"message": "Passwords do not match!"}), 400

    if len(password) < 6:
        return jsonify({"message": "Password must have at least 6 characters"}), 400
    
    if len(password) > 20:
        return jsonify({"message": "Password must not exceed 20 characters"}), 400
    
    if "@" not in email:
        return jsonify({"message": "Invalid email"}), 400

    domain = email.split("@")[-1]
    allowed_domains = ["aluno.uepb.edu.br"]
    if domain not in allowed_domains:
        return jsonify({"message": "Only specific email domains are allowed"}), 401

    hashed_password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

    data = {
        'nameStudent': name.lower(),
        'emailStudent': email.lower(),
        'birthStudent': birth,
        'passwordStudent': hashed_password
    }

    result = add_student_controller(data)

    if len(result) ==2:
        response,status_code = result
        return jsonify(response), status_code

    response, access_token, status_code = result
    return jsonify(response), status_code, access_token
 


@user_app.route("/api/student", methods=['PATCH'])
@jwt_required()
def update_user():
    data = request.get_json()
    user_id = get_jwt_identity()

    if not data or len(data) == 0:
        return jsonify({"error": "Nenhum campo enviado para atualização"}), 400

    try:
        update_student_controller(user_id["id"], data)
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
    response = get_students_controller()
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

@user_app.route('/api/student/<user_id>', methods=['GET'])
def get_user_route(user_id):
    response = get_student_by_id_controller(user_id)
    return jsonify(response)

@user_app.route('/api/student/email/<email>', methods=['GET'])
def get_user_by_id_email(email):
    user = get_student_by_email_controller(email)
    if user:
        return jsonify(user)
    else:
        return jsonify({"message": "Usuário não encontrado!"}), 404
    
@user_app.route('/api/student/upload_image', methods=['PATCH'])
@jwt_required()
def upload_image_student():
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    try:
        file_path = handle_image_upload(file)
        student_id = get_jwt_identity()["id"]
        destination_blob_name = f"students/{student_id}/profile_image.jpg"
        image_url = upload_image_to_firebase(file_path,destination_blob_name)
        upload_image_student_controller(image_url, student_id)
        delete_file_from_upload(file_name=file.filename)
        return jsonify({"message": "File uploaded successfully", "file_url": image_url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
