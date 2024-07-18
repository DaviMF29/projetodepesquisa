from models.Users import User


class Student(User):
    def __init__(self, name, email, password, last_name=None, birth=None, gender=None, institution=None, period=None, certificate=None, state=None, city=None):
        super().__init__(name, email, password, last_name, birth, gender, institution, certificate, state, city)
        self.period = period

    def to_db_format(self):
        return {
            'nameStudent': self.name,
            'emailStudent': self.email,
            'passwordStudent': self.password,
            'lastNameStudent': self.last_name,
            'birthStudent': self.birth,
            'genderStudent': self.gender,
            'institutionStudent': self.institution,
            'periodStudent': self.period,
            'certificateStudent': self.certificate,
            'stateStudent': self.state,
            'cityStudent': self.city
        }

        
    def create_student_service(self, connection):
        student_data = self.to_db_format()
        return self.create_user_service(connection, 'aluno', student_data)
    
    def update_student_service(connection, user_id, field, value):
        User.update_user_service(connection, 'aluno', user_id, field, value)


    @staticmethod
    def get_all_student_service(connection):
        return User.get_all_user_service(connection, 'aluno')
    
    @staticmethod
    def get_student_by_id_service(connection, user_id):
        return User.get_user_by_id_service(connection, user_id, 'aluno')
    
    @staticmethod
    def get_student_by_email_service(connection, email):
        return User.get_user_by_email_service(connection, email, 'aluno', 'emailStudent')

    @staticmethod
    def delete_student_service(connection, user_id):
        return User.delete_user_service(connection, user_id, 'aluno')
    