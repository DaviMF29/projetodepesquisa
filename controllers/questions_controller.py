from db.firebase import *
from db.bd_mysql import db_connection
from models.Questions import Questions


def get_questions_from_teacher_controller(conteudo, skill):
    connection = db_connection()

    conteudo = conteudo.upper()
    skill = skill.upper()

    try:
        conteudo = conteudo.encode('utf-8').decode('utf-8')
        skill = skill.encode('utf-8').decode('utf-8')
    except UnicodeEncodeError as e:
        return {"error": f"Erro de codificação UTF-8: {str(e)}"}, 400
    
    cabecalho, questions = Questions.get_questions_service_teacher(connection, conteudo, skill)
    if "error" in cabecalho:
        return cabecalho, 404
    
    response = {
        "Cabecalho": cabecalho,
        "Questões": questions
    }
    return response, 200
