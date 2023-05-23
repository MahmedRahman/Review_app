import mysql.connector

class UserTable:
    def __init__(self, host, user, password, database):
        self.db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.db.cursor()

    def create_user(self, name, email):
        sql = "INSERT INTO users (name, email) VALUES (%s, %s)"
        val = (name, email)
        self.cursor.execute(sql, val)
        self.db.commit()
        return self.cursor.lastrowid

    def get_user(self, user_id):
        sql = "SELECT * FROM users WHERE id = %s"
        val = (user_id,)
        self.cursor.execute(sql, val)
        return self.cursor.fetchone()

    def update_user(self, user_id, name, email):
        sql = "UPDATE users SET name = %s, email = %s WHERE id = %s"
        val = (name, email, user_id)
        self.cursor.execute(sql, val)
        self.db.commit()
        return self.cursor.rowcount

    def delete_user(self, user_id):
        sql = "DELETE FROM users WHERE id = %s"
        val = (user_id,)
        self.cursor.execute(sql, val)
        self.db.commit()
        return self.cursor.rowcount
    

    def get_all_users(self):
        sql = "SELECT * FROM users"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
