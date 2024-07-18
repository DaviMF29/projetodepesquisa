from flask import Blueprint, Flask, request, jsonify
from models.Email import sendEmail

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



# # #PRECISO APENAS PARA TESTAR O SENDEMAIL
# # # ATALHO PARA COMENTAR == CTRL + K -> CTRL + C