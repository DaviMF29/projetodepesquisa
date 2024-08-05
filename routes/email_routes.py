from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from db.bd_mysql import db_connection
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

        create_token_controller(user_id,user_type, userIdCrip)

        link = f'http://localhost:3000/{userIdCrip}'
        subject = 'Recuperação de senha'
        recipient = "davi.almeida@aluno.uepb.edu.br"

        if not isinstance(recipient, str):
            raise ValueError("Email inválido")
        
        body = f"Olá, você solicitou a recuperação de senha. Para redefinir sua senha, clique no link: {link}"
        
        sendEmail(subject, recipient, body)

        return jsonify({'message': 'E-mail enviado com sucesso'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# # #PRECISO APENAS PARA TESTAR O SENDEMAIL
# # # ATALHO PARA COMENTAR == CTRL + K -> CTRL + C