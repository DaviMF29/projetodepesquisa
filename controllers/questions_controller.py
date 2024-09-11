from db.firebase import *
from db.bd_mysql import db_connection
from models.Questions import Questions


def get_questions_from_teacher_controller(conteudo):
    connection = db_connection()

    conteudo = conteudo.upper()

    try:
        conteudo = conteudo.encode('utf-8').decode('utf-8')
    except UnicodeEncodeError as e:
        return {"error": f"Erro de codificação UTF-8: {str(e)}"}, 400
    
    questions = Questions.get_questions_service_teacher(connection, conteudo)

    
    response = {
        "Questões": questions
    }
    return response, 200
