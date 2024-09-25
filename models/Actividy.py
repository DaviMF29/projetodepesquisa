from mysql.connector import Error

class Activity:
    
    def create_activity_service(self, connection, id_group,id_content, description, deadline):
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO activity (id_group, id_content, description, deadline) VALUES (%s, %s, %s, %s)",
                           (id_group, id_content, description, deadline))
            connection.commit()
            print("Activity saved successfully")
            inserted_id = cursor.lastrowid 
            return inserted_id
            
        except Error as e:
            print(f"Error saving activity to database: {e}")
        
        finally:
            cursor.close()

    def get_activity_service(self, connection, id_content, id_group):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM activity WHERE id_content = %s AND id_group = %s" , (id_content,id_group,))
            result = cursor.fetchone()
            return result
        except Error as e:
            print(f"Error getting activity from database: {e}")
        finally:
            cursor.close()

    