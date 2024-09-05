from email.headerregistry import Group
import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
import jwt
from controllers.student_controller import get_id_by_email_controller
from db.bd_mysql import db_connection
from middleware.global_middleware import verify_student_is_in_group
from models.Student import Student
from models.Teacher import Teacher
from models.Group import Group
from models.Email import sendEmail
from passlib.hash import pbkdf2_sha256 as sha256
from controllers.token_controller import create_token_controller

from models.Token import Token
from models.Users import User

email_app = Blueprint("email_app", __name__)

@email_app.route('/api/send_email', methods=['POST'])
def sendEmail_route():
    try:
        data = request.json
        subject = data['subject']
        recipient = data['recipient']
        body = data['body']
        html_body = data.get('html_body')
        sendEmail(subject, recipient, body,html_body)

        return jsonify({'message': 'E-mail enviado com sucesso'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@email_app.route('/api/forgetPassword', methods=['POST'])
def forgetPassword():
    try:
        data = request.get_json()
        table_name = ""
        email_column = ""
        recipient = data.get('email')
        if not recipient or not isinstance(recipient, str):
            return jsonify({'error': 'Email inválido'}), 400

        connection = db_connection()
        if not connection:
            return jsonify({'error': 'Erro ao conectar com o banco de dados'}), 500
        
        if "servidor" in recipient:
            table_name = "professor"
            email_column = "emailTeacher"
            user_type = "teacher"
        elif "aluno" in recipient:
            table_name = "aluno"
            email_column = "emailStudent"
            user_type = "student"

        else:
            return jsonify({'error': "Domínio não permitido"}), 500 
        
        user = User.get_user_by_email_service(connection, recipient, table_name,email_column)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        token, error_message, status_code = create_token_controller(recipient, user_type, "", 'password')

        if not token:
            return {"error": error_message}, status_code


        link = f'http://localhost:3000/{token}'
        subject = 'Recuperação de senha'
        
        with open('templates/forget_password.html', 'r', encoding='utf-8') as file:
            body = file.read()
        
        body = body.replace('{link}', link)

        sendEmail(subject, recipient, body)

        return jsonify({'message': 'E-mail enviado com sucesso'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@email_app.route('/api/groupInvite', methods=['POST'])
@jwt_required()
def group_invite():
    connection = db_connection()
    if not connection:
        return jsonify({'error': 'Erro ao conectar com o banco de dados'}), 500
    try:
        data = request.get_json()
        teacherId = get_jwt_identity()['id']
        groupName = data['groupName']
        groupId = data['groupId']
        recipient = data['recipient']
                
        token, token_id, status_code = create_token_controller(recipient, 'student', int(groupId),'invite')
        if status_code != 201:
            return jsonify({'error': token_id}), status_code
        
        link = f"http://localhost:5500/templates/pagina-redirecionamento.html?token={token}"
        subject = 'Convite para grupo'

        if not isinstance(recipient, str):
            raise ValueError("Email inválido")
        
        teacher = Teacher.get_teacher_by_id_service(connection, teacherId)
        teacherName = teacher['name'] if teacher else 'Professor Desconhecido'
        
        with open('templates/group_invite.html', 'r', encoding='utf-8') as file:
            html = file.read()
            body = html.format(group=groupName, teacher=teacherName, link=link)
        
        sendEmail(subject, recipient, body)
        
        return jsonify({
            'message': 'E-mail enviado com sucesso',
            'token': token,
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
@email_app.route('/api/verifyInvite', methods=['GET'])
@jwt_required()
def verify_invite():
    try:
        connection = db_connection()
        if not connection:
            return jsonify({'error': 'Erro ao conectar com o banco de dados'}), 500
        
        user = get_jwt_identity()
        userEmail = User.get_email_by_id(user["id"])
        token = Token.get_token_by_user_email_service
        if token["email"]!= userEmail:
            return jsonify({"Emails incompativeis"})
        return jsonify({token})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()



# # # ATALHO PARA COMENTAR == CTRL + K -> CTRL + C