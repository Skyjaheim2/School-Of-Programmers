import mysql.connector
import os

db_user = os.environ.get("DB_USER")
db_password = os.environ.get('DB_PASSWORD')

mydb = mysql.connector.connect(host="localhost", user=db_user, passwd=db_password, database="student")

db = mydb.cursor()



class Major():
    def __init__(self, major_name):
        self.__major_name = major_name

    def getRequiredCourse(self, method=None):
        sql = "SELECT minimum_eng_level, minimum_math_level, major_requirements FROM Major WHERE name = %s"
        val = (self.__major_name,)
        db.execute(sql, val)
        result = db.fetchall()
        if len(result) == 0:
            return
        result = result[0]

        if method == "GET":
            minimum_eng_level = result[0]
            minimum_math_level = result[1]
            if result[2] != None:
                major_requirements = result[2].split()
            else:
                major_requirements = "Not Assigned"

            print()
            print("--------------------" + "-" * len(minimum_math_level))
            print(f"MINIMUM MATH LEVEL: {minimum_math_level}")
            print("--------------------" + "-" * len(minimum_math_level))
            print()
            print("-----------------------" + "-" * len(minimum_eng_level))
            print(f"MINIMUM ENGLISH LEVEL: {minimum_eng_level}")
            print("-----------------------" + "-" * len(minimum_eng_level))
            print()
            print("------------------")
            print("MAJOR REQUIREMENTS")
            print("------------------")
            print()
            print(major_requirements)

        elif method == "POST":
            return result

    @classmethod
    def getAllMajors(cls):
        db.execute("SELECT name FROM Major")
        all_majors = db.fetchall()
        all_majors = [all_majors[i][0] for i in range(len(all_majors))]
        return all_majors








