from aifc import Error

class User:
    def __init__(self, name, email, password, birth, gender=None, institution=None, certificate=None, state=None, city=None, matricula=None):
        self.id = None
        self.name = name
        self.email = email
        self.password = password
        self.birth = birth
        self.gender = gender
        self.institution = institution
        self.certificate = certificate
        self.state = state
        self.city = city
        self.matricula = matricula


    def create_user_service(self, connection, user_type, user_data):
        try:
            cursor = connection.cursor()
            if user_type == 'aluno':
                cursor.execute("""
                    INSERT INTO aluno (nameStudent, emailStudent, birthStudent, passwordStudent) 
                    VALUES (%s, %s, %s, %s)
                """, (
                    user_data['nameStudent'], user_data['emailStudent'], user_data['birthStudent'], user_data['passwordStudent']
                ))
                connection.commit()
                inserted_id = cursor.lastrowid 
                return inserted_id

            elif user_type == 'professor':
                cursor.execute("""
                    INSERT INTO professor (nameTeacher, emailTeacher, birthTeacher, passwordTeacher)
                    VALUES (%s, %s, %s, %s)
                """, (
                    user_data['nameTeacher'], user_data['emailTeacher'], user_data['birthTeacher'], user_data['passwordTeacher']
                ))
                connection.commit()
                inserted_id = cursor.lastrowid 
                return inserted_id

        except Exception as e:
            print(f"Erro ao criar usuário: {e}")
            connection.rollback()
            return None

        finally:
            cursor.close()
    

    def update_user_service(connection, table_name, user_id, field, value):
        cursor = connection.cursor()

        sql = f"UPDATE {table_name} SET {field} = %s WHERE id = %s"

        cursor.execute(sql, (value, user_id))
        connection.commit()
        cursor.close()
    

    @staticmethod
    def get_user_by_id_service(connection, user_id, table_name):
        cursor = connection.cursor()
        try:
            cursor.execute(f"SELECT * FROM {table_name} WHERE id = %s", (user_id,))
            user = cursor.fetchone()

            if user:
                return {
                    "id": user[0],
                    "name": user[1],
                    "email": user[2],
                    "password": user[3]
                }
            else:
                return None

        finally:
            cursor.close()


    @staticmethod
    def get_all_user_service(connection, table_name):
        cursor = connection.cursor()
        try:
            if table_name == 'aluno':
                cursor.execute(f"SELECT nameStudent AS name, emailStudent AS email FROM {table_name}")
            elif table_name == 'professor':
                cursor.execute(f"SELECT nameTeacher AS name, emailTeacher AS email FROM {table_name}")
            else:
                raise ValueError("Invalid table name")

            users = cursor.fetchall()
            return users

        except Exception as e:
            print(f"Erro ao buscar usuários: {e}")
            return []

        finally:
            cursor.close()

    
    @staticmethod
    def delete_user_service(connection, user_id, table_name):
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM {table_name} WHERE id = %s", (user_id,))
        connection.commit()
        cursor.close()


    @staticmethod
    def get_user_by_email_service(connection, email, table_name, email_column):
        cursor = connection.cursor()
        try:
            cursor.execute(f"SELECT * FROM {table_name} WHERE {email_column} = %s", (email,))
            user = cursor.fetchone()  

            if user:
                return {
                    "id": user[0],
                    "name": user[1],  
                    "email": user[2],
                    "password": user[3]
                    
                }
            else:
                return None

        finally:
            cursor.close()


    @staticmethod
    def get_all_emails_service(connection):
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT emailStudent AS email FROM aluno
                UNION
                SELECT emailTeacher AS email FROM professor
            """)
            emails = cursor.fetchall()
        finally:
            cursor.close()
        return emails



    @classmethod
    def rename_table(cls, connection, current_name, new_name):
        try:
            cursor = connection.cursor()
            cursor.execute(f"ALTER TABLE {current_name} RENAME TO {new_name}")
            connection.commit()
            cursor.close()
            print(f"Tabela '{current_name}' renomeada para '{new_name}' com sucesso.")
            return True
        except Error as e:
            print(f"Erro ao tentar renomear a tabela: {e}")
            return False

