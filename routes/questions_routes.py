from flask import request, jsonify, Blueprint

from controllers.questions_controller import *

from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

question_app = Blueprint("question_app", __name__)

@question_app.route("/api/question", methods=['POST'])
@jwt_required()
def create_question_route():
    data = request.get_json()
    response, status_code = create_questions_controller(data)
    return jsonify(response), status_code