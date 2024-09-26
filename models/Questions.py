import numpy as np
from decimal import Decimal

class Questions:
    @staticmethod
    def get_questions_by_level_service(connection, student_level, question_params):
        with connection.cursor() as cursor:
            # Consulta para obter questões e seus parâmetros
            query = """
                SELECT id_questions, skill_question, question, answer, slope, threshold, asymptote
                FROM questions
            """
            cursor.execute(query)
            results = cursor.fetchall()

        if not results:
            return {"error": "Nenhuma questão encontrada."}, 200

        # Iterar sobre as questões e os parâmetros TRI
        for row, params in zip(results, question_params):
            question_id = row[0]
            skill = row[1]
            question_image = row[2]
            answer = row[3]
            slope = row[4]  # Discrimination
            threshold = row[5]  # Difficulty
            asymptote = row[6]  # Guessing

            # Calcular a probabilidade de acerto com base nos parâmetros TRI
            prob_correct = calculate_question_prob(student_level, slope, threshold, asymptote)

            # Se a questão for adequada ao nível do aluno, retorna imediatamente
            if is_question_suitable(prob_correct):
                return {
                    "ID": question_id,
                    "Skill": skill,
                    "Question Image": question_image,
                    "Answer": answer,
                    "Question Value": prob_correct
                }, 200

        # Se nenhuma questão for adequada, retorna uma mensagem de erro
        return {"error": "Nenhuma questão adequada encontrada."}, 200

    def get_params_by_question_id(connection, question_id):
        query = "SELECT slope, threshold, asymptote FROM questions WHERE id_questions = %s"
        cursor = connection.cursor()
        cursor.execute(query, (question_id,))
        params = cursor.fetchone()
        return params
    
    def get_question_params(connection):
        query = "SELECT id_questions, slope, threshold, asymptote FROM questions"
        cursor = connection.cursor()
        cursor.execute(query)
        params = cursor.fetchall()
        return [(param[0], param[1], param[2], param[3]) for param in params]

def calculate_question_prob(student_level, slope, threshold, asymptote):

    student_level = float(student_level) if isinstance(student_level, Decimal) else student_level
    slope = float(slope) if isinstance(slope, Decimal) else slope
    threshold = float(threshold) if isinstance(threshold, Decimal) else threshold
    asymptote = float(asymptote) if isinstance(asymptote, Decimal) else asymptote

    return asymptote + (1 - asymptote) / (1 + np.exp(-slope * (student_level - threshold)))


def is_question_suitable(prob_correct):
    return 0.3 <= prob_correct <= 0.7
    
