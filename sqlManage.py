import mysql.connector as mysql


db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "Sala 206"
)

cursor = db.cursor()

def reset_table():
    sql = "DROP TABLE POMODORO.USERS; USE POMODORO; CREATE TABLE USERS (ID INT AUTO_INCREMENT PRIMARY KEY,LOGIN VARCHAR(20), PASSWORD VARCHAR(20), PRODTIME VARCHAR(10), BREAKTIME VARCHAR(10), CYCLES VARCHAR(10)); DROP TABLE POMODORO.RECORDS; USE POMODORO; CREATE TABLE RECORDS (ID INT AUTO_INCREMENT PRIMARY KEY,LOGIN VARCHAR(20), POMNAME VARCHAR(30), BEGTIME VARCHAR(20), ENDTIME VARCHAR(20), SESHES VARCHAR(10), TIMESSTOPPED VARCHAR(10), STATUS VARCHAR(10), DURATION VARCHAR(10), TPROD VARCHAR(10), TBREAK VARCHAR(10))";
    cursor.execute(sql)
    print("RESET: Tables reseted")
    return

def delete_user(username):
    sql = "DELETE FROM POMODORO.USERS WHERE BINARY LOGIN = %s"
    val = (username)
    cursor.execute(sql, val)
    db.commit()
    print("DELETE: User \"", username,"\" deleted from the database.",sep="")
    return

class login_page():
    def __init__(self, username, password):
        self.username = username
        self.password = password

        return

    def user_exists(self):
        sql = "SELECT * FROM POMODORO.USERS WHERE BINARY LOGIN = %s"
        val = [self.username]
        cursor.execute(sql, val)
        results = cursor.fetchall()
        if results:
            print("BAD USERNAME: User \"", self.username,"\" already exists.",sep="")
            return True
        else:
            print("NEW USERNAME: User \"", self.username,"\" is unique.",sep="")
            return False

    def create_user(self):
        sql = "INSERT INTO POMODORO.USERS (LOGIN, PASSWORD, PRODTIME, BREAKTIME, CYCLES) VALUES (%s, %s, %s, %s, %s)"
        val = (self.username, self.password, "600", "300", "5")
        cursor.execute(sql, val)
        db.commit()

        print("INSERT: User \"", self.username,"\" with password \"", self.password,"\" added to the database.",sep="")

        return

    def validate_login_sql(self):
        sql = "SELECT * FROM POMODORO.USERS WHERE BINARY LOGIN = %s AND BINARY PASSWORD = %s"
        val = (self.username, self.password)
        cursor.execute(sql, val)
        results = cursor.fetchall()
        if results:
            print("LOGIN: Login success. User \"", self.username,"\" with password \"", self.password,"\" logged in.",sep="")
            return True
        else:
            print("FAIL: Login failed. User \"", self.username,"\" with password \"", self.password,"\" does not exist.",sep="")

            return False

class main_page():
    def __init__(self, username) -> None:
        self.username = username
        return

    def obtain_prefs(self):
        # return list of prodtime, breaktime and cycles for given user
        sql = "SELECT PRODTIME, BREAKTIME, CYCLES FROM POMODORO.USERS WHERE BINARY LOGIN = %s"
        val = ([self.username])
        cursor.execute(sql, val)
        results = cursor.fetchall()
        db.commit()

        results = list(results[0])
        results = [int(i) for i in results]

        return results

    def write_prefs(self, prodtime, breaktime, cycles):
        sql = "UPDATE POMODORO.USERS SET PRODTIME = %s, BREAKTIME = %s, CYCLES = %s WHERE BINARY LOGIN = %s"
        val = (prodtime, breaktime, cycles, self.username)
        cursor.execute(sql, val)
        db.commit()

        print("UPDATE: User \"", self.username,"\" preferences updated.",sep="")

        return
    
    def insert_record(self, pomodoroName, beginTime, duration, endTime, seshes, timesStopped, status, total_prod, total_break):
        sql = "INSERT INTO POMODORO.RECORDS (LOGIN , POMNAME , BEGTIME , ENDTIME , SESHES , TIMESSTOPPED , STATUS, DURATION, TPROD, TBREAK) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (self.username, pomodoroName, beginTime, endTime, seshes, timesStopped, status, round(duration, 5), total_prod, total_break)
        cursor.execute(sql, val)
        db.commit()

        print("INSERT RECORD: Record for user \"", self.username,"\" added to the database.",sep="")

        return

    def obtain_records(self):
        sql = "SELECT * FROM POMODORO.RECORDS WHERE BINARY LOGIN = %s"
        val = ([self.username])
        cursor.execute(sql, val)
        results = cursor.fetchall()
        db.commit()

        return results

    def obtain_total_prod(self):
        sql = "SELECT SUM(TPROD) FROM POMODORO.RECORDS WHERE BINARY LOGIN = %s"
        val = ([self.username])
        cursor.execute(sql, val)
        results = cursor.fetchall()
        db.commit()

        results = list(results[0])
        results = [int(i) for i in results][0]

        return results

    def obtain_total_break(self):
        sql = "SELECT SUM(TBREAK) FROM POMODORO.RECORDS WHERE BINARY LOGIN = %s"
        val = ([self.username])
        cursor.execute(sql, val)
        results = cursor.fetchall()
        db.commit()

        results = list(results[0])
        results = [int(i) for i in results][0]

        return results
    
    def obtain_total_seshes(self):
        sql = "SELECT SUM(SESHES) FROM POMODORO.RECORDS WHERE BINARY LOGIN = %s"
        val = ([self.username])
        cursor.execute(sql, val)
        results = cursor.fetchall()
        db.commit()

        results = list(results[0])
        results = [int(i) for i in results][0]

        return results
    # longest duration of a pomodoro and display details of this session
    def obtain_longest_pom(self):
        sql = "SELECT * FROM POMODORO.RECORDS WHERE LOGIN = %s ORDER BY CAST(DURATION AS UNSIGNED) DESC LIMIT 1"
        val = ([self.username])
        cursor.execute(sql, val)
        results = cursor.fetchall()
        db.commit()

        return results
    def total_pomodoro(self):
        sql = "SELECT COUNT(*) FROM POMODORO.RECORDS WHERE BINARY LOGIN = %s"
        val = ([self.username])
        cursor.execute(sql, val)
        results = cursor.fetchall()
        db.commit()

        results = list(results[0])
        results = [int(i) for i in results]
        # only count them
        results = results[0]

        return results
    def complted_pomodoro(self):
        sql = "SELECT COUNT(*) FROM POMODORO.RECORDS WHERE BINARY LOGIN = %s AND STATUS = '1'"
        val = ([self.username])
        cursor.execute(sql, val)
        results = cursor.fetchall()
        db.commit()

        results = list(results[0])
        results = [int(i) for i in results]
        # only count them
        results = results[0]

        return results

    def average_duration(self):
        sql = "SELECT AVG(DURATION) FROM POMODORO.RECORDS WHERE BINARY LOGIN = %s"
        val = ([self.username])
        cursor.execute(sql, val)
        results = cursor.fetchall()
        db.commit()

        results = round(list(results[0])[0], 2)

        return results
    def most_common_name(self):
        sql = "SELECT POMNAME, COUNT(*) FROM POMODORO.RECORDS WHERE BINARY LOGIN = %s GROUP BY POMNAME ORDER BY COUNT(*) DESC LIMIT 3"
        val = ([self.username])
        cursor.execute(sql, val)
        results = cursor.fetchall()
        db.commit()

        results = [list(x) for x in results]

        return results

    def obtain_last_30_entries_without_fist_column(self):
        sql = "SELECT POMNAME, BEGTIME, ENDTIME, SESHES, TIMESSTOPPED, STATUS, DURATION, TPROD, TBREAK FROM POMODORO.RECORDS WHERE BINARY LOGIN = %s ORDER BY BEGTIME DESC LIMIT 50"
        val = ([self.username])
        cursor.execute(sql, val)
        results = cursor.fetchall()
        db.commit()

        results = [list(x) for x in results]

        return results