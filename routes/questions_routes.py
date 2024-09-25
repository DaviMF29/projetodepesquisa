from flask import request, jsonify, Blueprint

from controllers.questions_controller import *

from flask_jwt_extended import jwt_required

question_app = Blueprint("question_app", __name__)

@question_app.route("/api/question/level", methods=['GET'])
def get_questions_by_level_routes():
    student_level = request.args.get('level')

    if not student_level:
        return jsonify({"error": "Parâmetro 'level' é obrigatório."}), 400

    response, status_code = get_questions_by_level_service_controller()
    return jsonify(response), status_code