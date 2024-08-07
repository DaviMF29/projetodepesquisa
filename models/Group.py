from flask import json
import mysql.connector
from mysql.connector import Error

class Group:
    def __init__(self, id_teacher, title, period):
        self.id_teacher = id_teacher
        self.title = title
        self.period = period
        #self.students = students if students is not None else []

    def create_group_service(self, connection):
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO group_table (id_teacher, title, period) VALUES (%s, %s, %s)",
                           (self.id_teacher, self.title, self.period))
            connection.commit()
            print("Group saved successfully")
            inserted_id = cursor.lastrowid 
            return inserted_id
            
        except Error as e:
            print(f"Error saving group to database: {e}")
        
        finally:
            cursor.close()


    @staticmethod
    def add_student_to_group_service(connection, group_id, student_id):
        try:
            cursor = connection.cursor()
            '''cursor.execute("SELECT id_student FROM group_table WHERE id = %s", (group_id,))
            group_data = cursor.fetchone()
            if not group_data:
                cursor.close()
                return False

            student_ids = json.loads(group_data[0]) if group_data[0] else []
            if student_id not in student_ids:
                student_ids.append(student_id)
                student_ids_json = json.dumps(student_ids)'''

            cursor.execute("INSERT INTO student_group (id_aluno, id_grupo) VALUES (%s, %s)", (student_id, group_id))
            connection.commit()
            inserted_id = cursor.lastrowid 
            return inserted_id

        except Error as e:
            print(f"Error adding student to group: {e}")
            
        finally:
            cursor.close()

    @staticmethod
    def get_students_from_group_service(connection, title, group_Id):
        with connection.cursor() as cursor:
            query = """
            SELECT p.nameTeacher, e.nameStudent, g.title, g.period
                FROM group_table g
                JOIN professor p ON g.id_teacher = p.id
                JOIN student_group sg ON g.id_grupo = sg.id_grupo
                JOIN aluno e ON sg.id_aluno = e.id
                WHERE g.title = %s AND g.id_grupo = %s
            """
            cursor.execute(query, (title, group_Id))
            results = cursor.fetchall()

        teacher = {
            "nameTeacher": results[0][0],
            "title": results[0][2],
            "period": results[0][3]
        }

        students = [
            {
                "nameStudent": row[1]
                
            }
            for row in results
        ]

        return teacher, students
    
    @staticmethod
    def delete_student_from_group_service(connection, groupID, studentID):
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM student_group WHERE id_grupo = {groupID} and id_aluno = {studentID}")
        connection.commit()
        cursor.close()