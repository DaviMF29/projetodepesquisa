from flask import json
import mysql.connector
from mysql.connector import Error


class Questions:
    def __init__(self, question, option_1, option_2, option_3, option_4, option_5, answer):
        self.question = question
        self.option_1 = option_1
        self.option_2 = option_2
        self.option_3 = option_3
        self.option_4 = option_4
        self.option_5 = option_5
        self.answer = answer


    def create_questions_service(self, connection):
        try: 
            cursor = connection.cursor()
            cursor.execute("INSERT INTO questions (question, option_1, option_2, option_3, option_4, option_5, answer) VALUES ( %s, %s, %s, %s, %s, %s, %s)", 
                           (self.question, self.option_1, self.option_2, self.option_3, self.option_4, self.option_5, self.answer))
            connection.commit()
            print("Questions saved successfully")
            inserted_id = cursor.lastrowid
            print(inserted_id)
            return inserted_id

        except Error as e:
            print(f"Error saving question to database: {e}")
            return None

        finally:
            cursor.close()

