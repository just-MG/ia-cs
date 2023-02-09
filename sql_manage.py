import mysql.connector as mysql


db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "Sala 206"
)

cursor = db.cursor()

def create_user(username, password):
    sql = "INSERT INTO POMODORO.USERS (LOGIN, PASSWORD) VALUES (%s, %s)"
    val = (username, password)
    cursor.execute(sql, val)
    db.commit()
    print(cursor.rowcount, "record inserted.")


def delete_user(username):
    sql = "DELETE FROM POMODORO.USERS WHERE LOGIN = %s"
    val = (username)
    cursor.execute(sql, val)
    db.commit()
    print(cursor.rowcount, "record(s) deleted")

class user_check():
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def validate_login_sql(self):
        sql = "SELECT * FROM POMODORO.USERS WHERE LOGIN = %s AND PASSWORD = %s"
        val = (self.username, self.password)
        cursor.execute(sql, val)
        results = cursor.fetchall()
        if results:
            return True
        else:
            return False
