import mysql.connector
import os

db_user = os.environ.get("DB_USER")
db_password = os.environ.get('DB_PASSWORD')

mydb = mysql.connector.connect(host="localhost", user=db_user, passwd=db_password, database="student")

db = mydb.cursor()

from Person import Person
from Course import Course



class Professor(Person):
    MAX_COURSES_A_PROFESSOR_CAN_TEACH = 5

    def __init__(professor, firstName, lastName, address, age, phoneNumber, salary, coursesTaught):
        super().__init__(firstName, lastName, address, age, phoneNumber)
        professor.__salary = salary
        professor.__coursesTaught = coursesTaught


    # GETTER METHODS
    def getSalary(self):
        if self.__salary == None:
            return None
        if self.shouldGetBonus():
            self.__salary  = int(self.__salary) + 20000
        return "$" + " " + format(int(self.__salary), ',.2f')

    def getCoursesTaught(self):
        return self.__coursesTaught.split()

    # STATIC METHODS
    @staticmethod
    def checkIfCourseIsAvailableToSet(all_courses, subset_courses):
        course_has_been_found = 0
        for i in range(len(subset_courses)):
            for j in range(len(all_courses)):
                if subset_courses[i] == all_courses[j][0]:
                    course_has_been_found += 1

        return course_has_been_found == len(subset_courses)


    def getID(self):
        sql = "SELECT id FROM Professor WHERE name = %s"
        val = (self.getFullName(), )
        db.execute(sql, val)
        result = db.fetchall()[0][0]

        return result

    def setCoursesTaught(self, courses):
        # CHECKING COURSE FORMAT
        if ',' in courses:
            courses = courses.replace(',', '')

        # CHECK IF COURSES ARE AVAILABLE
        all_courses = Course.getAll_Courses()
        check_course = courses.split()

        if not Professor.checkIfCourseIsAvailableToSet(all_courses, check_course):
            return -1

        # CHECKING IF TOO MANY COURSES WERE ENTERED
        if len(courses.split()) > self.MAX_COURSES_A_PROFESSOR_CAN_TEACH:
            return -2

        self.__coursesTaught = courses


    # SETTER METHODS
    def setSalary(self, salary):
        # FORMAT SALARY
        if ' ' in salary:
            salary = salary.replace(' ', '')
        if '$'in salary:
            salary = salary.replace('$', '')
        if ',' in salary:
            salary = salary.replace(',', '')
        if '.' in salary:
            index = 0
            for i in range(len(salary)):
                if salary[i] == '.':
                    break
                index += 1
            salary = salary[:index]

        self.__salary = int(salary)









    # REGULAR METHODS
    def shouldGetBonus(self):
        return len(self.getCoursesTaught()) > 4