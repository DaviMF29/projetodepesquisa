from flask import json
import mysql.connector
from mysql.connector import Error

class Token:
    def __init__(self, user_id,type, user_id_sha):
        self.user_id = user_id
        self.type = type
        self.user_id_sha = user_id_sha


    @staticmethod
    def create_token_service(connection, user_id, type, user_id_sha):
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO token (user_id, type, user_id_sha) VALUES (%s,%s, %s)",
                (user_id, type,user_id_sha)
            )
            connection.commit()
            return cursor.lastrowid

        except Error as e:
            print(f"Erro ao criar token no banco de dados: {e}")
            return None

        finally:
            cursor.close()

    @staticmethod
    def delete_token_service(connection, user_id_sha):
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM token WHERE id = %s", (user_id_sha,))
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

        finally:
            cursor.close()
        
