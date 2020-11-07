from Person import Person
from Course import Course
import mysql.connector
import os

db_user = os.environ.get("DB_USER")
db_password = os.environ.get('DB_PASSWORD')

mydb = mysql.connector.connect(host="localhost", user=db_user, passwd=db_password, database="student")

db = mydb.cursor()

class Student(Person):
    MAX_COURSES_STUDENT_CAN_ENROLL_IN  = 6

    def __init__(self, firstName, lastName, address, age, phoneNumber, coursesEnrolledIn, grades, major):
        super().__init__(firstName, lastName, address, age, phoneNumber)
        self.__coursesEnrolledIn = coursesEnrolledIn
        self.__grades = grades
        self.__major  = major


    # GETTER METHODS
    def getID(self):
        sql = "SELECT id FROM Student WHERE name = %s"
        val = (self.getFullName(), )
        db.execute(sql, val)
        result = db.fetchall()[0][0]

        return result

    def getCoursesEnrolledIn(self):
        if self.__coursesEnrolledIn == None:
            return None
        return self.__coursesEnrolledIn

    def getGradesForAverage(self):
        if self.__grades == None:
            return None
        grades = self.__grades.split()
        # print(grades)

        grades_to_return = ""
        for grade in grades:
            if grade.replace('%', '').isnumeric():
                grades_to_return += grade
                grades_to_return += " "

        return grades_to_return.rstrip().replace('%','').split()

    def getGrades(self):
        if self.__grades == None:
            return None

        grades = self.__grades.split()

        grades_to_return = ""
        for grade in grades:
            if grade.isdigit():
                grades_to_return += grade + "%"
            if not grade.isdigit():
                grades_to_return += grade
            grades_to_return += " "

        grades_to_return = grades_to_return.rstrip()
        return grades_to_return



    def getMajor(self):
        if self.__major == None:
            return None
        return self.__major

    # CLASS METHODS
    @classmethod
    def getMAX_COURSES_STUDENT_CAN_ENROLL_IN(cls):
        return cls.MAX_COURSES_STUDENT_CAN_ENROLL_IN

    @classmethod
    def getAllMajors(cls):
        sql = "SELECT name FROM Major"
        db.execute(sql)
        all_majors = db.fetchall()

        return all_majors





    # STATIC METHODS
    @staticmethod
    def checkIfCourseIsAvailableToSet(all_courses, subset_courses):
        course_has_been_found = 0
        for i in range(len(subset_courses)):
            for j in range(len(all_courses)):
                if subset_courses[i] == all_courses[j][0]:
                   course_has_been_found += 1

        return course_has_been_found == len(subset_courses)

    @staticmethod
    def checkIfMajorIsAvailableToSet(major):
        all_majors = [Student.getAllMajors()[i][0] for i in range(len(Student.getAllMajors()))]
        if major not in all_majors:
            return False
        return True

    # SETTER METHODS
    def setCoursesEnrolledIn(self, courses):
        # CHECKING COURSE FORMAT
        if ',' in courses:
            courses = courses.replace(',', '')

        courses = courses.split()

        # CHECK IF COURSES ARE AVAILABLE
        all_courses = Course.getAll_Courses()
        check_course =  tuple(courses)                            # courses.split()

        if not Student.checkIfCourseIsAvailableToSet(all_courses, check_course):
             return -1

        # CHECKING IF TOO MANY COURSES WERE ENTERED
        if len(courses) > self.MAX_COURSES_STUDENT_CAN_ENROLL_IN:
            return -2

        self.__coursesEnrolledIn = courses


    def setGrades(self):
        if self.getCoursesEnrolledIn() == None:
            while True:
                error = input("Cant Set Grades Because Student Is Not Enrolled In Any Courses. Press (B) To Go Back: ").lower()
                if error == "b":
                    from Main_School import update_student_info
                    update_student_info()

        grades_to_set = ""
        try:
            for course in self.getCoursesEnrolledIn().split():
                while True:
                    grade = input(f"{course} Grade: ")
                    if grade != '' and grade.isdigit() and int(grade) <= 100:
                        break
                    if grade == "c":
                        from Main_School import update_student_info
                        update_student_info()
                grades_to_set += course + ":" + " " + grade + " "
        except TypeError:
            return
        grades_to_set = grades_to_set.rstrip()
        self.__grades = grades_to_set

    def setMajor(self, major):
        if not self.checkIfMajorIsAvailableToSet(major):
            return -1

        self.__major = major


    # GETTER METHODS
    def getAverageOfGrades(self):
        all_grades = self.getGradesForAverage()
        return int(all_grades[-1])




    def getGPA(self):
        grade = self.getAverageOfGrades()
        if grade == None:
            return None
        if grade >= 93:
            gpa = 4.0
        elif grade >= 90 and grade <= 92:
            gpa = 3.7
        elif grade >= 87 and grade <= 89:
            gpa = 3.3
        elif grade >= 83 and grade <= 86:
            gpa = 3.0
        elif grade >= 80 and grade <= 82:
            gpa = 2.7
        elif grade >= 77 and grade <= 79:
            gpa = 2.3
        elif grade >= 73 and grade <= 76:
            gpa = 2.0
        elif grade >= 70 and grade <= 72:
            gpa = 1.7
        elif grade >= 67 and grade <= 69:
            gpa = 1.3
        elif grade >= 65 and grade <= 66:
            gpa = 1.0
        else:
            gpa = 0.0

        return gpa


    def isPartTime(self):
        # RETURNS TRUE IF <= 2 ELSE IT RETURNS FALSE
        return len(self.getCoursesEnrolledIn()) <= 2

    def isFullTime(self):
        # RETURNS TRUE IF > 2 ELSE IT RETURNS FALSE
        return len(self.getCoursesEnrolledIn()) > 2

    def isOnAcademicProbation(self):
        return self.getAverageOfGrades() < 60

