from models.Statistic import Statistic

def create_statistc_controller(connection, data):
    
    id_student = data.get('id_student')
    id_activity = data.get('id_activity')
    id_question = data.get('id_question')
    answer_correct = data.get('answer_correct')

    return Statistic.create_statistc_service(connection, id_student, id_activity,id_question, answer_correct)

def group_answer_by_id_student_controller(connection, id_student,id_activity):
    questions = Statistic.group_answer_by_id_student_service(connection, id_student,id_activity)
    
    count_correct_answer = sum(1 for question in questions if question[1] == 1)
    
    total_questions = len(questions)

    if total_questions == 0:
        return {
            "message": "Não há respostas para essa atividade"
        }

    percentage = (count_correct_answer / total_questions) * 100

    return {
        "total_questions": total_questions,
        "correct_answers": count_correct_answer,
        "percentage": percentage
    }