from aifc import Error

class User:
    def __init__(self, name, email, password, last_name=None, birth=None, gender=None, institution=None, certificate=None, state=None, city=None):
        self.id = None
        self.name = name
        self.email = email
        self.password = password
        self.last_name = last_name
        self.birth = birth
        self.gender = gender
        self.institution = institution
        self.certificate = certificate
        self.state = state
        self.city = city


    def create_user_service(self, connection, user_type, user_data):
        try:
            cursor = connection.cursor()
            if user_type == 'aluno':
                cursor.execute("""
                    INSERT INTO aluno (nameStudent, emailStudent, passwordStudent) 
                    VALUES (%s, %s, %s)
                """, (
                    user_data['nameStudent'], user_data['emailStudent'], user_data['passwordStudent']
                ))
                connection.commit()
                inserted_id = cursor.lastrowid 
                return inserted_id

            elif user_type == 'professor':
                cursor.execute("""
                    INSERT INTO professor (nameTeacher, emailTeacher, passwordTeacher)
                    VALUES (%s, %s, %s)
                """, (
                    user_data['nameTeacher'], user_data['emailTeacher'], user_data['passwordTeacher']
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



'''
    @staticmethod
    def get_user_by_email_model(email):
        users_collection = db.users
        user = users_collection.find_one({"email": email})
        return user
    
    @staticmethod
    def get_user_by_id_model(id):
        users_collection = db.users
        user = users_collection.find_one({"_id": ObjectId(id)})
        if user:
            user["_id"] = str(user["_id"])
            return user
        return None
    
    @staticmethod
    def update_user(user_id, updated_fields):
        users_collection = db.users
        result = users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_fields})
        return result
        
    @staticmethod
    def delete_account_model(user_id):
        users_collection = db.users
        result = users_collection.find_one_and_delete({"_id": ObjectId(user_id)})
        return result
    
    def add_new_field_to_all_users(new_field_name):
        users_collection = db.users
        result = users_collection.update_many({}, {"$set": {new_field_name: []}})
        return result

    
    def update_user_image_model(user_id, image_url):
        users_collection = db.users
        result = users_collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'image': image_url}}
        )

        if result.modified_count == 0:
            raise Exception(f"Failed to update user's image with id {user_id}.")

        return {"message": "Image added successfully"}'''