from models.Student import Student
from db.bd_mysql import db_connection

from middleware.global_middleware import (
    verify_email_registered,
    verify_user)

def add_student_controller(data):
    connection = db_connection()
    name = data.get('nameStudent').lower()
    email = data.get('emailStudent').lower()
    password = data.get('passwordStudent')


    verifyEmail = verify_email_registered(connection,email)
    if verifyEmail:
        return {"message": "Email já cadastrado!"}, 400

    if connection:
        user = Student(
            name=name,
            email=email,
            password=password,
            
        )

        inserted_id = user.create_student_service(connection)
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

    try:
        if current_user_id != user_id:
            return {"message": "Sem permissão para deletar"}, 400

        verify_user(user_id)
        Student.delete_student_service(connection, user_id)
        return {"message": "User deletado"}, 200

    except Exception as e:
        return {"message": f"Erro ao deletar o usuário: {e}"}, 500

    finally:
        connection.close()









































'''
import base64
import uuid
import bcrypt
from bson import ObjectId
from db.firebase import *
from models.User import User


from middleware.global_middleware import (
    verify_email_registered,verify_user,verify_change_in_user,
    )


def create_user_controller(email,username, password):
    verify_email_registered(email)
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt(10))
    hashed_password_base64 = base64.b64encode(hashed_password).decode()
    image = ""
    user_id = User.create_user_model(username,email,image, hashed_password_base64)
    return {"id": user_id, "message": f"User {username} created"}, 201

def update_user_controller(user_id, new_data):
    updated_fields = {}
    for key, value in new_data.items():
        if key != "_id":  # proibir alteração do _id
            updated_fields[key] = value

    for field_name, new_value in updated_fields.items():
        verify_change_in_user(user_id, field_name, new_value)

    User.update_user(user_id, updated_fields)

    return {"message": "User updated"}, 200

def delete_user_controller(userId):
    verify_user(userId)
    User.delete_account_model(userId)
    return {"message": "User deleted"}, 200

def get_user_by_id_controller(user_id):
    try:
        user_id = ObjectId(user_id)
        user = User.get_user_by_id_model(user_id)
        if not user:
            return {"message": "User not found"}, 404

        user.pop('_id', None)

        return user
    except Exception as e:
        print(f"Failed to retrieve user: {e}")
        return {"message": "Failed to retrieve user"}, 500
'''

'''import base64
import bcrypt
from bson import ObjectId
from db.firebase import *
from models.Student import Student


from middleware.global_middleware import (
    verify_email_registered,verify_student
    )


def create_student_controller(email,studentname, password):
    verify_email_registered(email)
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt(10))
    hashed_password_base64 = base64.b64encode(hashed_password).decode()
    image = ""
    student_id = Student.create_student_model(studentname,email,image, hashed_password_base64)
    return {"id": student_id, "message": f"student {studentname} created"}, 201


def delete_student_controller(studentId):
    verify_student(studentId)
    Student.delete_account_model(studentId)
    return {"message": "student deleted"}, 200

def get_student_by_id_controller(student_id):
    try:
        student_id = ObjectId(student_id)
        student = Student.get_student_by_id_model(student_id)
        if not student:
            return {"message": "student not found"}, 404

        student.pop('_id', None)

        return student
    except Exception as e:
        print(f"Failed to retrieve student: {e}")
        return {"message": "Failed to retrieve student"}, 500

'''