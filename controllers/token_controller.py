from flask import jsonify
from models.Token import Token
from db.bd_mysql import db_connection

def create_token_controller(user_id,type, user_id_sha):
    connection = db_connection()
    
    if connection:
        try:
            token = Token.get_token_by_user_id_service(connection, user_id)
            if token:
                return jsonify({"message": "Token já existe para este usuário"}), 400
            token_id = Token.create_token_service(connection, user_id,type, user_id_sha)
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