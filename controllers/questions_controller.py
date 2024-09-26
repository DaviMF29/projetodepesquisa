from db.bd_mysql import db_connection
from models import Student
from models.Questions import Questions
from models.Student import Student
import numpy as np

def get_questions_by_level_service_controller(student_level):
    connection = db_connection()

    # Obter os parâmetros de todas as questões
    question_params = Questions.get_question_params(connection)
    
    # Obter a questão baseada no nível calculado do aluno
    response = Questions.get_questions_by_level_service(connection, student_level, question_params)

    return response, 200

# Função para definir o nível inicial do aluno (valor fixo)
def get_student_initial_level(user_id):
    connection = db_connection()
    return Student.get_student_lvl_service(connection,user_id)

# Função para calcular o nível do aluno (pode ser usada futuramente)
def calculate_student_level(student_responses, question_params):
    theta = 0.0
    learning_rate = 0.1

    # Sem histórico, o nível inicial é fixo, mas a função está preparada para calcular no futuro
    for response, params in zip(student_responses, question_params):
        discrimination, difficulty, guessing = params
        
        # Calcula a probabilidade de acerto da TRI de 3 parâmetros
        prob_correct = guessing + (1 - guessing) / (1 + np.exp(-discrimination * (theta - difficulty)))

        # Atualiza o theta baseado na resposta do aluno
        theta += learning_rate * (response - prob_correct)

    return theta