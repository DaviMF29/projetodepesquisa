from flask import Flask
from flask_jwt_extended import JWTManager
import os
from flask_cors import CORS
import json

from routes.student_routes import user_app
from routes.teacher_routes import teacher_app
from routes.group_routes import group_app
from routes.auth_routes import auth_app
from routes.email_routes import email_app
from routes.token_routes import token_app
from routes.questions_routes import question_app

app = Flask(__name__)

# Configuração do CORS para aceitar requisições de qualquer origem
CORS(app, resources={r"/*": {"origins": "*"}})

# Registro das Blueprints
app.register_blueprint(user_app)
app.register_blueprint(teacher_app)
app.register_blueprint(group_app)
app.register_blueprint(auth_app)
app.register_blueprint(email_app)
app.register_blueprint(token_app)
app.register_blueprint(question_app)

# Configurações adicionais
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Define o tamanho máximo do arquivo (16MB neste caso)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 86400  # 1 dia
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png'}  # Adicione 'png' à lista de tipos de arquivo permitidos
jwt = JWTManager(app)

@app.route('/')
def home():
    return "API de cadastro do screen programming"


credentials_path = os.getenv("FIREBASE_CREDENTIALS_PATH")

# Carregue as credenciais do arquivo JSON
with open(credentials_path) as f:
    firebase_credentials = json.load(f)

if __name__ == "__main__":
    print("Servidor rodando")
    app.run(debug=True)
