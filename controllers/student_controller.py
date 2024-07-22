from models.Student import Student
from db.bd_mysql import db_connection

from middleware.global_middleware import (
    verify_email_registered,
    verify_id_exists,
)

def add_student_controller(data):
    connection = db_connection()
    
    name = data.get('nameStudent').lower()
    email = data.get('emailStudent').lower()
    birth = data.get('birthStudent')
    password = data.get('passwordStudent')

    
    verifyEmail = verify_email_registered(connection,email)
    if verifyEmail:
        return {"message": "Email já cadastrado!"}, 400

    if connection:
        student = Student(
            name=name,
            email=email,
            birth=birth,
            password=password
        
        )

        inserted_id = student.create_student_service(connection)
        connection.close()
        
        if inserted_id is not None:
            return {"message": 'Usuário criado com sucesso!', "user_id": inserted_id}, 200
        else:
            return {"message": "Falha ao criar usuário"}, 500
    else:
        return {"message": "Falha ao conectar com o banco de dados!"}, 500



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
