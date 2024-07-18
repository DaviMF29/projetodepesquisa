import base64
import bcrypt
from db.firebase import *
from models.Group import Group
from db.bd_mysql import db_connection


# from middleware.global_middleware import (
# verify_email_registered, verify_user
# )

def create_group_controller(data):

    id_teacher = data.get('id_teacher')
    id_student = data.get("id_student")
    name = data.get("name").lower()
    period = data.get("period")

    connection = db_connection()
    if connection:

        group = Group(
            id_teacher,
            id_student,
            name,
            period
            )
    
        group.create_group_service(connection)
        inserted_id = group.create_group_service(connection)
        connection.close()
        
        if inserted_id is not None:
            return {"message": 'Grupo criado com sucesso!', "user_id": inserted_id}, 200
        else:
            return {"message": "Falha ao criar usuário"}, 500
    else:
        return {"message": "Falha ao conectar com o banco de dados!"}, 500
        

def delete_student_from_group_controller(group_id, student_id):
    Group.delete_student_from_group_model(group_id, student_id)
    return {"message": "Student deleted from group"}, 200

def add_student_to_group_controller(group_id, student_id):
    Group.add_student_to_group_model(group_id, student_id)
    return {"message": "Student added to group"}, 200

def get_students_from_group_controller(title):
    connection = db_connection()
    teacher,students = Group.get_students_from_group_service(connection,title)
    return {"Group": teacher,"Students":students}, 200