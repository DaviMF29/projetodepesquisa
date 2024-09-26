from flask import request, jsonify, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required

from controllers.questions_controller import *

question_app = Blueprint("question_app", __name__)

@question_app.route("/api/question/level", methods=['GET'])
@jwt_required()
def get_questions_by_level_routes():
    
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"error": "Parâmetro 'level' é obrigatório."}), 400
    student_level =get_student_initial_level(user_id)
    response, status_code = get_questions_by_level_service_controller(student_level)
    return jsonify(response), status_code