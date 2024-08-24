import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
import jwt
from db.bd_mysql import db_connection
from models.Teacher import Teacher
from models.Email import sendEmail
from passlib.hash import pbkdf2_sha256 as sha256
from controllers.token_controller import create_token_controller

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
@jwt_required()
def forgetPassword():
    connection = db_connection()
    if not connection:
        return jsonify({'error': 'Erro ao conectar com o banco de dados'}), 500
    try:
        user_identity = get_jwt_identity()
        user_id = user_identity['id'] 
        user_type = user_identity['type']

        if not isinstance(user_id, str):
            user_id = str(user_id)

        userIdCrip = sha256.hash(user_id)

        create_token_controller(user_id, user_type, userIdCrip)

        link = f'http://localhost:3000/{userIdCrip}'
        subject = 'Recuperação de senha'

        recipient = User.get_user_by_id_service(connection, user_id, 'aluno'
                                                if user_type == 'student' else 'professor')['email']

        if not isinstance(recipient, str):
            raise ValueError("Email inválido")
        
        with open('templates/forget_password.html', 'r', encoding='utf-8') as file:
            body = file.read()
        
        body = body.replace('{link}', link)

        recipient = "davi.almeida@aluno.uepb.edu.br"

        sendEmail(subject, recipient, body)

        return jsonify({'message': 'E-mail enviado com sucesso'})
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

@email_app.route('/api/groupInvite', methods=['POST'])
@jwt_required()
def group_invite():
    connection = db_connection()
    if not connection:
        return jsonify({'error': 'Erro ao conectar com o banco de dados'}), 500
    try:
        user_identity = get_jwt_identity()
        user_id = user_identity['id']
        user_type = user_identity['type']
        data = request.get_json()
        groupName = data['groupName']
        groupId = data['groupId']
        recipient = data['recipient']
        
        token, token_id, status_code = create_token_controller(user_id, user_type, groupId)

        if status_code != 201:
            return jsonify({'error': token_id}), status_code
        
        link = f'http://localhost:3000/{token}'
        subject = 'Convite para grupo'

        if not isinstance(recipient, str):
            raise ValueError("Email inválido")
        
        teacherName = Teacher.get_teacher_by_id_service(connection, user_id)['name']
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

# # # ATALHO PARA COMENTAR == CTRL + K -> CTRL + C