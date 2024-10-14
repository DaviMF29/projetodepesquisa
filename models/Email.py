import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import random
from db.bd_mysql import db_connection
from datetime import datetime, timedelta

load_dotenv()

def generateCode():
    return str(random.randint(100000, 900000))

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

def send_verification_code(email, connection):
    code = generateCode()
    subject = "Código de verificação"
    body = f"Seu código de verificação é: {code}"
    
    expires_at = datetime.now() + timedelta(minutes=10)

    try:
        cursor = connection.cursor()

        query = "INSERT INTO verification_codes (email, code, expires_at) VALUES (%s, %s, %s)"
        cursor.execute(query, (email, code, expires_at))
        connection.commit()
    except Exception as e:
        print(f"Erro ao inserir código de verificação no banco de dados: {e}")
        raise
    finally:
        cursor.close()

    sendEmail(subject, email, body)

def verify_code(email, code, connection):
    
    try:
        cursor = connection.cursor()

        query = "SELECT * FROM verification_codes WHERE email = %s AND code = %s"
        cursor.execute(query, (email, code))
        result = cursor.fetchone()

        if result is None:
            return False

    except Exception as e:
        print(f"Erro ao verificar código de verificação no banco de dados: {e}")
        return False
    
    finally:
        cursor.close()

    return result

