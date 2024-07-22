from models.Teacher import Teacher
from db.bd_mysql import db_connection

from middleware.global_middleware import (
    verify_id_exists
    ,verify_email_registered)

def add_teacher_controller(data):
    connection = db_connection()

    name = data.get('nameTeacher').lower()
    email = data.get('emailTeacher').lower()
    birth = data.get('birthTeacher')
    password = data.get('passwordTeacher')
    

    verifyEmail = verify_email_registered(connection,email)
    if verifyEmail:
        return {"message": "Email já cadastrado!"}, 400

    if connection:
        teacher = Teacher(
            name=name,
            email=email,
            birth=birth,
            password=password
        )
        teacher_id = teacher.create_teacher_service(connection)
        connection.close()
        
        if teacher_id:
            return {"id": teacher_id, "message": 'Usuário criado com sucesso!'}, 201
        else:
            return {"message": "Erro ao criar usuário!"}, 500
        
    else:
        return {"message": "Falha ao conectar com o banco de dados!"}, 500

def get_teacher_controller():
    connection = db_connection()
    if connection:
        users = Teacher.get_all_teacher_service(connection)
        connection.close()
        return users
    else:
        return {"message": "Falha ao conectar com o banco de dados!"}, 500

def update_teacher_controller(user_id, field, value):
    connection = db_connection()
    if connection:
        verify_id_exists(connection,user_id,'teacher')
        try:
            Teacher.update_teacher_service(connection, user_id, field, value)
            connection.close()
            return {"message": 'Atualização feita com sucesso!'}, 200
        except Exception as e:
            return {"error": str(e)}, 500
    else:
        return {"error": "Falha ao conectar com o banco de dados!"}, 500


def delete_teacher_controller(current_user_id, user_id):
    connection = db_connection()
    if not connection:
        return {"message": "Falha ao conectar com o banco de dados!"}, 500
    
    verify_id_exists(connection,user_id,'teacher')
    try:
        if current_user_id != user_id:
            return {"message": "Sem permissão para deletar"}, 400

        
        Teacher.delete_teacher_service(connection, user_id)
        return {"message": "User deletado"}, 200

    except Exception as e:
        return {"message": f"Erro ao deletar o usuário: {e}"}, 500

    finally:
        connection.close()

    
def get_teacher_by_id_email_controller(email):
    connection = db_connection()
    if connection:
        user = Teacher.get_teacher_by_email_service(connection, email)
        connection.close()
        return user
    else:
        return {"message": "Falha ao conectar com o banco de dados!"}, 500
