import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import random
import redis

load_dotenv()

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def generate_verification_code():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def send_verification_code(email):
    
    verification_code = generate_verification_code()
    subject = "Código de Verificação"
    body = f"Seu código de verificação é: {verification_code}"

    sendEmail(subject, email, body)

    redis_client.setex(f"verification_code:{email}", 180, verification_code)

def sendEmail(subject, recipient, body):
    email_user = os.getenv('EMAIL_USER')
    email_password = os.getenv('EMAIL_PASSWORD')

    if not email_user or not email_password:
        raise ValueError("Email or password environment variables not set")

    html_body = f"<p>{body}</p>"

    print(email_user,recipient)

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email_user
    msg['To'] = recipient
    msg.set_content(html_body, subtype='html', charset='utf-8')

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.starttls()
            s.login(email_user, email_password)
            s.send_message(msg)
        print('E-mail enviado com sucesso')
    except smtplib.SMTPException as e:
        print(f"Erro ao enviar e-mail: {e}")
        raise

def verify_code(email, input_code):
    stored_code = redis_client.get(f"verification_code:{email}")

    if stored_code is None:
        return False, "O Código de verificação expirou ou não foi enviado."
    
    if stored_code == input_code:
        return True, "Código verificado com sucesso!"
    else:
        return False, "Código de verificação inválido."