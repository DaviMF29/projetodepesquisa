import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

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
