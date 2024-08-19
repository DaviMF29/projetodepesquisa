from flask import json
import mysql.connector
from mysql.connector import Error


class Questions:
    def __init__(self, id_questions, id_group_questions, level_questions, skill_question, question, answer):
        self.id_questions = id_questions
        self.id_group_questions = id_group_questions
        self.level_questions = level_questions
        self.skill_question = skill_question
        self.question = question
        self.answer = answer


    @staticmethod
    def get_questions_service_teacher(connection, conteudo, skill):
        with connection.cursor() as cursor:
            query = """
            SELECT  q.id_questions, q.level_questions, q.skill_question, g.content, 
                    q.question,  q.answer 
            FROM questions q 
            JOIN group_questions g ON q.id_group_questions = g.id_group_questions 
            WHERE g.content = %s and q.skill_question = %s;
            """
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
                "RESPOSTA:": row[5]
            }
            for row in results
        ]
        return cabecalho, questions
