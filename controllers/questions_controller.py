from db.firebase import *
from db.bd_mysql import db_connection
from models.Questions import Questions


def create_questions_controller(data):
    
    question = data.get("question")
    option_1 = data.get("option_1").lower()
    option_2 = data.get("option_2").lower()
    option_3 = data.get("option_3").lower()
    option_4 = data.get("option_4").lower()
    option_5 = data.get("option_5").lower()
    answer = data.get("answer")

    connection = db_connection()
    if connection:

        question = Questions(
            question,
            option_1,
            option_2,
            option_3,
            option_4,
            option_5,
            answer
        )

       
        inserted_id = question.create_questions_service(connection)
        connection.close()


        if inserted_id is not None:
            return {"message": 'Questões criadas com sucesso!', "id_question": inserted_id}, 200
        else:
            return {"message": "Falha ao as questões"}, 500

    
    else:
        return {"message": "Falha ao conectar com o banco de dados!"}, 500


