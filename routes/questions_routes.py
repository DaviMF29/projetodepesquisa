from flask import request, jsonify, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.Questions import Questions
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

@question_app.route("/api/question/aswner", methods=['POST'])
@jwt_required()
def calculate_student_level_routes():
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"error": "Parâmetro 'user_id' é obrigatório."}), 400
    
    # Obtendo a resposta e o ID da questão do corpo da requisição
    data = request.json
    question_id = data.get("ID")
    student_answer = data.get("student_answer")
    
    if not question_id or student_answer is None:
        return jsonify({"error": "Parâmetros 'ID' e 'student_answer' são obrigatórios."}), 400

    is_correct = check_answer(question_id, student_answer)
    
    # Conectando ao banco de dados para obter os parâmetros da questão
    connection = db_connection()
    params = Questions.get_params_by_question_id(connection, question_id)

    if params is None:
        return jsonify({"error": "Parâmetros da questão não encontrados."}), 404

    # Desempacotando os parâmetros
    slope, threshold, asymptote = params

    if is_correct:
        new_level = calculate_student_level([1], [[slope, threshold, asymptote]], user_id)
        print(new_level)
        return jsonify({"message": "Resposta correta!", "new_level": new_level}), 200
    else:
        new_level = calculate_student_level([0], [[slope, threshold, asymptote]], user_id)
        return jsonify({"message": "Resposta incorreta.", "new_level": new_level}), 200

def check_answer(question_id, student_answer):
    connection = db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT answer FROM questions WHERE id_questions = %s", (question_id,))
        result = cursor.fetchone()

        # Verificar se a questão existe
        if result:
            correct_answer = result[0]
            return student_answer == correct_answer
        else:
            return False  # Questão não encontrada
    finally:
        cursor.close()