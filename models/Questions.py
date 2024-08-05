from flask import json
import mysql.connector
from mysql.connector import Error


class Questions:
    def __init__(self, question, option_1, option_2, option_3, option_4, option_5, answer, group_id):
        self.question = question
        self.option_1 = option_1
        self.option_2 = option_2
        self.option_3 = option_3
        self.option_4 = option_4
        self.option_5 = option_5
        self.answer = answer
        self.group_id = group_id


    def create_questions_service(self, connection):
        try: 
            cursor = connection.cursor()
            cursor.execute("INSERT INTO questions (question, option_1, option_2, option_3, option_4, option_5, answer, group_id) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)", 
                           (self.question, self.option_1, self.option_2, self.option_3, self.option_4, self.option_5, self.answer, self.group_id))
            connection.commit()
            print("Questions saved successfully")
            inserted_id = cursor.lastrowid
            return inserted_id

        except Error as e:
            print(f"Error saving question to database: {e}")
            return None

        finally:
            cursor.close()

    @staticmethod
    def delete_questions_service(connection, question):
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM questions WHERE question = {question}")
        connection.commit()
        cursor.close()

    @staticmethod
    def get_questions_service_teacher(connection, title):
        with connection.cursor() as cursor:
            select_query = """
            SELECT q.question, q.option_1, q.option_2, q.option_3, q.option_4, q.option_5, g.title
            FROM questions q
            JOIN group_table g 
            ON q.group_id = g.id_grupo 
            WHERE g.title = %s"""

            cursor.execute(select_query, (title,))
            results = cursor.fetchall()

            quizzes = []
            for row in results:
                quiz = {
                    "Question": row[0],
                    "Option 1": row[1],
                    "Option 2": row[2],
                    "Option 3": row[3],
                    "Option 4": row[4],
                    "Option 5": row[5]
                }
                quizzes.append(quiz)
            
            return quizzes, title

            
        