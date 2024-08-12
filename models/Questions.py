from flask import json
import mysql.connector
from mysql.connector import Error


class Questions:
    def __init__(self, id_questions, id_group_questions, level_questions, skill_question, question, option_a, option_b, option_c, option_d, answer):
        self.id_questions = id_questions
        self.id_group_questions = id_group_questions
        self.level_questions = level_questions
        self.skill_question = skill_question
        self.question = question
        self.option_1 = option_a
        self.option_2 = option_b
        self.option_3 = option_c
        self.option_4 = option_d
        self.answer = answer


    @staticmethod
    def get_questions_service_teacher(connection, conteudo, skill):
        with connection.cursor() as cursor:
            if skill == 'RECALLING':
                query = """
                SELECT  q.id_questions, q.level_questions, q.skill_question, g.content, 
                        q.question, q.option_a, q.option_b, q.answer 
                FROM questions q 
                JOIN group_questions g ON q.id_group_questions = g.id_group_questions 
                WHERE g.content = %s and q.skill_question = %s;
                """
            elif skill == 'RECOGNIZING':
                query = """
                SELECT  q.id_questions, q.level_questions, q.skill_question, g.content, 
                        q.question, q.option_a, q.option_b, q.option_c, q.option_d, q.answer 
                FROM questions q 
                JOIN group_questions g ON q.id_group_questions = g.id_group_questions 
                WHERE g.content = %s and q.skill_question = %s;
                """
            else:
                return {"error": "Skill inválido fornecido."}, []

            cursor.execute(query, (conteudo, skill,))
            results = cursor.fetchall()

        if not results:
            return {"error": "Nenhum resultado encontrado para os critérios fornecidos."}, []

        cabecalho = {
            "Level": results[0][1],
            "Skill": results[0][2],
            "Conteúdo": results[0][3],
        }

        questions = [
            {
                "ID": row[0],
                "Question": row[4],
                "a)": row[5],
                "b)": row[6],
                "c)": row[7] if len(row) > 7 else None,
                "d)": row[8] if len(row) > 8 else None,
                "RESPOSTA:": row[9]
            }
            for row in results
        ]

        return cabecalho, questions
