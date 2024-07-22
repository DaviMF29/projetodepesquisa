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

#def verify_username_registered(username):
    #user = Student.get_user_by_username_service(username)
    #if user:
        #abort(400, {"message": "Username is not available"})
    #return {"message": "Username is available"}

#def verify_email_registered(email):          
    #user = Student.get_user_by_email_model(email)
    #if user:
        #abort(400, {"message": "Email is not available"})
    #return {"message": "Email is available"}
 
#def verify_change_in_user(user_id, field_name, new_value):
    #user = verify_user(user_id)
    #if field_name in user:
        #current_value = user[field_name]
        #if current_value == new_value:
            #abort(400, f"The {field_name} is the same")
        #return current_value
    #else:
        #abort(400, f"User data is missing '{field_name}' field")