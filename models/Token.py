import os
from flask import json, jsonify
import jwt
import mysql.connector
from mysql.connector import Error

secretKey = os.getenv('SECRET_KEY')

class Token:
    def __init__(self, email,type, group_id,user_id_sha):
        self.email = email
        self.type = type
        self.group_id = group_id
        self.user_id_sha = user_id_sha


    @staticmethod
    def create_token_service(connection, user_email, type, group_id,user_id_sha):
        try:
            print(group_id)

            cursor = connection.cursor(buffered=True)
            cursor.execute(
                "INSERT INTO token (email, type,user_id_sha,groupId ) VALUES (%s,%s, %s, %s)",
                (user_email, type,user_id_sha, group_id)
            )
            connection.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Erro ao criar token no banco de dados: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def delete_token_service(connection, user_email):
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM token WHERE email = %s", (user_email,))
            connection.commit()
            return True

        except Error as e:
            print(f"Error deleting token from database: {e}")
            return False

        finally:
            cursor.close()

    @staticmethod
    def get_token_by_user_id_service(connection, user_id):
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM token WHERE user_id = %s", (user_id,))
            token = cursor.fetchone()
            
            if token is None:
                return None
            
            return token
        except Error as e:
            print(f"Error getting token from database: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_token_by_user_email_service(connection, user_email):
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM token WHERE email = %s", (user_email,))
            token = cursor.fetchone()
            
            if token is None:
                return None
            
            return token
        except Error as e:
            return None
        finally:
            cursor.close()

    def get_group_id_by_token(connection, token):
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT groupId FROM token WHERE token = %s", (token,))
            result = cursor.fetchone()
            
            if result is None:
                return None
            
            return result['groupId']
        except Error as e:
            return jsonify(f"Error getting token from database: {e}")

    


        
