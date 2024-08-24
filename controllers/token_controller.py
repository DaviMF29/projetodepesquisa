from flask import jsonify
from models.Token import Token
from db.bd_mysql import db_connection
import jwt
import datetime

def create_token_controller(user_id, user_type, secretKey, user_id_sha, group_id):
    connection = db_connection()
    
    if connection:
        try:
            token = Token.get_token_by_user_id_service(connection, user_id)
            if token:
                return jsonify({"message": "Token já existe para este usuário"}), 400
            
            payload = {
                'user_id': user_id,
                'user_type': user_type,
                'user_id_sha': user_id_sha,
                'group_id': group_id,
                'exp': datetime.datetime.now() + datetime.timedelta(hours=72)
            }
            
            token = jwt.encode(payload, secretKey, algorithm='HS256')
            
            token_id = Token.create_token_service(connection, user_id, user_type, token)
            
            if token_id:
                return jsonify({"token_id": token_id}), 201
            else:
                return jsonify({"message": "Falha ao criar o token"}), 500
        except Exception as e:
            print(f"Erro ao criar token: {e}")
            return jsonify({"message": "Erro interno no servidor"}), 500
        finally:
            connection.close()
    else:
        return jsonify({"message": "Falha ao conectar com o banco de dados!"}), 500


    
def delete_token_controller(user_id):
    connection = db_connection()
    
    if connection:
        try:
            token = Token.get_token_by_user_id_service(connection, user_id)
            if not token:
                return jsonify({"message": "Token não encontrado"}), 404
            deleted = Token.delete_token_service(connection, user_id)
            if deleted:
                return jsonify({"message": "Token deletado"}), 200
            else:
                return jsonify({"message": "Falha ao deletar token"}), 500
        except Exception as e:
            print(f"Erro ao deletar token: {e}")
            return jsonify({"message": "Erro interno no servidor"}), 500
        finally:
            connection.close()
    else:
        return jsonify({"message": "Falha ao conectar com o banco de dados!"}), 500