from flask import Flask
from flask_jwt_extended import JWTManager
import os
#from flask_cors import CORS


from routes.student_routes import user_app
from routes.teacher_routes import teacher_app
from routes.group_routes import group_app
from routes.auth_routes import auth_app


app = Flask(__name__)
app.register_blueprint(user_app)
app.register_blueprint(teacher_app)
app.register_blueprint(group_app)
app.register_blueprint(auth_app)


app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Define o tamanho máximo do arquivo (16MB neste caso)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 86400  # 1 dia
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png'}  # Adicione 'png' à lista de tipos de arquivo permitidos
jwt = JWTManager(app)


#cors = CORS(app, resources={r"/*": {"origins": "*"}})


if __name__ == "__main__":
    print("Servidor rodando")
    app.run(debug=True)
    
