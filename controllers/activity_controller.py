from flask import request
from db.firebase import *
from models.Actividy import Activity
from db.bd_mysql import db_connection

def create_activity_controller(data):
    id_group = data.get("id_group")
    id_content = data.get("id_content")
    description = data.get("description")
    deadline = data.get("deadline")

    connection = db_connection()

    activity = Activity()
    inserted_id = activity.create_activity_service(connection, id_group, id_content, description, deadline)
    if inserted_id is not None:
        return {"message": 'Atividade criada com sucesso!', "activity_id": inserted_id}, 200
    else:
        return {"message": "Falha ao criar atividade"}, 500

def get_activity_controller(data):
    id_group = data.get("id_group")
    id_content = data.get("id_content")

    connection = db_connection()

    activity = Activity()
    result = activity.get_activity_service(connection, id_content, id_group)
    if result is not None:
        return {"activity": result}, 200
    else:
        return {"message": "Atividade não encontrada"}, 404