from flask import abort
#from models.Student import Student
from models.Teacher import Teacher
from db.bd_mysql import db_connection
from models.Student import Student
from models.Users import User


@staticmethod
def verify_email_registered(connection, email):
    user = Student.get_student_by_email_service(connection, email)
    if not user:
        user = Teacher.get_teacher_by_email_service(connection, email)
    return user is not None

@staticmethod
def verify_id_exists(connection, user_id, user_type):
    if user_type == 'student':
        user = Student.get_student_by_id_service(connection, user_id)
    elif user_type == 'teacher':
        user = Teacher.get_teacher_by_id_service(connection, user_id)
    if not user:
        abort(404, {"message": "User not found"})
    return user
