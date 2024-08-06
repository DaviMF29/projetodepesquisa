from db.firebase import *
from db.bd_mysql import db_connection
from models.Questions import Questions


def create_questions_controller(data):
    
    question = data.get("question")
    option_1 = data.get("a)").lower()
    option_2 = data.get("b)").lower()
    option_3 = data.get("c)").lower()
    option_4 = data.get("d)").lower()
    option_5 = data.get("e)").lower()
    answer = data.get("answer").lower()
    id_group = data.get("id_group")

    connection = db_connection()
    if connection:

        question = Questions(
            question,
            option_1,
            option_2,
            option_3,
            option_4,
            option_5,
            answer, 
            id_group
        )

       
        inserted_id = question.create_questions_service(connection)
        connection.close()


        if inserted_id is not None:
            return {"message": 'Questões criadas com sucesso!', "id_question": inserted_id}, 200
        else:
            return {"message": "Falha ao as questões"}, 500

    
    else:
        return {"message": "Falha ao conectar com o banco de dados!"}, 500


def get_questions_from_teacher(title, groupId):
    connection = db_connection()
    questions, title_group = Questions.get_questions_service_teacher(connection, title, groupId)
    return {f"Questões do grupo {title_group}: ": questions}, 200


def delete_questions_from_group_controller(title, groupID):
    connection = db_connection()
    Questions.delete_questions_service()