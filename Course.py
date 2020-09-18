import mysql.connector
import os

db_user = os.environ.get("DB_USER")
db_password = os.environ.get('DB_PASSWORD')

mydb = mysql.connector.connect(host="localhost", user=db_user, passwd=db_password, database="student")

db = mydb.cursor()

class Course:
    MIN_STUDENTS = 15
    MAX_STUDENTS = 100

    def __init__(self, name):
        self.__name = name



    # GETTER METHOD
    @classmethod
    def getAll_Courses(cls):
        db.execute("SELECT name FROM Course")
        result = db.fetchall()

        return result

    def getCourseName(self):
        return self.__name

    def getDescription(self):
        sql = "SELECT description FROM Course WHERE name = %s"
        val = (self.getCourseName(),)
        db.execute(sql, val)
        description = db.fetchall()
        if len(description) == 0:
            return None
        return description[0][0]

    def getStudentNamesInCourse(self):
        sql = "SELECT studentsInCourse FROM Course WHERE name = %s"
        val = (self.getCourseName(),)
        db.execute(sql, val)
        students_in_course = db.fetchall()
        if students_in_course[0][0] == '':
            return None
        return students_in_course[0][0]

    def getTeachedBy(self):
        sql = "SELECT teachedBy FROM Course WHERE name = %s"
        val = (self.getCourseName(),)
        db.execute(sql, val)
        teached_by = db.fetchall()
        if len(teached_by) == 0:
            return None
        return teached_by[0][0]

    def getStudentCountInCourse(self):
        sql = "SELECT studentsCount FROM Course WHERE name = %s"
        val = (self.getCourseName(),)
        db.execute(sql, val)
        student_count = db.fetchall()
        if len(student_count) == 0:
            return None
        return student_count[0][0]

    # REGULAR METHODS
    def isCourseCancelled(self):
        return self.getStudentCountInCourse() < self.MIN_STUDENTS

    # DUNDER METHODS
    def __len__(self):
        if self.isCourseCancelled():
            return len("True")
        return len("False")
