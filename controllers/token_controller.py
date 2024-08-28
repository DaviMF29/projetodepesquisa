import os
from flask import jsonify
from models.Token import Token
from db.bd_mysql import db_connection
import jwt
import datetime

def create_token_controller(user_email, user_type, group_id):
    connection = db_connection()
    
    if connection:
        secretKey = os.getenv('SECRET_KEY')
        try:
            token_exists = Token.get_token_by_user_email_service(connection, user_email)
            if token_exists["group_id"] == group_id:
                return None, "Token já existe para este usuário", 400
            
            payload = {
                'email': user_email,
                'user_type': user_type,
                'group_id': group_id,
                'exp': datetime.datetime.now() + datetime.timedelta(hours=72)
            }
            
            token = jwt.encode(payload, secretKey, algorithm='HS256')
            
            token_id = Token.create_token_service(connection, user_email, group_id,user_type, token)
            if token_id:
                return token, None, 201
            else:
                return None, "Falha ao criar token", 500
        except Exception as e:
            error_message = f"Erro ao criar token: {str(e)}"
            return None, error_message, 500
        finally:
            connection.close()
    else:
        return None, "Falha ao conectar com o banco de dados!", 500


def delete_token_controller(user_email):
    connection = db_connection()
    
    if connection:
        try:
            token = Token.get_token_by_user_email_service(connection, user_email)
            if not token:
                return jsonify({"message": "Token não encontrado"}), 404
            deleted = Token.delete_token_service(connection, user_email)
            if deleted:
                return jsonify({"message": "Token deletado"}), 200
            else:
                return jsonify({"message": "Falha ao deletar token"}), 500
        except Exception as e:
            return jsonify({"message": "Erro interno no servidor"}), 500
        finally:
            connection.close()
    else:
        return jsonify({"message": "Falha ao conectar com o banco de dados!"}), 500