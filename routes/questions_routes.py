from flask import request, jsonify, Blueprint

from controllers.questions_controller import *

from flask_jwt_extended import jwt_required

question_app = Blueprint("question_app", __name__)

@question_app.route("/api/question", methods=['GET'])
def get_questions_from_group_routes():
    conteudo = request.args.get('conteudo')
    
    if not conteudo:
        return jsonify({"error": "Parâmetro 'conteudo' é obrigatórios."}), 400

    try:
        conteudo = conteudo.encode('utf-8').decode('utf-8')
    except UnicodeEncodeError as e:
        return jsonify({"error": f"Erro de codificação UTF-8: {str(e)}"}), 400

    response, status_code = get_questions_from_teacher_controller(conteudo)
    return jsonify(response), status_code
