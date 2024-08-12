from db.firebase import *
from db.bd_mysql import db_connection
from models.Questions import Questions


def get_questions_from_teacher(conteudo, skill):
    connection = db_connection()

    conteudo = conteudo.upper()
    skill = skill.upper()
    
    cabecalho, questions = Questions.get_questions_service_teacher(connection, conteudo, skill)
    if "error" in cabecalho:
        return cabecalho, 404
    
    response = {
        "Cabecalho": cabecalho,
        "Questões": questions
    }
    return response, 200
