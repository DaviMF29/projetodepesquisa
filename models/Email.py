import os
import smtplib
import email.message
from dotenv import load_dotenv

load_dotenv()

def sendEmail(subject, recipient, body):
    email_user = os.getenv('EMAIL_USER')
    email_password = os.getenv('EMAIL_PASSWORD')

    if not email_user or not email_password:
        raise ValueError("Email or password environment variables not set")

    html_body = f"<p>{body}</p>"
        
    msg = email.message.Message()
    msg['Subject'] = subject
    msg['From'] = email_user
    msg['To'] = recipient
    msg.add_header('Content-Type', 'text/html; charset=utf-8')
    msg.set_payload(html_body, charset='utf-8')

    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(email_user, email_password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        s.quit()
        print('E-mail enviado com sucesso')
    except smtplib.SMTPException as e:
        print(f"Erro ao enviar e-mail: {e}")
        raise
