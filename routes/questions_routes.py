from flask import request, jsonify, Blueprint

from controllers.questions_controller import *

from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

question_app = Blueprint("question_app", __name__)

@question_app.route("/api/question", methods=['GET'])
@jwt_required()
def get_questions_from_group_routes():
    conteudo = request.args.get('conteudo')
    skill = request.args.get('skill')

    if not conteudo or not skill:
        return jsonify({"error": "Parâmetros 'conteudo' e 'skill' são obrigatórios."}), 400

    response, status_code = get_questions_from_teacher(conteudo, skill)
    return jsonify(response), status_code
