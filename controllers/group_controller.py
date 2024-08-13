import base64
import bcrypt
from flask import request
from db.firebase import *
from models.Group import Group
from db.bd_mysql import db_connection


# from middleware.global_middleware import (
# verify_email_registered, verify_user
# )

def create_group_controller(teacherId, data):

    id_teacher = teacherId["id"]
    name = data.get("title").lower()
    period = data.get("period")

    connection = db_connection()
    if connection:

        group = Group(
            id_teacher,
            name,
            period
            )
        print(id_teacher)
        inserted_id = group.create_group_service(connection)
        connection.close()
        
        if inserted_id is not None:
            return {"message": 'Grupo criado com sucesso!', "group_id": inserted_id}, 200
        else:
            return {"message": "Falha ao criar usuário"}, 500
    else:
        return {"message": "Falha ao conectar com o banco de dados!"}, 500
        

def delete_student_from_group_controller(current_user_id,group_id, student_id):
    connection = db_connection()
    if not connection:
        return {"message": "Falha ao conectar com o banco de dados!"}, 500
    try:
        if current_user_id["id"] != Group.get_teacher_id_from_group_service(connection, group_id):
            return {"message": "Sem permissão para deletar"}, 400
        Group.delete_student_from_group_service(connection, group_id, student_id)
        return {"message": "Usuário deletado do grupo com sucesso!"}, 200
    
    except Exception as e:
        return {"message": f"Erro ao deletar o usuário: {e}"}, 500

def add_student_to_group_controller(group_id, student_id):
    connection = db_connection()

    idstudent = int(student_id)
    try:
        group, students = Group.get_students_from_group_service(connection, group_id)

        if students is not None:
            for i in range(len(students)):
                if students[i]["idStudent"] == idstudent:
                    return {"message": "Estudante já está no grupo"}, 400

        inserted_id = Group.add_student_to_group_service(connection, group_id, student_id)

        if inserted_id is not None:
            return {"message": "Estudante adicionado ao grupo"}, 200
        else:
            return {"message": "Falha ao adicionar estudante ao grupo"}, 500

    except Exception as e:
        print(f"Erro ao adicionar estudante ao grupo: {e}")
        return {"message": "Erro interno do servidor"}, 500

    finally:
        connection.close()

def get_students_from_group_controller(id_group):
    connection = db_connection()
    teacher,students = Group.get_students_from_group_service(connection,id_group)
    return {"Group": teacher,"Students":students}, 200

def get_students_geral(id_group):
    connection = db_connection()
    students = Group.get_students_from_group(connection, id_group)
    return {"Students": students}, 200

def delete_group_controller(current_user_id, group_id):
    connection = db_connection()
    if not connection:
        return {"message": "Falha ao conectar com o banco de dados!"}, 500
    try:
        
        if int(current_user_id["id"]) != Group.get_teacher_id_from_group_service(connection, group_id):
            return {"message": "Sem permissão para deletar"}, 400
        Group.delete_group_service(connection, group_id)
        return {"message": "Grupo deletado com sucesso!"}, 200
    except Exception as e:
        return {"message": f"Erro ao deletar o grupo: {e}"}, 500
    finally:
        connection.close()

def get_group_by_teacher_id_controller(teacher_id):
    connection = db_connection()
    if not connection:
        return {"message": "Falha ao conectar com o banco de dados!"}, 500
    try:
        groups = Group.get_group_by_teacher_id_service(connection, teacher_id)
        return {"groups": groups}, 200
    except Exception as e:
        return {"message": f"Erro ao buscar grupos: {e}"}, 500
    finally:
        connection.close()

def update_group_controller(teacher_id, group_id, data):
    connection = db_connection()
    if not connection:
        return {"message": "Falha ao conectar com o banco de dados!"}, 500
    
    teacherId_group = Group.get_teacher_id_from_group_service(connection, group_id)
    if int(teacher_id["id"]) != teacherId_group:
        return {"message": "Sem permissão para atualizar"}, 400
    
    try:
        for field, value in data.items():
            Group.update_group_service(connection, field, value, group_id)
        return {"message": 'Atualização feita com sucesso!'}, 200
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        connection.close()
