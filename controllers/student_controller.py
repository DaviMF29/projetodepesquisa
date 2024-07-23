from flask import jsonify
from models.Student import Student
from db.bd_mysql import db_connection

from middleware.global_middleware import (
    verify_email_registered,
    verify_id_exists,
)


def add_student_controller(data):
    try:
        connection = db_connection()

        if connection is None:
            raise ConnectionError("Falha ao conectar com o banco de dados.")

        name = data.get('nameStudent').lower()
        email = data.get('emailStudent').lower()
        birth = data.get('birthStudent')
        password = data.get('passwordStudent')

        try:
            birth_converted = birth.split('-') if '-' in birth else birth.split('/')
            birth = f"{birth_converted[2]}-{birth_converted[1]}-{birth_converted[0]}"
        except (IndexError, ValueError) as date_error:
            raise ValueError("Formato de data inválido.") from date_error

        if verify_email_registered(connection, email):
            return {"message": "Email já cadastrado!"}, 400

        student = Student(
            name=name,
            email=email,
            birth=birth,
            password=password
        )

        connection.close()


    except ConnectionError as conn_err:
        print(f"Erro de conexão com o banco de dados: {conn_err}")
        return {"message": "Erro de conexão com o banco de dados"}, 500

    except ValueError as val_err:
        print(f"Erro de validação: {val_err}")
        return {"message": str(val_err)}, 400

    except Exception as e:
        print(f"Erro no controlador de aluno: {e}")
        return {"message": "Internal Server Error"}, 500




def get_student_controller():
    connection = db_connection()
    if connection:
        users = Student.get_all_student_service(connection)
        connection.close()
        return users
    else:
        return {"message": "Falha ao conectar com o banco de dados!"}, 500

def update_student_controller(user_id, field, value):
    connection = db_connection()
    if connection:
        verify_id_exists(connection,user_id,'student')
        try:
            Student.update_student_service(connection, user_id, field, value)
            connection.close()
            return {"message": 'Atualização feita com sucesso!'}, 200
        except Exception as e:
            return {"error": str(e)}, 500
    else:
        return {"error": "Falha ao conectar com o banco de dados!"}, 500

def delete_student_controller(current_user_id, user_id):
    connection = db_connection()
    if not connection:
        return {"message": "Falha ao conectar com o banco de dados!"}, 500
    verify_id_exists(connection,user_id,'student')
    try:
        if current_user_id != user_id:
            return {"message": "Sem permissão para deletar"}, 400

        Student.delete_student_service(connection, user_id)
        return {"message": "User deletado"}, 200

    except Exception as e:
        return {"message": f"Erro ao deletar o usuário: {e}"}, 500

    finally:
        connection.close()

def get_student_by_id_controller(user_id):
    connection = db_connection()
    if connection:
        verify_id_exists(connection,user_id,'student')
        user = Student.get_student_by_id_service(connection, user_id)
        connection.close()
        return user
    else:
        return {"message": "Falha ao conectar com o banco de dados!"}, 500
