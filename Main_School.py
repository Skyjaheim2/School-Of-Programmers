import os
clear = lambda: os.system("cls")
import hashlib
from stdiomask import getpass
from time import sleep
try:
    import mysql.connector
except ImportError:
    print("Import Error: Do pip install mysql.connector-python To Use This Program")
    exit()
from datetime import date

current_date = date.today()
now = current_date.strftime("%B %d, %Y")

# CLASSES
from Professor import Professor
from Course import Course
from Major import Major
from Person import Person
from Student import Student
from Assignments import *

db_user = os.environ.get("DB_USER")
db_password = os.environ.get('DB_PASSWORD')

mydb = mysql.connector.connect(host="localhost", user=db_user, passwd=db_password, database="student")

db = mydb.cursor()




def login():
    clear()
    print("SCHOOL OF PROGRAMMERS")
    print(now)
    print("---------------------")
    print("Press (R) To Register")
    print("Press (E) To Exit")
    print("---------------------")
    print()
    print("LOGIN AS:")
    print()
    print("1 - Dean")
    print("2 - Professor")
    print("3 - Student")
    print()
    while True:
        user_choice = input("Choose An Option: ").lower()
        if user_choice == "1":
            DeanLogin()
        elif user_choice == "2":
            ProfessorLogin()
        elif user_choice == "3":
            StudentLogin()
        elif user_choice == "r":
            register()
        elif user_choice == "e":
            exit()


password_attempts = 1
MAX_PASSWORD_ATTEMPTS = 3
# DEAN LOGIN
def DeanLogin():
    clear()
    global dean_name, dean_password, password_attempts
    print("LOGIN AS DEAN")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    dean_name = input("Enter Your Full Name: ")
    # CHECKING IF C WAS ENTERED
    if len(dean_name) == 1:
        dean_name = dean_name.lower()
    if dean_name == "c":
        login()
    # CHECKING IF THE NAME IS REGISTERED
    sql = "SELECT * FROM Dean WHERE name = %s"
    val = (dean_name, )
    db.execute(sql, val)
    result = db.fetchall()
    if len(result) != 0:
        hashed_password = result[0][3]
    if len(result) == 0:
        not_registered("Dean")

    dean_password = getpass("Enter Your Password: ")
    # CHECKING IF THE PASSWORD MATCHES
    if not check_password_hash(dean_password, hashed_password):
        if password_attempts == MAX_PASSWORD_ATTEMPTS:
            reset_password("Dean")
        password_attempts += 1
        incorrect_password("Dean")

    update_course_database()
    update_major_database()
    DeanMenu(dean_name)


# PROFESSOR LOGIN
def ProfessorLogin():
    global prof_password, prof_name, password_attempts
    clear()
    print("LOGIN AS PROFESSOR")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    prof_name = input("Enter Your Full Name: ")
    # CHECKING IF C WAS ENTERED
    if len(prof_name) == 1:
        prof_name = prof_name.lower()
    if prof_name == "c":
        login()
    # CHECKING IF THE NAME IS REGISTERED
    sql = "SELECT * FROM Professor WHERE name = %s"
    val = (prof_name, )
    db.execute(sql, val)
    result = db.fetchall()
    if len(result) != 0:
        hashed_password = result[0][9]
    if len(result) == 0:
        not_registered("Professor")


    prof_password = getpass("Enter Your Password: ")
    # CHECKING IF THE PASSWORD MATCHES
    if not check_password_hash(prof_password, hashed_password):
        if password_attempts == MAX_PASSWORD_ATTEMPTS:
            reset_password("Prof")
        password_attempts += 1
        incorrect_password("Professor")

    update_course_database()
    update_major_database()
    ProfessorMenu(prof_name)



# STUDENT LOGIN
def StudentLogin():
    clear()
    global stu_name, stu_password, password_attempts
    print("LOGIN AS STUDENT")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    stu_name = input("Enter Your Full Name: ")
    # CHECKING IF C WAS ENTERED
    if len(stu_name) == 1:
        stu_name = stu_name.lower()
    if stu_name == "c":
        login()
    # CHECKING IF THE NAME IS REGISTERED
    sql = "SELECT * FROM Student WHERE name = %s"
    val = (stu_name, )
    db.execute(sql, val)
    result = db.fetchall()
    if len(result) != 0:
        hashed_password = result[0][11]
    if len(result) == 0:
        not_registered("Student")

    stu_password = getpass("Enter Your Password: ")
    # CHECKING IF THE PASSWORD MATCHES
    if not check_password_hash(stu_password, hashed_password):
        if password_attempts == MAX_PASSWORD_ATTEMPTS:
            reset_password("Stu")
        password_attempts += 1
        incorrect_password("Student")

    update_course_database()
    update_major_database()
    StudentMenu(stu_name)

# INCORRECT PASSWORD
def incorrect_password(came_from):
    while True:
        print()
        tmp = input("Incorrect Password. Press (T) To Try Again:\n"
                    "                    Press (B) To Go Back: ").lower()
        if tmp == "t":
            if came_from == "Dean":
                DeanLogin()
            elif came_from == "Professor":
                ProfessorLogin()
            elif came_from == "Student":
                StudentLogin()

        elif tmp == "b":
            login()


# NOT REGISTERED
def not_registered(came_from):
    while True:
        print()
        tmp = input("You Are Not Registered. Press (T) To Try Again:\n"
                    "                        Press (R) To Register: ").lower()
        if tmp == "t":
            if came_from == "Dean":
                DeanLogin()
            elif came_from == "Professor":
                ProfessorLogin()
            elif came_from == "Student":
                StudentLogin()

        elif tmp == "r":
            register()



def register():
    clear()
    print("REGISTER")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    print("AVAILABLE OPTIONS")
    print()
    print("1 - Register As Dean")
    print("2 - Register As Professor")
    print("3 - Register As Student")
    print()
    while True:
        while True:
            user_choice = input("Choose An Option: ").lower()
            if user_choice != '':
                break
        # CHECKING IF C WAS ENTERED
        if user_choice == "c":
            login()
        elif user_choice == "1":
            register_as_dean()
        elif user_choice == "2":
            register_as_professor()
        elif user_choice == "3":
            register_as_student()

# REGISTER AS DEAN
def register_as_dean():
    clear()
    print("REGISTER AS DEAN")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    while True:
        print()
        dean_name = input("Enter Your Full Name: ")
        # CHECKING IF C WAS ENTERED
        if dean_name.lower() == "c":
            login()
        if len(dean_name.split()) == 0 or len(dean_name.split()) == 1:
            print("Full Name Is Required")
        else:
            break


    # CHECK IF PERSON IS ALREADY REGISTERED
    sql = "SELECT * FROM Dean WHERE name = %s"
    val = (dean_name, )

    db.execute(sql, val)
    result = db.fetchall()

    if len(result) != 0:
        already_registered()

    # SECURITY ANIMAL
    while True:
        dean_s_animal = input("SECURITY QUESTION: What Is The Name Of Your Favorite Animal? ").lower()
        if dean_s_animal == "c":
            login()
        if dean_s_animal != '':
            break

    # PASSWORD
    while True:
        dean_password = input("Enter Your Password: ")
        if dean_password.lower() == "c":
            login()
        if dean_password != '':
            break

    # SANITIZE PASSWORD
    dean_password = sanitize_password(dean_password, dean_name)


    # CONFIRM PASSWORD
    while True:
        confirm_dean_password = input("Confirm Your Password: ")
        if confirm_dean_password.lower() == "c":
            login()
        if confirm_dean_password != '':
            break


    if dean_password != confirm_dean_password:
        confirm_dean_password = confirm_password_error(dean_name)


    # HASH PASSWORD
    confirm_dean_password = hash_password(confirm_dean_password)

    x = input()

    sql = "INSERT INTO Dean (name, security_animal, password) VALUES (%s, %s, %s)"
    val = (dean_name, dean_s_animal, confirm_dean_password)

    db.execute(sql, val)
    mydb.commit()

    print()
    while True:
        tmp = input("You Have Been Registered. Press (L) To Login: ")
        if tmp == "l":
            login()


# REGISTER AS PROFESSOR
def register_as_professor():
    clear()
    print("REGISTER AS PROFESSOR")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    while True:
        print()
        prof_name = input("Enter Your Full Name: ")
        # CHECKING IC WAS ENTERED
        if prof_name.lower() == "c":
            login()
        if len(prof_name.split()) == 0 or len(prof_name.split()) == 1:
            print("Full Name Is Required")
        else:
            break


    sql = "SELECT * FROM Professor WHERE name = %s"
    val = (prof_name, )

    db.execute(sql, val)
    result = db.fetchall()

    # CHECK IF PERSON IS ALREADY REGISTERED
    if len(result) != 0:
        already_registered()

    # SECURITY ANIMAL
    while True:
        prof_s_animal = input("SECURITY QUESTION: What Is The Name Of Your Favorite Animal? ").lower()
        if prof_s_animal == "c":
            login()
        if prof_s_animal != '':
            break

    # PASSWORD
    while True:
        prof_password = input("Enter Your Password: ")
        if prof_password.lower() == "c":
            login()
        if prof_password != '':
            break

    # SANITIZE PASSWORD
    prof_password = sanitize_password(prof_password, prof_name)

    # CONFIRM PASSWORD
    while True:
        confirm_prof_password = input("Confirm Your Password: ")
        if confirm_prof_password.lower() == "c":
            login()
        if confirm_prof_password != '':
            break

    if prof_password != confirm_prof_password:
        confirm_prof_password = confirm_password_error(prof_name)

    # HASH PASSWORD
    confirm_prof_password = hash_password(confirm_prof_password)

    # ADDRESS
    while True:
        prof_address = input("Enter Your Address: ")
        if prof_address.lower() == "c":
            login()
        if prof_address != '':
            break

    # AGE
    while True:
        prof_age = input("Enter Your Age: ")
        if prof_age.lower() == "c":
            login()
        if not checkAge(prof_age):
            print("Your Age Must Be A Number")
        if checkAge(prof_age):
            break
    prof_age = int(prof_age)

    # PHONE NUMBER
    while True:
        prof_phone_number = input("Enter Your Phone Number: ")
        if prof_phone_number != '':
            break


    # SANITIZE PHONE NUMBER
    prof_phone_number = sanitize_phone_number(prof_phone_number)


    # COURSES TAUGHT
    while True:
        prof_courses_taught = input("Enter The Courses You Teach: ")
        if prof_courses_taught != '':
            break

    # CHECKING IF THE COURSES ARE AVAILABLE
    prof_courses_taught = sanitize_courses(prof_courses_taught, "Register_As_Prof")


    Prof = Professor(prof_name.split()[0], prof_name.split()[1], prof_address, prof_age, prof_phone_number, None, prof_courses_taught)


    sql = "INSERT INTO Professor (name, address, email, age, phoneNumber, salary, CoursesTaught, security_animal, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (prof_name, Prof.getAddress(), Prof.getEmail(), Prof.getAge(), Prof.getPhoneNumber(), 60000.00, prof_courses_taught,
           prof_s_animal, confirm_prof_password)

    db.execute(sql, val)
    mydb.commit()

    print()
    while True:
        tmp = input("You Have Been Registered. Press (L) To Login: ").lower()
        if tmp == "l":
            login()







# REGISTER AS STUDENT
def register_as_student():
    clear()
    print("REGISTER AS STUDENT")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    while True:
        print()
        student_name = input("Enter Your Full Name: ")
        if student_name.lower() == "c":
            login()
        if len(student_name.split()) == 0 or len(student_name.split()) == 1:
            print("Full Name Required")
        else:
            break

    sql = "SELECT * FROM Student WHERE name = %s"
    val = (student_name, )

    db.execute(sql, val)
    result = db.fetchall()

    # CHECK IF PERSON IS ALREADY REGISTERED
    if len(result) != 0:
        already_registered()

    # SECURITY ANIMAL
    while True:
        student_s_animal = input("SECURITY QUESTION: What Is The Name Of Your Favorite Animal? ").lower()
        if student_s_animal == "c":
            login()
        if student_s_animal != '':
            break

    # PASSWORD
    while True:
        student_password = getpass("Enter Your Password: ")
        if student_password.lower() == "c":
            login()
        if student_password != '':
            break

    # SANITIZE PASSWORD
    student_password = sanitize_password(student_password, student_name)

    # CONFIRM PASSWORD
    while True:
        confirm_student_password = getpass("Confirm Your Password: ")
        if confirm_student_password.lower() == "c":
            login()
        if confirm_student_password != '':
            break

    if student_password != confirm_student_password:
        confirm_student_password = confirm_password_error(student_name)

    # HASH PASSWORD
    confirm_student_password = hash_password(confirm_student_password)

    # ADDRESS
    while True:
        student_address = input("Enter Your Address: ")
        if student_address.lower() == "c":
            login()
        if student_address != '':
            break

    # AGE
    while True:
        student_age = input("Enter Your Age: ")
        if student_age.lower() == "c":
            login()
        if not checkAge(student_age):
            print("Your Age Must Be A Number")
            print()
        else:
            break
    student_age = int(student_age)


    # PHONE NUMBER
    while True:
        student_phone_number = input("Enter Your Phone Number: ")
        if student_phone_number.lower() == "c":
            login()
        if student_phone_number != '':
            break

    # SANITIZE PHONE NUMBER
    student_phone_number = sanitize_phone_number(student_phone_number)


    Stu = Student(student_name.split()[0], student_name.split()[1], student_address, student_age, student_phone_number, None, None, None)


    sql = "INSERT INTO Student (name, address, email, age, phoneNumber, CoursesEnrolledIn, grades, major, GPA, security_animal, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (student_name, Stu.getAddress(), Stu.getEmail(), Stu.getAge(), Stu.getPhoneNumber(), Stu.getCoursesEnrolledIn(),
           Stu.getGrades(), Stu.getMajor(), Stu.getGPA(), student_s_animal, confirm_student_password)

    db.execute(sql, val)
    mydb.commit()

    print()
    while True:
        tmp = input("You Have Been Registered. Press (L) To Login: ").lower()
        if tmp == "l":
            login()


# ALREADY REGISTERED
def already_registered(came_from=None):
    if came_from == None:
        while True:
            print()
            tmp = input("You Are Already Registered. Press (L) To Login: ").lower()
            if tmp == "l":
                login()
    elif came_from == "Register Student":
        while True:
            print()
            tmp = input(f"This Student Has Already Been Already Registered. Press (T) To Try Again:\n"
                        f"                                                  Press (B) To Go Back: ").lower()
            if tmp == "t":
                register_student()
            elif tmp == "b":
                DeanMenu(None)
    elif came_from == "Register Professor":
        while True:
            print()
            tmp = input(f"This Professor Has Already Been Already Registered. Press (T) To Try Again:\n"
                        f"                                                    Press (B) To Go Back: ").lower()
            if tmp == "t":
                register_professor()
            elif tmp == "b":
                DeanMenu(None)


# DEAN MENU
def DeanMenu(name):
    clear()
    update_student_grades()
    # GETTING INBOX COUNT
    sql = "SELECT COUNT(*) FROM dean_notification"
    db.execute(sql)
    inbox_count = db.fetchall()[0][0]
    print("DEAN MENU")
    if name != None:
        print(f"Welcome {name}")
    print(now)
    print("-------------------------------")
    print("Press (L) To Log Out")
    print("Press (S) To Send Notification")
    print("Press (A) To Open Admin Options")
    print("Press (I) To Open Inbox")
    print("-------------------------------")
    print()
    print(f"INBOX: {inbox_count}")
    print()
    print()
    print("AVAILABLE OPTIONS")
    print()
    print("1 - View All Students            |  6  - Update Professor Info")
    print("2 - View All Professors          |  7  - Register Student")
    print("3 - View Specific Student        |  8  - Register Professor")
    print("4 - View Specific Professor      |  9  - Unregister Student")
    print("5 - Update Student Info          |  10 - Unregister Professor")

    print()
    while True:
        user_choice  = input("Choose An Option: ").lower()
        # CHECKING IF L WAS ENTERED
        if len(user_choice) == 1:
            user_choice = user_choice.lower()
        if user_choice == "l":
            login()
        elif user_choice == "i":
            dean_inbox()
        elif user_choice == "a":
            dean_admin_options()
        elif user_choice == "s":
            dean_send_notification()
        elif  user_choice == "1":
            view_all_students()
        elif user_choice == "2":
            view_all_professors()
        elif user_choice == "3":
            view_specific_student()
        elif user_choice == "4":
            view_specific_professor()
        elif user_choice == "5":
            update_student_info()
        elif user_choice == "6":
            update_professor_info()
        elif user_choice == "7":
            register_student()
        elif user_choice == "8":
            register_professor()
        elif user_choice == "9":
            unregister_student()
        elif user_choice == "10":
            unregister_professor()



# ------ STUDENT RELATED OPTIONS ------#

def view_all_students():
    clear()
    print("VIEW ALL STUDENTS")
    print("-"*len(now))
    print(now)
    print("-"*len(now))
    print()
    db.execute("SELECT * FROM Student")
    all_students = db.fetchall()

    attributes = ["Id", "Name", "Address", "Email", "Age", "Phone Number", "Courses Enrolled In", "Grades", "Major", "GPA"]

    k = 0
    print()
    for i in range(len(all_students)):
        print(f"|----------Student ( {i + 1} )----------|")
        print()
        for j in range(len(all_students[0]) - 2):
            print(f"{attributes[k]}: {all_students[i][j]}")
            k += 1
            if k == len(attributes):
                k = 0
        print()

    print()
    while True:
        print("-----------------------------------------------")
        tmp = input("Press (M) To Return To Dean Menu:\n"
                    "Press (A) To Take Action On A Specific Student: ").lower()
        if tmp == "m":
            DeanMenu(None)
        elif tmp == "a":
            take_action_on_student()
def view_all_majors(came_from=None):
    clear()
    print("---------------")
    print("VIEW ALL MAJORS")
    print("---------------")
    print()
    all_majors = Student.getAllMajors()
    for i in range(len(all_majors)):
        print(all_majors[i][0])
        print()

    while True:
        print("-------------------------------------------")
        back = input("Press (D) To Get The Description Of A Major:\n"
                     "Press (B) To Go Back: ").lower()
        if back != '' and (back == "d" or back == "b"):
            break
    if back == "d":
        while True:
            print()
            major_name = input("Enter The Name Of The Major: ")
            if major_name != '':
                break
        major_name = capitalize(major_name)
        # CHECKING VALID MAJOR NAME WAS ENTERED
        if not Student.checkIfMajorIsAvailableToSet(major_name):
            while True:
                print()
                if came_from == "Dean":
                    error = input("Invalid Major. Press (T) To Try Again:\nPress (M) To Return To Dean Menu: ").lower()
                    if error == "t":
                        view_all_majors("Dean")
                        break
                    elif error == "m":
                        DeanMenu(None)
                        break
                elif came_from == "Student":
                    print()
                    error = input(
                        "Invalid Major. Press (T) To Try Again:\nPress (M) To Return To Student Menu: ").lower()
                    if error == "t":
                        view_all_majors("Student")
                        break
                    elif error == "m":
                        StudentMenu(None)
                        break

        # GETTING THE DESCRIPTION, NAMES AND STUDENT COUNT IN THE MAJOR
        sql = "SELECT description, studentNames, studentCount FROM Major WHERE name = %s"
        val = (major_name,)
        db.execute(sql, val)
        results = db.fetchall()
        try:
            major_description = results[0][0]
            students_names = results[0][1]
            student_count = results[0][2]
        except IndexError:
            clear()
            print("An Error Occured")
            sleep(1.5)
            exit()

        clear()
        print("-" * len(major_name))
        print(major_name.upper())
        print("-" * len(major_name))
        print()
        print("------------------------" + "-" * len(str(student_count)))
        print(f"STUDENT COUNT IN MAJOR: {student_count}")
        print("------------------------" + "-" * len(str(student_count)))
        print()
        print(major_description)
        major = Major(major_name)
        major.getRequiredCourse("GET")

        while True:
            print()
            if came_from == "Dean":
                back = input("Press (C) To View More Majors:\nPress (M) To Modify Major:\n"
                             "Press (V) To View All Students In Major:\nPress (A) To Return Admin Options: ").lower()
                if back == "c":
                    view_all_majors("Dean")
                elif back == "m":
                    dean_modify_major(major_name, major.getRequiredCourse("POST"))
                elif back == "v":
                    view_students_in_major(major_name, students_names)
                elif back == "a":
                    dean_admin_options()
            elif came_from == "Student":
                back = input("Press (C) To View More Majors:\nPress (M) To Return To Student Menu: ").lower()
                if back == "c":
                    view_all_majors("Student")
                elif back == "m":
                    StudentMenu(None)
    elif back == "b":
        if came_from == "Dean":
            dean_admin_options()
        elif came_from == "Student":
            StudentMenu(None)
        elif came_from == "Prof":
            ProfessorMenu(None)

# VIEW STUDENTS IN MAJOR
def view_students_in_major(major_name, student_names):
    student_names = student_names.split()
    clear()
    print("------------" + "-" * len(major_name))
    print(f"STUDENTS IN {major_name.upper()}")
    print("------------" + "-" * len(major_name))
    print()
    student_names = [student_names[i] + " " + student_names[i + 1] for i in range(len(student_names) // 2)]

    for name in student_names:
        print(name)
    if len(student_names) == 0:
        print("No Students")

    while True:
        print()
        back = input("Press (B) To Go Back: ").lower()
        if back == "b":
            view_all_majors("Dean")
            break

# TAKE ACTION ON STUDENT
def take_action_on_student(name=None):
    clear()
    print("TAKE ACTION ON STUDENT")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    if name == None:
        while True:
            student_name = input("Enter The Name Of The Student: ")
            if student_name != '':
                break
        update_student_info(name=student_name, came_from="take_action")
    else:
        update_student_info(name=name)

# VIEW SPECIFIC STUDENT
def view_specific_student():
    clear()
    print("VIEW SPECIFIC STUDENT")
    print(now)
    print("--------------------------------")
    print("Press (M) To Return To Dean Menu")
    print("--------------------------------")
    print()
    print("SEARCH BY")
    print()
    print("1 -> Search By Id")
    print("2 -> Search By Full Name")
    print("3 -> Search By Email")
    print("4 -> Search By Age")
    print("5 -> Search By Major")
    print("6 -> Search By Courses Enrolled In")
    print()
    while True:
        user_choice = input("Choose An Option: ").lower()
        # CHECKING IF M WAS ENTERED
        if user_choice == "m":
            DeanMenu(None)
        elif user_choice == "1":
            search_student("Id", "id")
        elif user_choice == "2":
            search_student("Full Name", "name")
        elif user_choice == "3":
            search_student("Email", "email")
        elif user_choice == "4":
            search_student("Age", "age")
        elif user_choice == "5":
            search_student("Major", "major")
        elif user_choice == "6":
            search_student("Courses Enrolled In", "CoursesEnrolledIn")
def search_student(search_for, column_name):
    clear()
    print(f"SEARCH STUDENT BY {search_for.upper()}")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    where_val = input(f"Enter The Student's {search_for}: ")
    # CHECKING IF C WAS ENTERED
    if len(where_val) == 1:
        where_val = where_val.lower()
    if where_val == "c":
        DeanMenu(None)
    print()
    if where_val != "NULL":
        like_query = f"%{where_val}%"
        sql = f"SELECT * FROM Student WHERE {column_name} LIKE %s"
        val = (like_query,)
        db.execute(sql, val)
    else:
        db.execute(f"SELECT * FROM Student WHERE {column_name} IS NULL")

    found_students = db.fetchall()

    if len(found_students) != 0:
        attributes = ["Id", "Name", "Address", "Email", "Age", "Phone Number", "Courses Enrolled In", "Grades", "Major",
                      "GPA"]

        k = 0
        print()
        for i in range(len(found_students)):
            print(f"|----------Student ( {i + 1} )----------|")
            print()
            for j in range(len(found_students[0]) - 2):
                print(f"{attributes[k]}: {found_students[i][j]}")
                k += 1
                if k == len(attributes):
                    k = 0
            print()
        while True:
            print("-----------------------------------------------")
            if len(found_students) == 1:
                tmp = input("Press (M) To Return To Dean Menu:\n"
                            "Press (A) To Take Action On This Student:\n"
                            "Press (S) To Search Again: ").lower()
            else:
                tmp = input("Press (M) To Return To Dean Menu:\n"
                            "Press (A) To Take Action On A Student:\n"
                            "Press (S) To Search Again: ").lower()
            if tmp == "m":
                DeanMenu(None)
            elif tmp == "a" and len(found_students) == 1:
                take_action_on_student(found_students[0][1])
            elif tmp == "a":
                take_action_on_student()
            elif tmp == "s":
                view_specific_student()



    else:
        while True:
            none_found = input("No Student Found. Press (M) To Return To Dean Menu:\n"
                               "                  Press (S) To Search Again: ").lower()
            if none_found == "m":
                DeanMenu(None)
            elif none_found == "s":
                view_specific_student()

# UPDATE STUDENT INFO
def update_student_info(came_from=None, name=None):
    clear()
    if came_from == None:
        print("UPDATE STUDENT INFO")
    else:
        print("TAKE ACTION ON STUDENT")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    print("AVAILABLE OPTIONS")
    print()
    print("1 -> Update Address")
    print("2 -> Update Email")
    print("3 -> Update Age")
    print("4 -> Update Phone Number")
    print("5 -> Update Courses Enrolled In")
    print("6 -> Update Grades")
    print("7 -> Update Major")
    print()
    while True:
        user_option = input("Choose An Option: ").lower()
        if user_option == "c":
            DeanMenu(None)
        elif user_option == "1":
            update_student('Address', 'address', name)
        elif user_option == "2":
            update_student('Email', 'email', name)
        elif user_option == "3":
            update_student('Age', 'age', name)
        elif user_option == "4":
            update_student('Phone Number', 'PhoneNumber', name)
        elif user_option == "5":
            update_student('Courses Enrolled In', 'CoursesEnrolledIn', name)
        elif user_option == "6":
            update_student('Grades', 'grades', name)
        elif user_option == "7":
            update_student("Major", "major", name)
def update_student(current_change, column, name):
    clear()
    print("UPDATE STUDENT")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    if name == None:
        student_name = input("Enter The Name Of The Student: ")
    else:
        student_name = name

    # name = student_name
    print()
    # CHECKING IF C WAS ENTERED
    if len(student_name) == 1:
        student_name = student_name.lower()
    if student_name == "c":
        DeanMenu(None)
    # CHECKING IF STUDENT EXISTS
    sql = "SELECT * FROM Student WHERE name = %s"
    val = (student_name, )
    db.execute(sql, val)
    student_found = db.fetchall()

    if len(student_found) == 0:
        no_person_found()

    Stu = Student(student_name.split()[0], student_name.split()[1], student_found[0][2], student_found[0][4], student_found[0][5],
                  student_found[0][6], student_found[0][7], student_found[0][8])

    if current_change == "Address":
        print(f"CURRENT ADDRESS: {Stu.getAddress()}")
    elif current_change == "Email":
        print(f"CURRENT EMAIL: {Stu.getEmail()}")
    elif current_change == "Age":
        print(f"CURRENT AGE: {Stu.getAge()}")
    elif current_change == "Phone Number":
        print(f"CURRENT PHONE NUMBER: {Stu.getPhoneNumber()}")
    elif current_change == "Courses Enrolled In":
        print(f"CURRENT COURSES ENROLLED IN: {Stu.getCoursesEnrolledIn().split()}")
        before_change = Stu.getCoursesEnrolledIn()
        print()
        new_courses = input("Enter Their New Courses: ")
        # CHECKING IF C WAS ENTERED
        if len(new_courses) == 1:
            new_courses = new_courses.lower()
        if new_courses == "c":
            DeanMenu(None)
        if Stu.setCoursesEnrolledIn(new_courses) == -1:
            while True:
                print()
                error = input("Can't Set Course. Check If All Courses Entered Are Available. Press (T) To Try Again:\n"
                              "                                                              Press (V) To View All Courses:\n"
                              "                                                              Press (M) To Return To Dean Menu: ").lower()
                if error == "t":
                    update_student('Courses Enrolled In', 'CoursesEnrolledIn', student_name)
                elif error == "v":
                    view_all_course_general("Dean_Update_Student_Courses", ["Courses Enrolled In", "CoursesEnrolledIn", student_name])
                elif error == "m":
                    DeanMenu(None)

        elif Stu.setCoursesEnrolledIn(new_courses) == -2:
            while True:
                print()
                error = input(f"Cant Enroll In More Than {Stu.MAX_COURSES_STUDENT_CAN_ENROLL_IN} Courses. Press (T) To Try Again:\n"
                              f"                                               Press (M) To Return To Dean Menu: ").lower()

                if error == "t":
                    update_student('Courses Enrolled In', 'CoursesEnrolledIn', student_name)
                elif error == "m":
                    DeanMenu(None)

        # CONFIRMATION
        while True:
            confirmation = input(
                f"CONFIRMATION: Are You Sure You Want To Change {student_name} Courses Enrolled In? ").lower()
            if confirmation != '' and (confirmation == "yes" or confirmation == "no"):
                break

        if confirmation == "yes":
            Stu.setCoursesEnrolledIn(new_courses)

            sql = f"UPDATE Student SET {column} = %s WHERE name = %s"
            # getCoursesEnrolledIn() RETURNS A LIST SO I REMOVED THE LIST AND THE COMMAS AND JUST ADDED THE COURSE NAMES
            val = (', '.join(Stu.getCoursesEnrolledIn()).replace(',', ''), student_name)

            db.execute(sql, val)
            mydb.commit()
            update_course_database()

            # SET UP NOTIFICATION
            sql = "INSERT INTO student_notification (notification, received_from, date, stu_id) VALUES (%s, %s, %s, %s)"
            val = (f"You Were Enrolled In: {Stu.getCoursesEnrolledIn()}","Dean", now, Stu.getID())
            db.execute(sql, val)
            mydb.commit()
            print()
            print(f"You Changed {student_name} Courses Enrolled In From {before_change} To {Stu.getCoursesEnrolledIn()}")
            print()
            while True:
                back = input("Press (U) To Update More Students Info:\nPress (M) To Return To Dean Menu: ").lower()
                if back == "u":
                    update_student_info()
                elif back == "m":
                    DeanMenu(None)
        else:
            update_student_info(name=student_name)
    elif current_change == "Grades":
        current_grades = Stu.getGrades()

        if current_grades != None:
            print("-" * len(current_grades) + "----------------")

        print(f"CURRENT GRADES: {current_grades}")

        print(f"GPA: {Stu.getGPA()}")
        if current_grades != None:
            print("-" * len(current_grades) + "----------------")
        before_change = current_grades
        print()
        # CONFIRMATION
        while True:
            confirmation = input(
                f"CONFIRMATION: Are You Sure You Want To Change {student_name} Grades? ").lower()
            if confirmation != '' and (confirmation == "yes" or confirmation == "no"):
                break
        if confirmation == "yes":
            print()
            Stu.setGrades()
            # UPDATE GRADES
            sql = f"UPDATE Student SET {column} = %s WHERE name = %s"
            val = (Stu.getGrades(), student_name)
            db.execute(sql, val)
            mydb.commit()

            # UPDATE GPA
            sql = f"UPDATE Student SET GPA = %s WHERE name = %s"
            val = (Stu.getGPA(), student_name)

            db.execute(sql, val)
            mydb.commit()
            update_course_database()

            # SET UP NOTIFICATION
            sql = "INSERT INTO student_notification (notification, received_from, date, stu_id) VALUES (%s, %s, %s, %s)"
            val = (f"Your Grades Have Been Updated To: {Stu.getGrades()}", "Dean", now, Stu.getID())
            db.execute(sql, val)
            mydb.commit()
            print()
            print(f"You Changed {student_name} Grades From |{before_change}| To |{Stu.getGrades()}|")
            print()
            print(f"{student_name} GPA IS NOW: {Stu.getGPA()}")
            print()
            while True:
                back = input("Press (U) To Update More Students Info:\nPress (M) To Return To Dean Menu: ").lower()
                if back == "u":
                    update_student_info()
                elif back == "m":
                    DeanMenu(None)
        else:
            update_student_info(name=student_name)
    elif current_change == "Major":
        if Stu.getMajor() != None:
            print("-" * len(Stu.getMajor()) + "----------------")
        print(f"CURRENT MAJOR: {Stu.getMajor()}")
        if Stu.getMajor() != None:
            print("-" * len(Stu.getMajor()) + "----------------")
        before_change = Stu.getMajor()

        print()
        new_major = input("Enter Their New Major: ").rstrip()
        # CHECKING IF C WAS ENTERED
        if len(new_major) == 1:
            new_major = new_major.lower()
        if new_major == "c":
            DeanMenu(None)

        if Stu.setMajor(new_major) == -1:
            while True:
                print()
                error = input("Can't Set Major. Check If The Major You Entered Is Available. Press (T) To Try Again:\n"
                              "                                                              Press (S) To See All Majors:\n"
                              "                                                              Press (M) To Return To Main Menu: ").lower()
                if error == "t":
                    update_student('Major', 'major', student_name)
                elif error == "s":
                    view_all_majors("Dean")
                elif error == "m":
                    DeanMenu(None)

        # CONFIRMATION
        while True:
            confirmation = input(
                f"CONFIRMATION: Are You Sure You Want To Change {student_name} Major? ").lower()
            if confirmation != '' and (confirmation == "yes" or confirmation == "no"):
                break

        if confirmation == "yes":
            Stu.setMajor(new_major)

            sql = "UPDATE Student SET major = %s WHERE name = %s"
            val = (Stu.getMajor(), student_name)
            db.execute(sql, val)
            mydb.commit()

            # SET UP NOTIFICATION
            sql = "INSERT INTO student_notification (notification, received_from, date, stu_id) VALUES (%s, %s, %s, %s)"
            val = (f"Your Major Has Been Changed From: {before_change} To {Stu.getMajor()}", "Dean", now, Stu.getID())
            db.execute(sql, val)
            mydb.commit()

            print()
            print(f"You Changed {student_name} Major From {before_change} To {Stu.getMajor()}")
            print()
            while True:
                back = input("Press (U) To Update More Students Info:\nPress (M) To Return To Dean Menu: ").lower()
                if back == "u":
                    update_student_info()
                elif back == "m":
                    DeanMenu(None)
        else:
            update_student_info(name=student_name)

    # THE CHANGES
    print()
    update_changes = input(f"Enter Their New {current_change}: ")
    while True:
        confirmation = input(f"CONFIRMATION: Are You Sure You Want To Change {student_name} {current_change} To {update_changes}? ").lower()
        if confirmation != '' and (confirmation == "yes" or confirmation == "no"):
            break
    if confirmation == "yes":
        if len(update_changes) == 1:
            update_changes = update_changes.lower()
        if update_changes == 'c':
            update_student_info(name=name)

        sql = f"UPDATE Student SET {column} = %s WHERE name = %s"
        val = (update_changes, student_name)

        db.execute(sql, val)
        mydb.commit()

        # SET UP NOTIFICATION
        sql = "INSERT INTO student_notification (notification, received_from, date, stu_id) VALUES (%s, %s, %s, %s)"
        val = (f"Your {current_change} Has Been Changed To: {update_changes}", "Dean", now, Stu.getID())
        db.execute(sql, val)
        mydb.commit()

        print()
        print(f"You Changed {student_name} {current_change} To {update_changes}")
        print()
        back = input("Press (U) To Update More Students Info:\nPress (M) To Return To Dean Menu: ").lower()
        if back == "u":
            update_student_info()
        elif back == "m":
            DeanMenu(None)

    else:
        update_student_info()
def no_person_found(came_from=None, argv=None, kwargs=None):
    if came_from == None:
        while True:
            print()
            tmp = input(f"No Student Found With That Name. Press (T) To Try Again\n"
                        f"                                 Press (M) To Return To Dean Menu: ").lower()
            if tmp == "t":
                update_student_info()
            elif tmp == "m":
                DeanMenu(None)
    elif came_from == "Unregister Student":
        while True:
            print()
            tmp = input("That Student Was Not Found. Press (T) To Try Again:\n"
                        "                            Press (M) To Return To Dean Menu: ").lower()
            if tmp == "t":
                unregister_student()
            elif tmp == "m":
                DeanMenu(None)
    elif came_from == "Drop Student":
        if argv == "Prof":
            msg = "Professor Menu"
        elif argv == "Dean":
            msg = "Dean Menu"
        else:
            msg = "Main Menu"
        while True:
            print()
            tmp = input(f"That Student Was Not Found. Press (T) To Return To Courses:\n"
                        f"                            Press (M) To Return To {msg}: ").lower()
            if tmp == "t":
                view_all_courses_prof()
            elif tmp == "m":
                if argv == "Dean":
                    DeanMenu(None)
                elif argv == "Prof":
                    ProfessorMenu(None)

    elif came_from == "Unregister Professor":
        while True:
            print()
            tmp = input("That Professor Was Not Found. Press (T) To Try Again:\n"
                        "                              Press (M) To Return To Dean Menu: ").lower()
            if tmp == "t":
                unregister_professor()
            elif tmp == "m":
                DeanMenu(None)
    elif came_from == "Update Professor":
        while True:
            print()
            tmp = input("That Professor Was Not Found. Press (T) To Try Again:\n"
                        "                              Press (M) To Return To Dean Menu: ").lower()
            if tmp == "t":
                update_professor_info()
            elif tmp == "m":
                DeanMenu(None)

    elif came_from == "Notification":
        if argv == "Dean":
            if kwargs == "Send_To_Stu":
                menu = "Dean Menu"
                who  = "Student"
            elif kwargs == "Send_To_Prof":
                menu = "Dean Menu"
                who  = "Professor"
            elif kwargs == "Send_To_Dean":
                menu = "Dean Menu"
                who  = "Dean"

        elif argv == "Prof":
            if kwargs == "Send_To_Stu":
                menu = "Professor Menu"
                who = "Student"
            elif kwargs == "Send_To_Prof":
                menu = "Professor Menu"
                who = "Professor"
            elif kwargs == "Send_To_Dean":
                menu = "Professor Menu"
                who = "Dean"

        elif argv == "Stu":
            if kwargs == "Send_To_Stu":
                menu = "Student Menu"
                who  = "Student"
            elif kwargs == "Send_To_Prof":
                menu = "Student Menu"
                who  = "Professor"
            elif kwargs == "Send_To_Dean":
                menu = "Student Menu"
                who  = "Dean"
        while True:
            print()
            print(f"That {who} Was Not Found")
            print()
            tmp = input(f"Press (T) To Try Again:\nPress (M) To Return To {menu}")

            if tmp == "t":
                if argv == "Prof":
                    prof_send_notification()
                elif argv == "Dean":
                    dean_send_notification()
                elif argv == "Stu":
                    stu_send_notification()
            elif tmp == "m":
                if argv == "Prof":
                    ProfessorMenu(None)
                elif argv == "Dean":
                    ProfessorMenu(None)
                elif argv == "Stu":
                    StudentMenu(None)

    elif came_from == "Enroll_Student_In_Course":
        while True:
            print()
            tmp = input("That Student Was Not Found. Press (T) To Try Again:\n"
                        "                            Press (M) To Return To Dean Menu: ").lower()
            if tmp == "t":
                enroll_student_in_course(argv)
            elif tmp == "m":
                DeanMenu(None)



# DEAN VIEW ALL COURSES
def view_all_courses_dean():
    clear()
    print("----------------")
    print("VIEW ALL COURSES")
    print("----------------")
    print()
    all_courses = Course.getAll_Courses()
    db.execute("SELECT description FROM Course")

    description = db.fetchall()

    for i, course in enumerate(all_courses):
        print(f"{all_courses[i][0]} - {description[i][0][:indexOf(description[i][0], ':')]}")
        print()

    while True:
        dean_choice = input("Press (S) To Select A Course:\nPress (M) To Return To Dean Menu: ").lower()
        if dean_choice == "s":
            search_for_course_dean()
        elif dean_choice == "m":
            DeanMenu(None)
# DEAN SELECT COURSE
def select_course_dean(course_name):
    clear()
    course = Course(course_name)

    print("-" * len(course_name) + "-------")
    print(f"{course_name.upper()} COURSE")
    print("-" * len(course_name) + "-------")
    print()
    print("<<<<<<<<<<<<<<<< DESCRIPTION >>>>>>>>>>>>>>>>")
    print()
    print(course.getDescription())
    print()
    print()

    try:
        print("-" * len(course) + "------------------")
        print(f"COURSE CANCELLED: {course.isCourseCancelled()}")
        print(f"Class Size: {course.getStudentCountInCourse()}")
        print()
    except:
        print()
        print("An Error Occurred. Restart Application")
        sleep(1)
        exit()
    if course.getStudentCountInCourse() > 0:
        # COMPUTE THE CLASS AVERAGE
        all_grades = []
        all_names = course.getStudentNamesInCourse().split()
        for i in range(course.getStudentCountInCourse()):
            # GETTING STUDENTS INFO
            sql = "SELECT CoursesEnrolledIn, grades FROM Student WHERE name = %s"
            val = (all_names[i + i] + " " + all_names[i + i + 1],)
            db.execute(sql, val)
            result = db.fetchall()

            grades_for_course = {}
            grades_from_db = result[0][1].split()

            for grade in grades_from_db:
                # GENERATE DICTIONARY OF GRADES
                if ':' in grade:
                    grade_key = grade.replace(':', '')
                if grade.replace("%", '').isnumeric():
                    grade_value = grade.replace('%', '')

                    grades_for_course.update({grade_key: grade_value})

            all_grades.append(int(grades_for_course[course_name]))
        # COMPUTING THE AVERAGE GRADE FOR THE COURSE
        average = round(sum(all_grades) / len(all_grades))
        print(f"Class Average: {average}%")
    print("-" * len(course) + "------------------")
    print()

    while True:
        print("Press (S) To Search Again:")
        print("Press (E) To Enroll A Student In This Course:")
        print("Press (C) To Return To All Courses:")
        if course.getStudentCountInCourse() != 0:
            print("Press (V) To View All Students Enrolled In This Course: ")
        back = input("Press (A) To Return To Admin Options: ").lower()
        if back == "s":
            search_for_course_dean("Search")
        elif back == "e":
            enroll_student_in_course(course_name)
        elif back == "c":
            view_all_courses_dean()
        elif course.getStudentCountInCourse() != 0 and back == "v":
            view_students_enrolled_in_course_dean(course_name)
        elif back == "a":
            dean_admin_options()
# SEARCH FOR COURSE DEAN
def search_for_course_dean(came_from=None):
    while True:
        print()
        course_name = input("Enter The Name Of The Course: ").upper()
        if course_name != '':
            break
    # CHECK IF COURSE ENTERED IS IN THE LIST
    sql = "SELECT name FROM Course WHERE name = %s"
    val = (course_name,)
    db.execute(sql, val)
    result = db.fetchall()
    if len(result) == 0:
        course_not_found("Dean Search For Course")

    # COURSE WAS FOUND
    select_course_dean(course_name)
# STUDENT ENROLL IN COURSE
def enroll_student_in_course(course_name):
    clear()
    print("ENROLL STUDENT IN COURSE")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    # GET ALL THE COURSES CURRENTLY ENROLLED
    while True:
        print()
        stu_name = input("Enter The Name Of The Student: ")
        if stu_name != '':
            break

    # CHECKING IF C WAS ENTERED
    if len(stu_name) == 1:
        stu_name = stu_name.lower()
    if stu_name == "c":
        DeanMenu(None)

    sql = "SELECT CoursesEnrolledIn From Student WHERE name = %s"
    val = (stu_name,)
    db.execute(sql, val)
    # CHECKING IF THAT STUDENT WAS FOUND
    courses_enrolled_in = db.fetchall()
    if len(courses_enrolled_in) == 0:
        no_person_found("Enroll_Student_In_Course", course_name)
    courses_enrolled_in = courses_enrolled_in[0][0]
    print()
    print(f"Courses {stu_name} Is Currently Enrolled In: {courses_enrolled_in.split()}")

    # CHECK IF THE STUDENT IS ALREADY ENROLLED IN THE COURSE
    for course in courses_enrolled_in.split():
        if course_name == course:
            print()
            while True:
                print()
                back = input(f"Student Is Already Enrolled In This Course. Press (S) To Return To All Courses:\n"
                             "                                             Press (M) To Return To Dean Menu: ").lower()
                if back == "s":
                    view_all_courses_dean()
                elif back == "m":
                    DeanMenu(None)


    # CHECKING IF STUDENT CANT ENROLL IN ANY MORE COURSES
    if len(courses_enrolled_in.split()) == Student.MAX_COURSES_STUDENT_CAN_ENROLL_IN:
        while True:
            print()
            print(f"Student Can't Enroll In More Than {Student.MAX_COURSES_STUDENT_CAN_ENROLL_IN} Courses.")
            print()
            back = input("Press (S) To Return To All Courses\nPress (M) To Return To Dean Menu: ").lower()
            if back == "s":
                view_all_courses_dean()
            elif back == "m":
                DeanMenu(None)

    while True:
        print()
        confirmation = input(f"CONFIRMATION: Are You Sure You Want To Enroll {stu_name} In {course_name}? ")
        if confirmation != '' and (confirmation == "yes" or confirmation == "no"):
            break
    if confirmation == "yes":
        Stu = Student(stu_name.split()[0], stu_name.split()[1], None, None, None, None, None, None)

        new_courses_to_add = courses_enrolled_in + " " + course_name
        sql = "UPDATE Student SET CoursesEnrolledIn = %s WHERE id = %s"
        val = (new_courses_to_add, Stu.getID())
        db.execute(sql, val)
        mydb.commit()

        # SET UP NOTIFICATION
        sql = "SELECT id FROM Dean WHERE name = %s"
        val = (dean_name, )
        db.execute(sql, val)
        dean_id = db.fetchall()[0][0]

        sql = "INSERT INTO dean_notification (notification, received_from, date, person_id) VALUES (%s, %s, %s, %s)"
        val = (f"{stu_name} Has Been Enrolled In: {course_name}", f"Dean ({dean_name})", now, dean_id)
        db.execute(sql, val)
        mydb.commit()

        while True:
            print()
            print(f"{stu_name} Has Been Successfully Enrolled In {course_name}")
            print()
            back = input(f"Press (S) To Return To All Courses:\nPress (M) To Return To Dean Menu: ").lower()
            if back == "s":
                view_all_courses_dean()
            elif back == "m":
                DeanMenu(None)
    else:
        DeanMenu(None)
def view_students_enrolled_in_course_dean(course_name):
    clear()
    print("---------------------" + "-" * len(course_name))
    print(f"STUDENTS ENROLLED IN {course_name}")
    print("---------------------" + "-" * len(course_name))
    print()
    course = Course(course_name)
    # GET ALL STUDENTS IN COURSE
    sql = "SELECT studentsInCourse FROM Course WHERE name = %s"
    val = (course_name,)
    db.execute(sql, val)
    result = db.fetchall()[0][0].split()
    students_in_course = [result[i+i] + " " + result[i+i+1] for i in range(len(result) // 2)]

    print(students_in_course)

    while True:
        print()
        tmp = input("Press (V) To View Students Grades:\nPress (A) To Return To Admin Options: ").lower()
        if tmp == "v":
            all_names = course.getStudentNamesInCourse().split()
            num_students_in_course = course.getStudentCountInCourse()
            view_student_grade_for_course(course_name, "Dean")
            break
        elif tmp == "a":
            dean_admin_options()
            break


# REGISTER STUDENT
def register_student():
    clear()
    print("REGISTER STUDENT")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    while True:
        student_name = input("Enter Their Full Name: ")
        if student_name != '':
            break
    # CHECKING IF C WAS ENTERED
    if len(student_name) == 1:
        student_name = student_name.lower()
    if student_name == "c":
        DeanMenu(None)

    sql = "SELECT * FROM Student WHERE name = %s"
    val = (student_name, )

    db.execute(sql, val)
    result = db.fetchall()

    # CHECK IF PERSON IS ALREADY REGISTERED
    if len(result) != 0:
        already_registered("Register Student")

    # SECURITY ANIMAL
    while True:
        student_s_animal = input("SECURITY QUESTION: What Is The Name Of Their Favorite Animal? ").lower()
        if student_s_animal != '':
            break

    # PASSWORD
    while True:
        student_password = input("Enter Their Password: ")
        if student_password != '':
            break

    # SANITIZE PASSWORD
    student_password = sanitize_password(student_password, student_name, 'Student')

    # CONFIRM PASSWORD
    while True:
        confirm_student_password = input("Confirm Their Password: ")
        if confirm_student_password != '':
            break

    if student_password != confirm_student_password:
        confirm_student_password = confirm_password_error(student_name, 'Student')

    # HASH PASSWORD
    confirm_student_password = hash_password(confirm_student_password)

    # ADDRESS
    while True:
        student_address = input("Enter Their Address: ")
        if student_address != '':
            break

    # AGE
    while True:
        student_age = input("Enter Their Age: ")
        if student_age.lower() == "c":
            DeanMenu(None)
        if not checkAge(student_age):
            print("Their Age Must Be A Number")
        else:
            break
    student_age = int(student_age)


    # PHONE NUMBER
    while True:
        student_phone_number = input("Enter Their Phone Number: ")
        if student_phone_number != '':
            break

    # SANITIZE PHONE NUMBER
    student_phone_number = sanitize_phone_number(student_phone_number, 'Student')


    Stu = Student(student_name.split()[0], student_name.split()[1], student_address, student_age, student_phone_number, None, None, None)


    sql = "INSERT INTO Student (name, address, email, age, phoneNumber, CoursesEnrolledIn, grades, major, GPA, security_animal, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (student_name, Stu.getAddress(), Stu.getEmail(), Stu.getAge(), Stu.getPhoneNumber(), Stu.getCoursesEnrolledIn(),
           Stu.getGrades(), Stu.getMajor(), Stu.getGPA(), student_s_animal, confirm_student_password)

    db.execute(sql, val)
    mydb.commit()

    print()
    while True:
        tmp = input(f"{student_name} Student Has Been Registered. Press (B) To Go Back: ").lower()
        if tmp == "b":
            DeanMenu(None)
def unregister_student():
    clear()
    print("UNREGISTER STUDENT")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    while True:
        student_to_delete = input("Enter The Name Or Id Of The Student: ")
        if student_to_delete != '':
            break
    # CHECKING IF C WAS ENTERED
    if len(student_to_delete) == 1:
        student_to_delete = student_to_delete.lower()
    if student_to_delete == "c":
        DeanMenu(None)

    # CHECKING IF ID WAS ENTERED
    if student_to_delete.isdigit():
        # CHECKING IF THE STUDENT EXIST
        sql = "SELECT * FROM Student WHERE id = %s"
        val = (student_to_delete, )
        db.execute(sql, val)
        result = db.fetchall()
        if len(result) == 0:
            no_person_found("Unregister Student")

        # UNREGISTER THE STUDENT
        stu_id, name, address, email, age, phone_number, courses_enrolled_in, grades, major, gpa = \
        result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], result[0][5], result[0][6], result[0][7], \
        result[0][8], result[0][9]

        print()
        print("<" * (len(address) // 2), "DETAILS", ">" * (len(address) // 2 + 1))
        print()
        print("-" * len(address) + "---------")
        print()
        print(f"Id: {stu_id}")
        print(f"Name: {name}")
        print(f"Address: {address}")
        print(f"Email: {email}")
        print(f"Age: {age}")
        print(f"Phone Number: {phone_number}")
        print(f"Courses Enrolled In: {courses_enrolled_in}")
        print(f"Grades: {grades}")
        print(f"Major: {major}")
        print(f"GPA: {gpa}")
        print()
        print("-" * len(address) + "---------")
        print()
        while True:
            confirmation = input(f"CONFIRMATION: Are You Sure You Want To Unregister {result[0][1]}? ").lower()
            if confirmation != '' and (confirmation == "yes" or confirmation == "no"):
                break
        if confirmation == "yes":
            sql = "DELETE FROM Student WHERE id = %s"
            val = (student_to_delete, )
            db.execute(sql, val)
            mydb.commit()
            print()
            print(f"{result[0][1]} Has Been Unregistered.")
            while True:
                print()
                back = input("Press (U) To Unregister More Students:\nPress (M) To Return To Dean Menu: ").lower()
                if back == "u":
                    unregister_student()
                elif back == "m":
                    DeanMenu(None)
        else:
            DeanMenu(None)

    # CHECKING FOR STUDENT NAME
    else:
        # CHECKING IF STUDENT EXIST
        sql = "SELECT * FROM Student WHERE name = %s"
        val = (student_to_delete, )
        db.execute(sql, val)
        result = db.fetchall()
        if len(result) == 0:
            no_person_found("Unregister Student")
        # UNREGISTER THE STUDENT
        stu_id, name, address, email, age, phone_number, courses_enrolled_in, grades, major, gpa = \
        result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], result[0][5], result[0][6], \
        result[0][7],result[0][8], result[0][9]

        print()
        print("<" * (len(address) // 2), "DETAILS", ">" * (len(address) // 2 + 1))
        print()
        print("-" * len(address) + "---------")
        print()
        print(f"Id: {stu_id}")
        print(f"Name: {name}")
        print(f"Address: {address}")
        print(f"Email: {email}")
        print(f"Age: {age}")
        print(f"Phone Number: {phone_number}")
        print(f"Courses Enrolled In: {courses_enrolled_in}")
        print(f"Grades: {grades}")
        print(f"Major: {major}")
        print(f"GPA: {gpa}")
        print()
        print("-" * len(address) + "---------")
        print()
        while True:
            confirmation = input(f"CONFIRMATION: Are You Sure You Want To Unregister {result[0][1]}? ").lower()
            if confirmation != '' and (confirmation == "yes" or confirmation == "no"):
                break
        if confirmation == "yes":
            sql = "DELETE FROM Student WHERE name = %s"
            val = (student_to_delete, )
            db.execute(sql, val)
            mydb.commit()
            print()
            print(f"{result[0][1]} Has Been Unregistered.")
            while True:
                print()
                back = input("Press (U) To Unregister More Students:\nPress (M) To Return To Dean Menu: ").lower()
                if back == "u":
                    unregister_student()
                elif back == "m":
                    DeanMenu(None)
        else:
            DeanMenu(None)


# DEAN INBOX
def dean_inbox():
    clear()
    print("----------")
    print("YOUR INBOX")
    print("----------")
    print(now)
    print()

    sql = "SELECT id, notification, received_from, date, person_id FROM dean_notification"
    db.execute(sql)
    all_notifications = db.fetchall()


    if len(all_notifications) == 0:
        print("No Notifications")

    terminal_size = os.get_terminal_size().columns
    for i in range(len(all_notifications)):
        # AUTO FIT THE BROKEN LINES
        message_len = len(all_notifications[i][1]) + len('Message: ')
        received_from_len = len(all_notifications[i][2]) + len('Received From: ') + len(f' Id: {str(all_notifications[i][0])}')

        max_len_of_attributes = max([message_len, received_from_len])

        if max_len_of_attributes > terminal_size:
            broken_line_added = '-' * terminal_size
        else:
            if max_len_of_attributes == message_len:
                broken_line_added = '-' * message_len
            else:
                broken_line_added = '-' * received_from_len

        print(broken_line_added)
        print(f"Id: {all_notifications[i][0]}")
        print(f"Date: {all_notifications[i][3]}")
        print(f"Received From: {all_notifications[i][2]} Id: {all_notifications[i][4]}")
        print(f"Message: {all_notifications[i][1]}")
        print(broken_line_added)
        print()
        

    while True:
        print()
        print("Press CON To View All Conversations")
        print()
        print("Press (O) To Open A Notification:")
        print()
        print("Press (D) To Filter By Date:              |  Press (C) To Clear A Notification:")
        print("Press (F) To Filter By Received From:     |  Press (CA) To Clear All Notifications:")
        print("Press (M) To Filter By Message:           |  Press (S) To Return To Dean Menu:")
        print()
        filter = input("Choose An Option: ")
        if filter == "con":
            view_all_conversations(dean_name, 'Dean')
        elif filter == "o":
            open_dean_notification(all_notifications)
        elif filter == "d":
            filter_dean_notification_by_date(all_notifications)
        elif filter == "f":
            filter_dean_notification_by_received_from(all_notifications)
        elif filter == "m":
            filter_dean_notification_by_message(all_notifications)
        elif filter == "c":
            clear_dean_notification()
        elif filter == "ca":
            clear_all_dean_notifications()
        elif filter == "s":
            DeanMenu(None)



# DEAN OPEN NOTIFICATION
def open_dean_notification(notification):
    all_possible_id = [str(notification[i][0]) for i in range(len(notification))]
    print()
    while True:
        noti_id = input("Enter The Id Of The Notification: ")
        if noti_id not in all_possible_id:
            print("Invalid Id")
        else:
            break
    sql = "SELECT id, notification, received_from, date FROM dean_notification WHERE id = %s"
    val = (int(noti_id),)
    db.execute(sql, val)
    notification_to_open = db.fetchall()
    clear()
    # AUTO FIT THE BROKEN LINES
    max_len_of_attributes = max([len(notification_to_open[0][1]), len(notification_to_open[0][2])])
    if max_len_of_attributes == len(notification_to_open[0][1]):
        broken_line_added = "-" * len("Message: ")
    else:
        broken_line_added = "-" * len("Received From: ")

    message = notification_to_open[0][1]
    received_from = notification_to_open[0][2]
    print("-" * max_len_of_attributes + broken_line_added)
    print(f"Id: {notification_to_open[0][0]}")
    print(f"Date: {notification_to_open[0][3]}")
    print(f"Received From: {notification_to_open[0][2]}")
    print(f"Message: {notification_to_open[0][1]}")
    print("-" * max_len_of_attributes + broken_line_added)
    print()

    print("Press (R) To Respond:")
    while True:
        back = input("Press (B) To Go Back: ").lower()
        # RESPONSE
        if back == "r":
            receiverName = extractNameFromNotification(received_from)["receiverName"]
            receiverType = extractNameFromNotification(received_from)["Type"]
            if receiverName == None:
                while True:
                    print()
                    error = input("Unable To Respond: Please Contact The Admin. Press (B) To Go Back: ").lower()
                    if error == "b":
                        dean_inbox()
                        break
            else:
                respondToNotification(dean_name, "Dean", receiverType, receiverName, message)

        elif back == "b":
            dean_inbox()
            break
# FILTER DEAN NOTIFICATIONS
def filter_dean_notification_by_date(notifications):
    while True:
        print()
        date_to_filter = input("Enter The Date: ")
        if date_to_filter != '':
            break

    clear()
    total_found = 0
    print("-" * len(date_to_filter) + "--------------")
    print(f"Filtered by: {date_to_filter}")
    print("-" * len(date_to_filter) + "--------------")
    print()
    for i in range(len(notifications)):
        if date_to_filter in notifications[0][3]:
            print("-" * len(notifications[i][1]) + "---------")
            print(f"Id: {notifications[i][0]}")
            print(f"Date: {notifications[i][3]}")
            print(f"Received From: {notifications[i][2]}")
            print(f"Message: {notifications[i][1]}")
            print("-" * len(notifications[i][1]) + "---------")
            print()
            total_found += 1

    if total_found == 0:
        print()
        print("No Notifications Found")

    while True:
        print()
        back = input("Press (F) To Filter Again:\nPress (C) To Clear A Notification:\nPress (S) To Return To Dean Menu: ").lower()
        if back == "f":
            dean_inbox()
        if back == "c":
            clear_dean_notification()
        elif back == "s":
            DeanMenu(None)
def filter_dean_notification_by_received_from(notifications):
    while True:
        print()
        person_to_filter = input("Enter The Name: ")
        person_to_filter = capitalize(person_to_filter)
        if person_to_filter != '':
            break

    clear()
    total_found = 0
    print("-" * len(person_to_filter) + "--------------")
    print(f"Filtered by: {person_to_filter}")
    print("-" * len(person_to_filter) + "--------------")
    print()
    for i in range(len(notifications)):
        if person_to_filter in notifications[i][2]:
            print("-" * len(notifications[i][1]) + "---------")
            print(f"Id: {notifications[i][0]}")
            print(f"Date: {notifications[i][3]}")
            print(f"Received From: {notifications[i][2]}")
            print(f"Message: {notifications[i][1]}")
            print("-" * len(notifications[i][1]) + "---------")
            print()
            total_found += 1

    if total_found == 0:
        print()
        print("No Notifications Found")

    while True:
        print()
        back = input("Press (F) To Filter Again:\nPress (C) To Clear A Notification:\nPress (S) To Return To Dean Menu: ").lower()
        if back == "f":
            dean_inbox()
        elif back == "c":
            clear_dean_notification()
        elif back == "s":
            DeanMenu(None)
def filter_dean_notification_by_message(notifications):
    while True:
        print()
        message_to_filter = input("Enter The Message: ")
        if message_to_filter != '':
            break

    clear()
    total_found = 0
    print("-" * len(message_to_filter) + "--------------")
    print(f"Filtered by: {message_to_filter}")
    print("-" * len(message_to_filter) + "--------------")
    print()
    for i in range(len(notifications)):
        if message_to_filter in notifications[i][1]:
            print("-" * len(notifications[i][1]) + "---------")
            print(f"Id : {notifications[i][0]}")
            print(f"Date: {notifications[i][3]}")
            print(f"Received From: {notifications[i][2]}")
            print(f"Message: {notifications[i][1]}")
            print("-" * len(notifications[i][1]) + "---------")
            print()
            total_found += 1

    if total_found == 0:
        print()
        print("No Notifications Found")

    while True:
        print()
        back = input("Press (F) To Filter Again:\nPress (C) To Clear A Notification:\nPress (S) To Return To Dean Menu: ").lower()
        if back == "f":
            dean_inbox()
        elif back == "c":
            clear_dean_notification()
        elif back == "s":
            DeanMenu(None)
def clear_dean_notification():
    while True:
        print()
        notification_id = input("Enter The Id Of The Notification: ")
        if notification_id != '' and notification_id.isdigit():
            break

    while True:
        print()
        confirmation = input("CONFIRMATION: Are You Sure You Want To Clear This Notifications? ")
        if confirmation != '' and (confirmation == "yes" or confirmation == "no"):
            break

    if confirmation == "yes":
        sql = "DELETE FROM dean_notification WHERE id = %s"
        val = (int(notification_id), )
        db.execute(sql, val)
        mydb.commit()

        while True:
            print()
            back = input("Notification Deleted. Press (M) To Return To Dean Menu: ").lower()
            if back == "m":
                DeanMenu(None)
    else:
        DeanMenu(None)

def clear_all_dean_notifications():
    while True:
        print()
        confirmation = input("CONFIRMATION: Are You Sure You Want To Clear All Notifications? ")
        if confirmation != '' and (confirmation == "yes" or confirmation == "no"):
            break

    if confirmation == "yes":
        sql = "DELETE FROM dean_notification"
        db.execute(sql)
        mydb.commit()

        while True:
            print()
            back = input("All Notifications Cleared. Press (M) To Return To Dean Menu: ").lower()
            if back == "m":
                DeanMenu(None)
    else:
        DeanMenu(None)

# DEAN SEND NOTIFICATION
def dean_send_notification():
    clear()
    print("SEND NOTIFICATION")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    while True:
        print()
        to = input("To (Dean, Professor, Or Student): ").capitalize()
        if to != '' and (to == "Student" or to == "Professor" or to == "Dean"):
            break
        if to == '' or (to != "Student" or to != "Professor" or to != "Dean"):
            print("Messages Can Only Be Sent To: Dean, Professor Or Student")

    # CHECKING IF C WAS ENTERED
    if to.lower() == "c":
        DeanMenu(None)

    # STUDENT
    if to == "Student":
        while True:
            print()
            stu_name = capitalize(input("Enter The Name Of The Student: "))
            if stu_name.lower() == "c":
                DeanMenu(None)
            if stu_name != '':
                break
        sql = "SELECT id FROM Student WHERE name = %s"
        val = (stu_name, )
        db.execute(sql, val)
        stu_id = db.fetchall()
        if len(stu_id) == 0:
            no_person_found("Notification", "Dean", "Send_To_Stu")
        stu_id = stu_id[0][0]

        while True:
            message = input("Message: ")
            if message != '':
                break

        while True:
            print()
            confirmation = input("CONFIRMATION: Are You Sure You Want To Send This Message? ").lower()
            if confirmation == "yes" or confirmation == "no":
                break
        if confirmation == "yes":
            # CREATE CONVERSATION
            conversationInfo = {
                'convoId': f'{dean_name}(Dean) To {stu_name}(Student)',
                'date': now,
                'senderType': "Dean",
                'senderName': dean_name,
                'preMessage': None,
                'senderMessage': message,
                'receivedFrom': None
            }
            createConversation(conversationInfo)
            # SET UP NOTIFICATION
            sql = "INSERT INTO student_notification (notification, received_from, date, stu_id) VALUES (%s, %s, %s, %s)"
            val = (message, f"Dean ({dean_name})", now, stu_id)
            db.execute(sql, val)
            mydb.commit()

            while True:
                print()
                back = input("Your Message Has Been Sent. Press (S) To Send Another Message:\n"
                             "                            Press (M) To Return To Dean Menu: ").lower()
                if back == "s":
                    dean_send_notification()
                elif back == "m":
                    DeanMenu(None)
        elif confirmation == "no":
            DeanMenu(dean_name)

    # PROFESSOR
    elif to == "Professor":
        while True:
            print()
            professor_name = capitalize(input("Enter The Name Of The Professor: "))
            if professor_name.lower() == "c":
                DeanMenu(None)
            if professor_name != '':
                break
        sql = "SELECT id FROM Professor WHERE name = %s"
        val = (professor_name, )
        db.execute(sql, val)
        prof_id = db.fetchall()
        if len(prof_id) == 0:
            no_person_found("Notification", "Dean", "Send_To_Prof")
        prof_id = prof_id[0][0]

        while True:
            message = input("Message: ")
            if message != '':
                break
        while True:
            print()
            confirmation = input("CONFIRMATION: Are You Sure You Want To Send This Message? ").lower()
            if confirmation == "yes" or confirmation == "no":
                break
        if confirmation == "yes":
            # CREATE CONVERSATION
            conversationInfo = {
                'convoId': f'{dean_name}(Dean) To {professor_name}(Professor)',
                'date': now,
                'senderType': "Dean",
                'senderName': dean_name,
                'preMessage': None,
                'senderMessage': message,
                'receivedFrom': None
            }
            createConversation(conversationInfo)
            # SET UP NOTIFICATION
            sql = "INSERT INTO professor_notification (notification, received_from, date, prof_id) VALUES (%s, %s, %s, %s)"
            val = (message, f"Dean ({dean_name})", now, prof_id)
            db.execute(sql, val)
            mydb.commit()

            while True:
                print()
                back = input("Your Message Has Been Sent. Press (S) To Send Another Message:\n"
                             "                            Press (M) To Return To Dean Menu: ").lower()
                if back == "s":
                    dean_send_notification()
                    break
                elif back == "m":
                    DeanMenu(None)
                    break
        elif confirmation == "no":
            DeanMenu(dean_name)

    # DEAN
    elif to == "Dean":
        while True:
            print()
            deanName = capitalize(input("Enter The Name Of The Dean: "))
            if deanName.lower() == "c":
                DeanMenu(None)
            if deanName != '':
                break
        # CHECKING IF CORRECT NAME WAS ENTERED
        sql = "SELECT * FROM Dean WHERE name = %s"
        val = (deanName,)
        db.execute(sql, val)
        result = db.fetchall()
        if len(result) == 0:
            no_person_found("Notification", "Dean", "Send_To_Dean")

        # GETTING THE ID OF THE DEAN
        sql = "SELECT id FROM Dean WHERE name = %s"
        val = (dean_name, )
        db.execute(sql, val)
        dean_id = db.fetchall()[0][0]

        while True:
            message = input("Message: ")
            if message != '':
                break
        while True:
            print()
            confirmation = input("CONFIRMATION: Are You Sure You Want To Send This Message? ").lower()
            if confirmation == "yes" or confirmation == "no":
                break

        if confirmation == "yes":
            # CREATE CONVERSATION
            conversationInfo = {
                'convoId': f'{dean_name}(Dean) To {deanName}(Dean)',
                'date': now,
                'senderType': "Dean",
                'senderName': dean_name,
                'preMessage': None,
                'senderMessage': message,
                'receivedFrom': None
            }
            createConversation(conversationInfo)
            # SET UP NOTIFICATION
            sql = "INSERT INTO dean_notification (notification, received_from, date, person_id) VALUES (%s, %s, %s, %s)"
            val = (message, f"Dean ({dean_name})", now, dean_id)
            db.execute(sql, val)
            mydb.commit()

            while True:
                print()
                back = input("Your Message Has Been Sent. Press (S) To Send Another Message:\n"
                             "                            Press (M) To Return To Dean Menu: ").lower()
                if back == "s":
                    dean_send_notification()
                    break
                elif back == "m":
                    DeanMenu(None)
                    break
        elif confirmation == "no":
            DeanMenu(dean_name)


# ------ PROFESSOR RELATED OPTIONS ------#

def view_all_professors():
    clear()
    print("VIEW ALL PROFESSORS")
    print("-"*len(now))
    print(now)
    print("-"*len(now))
    print()
    db.execute("SELECT * FROM Professor")
    all_professors = db.fetchall()

    attributes = ["Id:", "Name:", "Address:", "Email:", "Age:", "Phone Number:", "Salary: $", "Courses Taught:"]

    k = 0
    print()
    for i in range(len(all_professors)):
        print(f"|----------Professor ( {i + 1} )----------|")
        print()
        for j in range(len(all_professors[0]) - 2):
            print(f"{attributes[k]} {all_professors[i][j]}")
            k += 1
            if k == len(attributes):
                k = 0
        print()

    print()
    while True:
        print("-----------------------------------------------")
        tmp = input("Press (M) To Return To Dean Menu:\n"
                    "Press (A) To Take Action On A Specific Professor: ").lower()
        if tmp == "m":
            DeanMenu(None)
        elif tmp == "a":
            take_action_on_professor()

# TAKE ACTION ON PROFESSOR
def take_action_on_professor(name=None):
    clear()
    print("TAKE ACTION ON PROFESSOR")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    if name == None:
        while True:
            professor_name = input("Enter The Name Of The Professor: ")
            if professor_name != '':
                break
        update_professor_info(name=professor_name)
    else:
        update_professor_info("Take Action",name)

# VIEW SPECIFIC PROFESSOR
def view_specific_professor():
    clear()
    print("VIEW SPECIFIC PROFESSOR")
    print(now)
    print("--------------------------------")
    print("Press (M) To Return To Dean Menu")
    print("--------------------------------")
    print()
    print("SEARCH BY")
    print()
    print("1 -> Search By Id")
    print("2 -> Search By Full Name")
    print("3 -> Search By Email")
    print("4 -> Search By Age")
    print("5 -> Search By Salary")
    print("6 -> Search By Courses Taught")
    print()
    while True:
        user_choice = input("Choose An Option: ").lower()
        # CHECKING IF M WAS ENTERED
        if user_choice == "m":
            DeanMenu(None)
        elif user_choice == "1":
            search_professor("Id", "id")
        elif user_choice == "2":
            search_professor("Full Name", "name")
        elif user_choice == "3":
            search_professor("Email", "email")
        elif user_choice == "4":
            search_professor("Age", "age")
        elif user_choice == "5":
            search_professor("Salary", "salary")
        elif user_choice == "6":
            search_professor("Courses Taught", "CoursesTaught")
def search_professor(search_for, column_name):
    clear()
    print(f"SEARCH PROFESSOR BY {search_for.upper()}")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    where_val = input(f"Enter The Professor's {search_for}: ")
    # CHECKING IF C WAS ENTERED
    if len(where_val) == 1:
        where_val = where_val.lower()
    if where_val == "c":
        DeanMenu(None)
    print()
    like_query = f"%{where_val}%"
    sql = f"SELECT * FROM Professor WHERE {column_name} LIKE %s"
    val = (like_query,)

    db.execute(sql, val)
    found_professors = db.fetchall()

    if len(found_professors) != 0:
        attributes = ["Id", "Name", "Address", "Email", "Age", "Phone Number", "Salary", "Courses Taught"]

        k = 0
        print()
        for i in range(len(found_professors)):
            print(f"|----------Professor ( {i + 1} )----------|")
            print()
            for j in range(len(found_professors[0]) - 2):
                print(f"{attributes[k]}: {found_professors[i][j]}")
                k += 1
                if k == len(attributes):
                    k = 0
            print()
        while True:
            print("-----------------------------------------------")
            if len(found_professors) == 1:
                tmp = input("Press (M) To Return To Dean Menu:\n"
                            "Press (A) To Take Action On This Professor:\n"
                            "Press (S) To Search Again: ").lower()
            else:
                tmp = input("Press (M) To Return To Dean Menu:\n"
                            "Press (A) To Take Action On A Professor:\n"
                            "Press (S) To Search Again: ").lower()
            if tmp == "m":
                DeanMenu(None)
            elif tmp == "a" and len(found_professors) == 1:
                take_action_on_professor(found_professors[0][1])
            elif tmp == "a":
                take_action_on_professor()
            elif tmp == "s":
                view_specific_professor()



    else:
        while True:
            none_found = input("No Professor Found. Press (M) To Return To Dean Menu:\n"
                               "                    Press (S) To Search Again: ").lower()
            if none_found == "m":
                DeanMenu(None)
            elif none_found == "s":
                view_specific_professor()

# UPDATE PROFESSOR INFO
def update_professor_info(came_from=None, name=None):
    clear()
    if came_from == None:
        print("UPDATE PROFESSOR INFO")
    else:
        print("TAKE ACTION ON PROFESSOR")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    print("AVAILABLE OPTIONS")
    print()
    print("1 -> Update Address")
    print("2 -> Update Email")
    print("3 -> Update Age")
    print("4 -> Update Phone Number")
    print("5 -> Salary")
    print("6 -> Courses Taught")
    print()
    while True:
        user_option = input("Choose An Option: ").lower()
        if user_option == "c":
            DeanMenu(None)
        elif user_option == "1":
            update_professor('Address', 'address', name)
        elif user_option == "2":
            update_professor('Email', 'email', name)
        elif user_option == "3":
            update_professor('Age', 'age', name)
        elif user_option == "4":
            update_professor('Phone Number', 'PhoneNumber', name)
        elif user_option == "5":
            update_professor('Salary', 'salary', name)
        elif user_option == "6":
            update_professor('Courses Taught', 'CoursesTaught', name)
def update_professor(current_change, column, name):
    clear()
    print("UPDATE PROFESSOR")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    if name == None:
        professor_name = input("Enter The Name Of The Professor: ")
    else:
        professor_name = name
    print()
    # CHECKING IF C WAS ENTERED
    if len(professor_name) == 1:
        professor_name = professor_name.lower()
    if professor_name == "c":
        DeanMenu(None)
    # CHECKING IF PROFESSOR EXISTS
    sql = "SELECT * FROM Professor WHERE name = %s"
    val = (professor_name,)
    db.execute(sql, val)
    professors_found = db.fetchall()

    if len(professors_found) == 0:
        no_person_found("Update Professor")


    Prof = Professor(professor_name.split()[0], professor_name.split()[1], professors_found[0][2], professors_found[0][4],
                  professors_found[0][5],professors_found[0][6], professors_found[0][7])


    if current_change == "Address":
        print(f"CURRENT ADDRESS: {Prof.getAddress()}")
    elif current_change == "Email":
        print(f"CURRENT EMAIL: {Prof.getEmail()}")
    elif current_change == "Age":
        print(f"CURRENT AGE: {Prof.getAge()}")
    elif current_change == "Phone Number":
        print(f"CURRENT PHONE NUMBER: {Prof.getPhoneNumber()}")
    elif current_change == "Salary":
        print(f"CURRENT SALARY: {Prof.getSalary()}")
        before_change = Prof.getSalary()

        update_changes = input(f"Enter Their New {current_change}: ")
        while True:
            confirmation = input(
                f"CONFIRMATION: Are You Sure You Want To Change {professor_name} Salary To {update_changes}? ").lower()
            if confirmation != '' and (confirmation == "yes" or confirmation == "no"):
                break
        if confirmation == "yes":
            if len(update_changes) == 1:
                update_changes = update_changes.lower()
            if update_changes == 'c':
                update_professor_info(name=name)

            # FORMAT SALARY
            if ' ' in update_changes:
                update_changes = update_changes.replace(' ', '')
            if '$' in update_changes:
                update_changes = update_changes.replace('$', '')
            if ',' in update_changes:
                update_changes = update_changes.replace(',', '')
            if '.' in update_changes:
                index = 0
                for i in range(len(update_changes)):
                    if update_changes[i] == '.':
                        break
                    index += 1
                update_changes = update_changes[:index]

            update_changes = format(float(update_changes),'.2f')
            Prof.setSalary(update_changes)

            sql = f"UPDATE Professor SET salary = %s WHERE name = %s"
            val = (update_changes, professor_name)

            db.execute(sql, val)
            mydb.commit()

            # SET UP NOTIFICATION
            sql = "INSERT INTO professor_notification (notification, received_from, date, prof_id) VALUES (%s, %s, %s, %s)"
            val = (f"Your Salary Has Been Changed From: {before_change} To: {Prof.getSalary()}", "Dean", now, Prof.getID())
            db.execute(sql, val)
            mydb.commit()

            print()
            print(f"You Changed {professor_name} Salary To {Prof.getSalary()}")
            print()
            back = input("Press (U) To Update More Professors Info:\nPress (M) To Return To Dean Menu: ").lower()
            if back == "u":
                update_professor_info()
            elif back == "m":
                DeanMenu(None)

        else:
            update_professor_info()
    elif current_change == "Courses Taught":
        print(f"CURRENT COURSES TAUGHT: {Prof.getCoursesTaught()}")
        before_change = Prof.getCoursesTaught()
        print()
        new_courses = input("Enter Their New Courses: ").upper()
        # CHECKING IF C WAS ENTERED
        if len(new_courses) == 1:
            new_courses = new_courses.lower()
        if new_courses == "c":
            DeanMenu(None)
        if Prof.setCoursesTaught(new_courses) == -1:
            while True:
                print()
                error = input("Can't Set Course Check If All Courses Entered Are Available. Press (T) To Try Again:\n"
                              "                                                             Press (V) To View All Courses:\n"
                              "                                                             Press (M) To Return To Dean Menu: ").lower()
                if error == "t":
                    update_professor('Courses Taught', 'CoursesTaught', professor_name)
                elif error == "v":
                    view_all_course_general("Dean_Update_Prof_Courses_Taught", ["Courses Taught", "CoursesTaught", professor_name])
                elif error == "m":
                    DeanMenu(None)

        elif Prof.setCoursesTaught(new_courses) == -2:
            while True:
                print()
                error = input(
                    f"Cant Teach More Than {Prof.MAX_COURSES_A_PROFESSOR_CAN_TEACH} Courses. Press (T) To Try Again:\n"
                    f"                                Press (M) To Return To Dean Menu: ").lower()

                if error == "t":
                    update_professor('Courses Taught', 'CoursesTaught', professor_name)
                elif error == "m":
                    DeanMenu(None)

        # CONFIRMATION
        while True:
            confirmation = input(
                f"CONFIRMATION: Are You Sure You Want To Change {professor_name} Courses Taught? ").lower()
            if confirmation != '' and (confirmation == "yes" or confirmation == "no"):
                break

        if confirmation == "yes":
            Prof.setCoursesTaught(new_courses)

            sql = f"UPDATE Professor SET {column} = %s WHERE name = %s"
            # getCoursesTaught() RETURNS A LIST SO I REMOVED THE LIST AND THE COMMAS AND JUST ADDED THE COURSE NAMES
            val = (', '.join(Prof.getCoursesTaught()).replace(',', ''), professor_name)

            db.execute(sql, val)
            mydb.commit()

            # SET UP NOTIFICATION
            sql = "INSERT INTO professor_notification (notification, received_from, date, prof_id) VALUES (%s, %s, %s, %s)"
            val = (f"The Courses You Teach Has Been Changed To: {Prof.getCoursesTaught()}", "Dean", now, Prof.getID())

            db.execute(sql, val)
            mydb.commit()

            print()
            print(f"You Changed {professor_name} Courses Taught From {before_change} To {Prof.getCoursesTaught()}")
            print()
            while True:
                back = input("Press (U) To Update More Professors Info:\nPress (M) To Return To Dean Menu: ").lower()
                if back == "u":
                    update_professor_info()
                elif back == "m":
                    DeanMenu(None)
        else:
            update_professor_info(name=professor_name)

    # THE CHANGES
    print()
    update_changes = input(f"Enter Their New {current_change}: ")
    while True:
        confirmation = input(
            f"CONFIRMATION: Are You Sure You Want To Change {professor_name} {current_change} To {update_changes}? ").lower()
        if confirmation != '' and (confirmation == "yes" or confirmation == "no"):
            break
    if confirmation == "yes":
        if len(update_changes) == 1:
            update_changes = update_changes.lower()
        if update_changes == 'c':
            update_professor_info(name=name)

        sql = f"UPDATE Professor SET {column} = %s WHERE name = %s"
        val = (update_changes, professor_name)

        db.execute(sql, val)
        mydb.commit()

        # SET UP NOTIFICATION
        sql = "INSERT INTO professor_notification (notification, received_from, date, prof_id) VALUES (%s, %s, %s, %s)"
        val = (f"Your {current_change} Has Been Changed To: {update_changes}", "Dean", now, Prof.getID())
        db.execute(sql, val)
        mydb.commit()

        print()
        print(f"You Changed {professor_name} {current_change} To {update_changes}")
        print()
        back = input("Press (U) To Update More Professors Info:\nPress (M) To Return To Dean Menu: ").lower()
        if back == "u":
            update_professor_info()
        elif back == "m":
            DeanMenu(None)

    else:
        update_professor_info()

# REGISTER PROFESSOR
def register_professor():
    clear()
    print("REGISTER PROFESSOR")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    while True:
        prof_name = input("Enter Their Full Name: ")
        if prof_name != '':
            break
    # CHECKING IF C WAS ENTERED
    if len(prof_name) == 1:
        prof_name = prof_name.lower()
    if prof_name == "c":
        login()

    sql = "SELECT * FROM Professor WHERE name = %s"
    val = (prof_name, )

    db.execute(sql, val)
    result = db.fetchall()

    # CHECK IF PERSON IS ALREADY REGISTERED
    if len(result) != 0:
        already_registered("Register Professor")

    # SECURITY ANIMAL
    while True:
        prof_s_animal = input("SECURITY QUESTION: What Is The Name Of Their Favorite Animal? ").lower()
        if prof_s_animal != '':
            break

    # PASSWORD
    while True:
        prof_password = getpass("Enter Their Password: ")
        if prof_password != '':
            break

    # SANITIZE PASSWORD
    prof_password = sanitize_password(prof_password, prof_name, "Professor")

    # CONFIRM PASSWORD
    while True:
        confirm_prof_password = getpass("Confirm Their Password: ")
        if confirm_prof_password != '':
            break

    if prof_password != confirm_prof_password:
        confirm_prof_password = confirm_password_error(prof_name, "Professor")

    # HASH PASSWORD
    confirm_prof_password = hash_password(confirm_prof_password)

    # ADDRESS
    while True:
        prof_address = input("Enter Their Address: ")
        if prof_address != '':
            break

    # AGE
    while True:
        prof_age = input("Enter Their Age: ")
        if prof_age == "c":
            DeanMenu(None)
        if not checkAge(prof_age):
            print("Their Age Must Be A Number")
        else:
            break
    prof_age = int(prof_age)

    # PHONE NUMBER
    while True:
        prof_phone_number = input("Enter Their Phone Number: ")
        if prof_phone_number != '':
            break


    # SANITIZE PHONE NUMBER
    prof_phone_number = sanitize_phone_number(prof_phone_number, "Professor")


    # COURSES TAUGHT
    while True:
        prof_courses_taught = input("Enter Their Courses Taught: ")
        if prof_courses_taught != '':
            break

    # CHECKING IF THE COURSES ARE AVAILABLE
    prof_courses_taught = sanitize_courses(prof_courses_taught, "Dean_Register_Professor")



    Prof = Professor(prof_name.split()[0], prof_name.split()[1], prof_address, prof_age, prof_phone_number, None, prof_courses_taught)



    sql = "INSERT INTO Professor (name, address, email, age, phoneNumber, salary, CoursesTaught, security_animal, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (prof_name, Prof.getAddress(), Prof.getEmail(), Prof.getAge(), Prof.getPhoneNumber(), 60000.00, prof_courses_taught,
           prof_s_animal, confirm_prof_password)

    db.execute(sql, val)
    mydb.commit()

    print()
    while True:
        tmp = input(f"{prof_name} Has Been Registered. Press (B) To Go Back: ").lower()
        if tmp == "b":
            DeanMenu(None)
def unregister_professor():
    clear()
    print("UNREGISTER PROFESSOR")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    while True:
        professor_to_delete = input("Enter The Name Or Id Of The Professor: ")
        if professor_to_delete != '':
            break
    # CHECKING IF C WAS ENTERED
    if len(professor_to_delete) == 1:
        professor_to_delete = professor_to_delete.lower()
    if professor_to_delete == "c":
        DeanMenu(None)

    # CHECKING IF ID WAS ENTERED
    if professor_to_delete.isdigit():
        # CHECKING IF THE PROFESSOR EXIST
        sql = "SELECT * FROM Professor WHERE id = %s"
        val = (professor_to_delete, )
        db.execute(sql, val)
        result = db.fetchall()
        if len(result) == 0:
            no_person_found("Unregister Professor")

        # UNREGISTER THE PROFESSOR
        print()
        prof_id, name, address, email, age, phone_number, salary, courses_taught = \
            result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], result[0][5], result[0][6], result[0][7]

        print("<" * (len(address)// 2), "DETAILS" , ">" * (len(address)// 2+1))
        print()
        print("-" * len(address) + "---------")
        print()
        print(f"Id: {prof_id}")
        print(f"Name: {name}")
        print(f"Address: {address}")
        print(f"Email: {email}")
        print(f"Age: {age}")
        print(f"Phone Number: {phone_number}")
        print(f"Salary: {format(salary, ',.2f')}")
        print(f"Courses Taught: {courses_taught}")
        print()
        print("-" * len(address) + "---------")
        print()
        while True:
            confirmation = input(f"CONFIRMATION: Are You Sure You Want To Unregister {name}? ").lower()
            if confirmation != '' and (confirmation == "yes" or confirmation == "no"):
                break
        if confirmation == "yes":
            sql = "DELETE FROM Professor WHERE id = %s"
            val = (professor_to_delete, )
            db.execute(sql, val)
            mydb.commit()
            print()
            print(f"{result[0][1]} Has Been Unregistered.")
            while True:
                print()
                back = input("Press (U) To Unregister More Professors:\nPress (M) To Return To Dean Menu: ").lower()
                if back == "u":
                    unregister_professor()
                elif back == "m":
                    DeanMenu(None)
        else:
            DeanMenu(None)

    # CHECKING FOR PROFESSOR NAME
    else:
        # CHECKING IF PROFESSOR EXIST
        sql = "SELECT * FROM Professor WHERE name = %s"
        val = (professor_to_delete, )
        db.execute(sql, val)
        result = db.fetchall()
        if len(result) == 0:
            no_person_found("Unregister Professor")

        # UNREGISTER THE PROFESSOR
        print()
        prof_id, name, address, email, age, phone_number, salary, courses_taught = \
            result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], result[0][5], result[0][6], result[0][
                7]
        print("<" * (len(address) // 2), "DETAILS", ">" * (len(address) // 2+1))
        print()
        print("-" * len(address) + "---------")
        print()
        print(f"Id: {prof_id}")
        print(f"Name: {name}")
        print(f"Address: {address}")
        print(f"Email: {email}")
        print(f"Age: {age}")
        print(f"Phone Number: {phone_number}")
        print(f"Salary: {format(salary, ',.2f')}")
        print(f"Courses Taught: {courses_taught}")
        print()
        print("-" * len(address) + "---------")
        print()
        while True:
            confirmation = input(f"CONFIRMATION: Are You Sure You Want To Unregister {result[0][1]}? ").lower()
            if confirmation != '' and (confirmation == "yes" or confirmation == "no"):
                break
        if confirmation == "yes":
            sql = "DELETE FROM Professor WHERE name = %s"
            val = (professor_to_delete, )
            db.execute(sql, val)
            mydb.commit()
            print()
            print(f"{result[0][1]} Has Been Unregistered.")
            while True:
                print()
                back = input("Press (U) To Unregister More Professors:\nPress (M) To Return To Dean Menu: ").lower()
                if back == "u":
                    unregister_professor()
                elif back == "m":
                    DeanMenu(None)
        else:
            DeanMenu(None)

# DEAN ADMIN OPTIONS
def dean_admin_options():
    sql = "SELECT id FROM Dean WHERE name = %s"
    val = (dean_name, )
    db.execute(sql, val)
    dean_id = db.fetchall()[0][0]
    clear()
    print("DEAN ADMIN OPTIONS")
    print(now)
    print("--------------------------------")
    print("Press (M) To Return To Dean Menu")
    print("--------------------------------")
    print()
    print("Press (C) To Change Your Password")
    print()
    print("Available Options")
    print()
    print("1 - View All Courses           | 6  - Add New Major")
    print("2 - Add New Course             | 7  - Remove Major")
    print("3 - Edit Course                | 8  - Delete All Professor Data")
    print("4 - Remove Course              | 9  - Delete All Student Data")
    print("5 - View All Majors            | 10 - Delete All Data")
    print()
    while True:
        print()
        dean_choice = input("Choose An Option: ").lower()
        if dean_choice != '':
            break
    if dean_choice == "m":
        DeanMenu(None)
    if dean_choice == "1":
        view_all_courses_dean()
    elif dean_choice == "2":
        add_new_course()
    elif dean_choice == "3":
        edit_course()
    elif dean_choice == "4":
        remove_course()
    elif dean_choice == "5":
        view_all_majors("Dean")
    elif dean_choice == "6":
        add_new_major()
    elif dean_choice == "7":
        remove_major()
    elif dean_choice == "8":
        delete_all_data()
    elif dean_choice == "c":
        change_dean_password(dean_name, dean_id)
    else:
        dean_admin_options()

# DEAN ADD NEW COURSE
def add_new_course():
    clear()
    print("ADD NEW COURSE")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    while True:
        print()
        view_course = input("Would You Like To View All Courses? ").lower()
        # CHECKING IF C WAS ENTERED
        if view_course == "c":
            dean_admin_options()
        if view_course != '' and (view_course == "yes" or view_course == "no"):
            break
    if view_course == "yes":
        view_all_courses_dean()
    else:
        # COURSE NAME SHORT
        while True:
            print()
            new_course_number = input("Enter The Course Number Eg. MATH-05: ").upper()
            # CHECKING IF C WAS ENTERED
            if len(new_course_number) == 1:
                new_course_number = new_course_number.lower()
            if new_course_number == "c":
                dean_admin_options()
            if new_course_number != '':
                break
        new_course_number = check_course_num_format(new_course_number)

        # COURSE NAME LONG
        while True:
            print()
            new_course_long_name = input("Enter The Full Name Of The Course: ").upper()
            # CHECKING IF C WAS ENTERED
            if len(new_course_long_name) == 1:
                new_course_long_name = new_course_long_name.lower()
            if new_course_long_name == "c":
                dean_admin_options()
            if new_course_long_name != '':
                break
        new_course_long_name += ":"
        # COURSE DESCRIPTION
        while True:
            print()
            new_course_description = input("Enter The Description Of The Course: ")
            # CHECKING IF C WAS ENTERED
            if len(new_course_description) == 1:
                new_course_description = new_course_description.lower()
            if new_course_description == "c":
                dean_admin_options()
            if new_course_description != '':
                break

        # ADD THE COURSE TO THE DATABASE
        full_description = new_course_long_name + " " + new_course_description
        try:
            sql = "INSERT INTO Course (name, description) VALUES (%s, %s)"
            val = (new_course_number, full_description)
            db.execute(sql, val)
            mydb.commit()
        except mysql.connector.errors.DataError:
            course_description_too_long()

        update_course_database()

        # SET UP NOTIFICATION
        notification = f"{new_course_number} Has Been Added - {new_course_long_name} {full_description}"
        received_from = f"Dean ({dean_name})"
        sql = "SELECT id FROM Dean WHERE name = %s"
        val = (dean_name, )
        db.execute(sql, val)
        dean_id = db.fetchall()[0][0]

        sql = "INSERT INTO dean_notification (notification, received_from, date, person_id) VALUES (%s, %s, %s, %s)"
        val = (notification, received_from, now, dean_id)
        db.execute(sql, val)
        mydb.commit()


        print()
        print(f"{new_course_number} Has Been Added")
        print("-" * len(new_course_number) + "---------------")
        print()
        print("Application Needs To Be Restarted To View New Courses")
        print()
        print(f"{full_description}")
        while True:
            print()
            back = input("Press (A) To Add Another Course:\nPress (M) To Return To Admin Options: ").lower()
            if back == "a":
                add_new_course()
                break
            elif back == "m":
                dean_admin_options()
                break
def check_course_num_format(course_number):
    course_number = course_number.replace(" ", "")
    if "-" not in course_number:
        while True:
            print()
            error = input("Invalid Course Number. Press (T) To Try Again:\n"
                          "                       Press (M) To Return To Dean Menu: ").lower()
            if error != '' and (error == "t" or error == "m"):
                break

        if error == "t":
            print()
            new_course_num = input("Enter The Course Number Eg. MATH-05: ").upper()
            new_course_num = check_course_num_format(new_course_num)

        elif error == "m":
            DeanMenu(None)

        return new_course_num
    return course_number
def course_description_too_long():
    while True:
        print()
        error = input("The Description Of That Course Is Too Long. Press (T) To Try Again:\n"
                      "                                            Press (A) To Return To Admin Options: ").lower()
        if error == "t":
            add_new_course()
            break
        elif error == "a":
            dean_admin_options()
# DEAN EDIT COURSE
def edit_course(courseName=None, courseDescriptionOrName=None):
    clear()
    print("EDIT COURSE")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    if courseName == None:
        while True:
            print()
            course_name = input("Enter The Name Of The Course: ").upper()
            if course_name != '':
                break
    else:
        course_name = courseName
    # CHECK IF C WAS ENTERED
    if course_name.lower() == "c":
        dean_admin_options()

    # CHECKING IF THE COURSE ENTERED IS AVAILABLE
    if not checkCourse(course_name):
        course_not_found("Edit_Course")

    print()
    sql = "SELECT description FROM Course WHERE name = %s"
    val = (course_name, )
    db.execute(sql, val)
    course_description = db.fetchall()[0][0]
    print()
    clear()
    print(f"{course_name}")
    print("-" * len(course_name))
    print()
    print(course_description)
    print()
    # CHANGES
    if courseDescriptionOrName == None:
        while True:
            print()
            print("AVAILABLE CHANGES")
            print()
            print("1 -> Edit Course Number: ")
            print("2 -> Edit Course Description: ")
            print()
            edit_to_make = input("Choose An Option: ").lower()
            if edit_to_make == "1" or edit_to_make == "2" or edit_to_make == "3":
                break
    else:
        edit_to_make = courseDescriptionOrName

    if edit_to_make == "1":
        while True:
            print()
            new_course_number = input("Enter The New Course Number: ").upper()
            if "-" not in new_course_number:
                print("Invalid Course Number")
            else:
                break

        # CONFIRMATION
        while True:
            confirmation = input("CONFIRMATION: Are You Sure You Want To Edit The Name Of This Course? ").lower()
            if confirmation != '' and (confirmation == "yes" or confirmation == "no"):
                break
        if confirmation == "yes":
            sql = "UPDATE Course SET name = %s WHERE name = %s"
            val = (new_course_number, course_name)
            db.execute(sql, val)
            mydb.commit()

            # SET UP NOTIFICATION
            notification = f"{course_name} Name Has Been Changed To - {new_course_number}"
            received_from = f"Dean ({dean_name})"
            sql = "SELECT id FROM Dean WHERE name = %s"
            val = (dean_name,)
            db.execute(sql, val)
            dean_id = db.fetchall()[0][0]

            sql = "INSERT INTO dean_notification (notification, received_from, date, person_id) VALUES (%s, %s, %s, %s)"
            val = (notification, received_from, now, dean_id)
            db.execute(sql, val)
            mydb.commit()

            while True:
                print()
                back = input("Course Name Has Been Changed. Press (E) To Edit More Courses:\n"
                             "                              Press (A) To Return To Admin Options: ").lower()
                if back == "e":
                    edit_course()
                    break
                elif back == "a":
                    dean_admin_options()
                    break

        elif confirmation == "no":
            dean_admin_options()

    elif edit_to_make == "2":
        while True:
            print()
            new_course_description = input("Enter The New Description Of The Course: ")
            if new_course_description != '':
                break

        # CHECKING COURSE FORMAT
        if course_description[:indexOf(course_description, ':')] != new_course_description[:indexOf(new_course_description, ':')]:
            print()
            print(f"You Need To Add {course_description[:indexOf(course_description, ':')]}: At The Beginning Of The "
                  f"Description")
            while True:
                print()
                error = input("Press (T) To Try Again:\nPress (A) To Return To Admin Options: ").lower()
                if error == "t":
                    edit_course(course_name, edit_to_make)
                    break
                elif error == "a":
                    dean_admin_options()
                    break

        # CONFIRMATION
        while True:
            confirmation = input("CONFIRMATION: Are You Sure You Want To Edit The Description Of This Course? ").lower()
            if confirmation != '' and (confirmation == "yes" or confirmation == "no"):
                break

        if confirmation == "yes":
            # SET UP NOTIFICATION
            notification = f"{course_name} Description Has Been Changed To - {new_course_description}"
            received_from = f"Dean ({dean_name})"
            sql = "SELECT id FROM Dean WHERE name = %s"
            val = (dean_name,)
            db.execute(sql, val)
            dean_id = db.fetchall()[0][0]

            sql = "INSERT INTO dean_notification (notification, received_from, date, person_id) VALUES (%s, %s, %s, %s)"
            val = (notification, received_from, now, dean_id)
            db.execute(sql, val)
            mydb.commit()

            sql = "UPDATE Course SET description = %s WHERE name = %s"
            val = (new_course_description, course_name)
            db.execute(sql, val)
            mydb.commit()

            while True:
                print()
                back = input("Course Description Has Been Changed. Press (E) To Edit More Courses:\n"
                             "                                     Press (A) To Return To Admin Options: ").lower()
                if back == "e":
                    edit_course()
                    break
                elif back == "a":
                    dean_admin_options()
                    break
        else:
            dean_admin_options()

# REMOVE COURSE
def remove_course():
    clear()
    print("REMOVE COURSE")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    while True:
        print()
        view_course = input("Would You Like To View All Courses? ").lower()
        # CHECKING IF C WAS ENTERED
        if view_course == "c":
            dean_admin_options()
        if view_course != '' and (view_course == "yes" or view_course == "no"):
            break
    if view_course == "yes":
        view_all_courses_dean()
    else:
        while True:
            print()
            course_to_remove = input("Enter The Name Of The Course To Remove: ").upper()
            if course_to_remove != '':
                break
        # CHECKING IF C WAS ENTERED
        if len(course_to_remove) == 1:
            course_to_remove = course_to_remove.lower()
        if course_to_remove == "c":
            dean_admin_options()

        # CHECK IT COURSE ENTERED IS AVAIALBLED
        if not checkCourse(course_to_remove):
            course_not_found("Dean Remove Course")

        # CONFIRMATION
        while True:
            confirmation = input(f"CONFIRMATION: Are You Sure You Want To Remove {course_to_remove}? ").lower()
            if confirmation != '' and (confirmation == "yes" or confirmation == "no"):
                break

        if confirmation == "yes":
            sql = "DELETE FROM Course WHERE name = %s"
            val = (course_to_remove, )
            db.execute(sql, val)
            mydb.commit()

            # SET UP NOTIFICATION
            notification = f"{course_to_remove} Has Been Removed"
            received_from = f"Dean ({dean_name})"
            sql = "SELECT id FROM Dean WHERE name = %s"
            val = (dean_name,)
            db.execute(sql, val)
            dean_id = db.fetchall()[0][0]

            sql = "INSERT INTO dean_notification (notification, received_from, date, person_id) VALUES (%s, %s, %s, %s)"
            val = (notification, received_from, now, dean_id)
            db.execute(sql, val)
            mydb.commit()

            while True:
                print()
                back = input("Course Has Been Removed. Press (R) To Remove Another Course:\n"
                             "                         Press (M) To Return To Dean Menu: ").lower()
                if back == "r":
                    remove_course()
                    break
                elif back == "m":
                    DeanMenu(None)
                    break
        elif confirmation == "no":
            DeanMenu(None)


# ADD MAJOR
def add_new_major():
    clear()
    print("ADD MAJOR")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    while True:
        print()
        new_major_name = capitalize(input("Enter The Name Of The Major: "))
        # CHECKING IF C WAS ENTERED
        if len(new_major_name) == 1:
            new_major_name = new_major_name.lower()
        if new_major_name == "c":
            dean_admin_options()
        if new_major_name != '':
            break
    while True:
        print()
        new_major_description = input("Enter The Description For The Major: ")
        # CHECKING IF C WAS ENTERED
        if len(new_major_description) == 1:
            new_major_description = new_major_name.lower()
        if new_major_description == "c":
            dean_admin_options()
        if new_major_description != '':
            break
    while True:
        print()
        minimum_eng_level = input("Enter The Minimum English Requirement: ").upper()
        # CHECKING IF C WAS ENTERED
        if len(minimum_eng_level) == 1:
            minimum_eng_level = minimum_eng_level.lower()
        if minimum_eng_level == "c":
            dean_admin_options()
        # VALIDATING COURSE
        if not checkCourse(minimum_eng_level):
            print("Invalid Course")
        if "ENG" not in minimum_eng_level:
            print("Course Must Be 'ENG'")
        if checkCourse(minimum_eng_level) and "ENG" in minimum_eng_level:
            break
    while True:
        print()
        minimum_math_level = input("Enter The Minimum Math Level: ").upper()
        # CHECKING IF C WAS ENTERED
        if len(minimum_math_level) == 1:
            minimum_math_level = minimum_math_level.lower()
        if minimum_math_level == "c":
            dean_admin_options()
        # VALIDATING COURSE
        if not checkCourse(minimum_math_level):
            print("Invalid Course")
        if "MATH" not in minimum_math_level:
            print("Course Must Be 'MATH'")
        if checkCourse(minimum_math_level):
            break
    while True:
        print()
        major_requirements = input("Enter The Major Requirements: ").upper()
        # CHECKING IF C WAS ENTERED
        if len(major_requirements) == 1:
            major_requirements = major_requirements.lower()
        if major_requirements == "c":
            dean_admin_options()
        # VALIDATING COURSE
        if not checkCourse(major_requirements):
            print("One Of The Courses Entered Is Invalid")
        if checkCourse(major_requirements):
            break
    while True:
        print()
        confirmation = input("Are You Sure You Want To Add This Major? ")
        if confirmation == "yes" or confirmation == "no":
            break
    if confirmation == "yes":
        sql = "INSERT INTO Major (name, description, minimum_eng_level, minimum_math_level, major_requirements) VALUES (%s, %s, %s, %s, %s)"
        val = (new_major_name, new_major_description, minimum_eng_level, minimum_math_level, major_requirements)
        db.execute(sql, val)
        mydb.commit()

        # SET UP NOTIFICATION
        notification = f"{new_major_name} Has Been Added"
        received_from = f"Dean ({dean_name})"
        sql = "SELECT id FROM Dean WHERE name = %s"
        val = (dean_name,)
        db.execute(sql, val)
        dean_id = db.fetchall()[0][0]

        sql = "INSERT INTO dean_notification (notification, received_from, date, person_id) VALUES (%s, %s, %s, %s)"
        val = (notification, received_from, now, dean_id)
        db.execute(sql, val)
        mydb.commit()

        while True:
            print()
            back = input("Major Added. Press (A) To Add More Majors:\n"
                         "             Press (M) To Return To Admin Options: ").lower()
            if back == "a":
                add_new_major()
            elif back == "m":
                dean_admin_options()

    elif confirmation == "no":
        dean_admin_options()
# REMOVE MAJOR
def remove_major():
    clear()
    print("REMOVE MAJOR")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    while True:
        print()
        major_to_remove = capitalize(input("Enter Major To Remove: "))
        if len(major_to_remove) == 1:
            major_to_remove = major_to_remove.lower()
        if major_to_remove == "c":
            dean_admin_options()
        # VALIDATING MAJOR ENTERED
        if not checkMajor(major_to_remove):
            print("Invalid Major")
        if checkMajor(major_to_remove):
            break

    while True:
        print()
        reason = input("Why Is This Major Being Removed? ")
        if reason != '':
            break
    while True:
        print()
        confirmation = input(f"CONFIRMATION: Are You Sure You Want To Remove {major_to_remove}?" )
        if confirmation == "yes" or confirmation == "no":
            break
    if confirmation == "yes":
        sql = "DELETE FROM Major WHERE name = %s"
        val = (major_to_remove, )
        db.execute(sql, val)
        mydb.commit()

        # SET UP NOTIFICATION
        notification = f"{major_to_remove} Has Been Removed Because: {reason}"
        received_from = f"Dean ({dean_name})"
        sql = "SELECT id FROM Dean WHERE name = %s"
        val = (dean_name,)
        db.execute(sql, val)
        dean_id = db.fetchall()[0][0]

        sql = "INSERT INTO dean_notification (notification, received_from, date, person_id) VALUES (%s, %s, %s, %s)"
        val = (notification, received_from, now, dean_id)
        db.execute(sql, val)
        mydb.commit()

        while True:
            print()
            back = input("Major Removed. Press (R) To Remove More Majors:\n"
                         "               Press (A) To Return To Admin Options: ").lower()
            if back == "r":
                remove_major()
            elif back == "a":
                dean_admin_options()
    elif confirmation == "no":
        view_all_majors("Dean")

# MODIFY MAJOR
def dean_modify_major(major_name, major_details):
    print()
    print("-------" + "-" * len(major_name))
    print(f"MODIFY {major_name.upper()}")
    print("-------" + "-" * len(major_name))
    print()
    print("OPTIONS")
    print()
    print("1 -> Change Description")
    print("2 -> Change Minimum Math Level")
    print("3 -> Change Minimum English Level")
    print("4 -> Change Major Requirements")
    while True:
        print()
        dean_choice = input("Choose An Option: ")
        if dean_choice == "1":
            change_major_description(major_name, major_details)
            break
        elif dean_choice == "2":
            change_minimum_math_level(major_name, major_details)
            break
        elif dean_choice == "3":
            change_minimum_eng_level(major_name, major_details)
            break
        elif dean_choice == "4":
            change_major_requirements(major_name, major_details)
            break
        elif dean_choice == "c":
            view_all_majors("Dean")
            break
        elif dean_choice == "a":
            dean_admin_options()
            break

# CHANGE MAJOR DESCRIPTION
def change_major_description(major_name, major_details):
    clear()
    print("-------" + "-" * len(major_name) + "-----------")
    print(f"CHANGE {major_name.upper()} DESCRIPTION")
    print("-------" + "-" * len(major_name) + "-----------")
    print()
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()

    sql = "SELECT description FROM Major WHERE name = %s"
    val = (major_name, )
    db.execute(sql, val)
    current_description = db.fetchall()[0][0]

    print(f"Current Description: {current_description}")
    while True:
        print()
        new_description = input("Enter New Description: ")
        if new_description != '':
            break
    # CHECKING IF C WAS ENTERED
    if len(new_description) == 1:
        new_description = new_description.lower()
    if new_description == "c":
        view_all_majors("Dean")
    while True:
        confirmation = input("CONFIRMATION: Are You Sure You Want To Change The Description? ")
        if confirmation != '' and (confirmation == "yes" or confirmation == "no"):
            break
    if confirmation == "yes":
        sql = "UPDATE Major SET description = %s WHERE name = %s"
        val = (new_description, major_name)
        db.execute(sql, val)
        mydb.commit()

        # SET UP NOTIFICATION
        notification = f"{major_name} Description Has Been Changed"
        received_from = f"Dean ({dean_name})"
        sql = "SELECT id FROM Dean WHERE name = %s"
        val = (dean_name,)
        db.execute(sql, val)
        dean_id = db.fetchall()[0][0]

        sql = "INSERT INTO dean_notification (notification, received_from, date, person_id) VALUES (%s, %s, %s, %s)"
        val = (notification, received_from, now, dean_id)
        db.execute(sql, val)
        mydb.commit()

        while True:
            print()
            back = input("Description Updated: Press (V) To View More Majors:\n"
                         "                     Press (A) To Return To Admin Options").lower()
            if back == "v":
                view_all_majors("Dean")
            elif back == "a":
                dean_admin_options()

    elif confirmation == "no":
        view_all_majors("Dean")
# CHANGE MINIMUM MATH LEVEL
def change_minimum_math_level(major_name, major_details):
    clear()
    print("-------" + "-" * len(major_name) + "-------")
    print(f"CHANGE {major_name.upper()} DETAILS")
    print("-------" + "-" * len(major_name) + "-------")
    print()
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    minimum_math_level = major_details[1]

    print(f"MINIMUM MATH LEVEL: {minimum_math_level}")

    while True:
        print()
        new_minimum_math_level = input("Enter New Minimum Math Level: ").upper()
        # CHECKING IF C WAS ENTERED
        if len(new_minimum_math_level) == 1:
            new_minimum_math_level = new_minimum_math_level.lower()
        if new_minimum_math_level == "c":
            view_all_majors("Dean")
        # VALIDATING COURSE ENTERED
        if not checkCourse(new_minimum_math_level):
            print("Invalid Math Course. Try Again")
        if checkCourse(new_minimum_math_level):
            break



    while True:
        confirmation = input("CONFIRMATION: Are You Sure You Want To Change The Minimum Math Level? ")
        if confirmation == "yes" or confirmation == "no":
            break
    if confirmation == "yes":
        sql = "UPDATE Major SET minimum_math_level = %s WHERE name = %s"
        val = (new_minimum_math_level, major_name)
        db.execute(sql, val)
        mydb.commit()

        # SET UP NOTIFICATION
        notification = f"{major_name} Minimum Math Level Has Been Changed From {minimum_math_level} To {new_minimum_math_level}"
        received_from = f"Dean ({dean_name})"
        sql = "SELECT id FROM Dean WHERE name = %s"
        val = (dean_name,)
        db.execute(sql, val)
        dean_id = db.fetchall()[0][0]

        sql = "INSERT INTO dean_notification (notification, received_from, date, person_id) VALUES (%s, %s, %s, %s)"
        val = (notification, received_from, now, dean_id)
        db.execute(sql, val)
        mydb.commit()

        while True:
            print()
            back = input("Minimum Math Level Changed: Press (V) To View More Majors:\n"
                         "                            Press (A) To Return To Admin Options").lower()
            if back == "v":
                view_all_majors("Dean")
            elif back == "a":
                dean_admin_options()


    elif confirmation == "no":
        view_all_majors("Dean")
# CHANGE MINIMUM ENG LEVEL
def change_minimum_eng_level(major_name, major_details):
    clear()
    print("--------" + "-" * len(major_name) + "-------")
    print(f"CHANGE {major_name.upper()} DETAILS")
    print("--------" + "-" * len(major_name) + "-------")
    print()
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    minimum_english_level = major_details[0]

    print(f"MINIMUM ENGLISH LEVEL: {minimum_english_level}")

    while True:
        print()
        new_minimum_english_level = input("Enter New Minimum English Level: ").upper()
        # CHECKING IF C WAS ENTERED
        if len(new_minimum_english_level) == 1:
            new_minimum_english_level = new_minimum_english_level.lower()
        if new_minimum_english_level == "c":
            view_all_majors("Dean")
        # VALIDATING COURSE ENTERED
        if not checkCourse(new_minimum_english_level):
            print("Invalid English Course. Try Again")
        if checkCourse(new_minimum_english_level):
            break



    while True:
        confirmation = input("CONFIRMATION: Are You Sure You Want To Change The Minimum English Level? ")
        if confirmation == "yes" or confirmation == "no":
            break
    if confirmation == "yes":
        sql = "UPDATE Major SET minimum_eng_level = %s WHERE name = %s"
        val = (new_minimum_english_level, major_name)
        db.execute(sql, val)
        mydb.commit()

        # SET UP NOTIFICATION
        notification = f"{major_name} Minimum English Level Has Been Changed From {minimum_english_level} To {new_minimum_english_level}"
        received_from = f"Dean ({dean_name})"
        sql = "SELECT id FROM Dean WHERE name = %s"
        val = (dean_name,)
        db.execute(sql, val)
        dean_id = db.fetchall()[0][0]

        sql = "INSERT INTO dean_notification (notification, received_from, date, person_id) VALUES (%s, %s, %s, %s)"
        val = (notification, received_from, now, dean_id)
        db.execute(sql, val)
        mydb.commit()

        while True:
            print()
            back = input("Minimum English Level Changed: Press (V) To View More Majors:\n"
                         "                               Press (A) To Return To Admin Options").lower()
            if back == "v":
                view_all_majors("Dean")
            elif back == "a":
                dean_admin_options()


    elif confirmation == "no":
        view_all_majors("Dean")
# CHANGE MAJOR REQUIREMENTS
def change_major_requirements(major_name, major_details):
    clear()
    print("--------" + "-" * len(major_name) + "-------")
    print(f"CHANGE {major_name.upper()} DETAILS")
    print("--------" + "-" * len(major_name) + "-------")
    print()
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    if major_details[2] != None:
        major_requirements = major_details[2].split()
    else:
        major_requirements = "Not Assigned"

    print(f"MAJOR REQUIREMENTS: {major_requirements}")
    while True:
        print()
        new_major_requirements = input("New Major Requirements: ").upper()
        if new_major_requirements.lower() == "c":
            view_all_majors("Dean")
            break
        if not checkCourse(new_major_requirements):
            print("One Of The Courses Entered Is Invalid. Please Check The Spelling Of All Courses Entered")
        if checkCourse(new_major_requirements):
            break
    # CHECKING IF C WAS ENTERED
    if len(new_major_requirements) == 1:
        new_major_requirements = new_major_requirements.lower()
    if new_major_requirements == "c":
        view_all_majors("Dean")

    while True:
        confirmation = input("CONFIRMATION: Are Your Sure You Want To Change The Major Requirements? ")
        if confirmation == "yes" or confirmation == "no":
            break
    if confirmation == "yes":
        sql = "UPDATE Major SET major_requirements = %s WHERE name = %s"
        val = (new_major_requirements, major_name)
        db.execute(sql, val)
        mydb.commit()

        # SET UP NOTIFICATION
        notification = f"{major_name} Major Requirements Have Been Changed To: {new_major_requirements.split()} "
        received_from = f"Dean ({dean_name})"
        sql = "SELECT id FROM Dean WHERE name = %s"
        val = (dean_name,)
        db.execute(sql, val)
        dean_id = db.fetchall()[0][0]

        sql = "INSERT INTO dean_notification (notification, received_from, date, person_id) VALUES (%s, %s, %s, %s)"
        val = (notification, received_from, now, dean_id)
        db.execute(sql, val)
        mydb.commit()

        while True:
            print()
            back = input("Major Requirements Changed: Press (V) To View More Majors:\n"
                         "                            Press (A) To Return To Admin Options").lower()
            if back == "v":
                view_all_majors("Dean")
            elif back == "a":
                dean_admin_options()

    elif confirmation == "no":
        dean_admin_options()


# DEAN CHANGE PASSWORD
def change_dean_password(dean_name, dean_id):
    clear()
    print("CHANGE DEAN PASSWORD")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    while True:
        print()
        pre_password = getpass("Enter Your Previous Password: ")
        if pre_password != dean_password:
            print("Passwords Don't Match")
        else:
            break

    while True:
        new_pwd = getpass("Enter Your New Password: ")
        if new_pwd != '':
            break

    # CHECKING IF C WAS ENTERED
    if len(new_pwd) == 1:
        new_pwd = new_pwd.lower()
    if new_pwd == "c":
        DeanMenu(dean_name)
    new_pwd = sanitize_password(new_pwd, dean_name)

    while True:
        confirm_new_pwd = getpass("Confirm Your Password: ")
        if confirm_new_pwd != '':
            break

    if new_pwd != confirm_new_pwd:
        confirm_new_pwd = confirm_password_error(dean_name)

    confirm_new_pwd = hash_password(confirm_new_pwd)

    # CHANGE PASSWORD
    sql = "UPDATE Dean SET password = %s WHERE id = %s"
    val = (confirm_new_pwd, dean_id)

    db.execute(sql, val)
    mydb.commit()

    while True:
        print()
        back = input("Your Password Has Been Changed. Press (B) To Go Back: ").lower()
        if back == "b":
            DeanMenu(dean_name)








# CHECK MAJOR
def checkMajor(major_name):
    db.execute("SELECT name FROM Major")
    all_majors = db.fetchall()

    all_majors = [all_majors[i][0] for i in range(len(all_majors))]

    return major_name in all_majors








# PROFESSOR MENU
def ProfessorMenu(name):
    clear()
    update_student_grades()
    # GETTING INBOX COUNT
    try:
        Prof = Professor(prof_name.split()[0], prof_name.split()[1], None, None, None, None, None)
    except:
        Prof = Professor(name.split()[0], name.split()[1], None, None, None, None, None)

    sql = "SELECT COUNT(*) FROM professor_notification WHERE prof_id = %s"
    val = (Prof.getID(), )
    db.execute(sql, val)
    inbox_count = db.fetchall()[0][0]
    print("PROFESSOR MENU")
    if name != None:
        print(f"Welcome {name}")
    print(now)
    print("-----------------------")
    print("Press (L) To Log Out")
    print("Press (S) To Send Notification")
    print("Press (I) To Open Inbox")
    print("-----------------------")
    print()
    print(f"INBOX: {inbox_count}")
    print()
    print("AVAILABLE OPTIONS")
    print()
    print("1 - View Profile")
    print("2 - View All Courses")
    print("3 - View Courses Taught")
    print("4 - Create Assignment")
    print("5 - Issue Assignment")
    print()
    while True:
        prof_choice = input("Choose An Option: ").lower()
        if prof_choice != '':
            break
    if prof_choice == "l":
        login()
    elif prof_choice == "i":
        professor_inbox()
    elif prof_choice == "s":
        prof_send_notification()
    elif prof_choice == "1":
        view_prof_profile()
    elif prof_choice == "2":
        view_all_courses_prof()
    elif prof_choice == "3":
        view_courses_taught()
    elif prof_choice == "4":
        prof_create_assignment()
    elif prof_choice == "5":
        prof_issue_assignment()
    else:
        ProfessorMenu(None)
# VIEW PROFESSOR PROFILE
def view_prof_profile():
    clear()
    # CHECKING IF THE PROFESSOR EXIST
    sql = "SELECT * FROM Professor WHERE name = %s"
    val = (prof_name,)
    db.execute(sql, val)
    result = db.fetchall()

    try:
        Prof = Professor(result[0][1].split()[0], result[0][1].split()[1], result[0][2], result[0][4], result[0][5], result[0][6], result[0][7])
    except IndexError:
        print("-----")
        print("ERROR")
        print("-----")
        print("An Error Occurred. The Program Will End In A Few Seconds.. Please Restart.")
        from time import sleep
        sleep(2.5)
        exit()

    # AUTO FIT HEADINGS
    addressLen = len(Prof.getAddress()) + len("Address: ")
    coursesLen = Prof.getLenCoursesTaught()
    max_len_of_attributes = max([addressLen, coursesLen])

    # print(f"Len Address: {addressLen}")
    # print(f"Len Courses: {coursesLen}")

    # print("<" * (max_len_of_attributes // 2), "PROFILE", ">" * (max_len_of_attributes // 2 + 1))

    print("<" * (max_len_of_attributes // 2 - 5) + " PROFILE " + ">" * (max_len_of_attributes // 2 - 4))

    print("-" * max_len_of_attributes)
    print()
    print(f"Id: {Prof.getID()}")
    print(f"Name: {Prof.getFullName()}")
    print(f"Address: {Prof.getAddress()}")
    print(f"Email: {Prof.getEmail()}")
    print(f"Age: {Prof.getAge()}")
    print(f"Phone Number: {Prof.getPhoneNumber()}")
    print(f"Salary: {Prof.getSalary()}")
    print(f"Courses Taught: {Prof.getCoursesTaught()}")
    print()
    print("-" * max_len_of_attributes)
    print()
    while True:
        back = input("Press (C) To Change Your Password:\nPress (M) To Return To Professor Menu: ").lower()
        if back == "m":
            ProfessorMenu(Prof.getFullName())
        elif back == "c":
            change_professor_password(prof_name, Prof.getID())


# VIEW ALL COURSES
def view_all_courses_prof(came_from=None):
    clear()
    print("----------------")
    print("VIEW ALL COURSES")
    print("----------------")
    print()
    all_courses = Course.getAll_Courses()
    db.execute("SELECT description FROM Course")

    description = db.fetchall()

    for i, course in enumerate(all_courses):
        print(f"{all_courses[i][0]} - {description[i][0][:indexOf(description[i][0], ':')]}")
        print()

    while True:
        prof_choice = input("Press (S) To Select A Course:\nPress (M) To Return To Professor Menu: ").lower()
        if prof_choice == "s":
            search_for_course_prof()
        elif prof_choice == "m":
            ProfessorMenu(None)

# SEARCH FOR COURSE
def search_for_course_prof(came_from=None):
    while True:
        print()
        course_name = input("Enter The Name Of The Course: ").upper()
        if course_name != '':
            break
    # CHECK IF COURSE ENTERED IS IN THE LIST
    sql = "SELECT name FROM Course WHERE name = %s"
    val = (course_name,)
    db.execute(sql, val)
    result = db.fetchall()
    if len(result) == 0:
        course_not_found("Prof Search For Course")

    # COURSE WAS FOUND
    select_course_prof(course_name)

# VIEW COURSES TAUGHT
def view_courses_taught():
    clear()
    print("-----------------")
    print("COURSES YOU TEACH")
    print("-----------------")
    print()
    sql = "SELECT CoursesTaught From Professor WHERE name =%s"
    val = (prof_name,)
    db.execute(sql, val)
    courses_taught = db.fetchall()[0][0]
    print(f"Courses You Currently Teach: {courses_taught.split()}")

    while True:
        print()
        prof_option = input("Press (U) To Update The Courses You Teach:\nPress (M) To Return To Professor Menu: ").lower()
        if prof_option == "u":
            break
        elif prof_option == "m":
            ProfessorMenu(None)

    while True:
        print()
        new_courses = input("Enter The New Courses You Teach: ").upper()
        if new_courses != '':
            break

    # UPDATE COURSES TAUGHT
    new_courses = sanitize_courses(new_courses, "Prof_Change_Courses_Taught")

    while True:
        confirmation = input(f"CONFIRMATION: Are You Sure You Want To Change The Courses You Teach To: {new_courses}? ")
        if confirmation != '' and (confirmation == "yes" or confirmation == "no"):
            break
    if confirmation == "yes":
        sql = "UPDATE Professor SET CoursesTaught = %s WHERE name = %s"
        val = (new_courses, prof_name)
        db.execute(sql, val)
        mydb.commit()

        # SET UP NOTIFICATION
        Prof = Professor(prof_name.split()[0], prof_name.split()[1], None, None, None, None, None)
        sql = "INSERT INTO dean_notification (notification, received_from, date, person_id) VALUES (%s, %s, %s, %s)"
        val = (f"{prof_name} Changed Their Courses Teached To: {new_courses}", "Professor", now, Prof.getID())
        db.execute(sql, val)
        mydb.commit()

        while True:
            print()
            back = input("Courses Taught Successfully Updated. Press (M) To Return To Professor Menu: ").lower()
            if back == "m":
                ProfessorMenu(None)
    else:
        ProfessorMenu(None)

# COURSE NOT FOUND
def course_not_found(came_from=None, argv=None):

    print()
    while True:
        print()
        if came_from != "Dean Search For Course":
            error = input("That Course Was Not Found. Press (T) To Try Again:\n"
                          "                           Press (B) To Go Back: ").lower()
        else:
            error = input("That Course Was Not Found. Press (T) To Try Again:\n"
                          "                           Press (A) To Add Course:\n"
                          "                           Press (B) To Go Back: ").lower()
        if error == "t":
            if came_from == "Edit_Course":
                edit_course()
            elif came_from == "Student Search For Course":
                search_for_course_stu()
            elif came_from == "Dean Search For Course":
                search_for_course_dean()
            elif came_from == "Prof Search For Course":
                search_for_course_prof()
            elif came_from == "Dean Remove Course":
                remove_course()
        elif error == "b":
            if came_from == "Edit_Course":
                DeanMenu(None)
            elif came_from == "Student Search For Course":
                StudentMenu(None)
            elif came_from == "Dean Search For Course":
                dean_admin_options()
            elif came_from == "Prof Search For Course":
                ProfessorMenu(None)
            elif came_from == "Dean Remove Course":
                dean_admin_options()
        elif error == "a" and came_from == "Dean Search For Course":
            add_new_course()

# SELECT COURSE
def select_course_prof(course_name):
    clear()
    course = Course(course_name)

    print("-" * len(course_name) + "-------")
    print(f"{course_name.upper()} COURSE")
    print("-" * len(course_name) + "-------")
    print()
    print("<<<<<<<<<<<<<<<< DESCRIPTION >>>>>>>>>>>>>>>>")
    print()
    print(course.getDescription())
    print()

    try:
        print("-" * len(course) + "------------------")
        print(f"COURSE CANCELLED: {course.isCourseCancelled()}")
        print("-" * len(course) + "------------------")
        print()
    except:
        print("An Error Occurred. Restart Application")
        sleep(1)
        exit()
    # GET THE NAMES OF THE STUDENTS ENROLLED
    names = course.getStudentNamesInCourse()
    if names != None:
        names = names.split()
        students_in_course = [names[i+i] + " " + names[i+i+1] for i in range(len(names) // 2)]
    else:
        students_in_course = None

    print(f"Students In Course: {students_in_course}")
    # IF NO STUDENTS ARE IN THE COURSE THEN THE studentsCount IS NOT SHOWN
    if course.getStudentNamesInCourse() != None:
        # GET THE STUDENT COUNT
        print(f"Number Of Students Enrolled: {course.getStudentCountInCourse()}")
        # COMPUTE THE CLASS AVERAGE
        average = get_class_average(course_name)
        print(f"Class Average: {average}%")
        print()

    if course.getStudentCountInCourse() != 0:
        while True:
            print("Press (S) To Search Again:")
            print("Press (A) To Add This Course To The List Of Courses You Teach:")
            print("Press (D) To Drop A Student From This Course:")
            print("Press (V) View Student's Grade:")
            back = input("Press (M) To Return To Professor Menu: ").lower()
            if back == "s":
                search_for_course_prof("Search")
            elif back == "a":
                add_course_to_list_of_courses_teached(course_name)
            elif back == "d":
                if not profCanDropStudent(prof_name, course_name):
                    while True:
                        print()
                        error = input("You Are Not Currently Teaching This Course So You Are Unable To Drop This Student. Press (B) To Go Back: ").lower()
                        if error == "b":
                            select_course_prof(course_name)

                drop_student_from_course(course_name)
            elif back == "v":
                view_student_grade_for_course(course_name)
            elif back == "m":
                ProfessorMenu(prof_name)

    # GENERIC
    while True:
        print()
        print("Press (S) To Search Again:")
        print("Press (A) To Add This Course To The List Of Courses You Teach:")
        back = input("Press (M) To Return To Professor Menu: ").lower()
        if back == "s":
            search_for_course_prof("Search")

        elif back == "a":
            add_course_to_list_of_courses_teached(course_name)

        elif back == "m":
            ProfessorMenu(None)


def profCanDropStudent(prof_name, course_name):
    sql = "SELECT CoursesTaught FROM Professor WHERE name = %s"
    val = (prof_name, )
    db.execute(sql, val)
    results = db.fetchall()
    if len(results) == 0:
        return False
    results = results[0][0].split()
    return course_name in results


def get_class_average(course_name):
    sql = "SELECT * FROM grade_book WHERE course_name = %s"
    val = (course_name,)
    db.execute(sql, val)
    results = db.fetchall()
    if len(results) == 0:
        return 0


    grade_book = {}

    for i in range(len(results)):
        sql = "SELECT name FROM Student WHERE id = %s"
        val = (results[i][1],)
        db.execute(sql, val)
        all_names = db.fetchall()[0][0]
        # ADD STUDENT NAMES AND THEIR CORRESPONDING GRADES FROM THE GRADE BOOK
        grade_book.update({all_names: results[i][3:]})

    student_grade_book_averages = []
    for grades in grade_book:
        grades_to_average = [grade_book[grades][i] for i in range(len(grade_book[grades])) if grade_book[grades][i] != None]
        student_grade_book_averages.append(compute_average(grades_to_average))

    class_average = round(sum(student_grade_book_averages) / len(student_grade_book_averages))

    return class_average


def compute_average(items: list):
    sum = 0
    for item in items:
        sum += int(item.replace('%', ''))
    average = round(sum / len(items))

    return average
# ADD COURSE TO LIST OF COURSES TEACHED
def add_course_to_list_of_courses_teached(course_name):
    clear()
    print("--------------------------------")
    print("ADD TO LIST OF COURSES YOU TEACH")
    print("--------------------------------")
    print()
    # GET ALL THE COURSES CURRENTLY TEACHED
    sql = "SELECT CoursesTaught From Professor WHERE name =%s"
    val = (prof_name, )
    db.execute(sql, val)
    courses_taught = db.fetchall()[0][0]
    print(f"Courses You Currently Teach: {courses_taught.split()}")

    # CHECK IF THE PROFESSOR IS ALREADY TEACHING THE COURSE SELECTED
    for course in courses_taught.split():
        if course_name == course:
            print()
            while True:
                print()
                back = input("You Are Already Teaching This Course. Press (S) To Return To All Courses:\n"
                             "                                      Press (M) To Return To Professor Menu: ").lower()
                if back == "s":
                    view_all_courses_prof()
                elif back == "m":
                    ProfessorMenu(None)

    while True:
        print()
        confirmation = input(f"CONFIRMATION: Are You Sure You Want To Add {course_name} To The List Of Courses You Teach? ")
        if confirmation != '' and (confirmation == "yes" or confirmation == "no"):
            break
    if confirmation == "yes":
        new_courses_to_add = courses_taught + " " + course_name
        sql = "UPDATE Professor SET CoursesTaught = %s WHERE name = %s"
        val = (new_courses_to_add, prof_name)
        db.execute(sql, val)
        mydb.commit()

        # SET UP NOTIFICATION
        Prof = Professor(prof_name.split()[0], prof_name.split()[1], None, None, None, None, None)
        sql = "INSERT INTO dean_notification (notification, received_from, date, person_id) VALUES (%s, %s, %s, %s)"
        val = (f"{prof_name} Added {course_name} To Their Schedule", "Professor", now, Prof.getID())
        db.execute(sql, val)
        mydb.commit()

        while True:
            print()
            back = input("Courses Successfully Added. Press (S) To Return To All Courses:\n"
                         "                            Press (M) To Return To Professor Menu: ").lower()
            if back == "s":
                view_all_courses_prof()
            elif back == "m":
                ProfessorMenu(None)
    else:
        ProfessorMenu(None)
# DROP STUDENT FROM COURSE
def drop_student_from_course(course_name):
    clear()
    print("DROP STUDENT FROM COURSE ")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    while True:
        name_to_drop = input("Enter The Name Of The Student: ")
        if name_to_drop != '':
            break
    # CHECKING IF C WAS ENTERED
    if len(name_to_drop) == 1:
        name_to_drop = name_to_drop.lower()
    if name_to_drop == "c":
        select_course_prof(course_name)
    # CHECKING IF THE STUDENT WAS FOUND
    sql = "SELECT * FROM Student WHERE name = %s"
    val = (name_to_drop, )
    db.execute(sql, val)
    result = db.fetchall()
    if len(result) == 0:
        no_person_found("Drop Student", "Prof")

    # CHECKING IF C WAS ENTERED
    if len(name_to_drop) == 1:
        name_to_drop = name_to_drop.lower()
    if name_to_drop == "c":
        ProfessorMenu(None)

    while True:
        reason = input("Why Is This Student Being Dropped? ")
        if reason != '':
            break

    # CONFIRMATION
    while True:
        confirmation = input(f"CONFIRMATION: Are You Sure You Want To Drop {name_to_drop} From {course_name}? ").lower()
        if confirmation != '' and (confirmation == "yes" or confirmation == "no"):
            break

    if confirmation == "yes":
        # DROP STUDENT FROM COURSE
        sql = "SELECT studentsInCourse FROM Course WHERE name = %s"
        val = (course_name,)
        db.execute(sql, val)
        students_in_course = db.fetchall()[0][0]

        tmp_students_in_course = students_in_course.split()
        new_names_to_add_to_database = ""

        for i in range(len(tmp_students_in_course) // 2):
            if tmp_students_in_course[i+i] + " " + tmp_students_in_course[i+i+1] != name_to_drop:
                new_names_to_add_to_database += tmp_students_in_course[i+i] + " " + tmp_students_in_course[i+i+1]
                new_names_to_add_to_database += " "

        new_names_to_add_to_database = new_names_to_add_to_database.rstrip()

        sql = "UPDATE Course Set studentsInCourse = %s WHERE name = %s"
        val = (new_names_to_add_to_database, course_name)
        db.execute(sql, val)
        mydb.commit()

        # REMOVE COURSE FROM LIST OF COURSES ENROLLED FOR THE STUDENT
        sql = "SELECT CoursesEnrolledIn FROM Student WHERE name = %s"
        val = (name_to_drop, )
        db.execute(sql, val)
        courses_enrolled_in = db.fetchall()[0][0]

        new_courses_to_add_to_database = courses_enrolled_in.replace(course_name, '').strip()
        sql = "UPDATE Student SET CoursesEnrolledIn = %s WHERE name = %s"
        val = (new_courses_to_add_to_database, name_to_drop)
        db.execute(sql, val)
        mydb.commit()


        # SETTING UP NOTIFICATION
        notification  = f"You Have Been Dropped From {course_name.upper()} For The Reason: {reason}"
        received_from = "Professor"
        date          = now
        stu_id        = result[0][0]

        # SEND NOTIFICATION TO STUDENT
        sql = "INSERT INTO student_notification (notification, received_from, date, stu_id) VALUES (%s, %s, %s, %s)"
        val = (notification, received_from, date, stu_id)
        db.execute(sql, val)
        mydb.commit()

        # SEND NOTIFICATION TO DEAN
        Prof = Professor(prof_name.split()[0], prof_name.split()[1], None, None, None, None, None)
        sql = "INSERT INTO dean_notification (notification, received_from, date, person_id) VALUES (%s, %s, %s, %s)"
        val = (f"{prof_name} Dropped: {name_to_drop} For: {reason}", "Professor", now, Prof.getID())
        db.execute(sql, val)
        mydb.commit()

        update_course_database()
        print()
        while True:
            back = input(f"You Have Dropped {name_to_drop} From {course_name} Press (M) To Return To Professor Menu: ").lower()
            if back == "m":
                ProfessorMenu(None)

    else:
        view_all_courses_prof()
# VIEW STUDENT GRADE FOR COURSE
def view_student_grade_for_course(course_name, came_from=None):
    clear()
    print("-------------------")
    print("VIEW STUDENT GRADES")
    print("-------------------")
    print()
    sql = "SELECT * FROM grade_book WHERE course_name = %s"
    val = (course_name,)
    db.execute(sql, val)
    results = db.fetchall()

    grade_book = {}

    for i in range(len(results)):
        sql = "SELECT name FROM Student WHERE id = %s"
        val = (results[i][1],)
        db.execute(sql, val)
        all_names = db.fetchall()[0][0]

        grade_book.update({all_names: results[i][3:]})

    print()
    for grade in grade_book:
        print(f"{grade}: |GRADE-1|GRADE-2|GRADE-3|GRADE-4|GRADE-5|AVG|")
        # CHANGE THE TUPLE OF GRADES TO A LIST
        grades  = [grade_book[grade][i] for i in range(len(grade_book[grade]))]
        stu_avg = round(sum([int(grade.replace('%','')) for grade in grades if grade != None]) / len([grade for grade in grades if grade != None]))
        print(f" " * (len(grade) +2)+ f"{grades} {stu_avg}%")
        print()

    while True:
        print()
        if came_from == None:
            menu_to_return = "Professor Menu"
        elif came_from == "Dean":
            menu_to_return = "Dean Menu"
        back = input(f"Press (B) To Go Back:\nPress (M) To Return To {menu_to_return}: ").lower()
        if back == "b":
            if came_from == "Dean":
                view_students_enrolled_in_course_dean(course_name)
            select_course_prof(course_name)
        elif back == "m":
            if came_from == "Dean":
                DeanMenu(None)
            ProfessorMenu(None)

# CHANGE PROFESSOR PASSWORD
def change_professor_password(prof_name, prof_id):
    clear()
    print("CHANGE PROFESSOR PASSWORD")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    while True:
        print()
        pre_password = getpass("Enter Your Previous Password: ")
        if pre_password != prof_password:
            print("Passwords Don't Match")
        else:
            break

    while True:
        new_pwd = getpass("Enter Your New Password: ")
        if new_pwd != '':
            break

    # CHECKING IF C WAS ENTERED
    if len(new_pwd) == 1:
        new_pwd = new_pwd.lower()
    if new_pwd == "c":
        ProfessorMenu(prof_name)
    new_pwd = sanitize_password(new_pwd, prof_name)

    while True:
        confirm_new_pwd = getpass("Confirm Your Password: ")
        if confirm_new_pwd != '':
            break

    if new_pwd != confirm_new_pwd:
        confirm_new_pwd = confirm_password_error(prof_name)

    confirm_new_pwd = hash_password(confirm_new_pwd)

    # CHANGE PASSWORD
    sql = "UPDATE Professor SET password = %s WHERE id = %s"
    val = (confirm_new_pwd, prof_id)

    db.execute(sql, val)
    mydb.commit()

    print()
    while True:
        back = input("Your Password Has Been Changed. Press (B) To Go Back: ").lower()
        if back == "b":
            ProfessorMenu(prof_name)

# PROF SEND NOTIFICATION
def prof_send_notification():
    clear()
    print("SEND NOTIFICATION")
    print(now)
    print("---------------------------------")
    print("Press (A) To Send An Announcement")
    print("Press (C) To Cancel")
    print("---------------------------------")
    print()
    while True:
        print()
        to = input("To (Dean, Professor, Or Student): ").capitalize()
        # CHECKING IF C WAS ENTERED
        if to.lower() == "c":
            ProfessorMenu(None)

        # CHECKING IF A WAS ENTERED
        if to.lower() == "a":
            prof_send_announcement()

        if to != '' and (to == "Student" or to == "Professor" or to == "Dean"):
            break
        if to == '' or (to != "Student" or to != "Professor" or to != "Dean"):
            print("Messages Can Only Be Sent To: Dean, Professor Or Student")


    # STUDENT
    if to == "Student":
        while True:
            print()
            stu_name = capitalize(input("Enter The Name Of The Student: "))
            if stu_name.lower() == "c":
                ProfessorMenu(None)
            if stu_name != '':
                break
        sql = "SELECT id FROM Student WHERE name = %s"
        val = (stu_name, )
        db.execute(sql, val)
        stu_id = db.fetchall()
        if len(stu_id) == 0:
            no_person_found("Notification", "Prof", "Send_To_Stu")
        stu_id = stu_id[0][0]

        while True:
            message = input("Message: ")
            if message != '':
                break

        while True:
            print()
            confirmation = input("CONFIRMATION: Are You Sure You Want To Send This Message? ").lower()
            if confirmation == "yes" or confirmation == "no":
                break
        if confirmation == "yes":
            # CREATE CONVERSATION
            conversationInfo = {
                'convoId': f'{prof_name}(Professor) To {stu_name}(Student)',
                'date': now,
                'senderType': "Professor",
                'senderName': stu_name,
                'preMessage': None,
                'senderMessage': message,
                'receivedFrom': None
            }
            createConversation(conversationInfo)
            # SET UP NOTIFICATION
            sql = "INSERT INTO student_notification (notification, received_from, date, stu_id) VALUES (%s, %s, %s, %s)"
            val = (message, f"Professor ({prof_name})", now, stu_id)
            db.execute(sql, val)
            mydb.commit()

            while True:
                print()
                back = input("Your Message Has Been Sent. Press (S) To Send Another Message:\n"
                             "                            Press (M) To Return To Professor Menu: ").lower()
                if back == "s":
                    prof_send_notification()
                elif back == "m":
                    ProfessorMenu(None)
        elif confirmation == "no":
            ProfessorMenu(prof_name)


    # PROFESSOR
    elif to == "Professor":
        while True:
            print()
            professor_name = capitalize(input("Enter The Name Of The Professor: "))
            if professor_name.lower() == "c":
                ProfessorMenu(None)
            if professor_name != '':
                break
        sql = "SELECT id FROM Professor WHERE name = %s"
        val = (professor_name, )
        db.execute(sql, val)
        prof_id = db.fetchall()
        if len(prof_id) == 0:
            no_person_found("Notification", "Prof", "Send_To_Prof")
        prof_id = prof_id[0][0]

        while True:
            message = input("Message: ")
            if message != '':
                break

        while True:
            print()
            confirmation = input("CONFIRMATION: Are You Sure You Want To Send This Message? ").lower()
            if confirmation == "yes" or confirmation == "no":
                break
        if confirmation == "yes":
            # CREATE CONVERSATION
            conversationInfo = {
                'convoId': f'{prof_name}(Professor) To {professor_name}(Professor)',
                'date': now,
                'senderType': "Professor",
                'senderName': prof_name,
                'preMessage': None,
                'senderMessage': message,
                'receivedFrom': None
            }
            createConversation(conversationInfo)
            # SET UP NOTIFICATION
            sql = "INSERT INTO professor_notification (notification, received_from, date, prof_id) VALUES (%s, %s, %s, %s)"
            val = (message, f"Professor ({prof_name})", now, prof_id)
            db.execute(sql, val)
            mydb.commit()

            while True:
                print()
                back = input("Your Message Has Been Sent. Press (S) To Send Another Message:\n"
                             "                            Press (M) To Return To Professor Menu: ").lower()
                if back == "s":
                    prof_send_notification()
                    break
                elif back == "m":
                    ProfessorMenu(None)
                    break
        elif confirmation == "no":
            ProfessorMenu(prof_name)

    # DEAN
    elif to == "Dean":
        while True:
            print()
            deanName = capitalize(input("Enter The Name Of The Dean: "))
            if deanName.lower() == "c":
                ProfessorMenu(None)
            if deanName != '':
                break
        # CHECKING IF CORRECT NAME WAS ENTERED
        sql = "SELECT * FROM Dean WHERE name = %s"
        val = (deanName,)
        db.execute(sql, val)
        result = db.fetchall()
        if len(result) == 0:
            no_person_found("Notification", "Prof", "Send_To_Dean")

        # GETTING THE ID OF THE PROFESSOR
        sql = "SELECT id FROM Professor WHERE name = %s"
        val = (prof_name, )
        db.execute(sql, val)
        prof_id = db.fetchall()[0][0]

        while True:
            message = input("Message: ")
            if message != '':
                break

        while True:
            print()
            confirmation = input("CONFIRMATION: Are You Sure You Want To Send This Message? ").lower()
            if confirmation == "yes" or confirmation == "no":
                break
        if confirmation == "yes":
            # CREATE CONVERSATION
            conversationInfo = {
                'convoId': f'{prof_name}(Professor) To {deanName}(Dean)',
                'date': now,
                'senderType': "Professor",
                'senderName': prof_name,
                'preMessage': None,
                'senderMessage': message,
                'receivedFrom': None
            }
            createConversation(conversationInfo)
            # SET UP NOTIFICATION
            sql = "INSERT INTO dean_notification (notification, received_from, date, person_id) VALUES (%s, %s, %s, %s)"
            val = (message, f"Professor ({prof_name})", now, prof_id)
            db.execute(sql, val)
            mydb.commit()

            while True:
                print()
                back = input("Your Message Has Been Sent. Press (S) To Send Another Message:\n"
                             "                            Press (M) To Return To Professor Menu: ").lower()
                if back == "s":
                    prof_send_notification()
                    break
                elif back == "m":
                    ProfessorMenu(None)
                    break
        elif confirmation == "no":
            ProfessorMenu(prof_name)

# PROF SEND ANNOUNCEMENT
def prof_send_announcement(announcement_to_send=None, course_name=None):
    if announcement_to_send == None:
        clear()
        # GET THE COURSES BEING TAUGHT
        sql = "SELECT CoursesTaught FROM Professor WHERE name = %s"
        val = (prof_name, )
        db.execute(sql, val)
        courses_taught = db.fetchall()[0][0]
        print("SEND ANNOUNCEMENT")
        print(now)
        print("-------------------")
        print("Press (C) To Cancel")
        print("-------------------")
        print()
        print(f"Courses You Are Currently Teaching: {courses_taught.split()}")
        while True:
            print()
            prof_choice = input("Enter The Name Of The Course You Want To Send An Announcement To: ").upper()
            if prof_choice != '':
                break
        # CHECKING IF C WAS ENTERED
        if len(prof_choice) == 1:
            prof_choice = prof_choice.lower()
        if prof_choice == "c":
            ProfessorMenu(None)

        # CHECK IF THE CORRECT COURSE WAS ENTERED
        if prof_choice not in courses_taught.split():
            while True:
                print()
                error = input("You Are Not Teaching That Course. Press (T) To Try Again:\n"
                              "                                  Press (M) To Return To Professor Menu: ").lower()
                if error == "t":
                    prof_send_announcement()
                elif error == "m":
                    ProfessorMenu(None)


        # THE ANNOUNCEMENT
        while True:
            print()
            announcement = input("Enter the Announcement: ")
            if announcement != '':
                break

        # CONFIRMATION
        while True:
            confirmation = input("CONFIRMATION: Are You Sure You Want To Send This Announcement? ")
            if confirmation != '' and (confirmation == "yes" or confirmation == "no"):
                break


        if confirmation == "yes":
            # GET THE STUDENTS ID
            like_query = f"%{prof_choice}%"
            sql = "SELECT id FROM Student WHERE CoursesEnrolledIn LIKE %s"
            val = (like_query, )
            db.execute(sql, val)
            all_id = db.fetchall()

            for i in range(len(all_id)):
                sql = "INSERT INTO student_notification (notification, received_from, date, stu_id) VALUES (%s, %s, %s, %s)"
                val = (announcement, f"Professor ({prof_name}) [{prof_choice}]", now, all_id[i][0])
                db.execute(sql, val)
                mydb.commit()


            while True:
                print()
                back = input("Announcement Sent. Press (S) To Send Another:\n"
                             "                   Press (M) To Return To Professor Menu: ").lower()
                if back == "s":
                    prof_send_announcement()
                elif back == "m":
                    ProfessorMenu(None)

        elif confirmation == "no":
            prof_send_announcement()

    elif announcement_to_send != None:
        if course_name == None:
            return
        announcement = announcement_to_send
        # GET THE STUDENTS ID
        like_query = f"%{course_name}%"
        sql = "SELECT id FROM Student WHERE CoursesEnrolledIn LIKE %s"
        val = (like_query,)
        db.execute(sql, val)
        all_id = db.fetchall()

        for i in range(len(all_id)):
            sql = "INSERT INTO student_notification (notification, received_from, date, stu_id) VALUES (%s, %s, %s, %s)"
            val = (announcement, f"Professor ({prof_name}) [{course_name}]", now, all_id[i][0])
            db.execute(sql, val)
            mydb.commit()

# PROF INBOX
def professor_inbox():
    clear()
    print("----------")
    print("YOUR INBOX")
    print("----------")
    print(now)
    print()
    Prof = Professor(prof_name.split()[0], prof_name.split()[1], None, None, None, None, None)

    sql = "SELECT id, notification, received_from, date FROM professor_notification WHERE prof_id = %s"
    val = (Prof.getID(),)
    db.execute(sql, val)
    all_notifications = db.fetchall()

    if len(all_notifications) == 0:
        print("No Notifications")

    terminal_size = os.get_terminal_size().columns
    for i in range(len(all_notifications)):
       # AUTO FIT THE BROKEN LINES
        message_len = len(all_notifications[i][1]) + len('Message: ')
        received_from_len = len(all_notifications[i][2]) + len('Received From: ')

        max_len_of_attributes = max([message_len, received_from_len])

        if max_len_of_attributes > terminal_size:
            broken_line_added = '-' * terminal_size
        else:
            if max_len_of_attributes == message_len:
                broken_line_added = '-' * message_len
            else:
                broken_line_added = '-' * received_from_len

        print(broken_line_added)
        print(f"Id: {all_notifications[i][0]}")
        print(f"Date: {all_notifications[i][3]}")
        print(f"Received From: {all_notifications[i][2]}")
        print(f"Message: {all_notifications[i][1]}")
        print(broken_line_added)
        print()

    while True:
        print()
        print("Press (CON) To View All Conversations:")
        print()
        print("Press (O) To Open A Notification:")
        print()
        print("Press (D) To Filter By Date:              |  Press (C) To Clear A Notification:")
        print("Press (F) To Filter By Received From:     |  Press (CA) To Clear All Notifications:")
        print("Press (M) To Filter By Message:           |  Press (S) To Return To Professor Menu:")
        print()
        filter = input("Choose An Option: ")
        if filter == 'con':
            view_all_conversations(prof_name, 'Professor')
        elif filter == "o":
            open_prof_notification(all_notifications)
        elif filter == "d":
            filter_prof_notification_by_date(all_notifications)
        elif filter == "f":
            filter_prof_notification_by_received_from(all_notifications)
        elif filter == "m":
            filter_prof_notification_by_message(all_notifications)
        elif filter == "c":
            clear_professor_notification()
        elif filter == "ca":
            clear_all_professor_notifications(Prof.getID())
        elif filter == "s":
            ProfessorMenu(None)

# OPEN NOTIFICATION
def open_prof_notification(notification):
    all_possible_id = [str(notification[i][0]) for i in range(len(notification))]
    print()
    while True:
        noti_id = input("Enter The Id Of The Notification: ")
        if noti_id not in all_possible_id:
            print("Invalid Id")
        else:
            break
    sql = "SELECT id, notification, received_from, date FROM professor_notification WHERE id = %s"
    val = (int(noti_id),)
    db.execute(sql, val)
    notification_to_open = db.fetchall()
    clear()
    # AUTO FIT THE BROKEN LINES
    max_len_of_attributes = max([len(notification_to_open[0][1]), len(notification_to_open[0][2])])
    if max_len_of_attributes == len(notification_to_open[0][1]):
        broken_line_added = "-" * len("Message: ")
    else:
        broken_line_added = "-" * len("Received From: ")

    message = notification_to_open[0][1]
    received_from = notification_to_open[0][2]
    print("-" * max_len_of_attributes + broken_line_added)
    print(f"Id: {notification_to_open[0][0]}")
    print(f"Date: {notification_to_open[0][3]}")
    print(f"Received From: {notification_to_open[0][2]}")
    print(f"Message: {notification_to_open[0][1]}")
    print("-" * max_len_of_attributes + broken_line_added)
    print()
    assignment = False
    if "Submitted" in message:
        assignment = True
        print("Press (V) To View Submission:")

    print("Press (R) To Respond:")
    while True:
        back = input("Press (B) To Go Back: ").lower()
        # RESPONSE
        if back == "r":
            receiverName = extractNameFromNotification(received_from)["receiverName"]
            receiverType = extractNameFromNotification(received_from)["Type"]
            if receiverName == None:
                while True:
                    print()
                    error = input("Unable To Respond: Please Contact The Dean. Press (B) To Go Back: ").lower()
                    if error == "b":
                        professor_inbox()
                        break
            else:
                respondToNotification(prof_name, "Professor", receiverType, receiverName, message)
        # ASSIGNMENT SUBMISSION
        elif back == "v" and assignment:
            try:
                assign_id = int(message[-1])
                # EXTRACT STU ID FROM MESSAGE
                stu_id = extract_stu_id(message)
            except:
                while True:
                    print()
                    error = input("Error Loading Submission. Press (B) To Go Back: ").lower()
                    if error == "b":
                        ProfessorMenu(None)
                        break
            # OPEN THE ASSIGNMENT
            prof_open_submission(stu_id, assign_id)


        elif back == "b":
            professor_inbox()
            break





def extract_stu_id(message):
    stu_id = ""
    i = 0
    while message.split('(')[1][i].isdigit():
        id_numbers = message.split('(')[1][i]
        stu_id += id_numbers
        i += 1
    if stu_id != "":
        return int(stu_id)
    return None

# OPEN SUBMISSION
def prof_open_submission(stu_id, assign_id):
    clear()
    submissionMessage = getSubmissionMessage(assign_id)
    print("OPEN SUBMISSION")
    print("---------------")
    print()
    if submissionMessage != None:
        print("-"*len(submissionMessage))
        print(submissionMessage)
        print("-" * len(submissionMessage))
        print()

    # GET THE ASSIGNMENT QUESTIONS
    sql = "SELECT * FROM assignments WHERE id = %s"
    val = (assign_id, )
    db.execute(sql, val)
    results = db.fetchall()
    if len(results) == 0:
        submission_loading_error()
    if assignmentIsShortAnswer(results):
        # GET THE ASSIGNMENT QUESTIONS
        assign_questions = [results[i][5] for i in range(len(results))]
        course_name = results[0][13]
        # GET THE ASSIGNMENT ANSWERS
        sql = "SELECT answers FROM assignment_submissions WHERE stu_id = %s AND assignment_id = %s"
        val = (stu_id, assign_id)
        db.execute(sql, val)
        results = db.fetchall()
        if len(results) == 0:
            submission_loading_error()
        assign_answers = results[0][0].rstrip()
        assign_answers = assign_answers.split('\n\n')

        for i in range(len(assign_questions)):
            print(f"{i + 1}.{assign_questions[i]}")
            print(f"Student Answer: {assign_answers[i][2:]}")
            print()

        assign_student_grade(stu_id, course_name, prof_name)

    elif assignmentIsMixed(results):
        # GET THE ASSIGNMENT QUESTIONS
        assign_questions = [results[i][5] for i in range(len(results))]
        course_name = results[0][13]

        # GET THE ASSIGNMENT ANSWER PROMPTS
        # DICT WITH QUESTION_NUM AS KEY AND ANSWERS PROMPTS AS VALUE
        assign_prompts = {results[i][6]:results[i][7] for i in range(len(results)) if results[i][6] != None and results[i][7] != None}
        # assign_prompts = [results[i][7] for i in range(len(results)) if results[i][7] != None]
        sql = "SELECT answers FROM assignment_submissions WHERE stu_id = %s AND assignment_id = %s"
        val = (stu_id, assign_id)
        db.execute(sql, val)
        results = db.fetchall()
        if len(results) == 0:
            submission_loading_error()
        # GET THE ASSIGNMENT ANSWERS
        assign_answers = results[0][0].rstrip()
        # SEPARATE THE QUESTION NUMBERS FROM THE STRING OF ANSWERS AND CREATE A DICT WITH KEY = THE QUESTION NUMBER AND VALUE = The QUESTION
        question_num = [assign_answers[i] for i in range(len(assign_answers)) if assign_answers[i].isdigit() and assign_answers[i+1] == '.']
        assign_answers = {int(question_num[i]): assign_answers.split('\n\n')[i][2:] for i in range(len(question_num))}

        studentMultipleChoiceAnswers = eval(getStudentMultipleChoiceAnswers(submissionMessage))
        # print(studentMultipleChoiceAnswers[2])

        for i in range(len(assign_questions)):
            current_question_num = i+1
            current_question = assign_questions[i]
            if questionIsShortAnswer(assign_id, i+1):
                print(f"{current_question_num}.{current_question}")
                print(f"Student Answer: {assign_answers[current_question_num]}")
                print()
            else:
                print(f"{i + 1}.{current_question}")
                print(assign_prompts[current_question_num])
                # print(studentMultipleChoiceAnswers[question_num])
                print(f'Student Answer: {studentMultipleChoiceAnswers[current_question_num]}')
                print()

        assign_student_grade(stu_id, course_name, prof_name)


    while True:
        print()
        back = input("Grade Assigned. Press (B) To Go Back: ").lower()
        if back == "b":
            professor_inbox()
            break


def getSubmissionMessage(assign_id):
    sql = "SELECT message FROM assignment_submissions WHERE assignment_id = %s"
    val = (assign_id,)
    db.execute(sql, val)
    results = db.fetchall()
    if len(results) == 0:
        return None
    return results[0][0]

def getStudentMultipleChoiceAnswers(sub_message):
    student_answers = ''
    i = 0
    while i < len(sub_message):
        if sub_message[i] == '{':
            start = True
            while start:
                student_answers += sub_message[i]
                if sub_message[i] == '}':
                    start = False
                i += 1
        i += 1

    return student_answers



def submission_loading_error():
    while True:
        print()
        error = input("Error Loading Submission. Press (B) To Go Back: ").lower()
        if error == "b":
            ProfessorMenu(prof_name)
            break
def assign_student_grade(stu_id, course_name, prof_name):
    while True:
        print()
        stu_grade = input("Assign Their Grade(%): ")
        stu_grade = stu_grade.replace('%', '')

        if not stu_grade.isdigit():
            print()
            print("Grade Must Be A Number")
        else:
            stu_grade = int(stu_grade)
            if stu_grade < 0 or stu_grade > 100:
                print()
                print("Grade Can Only Be From 0 --> 100.")
            else:
                break
    stu_grade = str(stu_grade) + '%'

    while True:
        print()
        confirmation = input("CONFIRMATION: Are You Sure You Want To Assign This Grade? ")
        if confirmation == "yes" or confirmation == "no":
            break

    if confirmation == "yes":
        update_grade_book(course_name, stu_id, stu_grade, prof_name)
    elif confirmation == "no":
        ProfessorMenu(prof_name)


# FILTER PROFESSOR NOTIFICATIONS
def filter_prof_notification_by_date(notifications):
    while True:
        print()
        date_to_filter = input("Enter The Date: ")
        if date_to_filter != '':
            break

    clear()
    total_found = 0
    print("-" * len(date_to_filter) + "--------------")
    print(f"Filtered by: {date_to_filter}")
    print("-" * len(date_to_filter) + "--------------")
    print()
    for i in range(len(notifications)):
        if date_to_filter in notifications[i][3]:
            print("-" * len(notifications[i][1]) + "---------")
            print(f"Id: {notifications[i][0]}")
            print(f"Date: {notifications[i][3]}")
            print(f"Received From: {notifications[i][2]}")
            print(f"Message: {notifications[i][1]}")
            print("-" * len(notifications[i][1]) + "---------")
            print()
            total_found += 1

    if total_found == 0:
        print()
        print("No Notifications Found")

    while True:
        print()
        back = input("Press (F) To Filter Again:\nPress (C) To Clear A Notification:\nPress (S) To Return To Professor Menu: ").lower()
        if back == "f":
            professor_inbox()
        if back == "c":
            clear_professor_notification()
        elif back == "s":
            ProfessorMenu(None)
def filter_prof_notification_by_received_from(notifications):
    while True:
        print()
        person_to_filter = input("Enter The Name: ")
        person_to_filter = capitalize(person_to_filter)
        if person_to_filter != '':
            break

    clear()
    total_found = 0
    print("-" * len(person_to_filter) + "--------------")
    print(f"Filtered by: {person_to_filter}")
    print("-" * len(person_to_filter) + "--------------")
    print()
    for i in range(len(notifications)):
        if person_to_filter in notifications[i][2]:
            print("-" * len(notifications[i][1]) + "---------")
            print(f"Id: {notifications[i][0]}")
            print(f"Date: {notifications[i][3]}")
            print(f"Received From: {notifications[i][2]}")
            print(f"Message: {notifications[i][1]}")
            print("-" * len(notifications[i][1]) + "---------")
            print()
            total_found += 1

    if total_found == 0:
        print()
        print("No Notifications Found")

    while True:
        print()
        back = input("Press (F) To Filter Again:\nPress (C) To Clear A Notification:\nPress (S) To Return To Professor Menu: ").lower()
        if back == "f":
            professor_inbox()
        elif back == "c":
            clear_professor_notification()
        elif back == "s":
            ProfessorMenu(None)
def filter_prof_notification_by_message(notifications):
    while True:
        print()
        message_to_filter = input("Enter The Message: ")
        if message_to_filter != '':
            break

    clear()
    total_found = 0
    print("-" * len(message_to_filter) + "--------------")
    print(f"Filtered by: {message_to_filter}")
    print("-" * len(message_to_filter) + "--------------")
    print()
    for i in range(len(notifications)):
        if message_to_filter in notifications[i][1]:
            print("-" * len(notifications[i][1]) + "---------")
            print(f"Id: {notifications[i][0]}")
            print(f"Date: {notifications[i][3]}")
            print(f"Received From: {notifications[i][2]}")
            print(f"Message: {notifications[i][1]}")
            print("-" * len(notifications[i][1]) + "---------")
            print()
            total_found += 1

    if total_found == 0:
        print()
        print("No Notifications Found")

    while True:
        print()
        back = input("Press (F) To Filter Again:\nPress (C) To Clear A Notification:\nPress (S) To Return To Professor Menu: ").lower()
        if back == "f":
            professor_inbox()
        elif back == "c":
            clear_professor_notification()
        elif back == "s":
            ProfessorMenu(None)
def clear_professor_notification():
    while True:
        print()
        notification_id = input("Enter The Id Of The Notification: ")
        if notification_id != '' and notification_id.isdigit():
            break

    while True:
        print()
        confirmation = input("CONFIRMATION: Are You Sure You Want To Clear This Notifications? ")
        if confirmation != '' and (confirmation == "yes" or confirmation == "no"):
            break

    if confirmation == "yes":
        sql = "DELETE FROM professor_notification WHERE id = %s"
        val = (int(notification_id), )
        db.execute(sql, val)
        mydb.commit()

        while True:
            print()
            back = input("Notification Deleted. Press (M) To Return To Professor Menu: ").lower()
            if back == "m":
                ProfessorMenu(None)
    else:
        ProfessorMenu(None)
def clear_all_professor_notifications(prof_id):
    while True:
        print()
        confirmation = input("CONFIRMATION: Are You Sure You Want To Clear All Notifications? ")
        if confirmation != '' and (confirmation == "yes" or confirmation == "no"):
            break

    if confirmation == "yes":
        sql = "DELETE FROM professor_notification WHERE prof_id = %s"
        val = (prof_id, )
        db.execute(sql, val)
        mydb.commit()

        while True:
            print()
            back = input("All Notifications Cleared. Press (M) To Return To Professor Menu: ").lower()
            if back == "m":
                ProfessorMenu(None)
    else:
        ProfessorMenu(None)


# PROF CREATE EXAM
def prof_create_assignment():
    clear()
    sql = "SELECT CoursesTaught FROM Professor WHERE name = %s"
    val = (prof_name,)
    db.execute(sql, val)
    results = db.fetchall()
    if len(results) == 0:
        while True:
            print()
            error = input("You Are Not Currently Teaching A Course So You Are Unable To Create An Assignment\n\n"
                          "Press (M) To Return To Professor Menu").lower()
            if error == "m":
                ProfessorMenu(None)
                break
    prof_courses_taught = results[0][0].split()
    print("CREATE ASSIGNMENT")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    print(f"Courses You Teach: {prof_courses_taught}")
    print()
    courses = {}
    for i, course in enumerate(prof_courses_taught, 1):
        print(f"{i} - Create {course} Assignment")
        courses.update({i: course})

    while True:
        print()
        prof_choice = input("Choose An Option : ")
        if prof_choice.lower() == "c":
            ProfessorMenu(None)
        if prof_choice.isdigit():
            range_of_choices = [i for i in range(1, len(prof_courses_taught) + 1)]
            prof_choice = int(prof_choice)
            if prof_choice not in range_of_choices:
                print("Invalid Choice")
            else:
                break
        else:
            print("Invalid Choice")

    createAssignmentPrompt(courses[int(prof_choice)])



# CREATE ASSIGNMENT
def createAssignmentPrompt(course_name):
    clear()
    print("CREATE ASSIGNMENT")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    print("AVAILABLE ASSIGNMENTS ")
    print()
    print("1 - Exam(Short Answer)        |  7 - Quiz(Short Answer)")
    print("2 - Exam(Multiple Choice)     |  8 - Quiz(Multiple Choice)")
    print("3 - Exam(Mixed)               |  9 - Quiz(Mixed)")
    print("                              |")
    print("4 - Test(Short Answer)        |")
    print("5 - Test(Multiple Choice)     |")
    print("6 - Test(Mixed)               |")
    while True:
        print()
        assign_choice = input("Choose An Option: ").lower()
        if assign_choice == "c":
            ProfessorMenu(prof_name)
        
        # MULTIPLE CHOICE QUESTIONS
        elif assign_choice == "2" or assign_choice == "5" or assign_choice == "8":
            if assign_choice == "2":
                assignment_type = "Exam(Multiple Choice)"
            elif assign_choice == "5":
                assignment_type  = "Test(Multiple Choice)"
            elif assign_choice == "8":
                assignment_type = "Quiz(Multiple Choice)"
            Assignment = MultipleChoiceAssignment(course_name, assignment_type, prof_name)
            Assignment.createAssignment()

        # SHORT ANSWER QUESTIONS
        elif assign_choice == "1" or assign_choice == "4" or assign_choice == "7":
            if assign_choice == "1":
                assignment_type = "Exam(Short Answer)"
            elif assign_choice == "4":
                assignment_type = "Test(Short Answer)"
            elif assign_choice == "7":
                assignment_type = "Quiz(Short Answer)"
            Assignment = ShortAnswerAssignment(course_name, assignment_type, prof_name)
            Assignment.createAssignment()

        # MIXED ANSWER QUESTIONS
        elif assign_choice == "3" or assign_choice == "6" or assign_choice == "9":
            if assign_choice == "3":
                assignment_type = "Exam(Mixed)"
            elif assign_choice == "6":
                assignment_type = "Test(Mixed)"
            elif assign_choice == "9":
                assignment_type = "Quiz(Mixed)"
            Assignment = MixedAssignment(course_name, assignment_type, prof_name)
            Assignment.createAssignment()


# ISSUE ASSIGNMENT
def prof_issue_assignment():
    clear()
    # GET PROF ID
    prof_id = Professor.get_prof_id(prof_name)
    sql = "SELECT title, assignment_type, due_date FROM assignments WHERE prof_id = %s ORDER BY id ASC"
    val = (prof_id,)
    db.execute(sql, val)
    results = db.fetchall()
    if results == 0:
        return

    all_created_assignments = removeDuplicates([assign[0] for assign in results])
    all_assignment_types    = removeRightDuplicateAssignmentTypes(all_created_assignments)


    print("All Created Assignments")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    print("Press (D) To Delete An Assignment")
    print()

    # STORE THE ASSIGNMENT INCREMENT IN A DICT SO IT CAN EASILY BE DELETED
    assign_inc = {}
    for i in range(len(all_created_assignments)):
        assign_inc.update({i+1: all_created_assignments[i]})
        print(f"{i + 1} - {all_created_assignments[i]} [{all_assignment_types[i]}]")

    while True:
        print()
        assign_to_issue = input("Select An Assignment: ")
        if assign_to_issue.lower() == "c":
            ProfessorMenu(prof_name)
        elif assign_to_issue.lower() == "d":
            while True:
                print()
                assign_to_delete = input("Enter The Number Of The Assignment To Delete: ").lower()
                if assign_to_delete == "c":
                    prof_issue_assignment()
                    break
                if assign_to_delete not in [str(i + 1) for i in range(len(all_created_assignments))]:
                    print("Invalid Assignment")
                else:
                    delete_assignment(assign_inc[int(assign_to_delete)])
                    break

        if assign_to_issue not in [str(i + 1) for i in range(len(all_created_assignments))]:
            print("Invalid Assignment")
        else:
            break
    assignment_to_issue = all_created_assignments[int(assign_to_issue) - 1]
    assignment_type = all_assignment_types[int(assign_to_issue) - 1]

    clear()
    open_assignment(assignment_to_issue)

    # CONFIRMATION
    while True:
        print()
        confirmation = input(f"CONFIRMATION: Are You Sure You Want To Issue {assignment_to_issue}? ").lower()
        if confirmation == "yes" or confirmation == "no":
            break

    if confirmation == "yes":
        sql = "SELECT due_date, course_name, id FROM assignments WHERE title = %s"
        val = (assignment_to_issue,)
        db.execute(sql, val)
        results = db.fetchall()
        if len(results) == 0:
            due_date    = "Unknown"
            course_name = "Unknown"
            assign_id   = "Unknown"
        else:
            due_date    = results[0][0]
            course_name = results[0][1]
            assign_id   = results[0][2]
        announcement = f"You Have An Upcoming {course_name} {assignment_type} Due {due_date} ID: {assign_id}"
        prof_send_announcement(announcement, course_name)

        while True:
            print()
            back = input("Assignment Issued. Press (M) To Return To Professor Menu: ").lower()
            if back == "m":
                ProfessorMenu(prof_name)
    elif confirmation == "no":
        ProfessorMenu(prof_name)



# OPEN ASSIGNMENT
def open_assignment(assignment_title):
    sql = "SELECT * FROM assignments WHERE title = %s"
    val = (assignment_title,)
    db.execute(sql, val)
    results = db.fetchall()
    # NO ASSIGNMENT FOUND
    if len(results) == 0:
        unable_to_open_assign()
    title = results[0][2]
    description = results[0][3]
    duration = results[0][11]
    due_date = results[0][12]
    num_assign_questions = len(results)
    

    if assignmentIsShortAnswer(results):
        print(f"<<<<<<<<<< {title} >>>>>>>>>>")            
        print()
        if description != '':
            print("-" * len(description))
            print(description)
            print("-" * len(description))
            print()
        print(f"Duration: {duration} Mins")
        print(f"Due Date: {due_date}")
        print()
        for i in range(num_assign_questions):
            question_num = (i+1)
            current_question = results[i][5]
            print(f'{question_num}.{current_question}')
            print()

        while True:
            print()
            back = input("Press (I) To Issue This Assignment:\nPress (E) To Edit This Assignment:\nPress (C) To Cancel: ").lower()
            if back == "i":
                return
            elif back == "e":
                prof_edit_assignment(results)
            elif back == "c":
                prof_issue_assignment()
                break

    elif assignmentIsMixed(results):
        print(f"<<<<<<<<<< {title} >>>>>>>>>>")            
        print()
        if description != '':
            print("-" * len(description))
            print(description)
            print("-" * len(description))
            print()
        print(f"Duration: {duration} Mins")
        print(f"Due Date: {due_date}")
        print()
        for i in range(len(results)):
            # DISPLAY THE MULTIPLCE CHOICE QUESTION
            if results[i][6] != None and results[i][7] != None and results[i][8] != None and results[i][9] != None:
                multiple_choice_questions = results[i][5]
                answer_prompts = results[i][7]
                correct_answers = results[i][9]
                print(f'{i+1}.{multiple_choice_questions}')
                print(answer_prompts)
                print(f"Correct Answer: {correct_answers}")
                print()
            # DISPLAY THE SHORT ANSWER QUESTION
            else:
                short_ans_questions = results[i][5]
                print(f"{i+1}.{short_ans_questions}")
                print()

        while True:
            print()
            back = input("Press (I) To Issue This Assignment:\nPress (E) To Edit This Assignment:\nPress (C) To Cancel: ").lower()
            if back == "i":
                return
            if back == "e":
                prof_edit_assignment(results)
                break
            elif back == "c":
                prof_issue_assignment()
                break


    elif assignmentIsMultipleChoice(results):
        # RETRIEVE THE CORRECT ANSWERS
        assign_answers = {}
        for i in range(len(results)):
            current_question_num, correct_answer = results[i][8], results[i][9]
            assign_answers.update({current_question_num: correct_answer})

        print(f"<<<<<<<<<< {title} >>>>>>>>>>")
        print()
        if description != '':
            print("-" * len(description))
            print(description)
            print("-" * len(description))
            print()
        print(f"Duration: {duration} Mins")
        print(f"Due Date: {due_date}")
        print()
        for i in range(num_assign_questions):
            answer_prompts = results[i][7]
            question_num = i+1
            current_question = results[i][5]

            print(f"{question_num}.{current_question}")
            print(answer_prompts)
            print(f"Correct Answer: {assign_answers[i+1]}")
            print()

        while True:
            print()
            back = input("Press (I) To Issue This Assignment:\nPress (E) To Edit This Assignment:\nPress (C) To Cancel: ").lower()
            if back == "i":
                return
            elif back == "e":
                prof_edit_assignment(results)
                break
            elif back == "c":
                prof_issue_assignment()
                break
# EDIT ASSIGNMENT
def prof_edit_assignment(assignment_info):
    print()
    assign_id = assignment_info[0][0]
    title = assignment_info[0][2]
    description = assignment_info[0][3]
    questions = [assignment_info[i][5] for i in range(len(assignment_info))]
    answer_prompts = [assignment_info[i][7] for i in range(len(assignment_info))]
    correct_answers = [assignment_info[i][9] for i in range(len(assignment_info))]
    duration = assignment_info[0][11]
    due_date = assignment_info[0][12]
    # assignment_type = 'Short Answer' if assignmentIsShortAnswer(assignment_info) else 'Multiple Choice' if assignmentIsMultipleChoice(assignment_info) else 'Mixed'
    num_assign_questions = len(assignment_info)

    print("---------------")
    print("EDIT ASSIGNMENT")
    print("---------------")
    print()
    print("Press (C) To Cancel")
    print()
    print("EDITS AVAILABLE")
    print()
    print("1 - Edit Title")
    print("2 - Edit Description")
    print("3 - Edit Duration")
    print("4 - Edit Due Date")
    print("5 - Edit Questions")
    print()
    print("6 - Edit Answer Prompts")
    print("7 - Edit Correct Answer")
    print("8 - Edit Question Type")
    print("9 - Add Question")
    print("10 - Delete Question")
    print()
    while True:
        print()
        edit_to_make = input("Choose An Option: ")
        if edit_to_make == 'c':
            prof_issue_assignment()
            break
        if edit_to_make in ['1','2','3','4','5','6','7','8', '9','10']:
            break
    if edit_to_make == '1':
        editAssignment('Title', 'title', title, assign_id)
    elif edit_to_make == '2':
        editAssignment('Description', 'description', description, assign_id)
    elif edit_to_make == '3':
        editAssignment('Duration', 'duration', duration, assign_id)
    elif edit_to_make == '4':
        editAssignment('Due Date', 'due_date', due_date, assign_id)
    elif edit_to_make == '5':
        editAssignment('Question', 'questions', questions, assign_id)
    elif edit_to_make == '6':
        if assignmentIsShortAnswer(assignment_info):
            while True:
                print()
                error = input("This Edit Is Only Available For Mixed And Multiple Choice Assignments. Press (B) To Go Back: ").lower()
                if error == 'b':
                    prof_edit_assignment(assignment_info)
                    break
        else:
            editAssignment('Answer Prompt', 'answer_prompts', answer_prompts, assign_id, num_assign_questions)
    elif edit_to_make == '7':
        if assignmentIsShortAnswer(assignment_info):
             while True:
                print()
                error = input("This Edit Is Only Available For Mixed And Multiple Choice Assignments. Press (B) To Go Back: ").lower()
                if error == 'b':
                    prof_edit_assignment(assignment_info)
                    break

        else:
             editAssignment('Correct Answer', 'correct_answer', correct_answers, assign_id, num_assign_questions)
    elif edit_to_make == '8':
        editAssignment('Question Type', 'question_type', None, assign_id, num_assign_questions)
    elif edit_to_make == '9':
        editAssignment('Add Question', None, assignment_info, assign_id, num_assign_questions)
    elif edit_to_make == '10':
        editAssignment('Delete Question', None, assignment_info, assign_id, num_assign_questions)



def editAssignment(editToMake, columnName, oldValue, assign_id, numQuestions=None):
    # SPECIAL EDITS
    if editToMake == 'Due Date':
        print()
        print("EDIT DUE DATE")
        print("-------------")
        print()
        print(f"Current Due Date: {oldValue}")
        while True:
            formatError = False
            tmpAssign = Assignment()
            validateDueDate = tmpAssign.validateDueDate
            print()
            newDueDate = input("Enter The New Due Date(MM/DD/YYYY): ")
            if newDueDate.lower() == 'c':
                prof_issue_assignment()
                break
            if validateDueDate(newDueDate) == 0:
                formatError = True
                print("Invalid Date Format")
            elif validateDueDate(newDueDate) == -1:
                formatError = True
                print("Invalid Month")
            elif validateDueDate(newDueDate) == -2:
                formatError = True
                print("Invalid Day")
            elif validateDueDate(newDueDate) == -3:
                formatError = True
                print("That Date Has Already Passed")
            if not formatError:
                break

        # CONFIRMATION
        while True:
            print()
            confirmation = input(f"CONFIRMATION: Are You Sure You Want To Edit The Due Date Of This Assignment? ").lower()
            if confirmation == "yes" or confirmation == "no":
                break
        if confirmation == "yes":
            sql = f"UPDATE assignments SET due_date = %s WHERE id = %s"
            val = (newDueDate, assign_id)
            db.execute(sql, val)
            mydb.commit()
            while True:
                print()
                back = input(f"Assignment Due Date Changed. Press (B) To Go Back: ").lower()
                if back == "b":
                    prof_issue_assignment()
                    break
        else:
            prof_issue_assignment()

    elif editToMake == 'Question':
        print()
        print("EDIT QUESTION")
        print("-------------")
        while True:
            print()
            question_num = input("Enter The Question Number: ")
            if question_num.lower() == 'c':
                prof_issue_assignment()
                break
            range_of_values = [str(i+1) for i in range(len(oldValue))]
            if question_num not in range_of_values or not question_num.isdigit():
                print("Invalid Question Number")
                print()
            else:
                break
        displayQuestion(assign_id, int(question_num), 'editAssignment')

        while True:
            print()
            new_question = input("Enter The New Question: ")
            if new_question.lower() == 'c':
                prof_issue_assignment()
                break
            if new_question != '':
                break
        while True:
            print()
            confirmation = input("CONFIRMATION: Are You Sure You Want To Edit This Question? ").lower()
            if confirmation == "yes" or confirmation == "no":
                break
        if confirmation == "yes":
            sql = "UPDATE assignments SET questions = %s WHERE question_num = %s AND id = %s"
            val = (new_question, int(question_num), assign_id)
            db.execute(sql, val)
            mydb.commit()
            while True:
                print()
                back = input(f"Assignment {editToMake} Changed. Press (B) To Go Back: ").lower()
                if back == "b":
                    prof_issue_assignment()
                    break
        else:
            prof_issue_assignment()

    elif editToMake == 'Answer Prompt':
        print()
        print("EDIT ANSWER PROMPT")
        print("------------------")
        while True:
            print()
            question_num = input("Enter The Question Number: ")
            if question_num.lower() == 'c':
                prof_issue_assignment()
                break
            range_of_values = [str(i+1) for i in range(numQuestions)]
            error = False
            if question_num not in range_of_values or not question_num.isdigit():
                error = True
                print("Invalid Question Number")
            if not error:
                if questionIsShortAnswer(assign_id, int(question_num)):
                    error = True
                    print("That Question Is Short Answer. Only Multiple Choice Answer Prompts Can Be Changed.")
            if not error:
                break
        displayQuestion(assign_id, int(question_num), 'editAssignment')
        # CONVERT THE STRING OF OLD ANSWER PROMPTS TO A DICT
        array_of_ans = oldValue[int(question_num)-1].split('\n')
        old_prompt_answer = {}
        
        for item in array_of_ans:
            item = item.split('.')
            letter_prompt = item[0]
            answer_to_prompt = item[1].lstrip()

            old_prompt_answer.update({f'{letter_prompt}.': answer_to_prompt})
        cpy_pre_prompt_answers = old_prompt_answer

        
        tmp_prompt_answer = {}
        while True:
            print()
            answer_prompt_to_change = input('Which Answer Prompt Would You Like To Change? ').lower()
            # GET ALL POSSIBLE ANSWER COMBINATIONS
            range_of_values = ''
            for perm in permuteString('abcd'):
                for item in perm:
                    range_of_values += f'{item} '
            if answer_prompt_to_change not in range_of_values:
                print("Invalid. Enter a,b,c or d")
            else:
                print()
                for prompt in answer_prompt_to_change.split(',') if ',' in answer_prompt_to_change else answer_prompt_to_change.split():
                    new_prompt = input(f"Enter The New Answer Prompt For {prompt}: ")
                    tmp_prompt_answer.update({f'{prompt}.': new_prompt})
                break
        prompt_ans_to_store = ''
        answer_choices = ['a.','b.','c.','d.']
        for ans in tmp_prompt_answer:
            cpy_pre_prompt_answers[ans] = tmp_prompt_answer[ans]

        for i in range(len(cpy_pre_prompt_answers)):
            prompt_ans_to_store += f'{answer_choices[i]} {cpy_pre_prompt_answers[answer_choices[i]]}\n'
            
        prompt_ans_to_store = prompt_ans_to_store[:len(prompt_ans_to_store) - 1]

        while True:
            print()
            confirmation = input(f'CONFIRMATION: Are You Sure You Want To Change The Answer Prompt For This Question? ').lower()
            if confirmation == "yes" or confirmation == "no":
                break
        if confirmation == "yes":
            sql = "UPDATE assignments SET answer_prompts = %s WHERE question_num = %s AND id = %s"
            val = (prompt_ans_to_store, int(question_num), assign_id)
            db.execute(sql, val)
            mydb.commit()
            while True:
                print()
                back = input(f"Assignment {editToMake} Changed. Press (B) To Go Back: ").lower()
                if back == "b":
                    prof_issue_assignment()
                    break
        else:
            prof_issue_assignment()

    elif editToMake == 'Correct Answer':
        print()
        print("EDIT CORRECT ANSWER")
        print("-------------------")
        print()
        while True:
            print()
            question_num = input("Enter The Question Number: ")
            if question_num.lower() == 'c':
                prof_issue_assignment()
                break
            range_of_values = [str(i+1) for i in range(numQuestions)]
            error = False
            if question_num not in range_of_values or not question_num.isdigit():
                error = True
                print("Invalid Question Number")
            if not error:
                if questionIsShortAnswer(assign_id, int(question_num)):
                    error = True
                    print("That Question Is Short Answer. Only Multiple Choice Correct Answers Can Be Changed.")
            if not error:
                break
        displayQuestion(assign_id, int(question_num), 'editAssignment')
        while True:
            print()
            new_correct_answer  = input("Enter The New Correct Answer: ").lower()
            if new_correct_answer not in ['a','b','c','d']:
                print("Invalid Correct Answer. Enter a, b, c or d")
                print()
            else:
                break
        while True:
            print()
            confirmation = input("CONFIRMATION: Are You Sure You Want To Edit This Correct Answer? ").lower()
            if confirmation == "yes" or confirmation == "no":
                break
        if confirmation == "yes":
            new_correct_answer += '.'
            sql = "UPDATE assignments SET correct_answer = %s WHERE question_num = %s AND id = %s"
            val = (new_correct_answer, int(question_num), assign_id)
            db.execute(sql, val)
            mydb.commit()
            while True:
                print()
                back = input(f"Assignment {editToMake} Changed. Press (B) To Go Back: ").lower()
                if back == "b":
                    prof_issue_assignment()
                    break
        else:
            prof_issue_assignment()

    elif editToMake == 'Question Type':
        print()
        print("EDIT QUESTION TYPE")
        print("------------------")
        while True:
            print()
            question_num = input('Enter The Question Number: ')
            if question_num.lower() == 'c':
                prof_issue_assignment()
                break
            range_of_values = [str(i+1) for i in range(numQuestions)]
            if question_num not in range_of_values:
                print('Invalid Question Number')
            else:
                break
        question_num = int(question_num)
        displayQuestion(assign_id, question_num, 'editAssignment')
        while True:
            print()
            newQuestionType = input('Enter The New Question Type: ').title()
            if newQuestionType.lower() == 'c':
                prof_issue_assignment()
                break
            if newQuestionType not in ['Short Answer', 'Multiple Choice']:
                print("Invalid Question Type. Enter 'Multiple Choice' or 'Short Answer'")
            else:
                break

        if newQuestionType == 'Short Answer':
            if questionIsShortAnswer(assign_id, question_num):
                while True:
                    print()
                    error = input("This Question Is Already Short Answer.\n\nPress (T) To Try Again:\nPress (B) To Go Back: ").lower()
                    if error == 't':
                        editAssignment(editToMake, columnName, oldValue, assign_id, numQuestions)
                        break
                    elif error == 'b':
                        prof_issue_assignment()
                        break
            else:
                while True:
                    print()
                    changeQuestion = input('Do You Want To Change The Question? ').lower()
                    if changeQuestion in ['yes', 'no']:
                        break
                if changeQuestion == 'yes':
                    while True:
                        newQuestion = input('Enter The New Question: ')
                        if newQuestion.lower() == 'c':
                            prof_issue_assignment()
                            break
                        if newQuestion != '':
                            break

                while True:
                    print()
                    confirmation = input('CONFIRMATION: Are You Sure You Want To Change This Question Type? ').lower()
                    if confirmation in ['yes', 'no']:
                        break
                if confirmation == 'yes':
                    if changeQuestion == 'yes':
                        # UPDATE QUESTION
                        sql = 'UPDATE assignments SET questions = %s WHERE question_num = %s AND id = %s'
                        val = (newQuestion, question_num, assign_id)
                        db.execute(sql, val)
                        mydb.commit()

                    # SET ALL THE COLUMNS RELATED TO MULTIPLE CHOICE TO NULL
                    columsToChange = ['answer_prompts_num', 'answer_prompts', 'correct_answer_num', 'correct_answer']
                    for i in range(len(columsToChange)):
                        sql = f"UPDATE assignments SET {columsToChange[i]} = %s WHERE question_num = %s AND id = %s"
                        val = (None, question_num, assign_id)
                        db.execute(sql, val)
                        mydb.commit()

                    while True:
                        print()
                        back = input('Question Type Changed. Press (B) To Go Back: ').lower()
                        if back == 'b':
                            prof_issue_assignment()
                            break

                elif confirmation == 'no':
                    prof_issue_assignment()

        elif newQuestionType == 'Multiple Choice':
            if not questionIsShortAnswer(assign_id, question_num):
                while True:
                    print()
                    error = input("This Question Is Already Multiple Choice.\n\nPress (T) To Try Again:\nPress (B) To Go Back: ").lower()
                    if error == 't':
                        editAssignment(editToMake, columnName, oldValue, assign_id, numQuestions)
                        break
                    elif error == 'b':
                        prof_issue_assignment()
                        break
            else:
                while True:
                    print()
                    changeQuestion = input('Do You Want To Change The Question? ').lower()
                    if changeQuestion in ['yes', 'no']:
                        break
                if changeQuestion == 'yes':
                    while True:
                        newQuestion = input('Enter The New Question: ')
                        if newQuestion.lower() == 'c':
                            prof_issue_assignment()
                            break
                        if newQuestion != '':
                            break
                print()
                # GET THE INFORMATION FOR THE MULTIPLE CHOICE
                answer_choices = ['a.','b.','c.','d.']
                prompt_answers = {}
                for choice in answer_choices:
                    while True:
                        assigned_ans_prompt = input(f'{choice}:')
                        if assigned_ans_prompt != '':
                            break
                    if assigned_ans_prompt.lower() == 'c':
                        ProfessorMenu(prof_name)
                    prompt_answers.update({choice: assigned_ans_prompt})
                prompt_ans_to_store = f"a. {prompt_answers['a.']}\nb. {prompt_answers['b.']}\nc. {prompt_answers['c.']}\nd. {prompt_answers['d.']}"
                # GET THE CORRECT ANSWER
                while True:
                    print()
                    correct_answer = input("Enter The Correct Answer: ").lower()
                    correct_answer += '.'
                    if correct_answer not in answer_choices:
                        print("Invalid Choice. Enter a,b,c, or d")
                    else:
                        break
                while True:
                    print()
                    confirmation = input('CONFIRMATION: Are You Sure You Want To Change This Question Type? ').lower()
                    if confirmation in ['yes', 'no']:
                        break
                if confirmation == 'yes':
                    if changeQuestion == 'yes':
                        # UPDATE QUESTION
                        sql = 'UPDATE assignments SET questions = %s WHERE question_num = %s AND id = %s'
                        val = (newQuestion, question_num, assign_id)
                        db.execute(sql, val)
                        mydb.commit()

                    # ADD THE ENTRIES FOR MULTIPLE CHOICE
                    columsToChange = {
                        'answer_prompts_num': question_num,
                        'answer_prompts': prompt_ans_to_store,
                        'correct_answer_num': question_num,
                        'correct_answer': correct_answer,
                    }
                    for entry in columsToChange:
                        sql = f'UPDATE assignments SET {entry} = %s WHERE question_num = %s AND id = %s'
                        val = (columsToChange[entry], question_num, assign_id)
                        db.execute(sql, val)
                        mydb.commit()

                    while True:
                        print()
                        back = input('Question Type Changed. Press (B) To Go Back: ').lower()
                        if back == 'b':
                            prof_issue_assignment()
                            break

                elif confirmation == 'no':
                    prof_issue_assignment()

    elif editToMake == 'Add Question':
        print()
        print("ADD QUESTION")
        print("------------")
        print()
        while True:
            print()
            newQuestionType = input(f'Enter The Question Type: ').title()
            if newQuestionType.lower() == 'c':
                prof_issue_assignment()
                break
            if newQuestionType not in ['Multiple Choice', 'Short Answer']:
                print("Invalid Question Type. Enter 'Short Answer' Or 'Multiple Choice'")
            else:
                break
        if newQuestionType == 'Short Answer':
            print()
            print("LAST QUESTION")
            print("-------------")
            displayQuestion(assign_id, numQuestions, "editAssignment")
            print()
            while True:
                print()
                newShortAnsQuestion = input('Enter The New Question: ')
                if newShortAnsQuestion.lower() == 'c':
                    prof_issue_assignment()
                    break
                if newShortAnsQuestion != '':
                    break

            while True:
                print()
                confirmation = input("CONFIRMATION: Are You Sure You Want To Add This Question? ").lower()
                if confirmation in ['yes', 'no']:
                    break
            if confirmation == 'yes':
                # ADD QUESTION TO THE ASSIGNMENT
                numDatabaseColumns = 14

                sql = "INSERT INTO assignments VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                assign_id, assign_type, title, description, question_num, questions, answer_prompt_num, answer_promtps, correct_answer_num, correct_answer, prof_id, duration, due_date, course_name = [oldValue[0][i] for i in range(numDatabaseColumns)]
                val = (assign_id, assign_type, title, description, (numQuestions+1), newShortAnsQuestion, answer_prompt_num, answer_promtps, correct_answer_num, correct_answer, prof_id, duration, due_date, course_name)
                db.execute(sql, val)
                mydb.commit()
                while True:
                    print()
                    back = input("Short Answer Question Added. Press (B) to Go Back:").lower()
                    if back == 'b':
                        prof_issue_assignment()
                        break
            elif confirmation == 'no':
                prof_issue_assignment()
 
        elif newQuestionType == 'Multiple Choice':
            print()
            print("LAST QUESTION")
            print("-------------")
            displayQuestion(assign_id, numQuestions, "editAssignment")
            print()
            while True:
                print()
                newMultipleChoiceQuestion = input('Enter The New Question: ')
                if newMultipleChoiceQuestion.lower() == 'c':
                    prof_issue_assignment()
                    break
                if newMultipleChoiceQuestion != '':
                    break

            answer_choices = ['a.','b.','c.','d.']
            tmp_prompt_answer = {}

            for choice in answer_choices:
                while True:
                    assigned_ans_prompt = input(f"{choice.replace('.', '')}: ")
                    if assigned_ans_prompt != '':
                        break
                    if assigned_ans_prompt.lower() == 'c':
                        prof_issue_assignment()
                        break
                tmp_prompt_answer.update({choice: assigned_ans_prompt})

            print()   
            while True:
                newCorrectAnswer = input("Enter The Correct Answer: ").lower()
                newCorrectAnswer += '.'
                if newCorrectAnswer not in answer_choices:
                    print("Invalid Correct Answer. Enter a,b,c or d")
                else:
                    break

            # STORE ALL THE PROMPT ANSWERS
            prompt_ans_to_store = f"a. {tmp_prompt_answer['a.']}\nb. {tmp_prompt_answer['b.']}\nc. {tmp_prompt_answer['c.']}\nd. {tmp_prompt_answer['d.']}"

            while True:
                print()
                confirmation = input("CONFIRMATION: Are You Sure You Want To Add This Question? ").lower()
                if confirmation in ['yes', 'no']:
                    break

            if confirmation == 'yes':
                # ADD QUESTION TO THE ASSIGNMENT
                numDatabaseColumns = 14

                sql = "INSERT INTO assignments VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                assign_id, assign_type, title, description, question_num, questions, answer_prompt_num, answer_promtps, correct_answer_num, correct_answer, prof_id, duration, due_date, course_name = [oldValue[0][i] for i in range(numDatabaseColumns)]
                val = (assign_id, assign_type, title, description, (numQuestions+1), newMultipleChoiceQuestion, (numQuestions+1), prompt_ans_to_store, (numQuestions+1), newCorrectAnswer, prof_id, duration, due_date, course_name)
                db.execute(sql, val)
                mydb.commit()
                while True:
                    print()
                    back = input("Multiple Choice Question Added. Press (B) to Go Back:").lower()
                    if back == 'b':
                        prof_issue_assignment()
                        break
            elif confirmation == 'no':
                prof_issue_assignment()

    elif editToMake == 'Delete Question':
        print()
        print("DELETE QUESTION")
        print("---------------")
        while True:
            print()
            questionNumToDelete = input("Enter The Question Number: ")
            if questionNumToDelete not in [str(i+1) for i in range(numQuestions)]:
                print("Invalid Question Number")
            else:
                break
        displayQuestion(assign_id, int(questionNumToDelete), 'editAssignment')
        print()
        while True:
            print()
            confirmation = input("CONFIRMATION: Are You Sure Want To Delete This Question? ")
            if confirmation in ['yes', 'no']:
                break

        if confirmation == 'yes':
            sql = "DELETE FROM assignments WHERE question_num = %s AND id = %s"
            val = (int(questionNumToDelete), assign_id)
            db.execute(sql, val)
            mydb.commit()

            while True:
                print()
                back = input("Question Deleted. Press (B) To Go Back: ").lower()
                if back == 'b':
                    prof_issue_assignment()
                    break
        elif confirmation == 'no':
            prof_issue_assignment()


    # REGULAR EDITS
    print()
    print(f"EDIT {editToMake.upper()}")
    print('-----' + '-'*len(editToMake))
    while True:
        print()
        newEdit = input(f"Enter The New {editToMake}: ")
        if newEdit.lower() == 'c':
            prof_issue_assignment()
            break
        if newEdit == oldValue:
            print(f"That Is Already The Name Of The {editToMake}")
            print()
        if newEdit != oldValue and newEdit != '':
            break
    # CONFIRMATION
    while True:
        print()
        confirmation = input(f"CONFIRMATION: Are You Sure You Want To Edit The {editToMake} Of This Assignment? ").lower()
        if confirmation == "yes" or confirmation == "no":
            break
    if confirmation == "yes":
        sql = f"UPDATE assignments SET {columnName} = %s WHERE id = %s"
        val = (newEdit, assign_id)
        db.execute(sql, val)
        mydb.commit()
        while True:
            print()
            back = input(f"Assignment {editToMake} Changed. Press (B) To Go Back: ").lower()
            if back == "b":
                prof_issue_assignment()
                break
    else:
        prof_issue_assignment()

def displayQuestion(assign_id: int, question_num: int, calledFrom):
    if questionIsShortAnswer(assign_id, question_num):
        sql = "SELECT questions FROM assignments WHERE question_num = %s AND id = %s"
        val = (question_num, assign_id)
        db.execute(sql, val)
        results = db.fetchall()
        if len(results) == 0:
            errorLoadingQuestion(calledFrom)
        Question = results[0][0]
        print()
        print(f'{question_num}.{Question}')
        
    else:
        sql = 'SELECT questions, answer_prompts, correct_answer FROM assignments WHERE question_num = %s AND id = %s'
        val = (question_num, assign_id)
        db.execute(sql, val)
        results = db.fetchall()
        if len(results) == 0:
            errorLoadingQuestion(calledFrom)
        Question = results[0][0]
        answerPromtps = results[0][1]
        correctAnswer = results[0][2]
        print()
        print(f'{question_num}.{Question}')
        print(answerPromtps)
        print(f'Correct Answer: {correctAnswer}')
        



def errorLoadingQuestion(calledFrom):
    while True:
        print()
        error = input('Error Displaying Question. Press (B) To Go Back').lower()
        if error == 'b':
            if calledFrom == 'editAssignment':
                prof_issue_assignment()
                break

# DELETE ASSIGNMENT
def delete_assignment(assignment_title):
    while True:
        print()
        confirmation = input(f"CONFIRMATION: Are You Sure You Want To Delete ({assignment_title})? ").lower()
        if confirmation == "yes" or confirmation == "no":
            break
    if confirmation == "yes":
        sql = "DELETE FROM assignments WHERE title = %s"
        val = (assignment_title,)
        db.execute(sql, val)
        mydb.commit()
        while True:
            print()
            back = input("Assignment Deleted. Press (B) To Go Back: ").lower()
            if back == "b":
                prof_issue_assignment()
                break
    elif confirmation == "no":
        prof_issue_assignment()


# ASSIGNMENT IS SHORT ANSWER
def assignmentIsShortAnswer(assign_info):
    for i in range(len(assign_info)):
        if assign_info[i][6] != None and assign_info[i][7] != None and assign_info[i][8] != None and assign_info[i][9] != None:
            return False
    return True
def assignmentIsMixed(assign_info):
    multiple_choice_questions = 0
    short_ans_questions = 0
    for i in range(len(assign_info)):
        if assign_info[i][6] != None and assign_info[i][7] != None and assign_info[i][8] != None and assign_info[i][9] != None:
            multiple_choice_questions += 1
        else:
            short_ans_questions += 1
    return multiple_choice_questions != 0 and short_ans_questions != 0
def assignmentIsMultipleChoice(assign_info):
    for i in range(len(assign_info)):
        if assign_info[i][6] == None and assign_info[i][7] == None and assign_info[i][8] == None and assign_info[i][9] == None:
            return False
    return True


# UNABLE TO OPEN ASSIGNMENT
def unable_to_open_assign():
    while True:
        print()
        error = input("Unable To Load Assignment. Press (B) To Go Back: ")
        if error == 'b':
            prof_issue_assignment()
            break

# STUDENT MENU
def StudentMenu(name):
    update_student_grades()
    clear()
    print("STUDENT MENU")
    if name != None:
        print(f"Welcome {name}")

    # GET THE AMOUNT OF MESSAGES IN INBOX
    Stu = Student(stu_name.split()[0], stu_name.split()[1], None, None, None, None, None, None)
    sql = "SELECT COUNT(*) FROM student_notification WHERE stu_id = %s"
    val = (Stu.getID(), )
    db.execute(sql, val)
    inbox_count = db.fetchall()[0][0]
    print(now)
    print("------------------------------")
    print("Press (L) To Log Out")
    print("Press (S) To Send Notification")
    print("Press (I) To Open Inbox")
    print("------------------------------")
    print()
    print(f"INBOX: {inbox_count}")
    print()
    print("AVAILABLE OPTIONS")
    print()
    print("1 - View Profile")
    print("2 - View All Courses")
    print("3 - View All Majors")

    print()
    while True:
        stu_choice = input("Choose An Option: ").lower()
        if stu_choice != '':
            break

    if stu_choice == "l":
        login()
    elif stu_choice == "s":
        stu_send_notification()
    elif stu_choice == "i":
        student_inbox()
    elif stu_choice == "1":
        view_student_profile()
    elif stu_choice == "2":
        view_all_courses_stu()
    elif stu_choice == "3":
        view_all_majors("Student")


# VIEW STUDENT PROFILE
def view_student_profile():
    clear()
    sql = "SELECT * FROM Student WHERE name = %s"
    val = (stu_name, )
    db.execute(sql, val)
    result = db.fetchall()[0]
    try:
        Stu = Student(result[1].split()[0], result[1].split()[1], result[2], result[4], result[5], result[6], result[7], result[8])
    except IndexError:
        print("-----")
        print("ERROR")
        print("-----")
        print("An Error Occurred. The Program Will End In A Few Seconds.. Please Restart.")
        from time import sleep
        sleep(2.5)
        exit()




    print("<" * (len(Stu.getAddress()) // 2), "PROFILE", ">" * (len(Stu.getAddress()) // 2 + 1))

    print("-" * len(Stu.getAddress()) + "---------")
    print()
    print(f"Id: {Stu.getID()}")
    print(f"Name: {Stu.getFullName()}")
    print(f"Address: {Stu.getAddress()}")
    print(f"Email: {Stu.getEmail()}")
    print(f"Age: {Stu.getAge()}")
    print(f"Phone Number: {Stu.getPhoneNumber()}")
    print(f"Courses Enrolled In: {Stu.getCoursesEnrolledIn().split() if result[6] != None else Stu.getCoursesEnrolledIn()}")
    print(f"Grades: ", [Stu.getGrades().split()[i+i] + " " + Stu.getGrades().split()[i+i+1] for i in range(len(Stu.getGrades().split()) // 2)] if result[7] != None else Stu.getGrades())
    print(f"GPA: {Stu.getGPA() if Stu.getGrades() != None else None}")
    print(f"Major: {Stu.getMajor()}")
    print("-" * len(Stu.getAddress()) + "---------")
    print()
    while True:
        back = input("Press (C) To Change Your Password:\n"
                     "Press (D) To Drop A Class:\n"
                     "Press (R) To Request Major Change:\n"
                     "Press (V) To View Grade Book:\n"
                     "Press (M) To Return To Student Menu: ").lower()
        if back == "m":
            StudentMenu(Stu.getFullName())
        elif back == "r":
            request_major_change(Stu.getID(), Stu.getFullName(), Stu.getMajor())
        elif back == "v":
            student_view_grade_book(Stu.getID())
        elif back == "d":
            drop_class(Stu.getID(), Stu.getCoursesEnrolledIn())
        elif back == "c":
            change_student_password(stu_name, Stu.getID())


# CHANGE STUDENT PASSWORD
def change_student_password(stu_name, stu_id):
    clear()
    print("CHANGE STUDENT PASSWORD")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    while True:
        print()
        pre_password = getpass("Enter Your Previous Password: ")
        if pre_password != stu_password:
            print("Passwords Don't Match")
        else:
            break

    while True:
        print()
        new_pwd = getpass("Enter Your New Password: ")
        if new_pwd != '':
            break

    # CHECKING IF C WAS ENTERED
    if len(new_pwd) == 1:
        new_pwd = new_pwd.lower()
    if new_pwd == "c":
        StudentMenu(stu_name)
    new_pwd = sanitize_password(new_pwd, stu_name)

    confirm_new_pwd = getpass("Confirm Your Password: ")

    if new_pwd != confirm_new_pwd:
        confirm_new_pwd = confirm_password_error(stu_name)

    confirm_new_pwd = hash_password(confirm_new_pwd)

    # CHANGE PASSWORD
    sql = "UPDATE Student SET password = %s WHERE id = %s"
    val = (confirm_new_pwd, stu_id)

    db.execute(sql, val)
    mydb.commit()

    print()
    while True:
        back = input("Your Password Has Been Changed. Press (B) To Go Back: ").lower()
        if back == "b":
            StudentMenu(stu_name)

# VIEW GRADE BOOK
def student_view_grade_book(stu_id):
    clear()
    print("---------------")
    print("YOUR GRADE BOOK")
    print("---------------")
    print()
    sql = "SELECT * FROM grade_book WHERE stu_id = %s"
    val = (stu_id,)
    db.execute(sql, val)
    results = db.fetchall()
    grade_book = {}
    course_names = [results[i][2] for i in range(len(results))]
    course_grades = [results[i][3:] for i in range(len(results))]

    for i in range(len(course_names)):
        grade_book.update({course_names[i]: course_grades[i]})

    for grade in grade_book:
        print(f"{grade} |GRADE-1|GRADE-2|GRADE-3|GRADE-4|GRADE-5|AVG")
        grades_to_avg = [grade for grade in grade_book[grade] if grade != None]
        stu_avg = compute_average(grades_to_avg)

        print(f" " * (len(grade) + 1) + f"{[grade_book[grade][i] for i in range(len(grade_book[grade]))]} {stu_avg}%")
        print()

    while True:
        print()
        back = input("Press (B) To Go Back: ").lower()
        if back == "b":
            view_student_profile()
            break
# STUDENT INBOX
def student_inbox():
    clear()
    print("----------")
    print("YOUR INBOX")
    print("----------")
    print(now)
    print()
    Stu = Student(stu_name.split()[0], stu_name.split()[1], None, None, None, None, None, None)

    sql = "SELECT id, notification, received_from, date FROM student_notification WHERE stu_id = %s"
    val = (Stu.getID(), )
    db.execute(sql, val)
    all_notifications = db.fetchall()

    if len(all_notifications) == 0:
        print("No Notifications")

    terminal_size = os.get_terminal_size().columns
    for i in range(len(all_notifications)):
        # AUTO FIT THE BROKEN LINES
        message_len = len(all_notifications[i][1]) + len('Message: ')
        received_from_len = len(all_notifications[i][2]) + len('Received From: ')

        max_len_of_attributes = max([message_len, received_from_len])

        if max_len_of_attributes > terminal_size:
            broken_line_added = '-' * terminal_size
        else:
            if max_len_of_attributes == message_len:
                broken_line_added = '-' * message_len
            else:
                broken_line_added = '-' * received_from_len

        print(broken_line_added)
        print(f"Id: {all_notifications[i][0]}")
        print(f"Date: {all_notifications[i][3]}")
        print(f"Received From: {all_notifications[i][2]}")
        print(f"Message: {all_notifications[i][1]}")
        print(broken_line_added)
        print()

    while True:
        print()
        print("Press (CON) To View All Conversations: ")
        print("Press (O) To Open A Notification: ")
        print()
        print("Press (D) To Filter By Date:              |  Press (C) To Clear A Notification:")
        print("Press (F) To Filter By Received From:     |  Press (CA) To Clear All Notifications:")
        print("Press (M) To Filter By Message:           |  Press (S) To Return To Student Menu:")
        print()
        filter = input("Choose An Option: ")
        if filter == "con":
            view_all_conversations(stu_name, 'Student')
        elif filter == "o":
            open_stu_notification(all_notifications)
            break
        elif filter == "d":
            filter_stu_notification_by_date(all_notifications)
            break
        elif filter == "f":
            filter_stu_notification_by_received_from(all_notifications)
            break
        elif filter == "m":
            filter_stu_notification_by_message(all_notifications)
            break
        elif filter == "c":
            clear_student_notification()
            break
        elif filter == "ca":
            clear_all_student_notifications(Stu.getID())
            break
        elif filter == "s":
            StudentMenu(None)
            break

# VIEW CONVERSATIONS
def view_all_conversations(name, user):
    clear()
    print("-------------")
    print("CONVERSATIONS")
    print("-------------")
    print()
    sql =  "SELECT convoId, date FROM Conversations WHERE senderName = %s"
    val = (name, )
    db.execute(sql,val)
    results = db.fetchall()
    if len(results) == 0:
        print("No Conversations")

    results = removeDuplicates(results)
    all_convo = {}


    for i, convoInfo in enumerate(results,1):
        all_convo.update({str(i): convoInfo[0]})
        print("-"*len(convoInfo[0]) + "----")
        print(f'    {convoInfo[1]}')
        print(f'{i} - {convoInfo[0]}')
        print("-" * len(convoInfo[0]) + "----")
        print()

    while True:
        print()
        back = input("Press (O) To Open A Conversation:\nPress (B) To Go Back: ").lower()
        if back == "o" or back == "b":
            break

    if back == "o":
        while True:
            print()
            convo_look_up = input("Enter The ID Of The Conversation: ")
            all_possible_id = [str(i+1) for i in range(len(all_convo))]
            if convo_look_up not in all_possible_id:
                print("Invalid ID")
                print()
            else:
                if convo_look_up.lower() == 'b':
                    break
                break
        print()
        convo_view(all_convo[convo_look_up], user, True)

    if back == "b":
        if user == 'Student':
            student_inbox()
        elif user == 'Professor':
            professor_inbox()
        elif user == 'Dean':
            dean_inbox()






# OPEN NOTIFICATION
def open_stu_notification(notification):
    all_possible_id = [str(notification[i][0]) for i in range(len(notification))]
    print()
    while True:
        noti_id = input("Enter The Id Of The Notification: ")
        if noti_id not in all_possible_id:
            print("Invalid Id")
        else:
            break
    sql = "SELECT id, notification, received_from, date FROM student_notification WHERE id = %s"
    val = (int(noti_id),)
    db.execute(sql, val)
    notification_to_open = db.fetchall()
    clear()
    # AUTO FIT THE BROKEN LINES
    max_len_of_attributes = max([len(notification_to_open[0][1]), len(notification_to_open[0][2])])
    if max_len_of_attributes == len(notification_to_open[0][1]):
        broken_line_added = "-" * len("Message: ")
    else:
        broken_line_added = "-" * len("Received From: ")

    message = notification_to_open[0][1]
    received_from = notification_to_open[0][2]
    print("-" * max_len_of_attributes + broken_line_added)
    print(f"Id: {notification_to_open[0][0]}")
    print(f"Date: {notification_to_open[0][3]}")
    print(f"Received From: {notification_to_open[0][2]}")
    print(f"Message: {notification_to_open[0][1]}")
    print("-" * max_len_of_attributes + broken_line_added)
    print()

    print("Press (R) To Respond:")
    if "Test" in message or "Quiz" in message or "Exam" in message:
        assignment = True
        print("Press (S) To Begin:")
    else:
        assignment = False
    while True:
        back = input("Press (B) To Go Back: ").lower()
        if back == "r":
            receiverName = extractNameFromNotification(received_from)["receiverName"]
            receiverType = extractNameFromNotification(received_from)["Type"]

            if receiverName == None:
                if receiverType == "Dean":
                    respondToNotification(stu_name, "Student", receiverType, receiverName, message)
                while True:
                    print()
                    error = input("Unable To Respond: Please Contact The Dean. Press (B) To Go Back: ").lower()
                    if error == "b":
                        student_inbox()
                        break
            else:
                respondToNotification(stu_name, "Student", receiverType, receiverName, message)
        elif back == "s" and assignment:
            assignment_id = message.split()[-1]
            take_assign(assignment_id)
            break

        elif back == "b":
            student_inbox()
            break

# TAKE ASSIGNMENT
def take_assign(assignment_id):
    clear()
    stu_id = get_student_id(stu_name)

    sql = "SELECT * FROM assignments WHERE id = %s"
    val = (assignment_id,)
    db.execute(sql, val)
    results = db.fetchall()
    if len(results) == 0:
        assignment_no_longer_available()
    assign_type = results[0][1]
    title = results[0][2]
    description = results[0][3]
    duration = results[0][11]
    due_date = results[0][12]
    course_name = results[0][13]
    prof_id = results[0][10]

    num_assign_questions = len(results)

    # CHECKING IF THE DUE DATE HAS PASSED
    if isDue(due_date):
        while True:
            print("---------------")
            print("DUE DATE PASSED")
            print("---------------")
            print()
            print(f"Due Date: {due_date}")
            print()
            back = input("The Due Date For This Assignment Has Passed. Press (B) To Go Back: ").lower()
            if back == "b":
                student_inbox()
                break

    # THE ASSIGNMENT IS SHORT ANSWER
    if assignmentIsShortAnswer(results):
        print(f"<<<<<<<<<< {title} >>>>>>>>>>")
        print()
        print(f"Duration: {duration} Mins")
        print(f"Due Date: {due_date}")
        print(f"Number Of Questions: {num_assign_questions}")
        print()
        if description != None:
            print("-" * len(description))
            print(description)
            print("-" * len(description))
            print()

        student_answers = {}

        for i in range(num_assign_questions):
            print(f"{i + 1}.{results[i][5]}")
            while True:
                answer = input("Answer: ")
                if answer != '':
                    break
            student_answers.update({i + 1: answer})
            print()

        answers_to_add_to_db = ""
        for ans in student_answers:
            answers_to_add_to_db += f"{ans}.{student_answers[ans]}\n"
            answers_to_add_to_db += "\n"

        # SEND ASSIGNMENT TO PROFESSOR
        notification = f"{stu_name}({stu_id}) Submitted {title} ID: {assignment_id}"
        received_from = f"Student ({stu_name})"

        sql = "INSERT INTO professor_notification (notification, received_from, date, prof_id) VALUES (%s, %s, %s, %s)"
        val = (notification, received_from, now, prof_id)
        db.execute(sql, val)
        mydb.commit()

        # ADD ASSIGNMENT TO DATABASE
        sql = "INSERT INTO assignment_submissions (stu_id, assignment_id, answers) VALUES (%s, %s, %s)"
        val = (stu_id, assignment_id, answers_to_add_to_db)
        db.execute(sql, val)
        mydb.commit()

        while True:
            print()
            back = input("Assignment Complete. Press (M) To Return To Student Menu: ").lower()
            if back == "m":
                StudentMenu(stu_name)
                break

    # THE ASSIGNMENT IS MULTIPLE CHOICE
    
    elif assignmentIsMultipleChoice(results):
        # RETRIEVE THE CORRECT ANSWERS
        assign_answers = {}
        for i in range(len(results)):
            assign_answers.update({results[i][8]: results[i][9]})
        print(f"<<<<<<<<<< {title} >>>>>>>>>>")
        print()
        print(f"Duration: {duration} Mins")
        print(f"Due Date: {due_date}")
        print(f"Number Of Questions: {num_assign_questions}")
        print()
        if description != None:
            print("-" * len(description))
            print(description)
            print("-" * len(description))
            print()

        student_answers = {}

        for i in range(num_assign_questions):
            print(f"{i + 1}.{results[i][5]}")
            print(results[i][7])
            while True:
                answer = input("Answer: ")
                if answer in ['a', 'b', 'c', 'd']:
                    break
            student_answers.update({i + 1: answer})
            print()

        grade = checkAssignment(assign_answers, student_answers, num_assign_questions)[0]
        stu_correct_answers = checkAssignment(assign_answers, student_answers, num_assign_questions)[1]
        stu_incorrect_answers = checkAssignment(assign_answers, student_answers, num_assign_questions)[2]
        print()
        print(f"<<<<<<<<<< RESULT >>>>>>>>>>")
        print()
        print(f"GRADE: {grade}")
        print(f"Questions You Got Correct: {stu_correct_answers}")
        print(f"Questions You Got Incorrect: {stu_incorrect_answers}")
        print()

        if assign_type == "Quiz":
            print("Press (R) To Retake Quiz:")

        while True:
            back = input("Press (M) To Return To Student Menu: ").lower()
            if back == "r" and assign_type == "Quiz":
                take_assign(assignment_id)
                break
            elif back == "m":
                # UPDATE STUDENT GRADE BOOK
                prof_name = getProfessorName(prof_id)
                assignment_grade = grade.replace(' ', '')
                update_grade_book(course_name, stu_id, assignment_grade, prof_name)

                mydb.commit()

                StudentMenu(stu_name)

    elif assignmentIsMixed(results):
        # RETRIEVE THE CORRECT ANSWERS
        assign_answers = {}
        for i in range(len(results)):
            if not questionIsShortAnswer(assignment_id, i+1):
                assign_answers.update({results[i][8]: results[i][9]})
        prof_id = results[0][10]
        print(f"<<<<<<<<<< {title} >>>>>>>>>>")
        print()
        print(f"Duration: {duration} Mins")
        print(f"Due Date: {due_date}")
        print(f"Number Of Questions: {num_assign_questions}")
        print()
        if description != None:
            print("-" * len(description))
            print(description)
            print("-" * len(description))
            print()

        shortAnswers = {}
        multipleChoiceAnswers = {}
        multiple_choice_question_count = 0


        for i in range(num_assign_questions):
            if questionIsShortAnswer(assignment_id, i+1):
                print(f"{i + 1}.{results[i][5]}")
                while True:
                    answer = input("Answer: ")
                    if answer != '':
                        break
                shortAnswers.update({i + 1: answer})
                print()
            else:
                print(f"{i + 1}.{results[i][5]}")
                print(results[i][7])
                while True:
                    answer = input("Answer: ")
                    if answer in ['a', 'b', 'c', 'd']:
                        break
                multipleChoiceAnswers.update({i + 1: answer})
                multiple_choice_question_count += 1
                print()

        grade = checkAssignment(assign_answers, multipleChoiceAnswers, multiple_choice_question_count)[0]
        stu_correct_answers = checkAssignment(assign_answers, multipleChoiceAnswers, num_assign_questions)[1]
        # stu_incorrect_answers = checkAssignment(assign_answers, multipleChoiceAnswers, num_assign_questions)[2]

        answers_to_add_to_db = ""
        for ans in shortAnswers:
            answers_to_add_to_db += f"{ans}.{shortAnswers[ans]}\n"
            answers_to_add_to_db += "\n"



        # SEND ASSIGNMENT TO PROFESSOR
        notification = f"{stu_name}({stu_id}) Submitted {title} ID: {assignment_id}"
        received_from = f"Student ({stu_name})"

        sql = "INSERT INTO professor_notification (notification, received_from, date, prof_id) VALUES (%s, %s, %s, %s)"
        val = (notification, received_from, now, prof_id)
        db.execute(sql, val)
        mydb.commit()

        # ADD ASSIGNMENT TO DATABASE
        message = f"Multiple Choice Answers: {str(multipleChoiceAnswers)} Grade: {grade}"
        sql = "INSERT INTO assignment_submissions (stu_id, assignment_id, answers, message) VALUES (%s, %s, %s, %s)"
        val = (stu_id, assignment_id, answers_to_add_to_db, message)
        db.execute(sql, val)
        mydb.commit()

        print(f"<<<<<<<<<< RESULT >>>>>>>>>>")
        print()
        print(f"MULTIPLE CHOICE GRADE: {grade}")
        print(f"You Got Correct: {len(stu_correct_answers)} Out Of {multiple_choice_question_count} Multiple Choice Questions Correct")
        while True:
            print()
            back = input("Your Short Answers Have Been Submitted. Press (M) To Return To Main Menu: ").lower()
            if back == 'm':
                StudentMenu(stu_name)

        while True:
            print()
            back = input("Assignment Complete. Press (M) To Return To Student Menu: ").lower()
            if back == "m":
                StudentMenu(stu_name)
                break

def questionIsShortAnswer(assign_id, question_num):
    sql = "SELECT * FROM assignments WHERE id = %s AND question_num = %s"
    val = (assign_id, question_num)
    db.execute(sql, val)
    results = db.fetchall()

    return results[0][6] == None and results[0][7] == None and results[0][8] == None and results[0][9] == None

def assignment_no_longer_available():
    while True:
        print()
        error = input("This Assignment Is No Longer Available. Contact The Professor.\n\nPress (B) To Go Back:").lower()
        if error == "b":
            StudentMenu(stu_name)
            break


def checkAssignment(correct_answers, student_answers, num_questions):
    correct_answers = [correct_answers[ans] for ans in correct_answers]
    student_answers = [student_answers[ans] for ans in student_answers]

    student_correct_ans   = []
    student_incorrect_ans = []
    for i in range(len(correct_answers)):
        if student_answers[i] == correct_answers[i].replace('.', ''):
            student_correct_ans.append(i+1)
        else:
            student_incorrect_ans.append(i+1)

    grade = str(int((len(student_correct_ans) / num_questions) * 100))
    grade = f"{grade} %"

    if len(student_correct_ans) == 0:
        student_correct_ans = None
    if len(student_incorrect_ans) == 0:
        student_incorrect_ans = None

    return (grade, student_correct_ans, student_incorrect_ans)
def isDue(due_date):
    all_months = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8,
                  "September": 9, "October": 10, "November": 11, "December": 12}

    try:
        today_date_day   = now.split()[1].replace(',', '')
        today_date_month = now.split()[0]
        today_date_year  = now.split()[2]

        due_date_day   = due_date.split()[1].replace(',', '')
        due_date_month = due_date.split()[0]
        due_date_year  = due_date.split()[2].replace(',', '')

        Today    = [all_months[today_date_month], today_date_day, today_date_year]
        Due_Date = [all_months[due_date_month], due_date_day, due_date_year]

        # THE YEAR HAS PASSED
        if Due_Date[2] < Today[2]:
            return True
        # MONTH HAS PASSED
        if Due_Date[0] < Today[0]:
            return True
        # DAY HAS PASSED
        if Due_Date[0] == Today[0]:
            if Due_Date[1] < Today[1]:
                return True
        return False
    except:
        return False

def update_grade_book(course_name, stu_id, assign_grade, prof_name):
    # UPDATE STUDENT GRADE BOOK
    sql = "SELECT * FROM grade_book WHERE stu_id = %s AND course_name = %s"
    val = (stu_id, course_name)
    db.execute(sql, val)
    results = db.fetchall()
    if len(results) == 0:
        results =  [None, None, None, None, None, None, None, None, None, None]
    else:
        results = results[0]

    grade_book = {
        'grade_1': results[3],
        'grade_2': results[4],
        'grade_3': results[5],
        'grade_4': results[6],
        'grade_5': results[7],
    }
    assignment_grade = assign_grade

    for grade in grade_book:
        sql = "SELECT course_name FROM grade_book WHERE course_name = %s AND stu_id = %s"
        val = (course_name, stu_id)
        db.execute(sql, val)
        results = db.fetchall()
        if len(results) != 0:
            if grade_book[grade] == None:
                sql = f"UPDATE grade_book SET {grade} = %s WHERE stu_id = %s AND course_name = %s"
                val = (assignment_grade, stu_id, course_name)
                db.execute(sql, val)
                mydb.commit()
                # SEND STUDENT A NOTIFICATION
                senderType = 'Professor'
                senderName = prof_name
                message = f"Your {course_name} Grade Has Been Updated To: {assignment_grade}"
                sql = "INSERT INTO student_notification (notification, received_from, date, stu_id) VALUES (%s, %s, %s, %s)"
                val = (message, f"{senderType} ({senderName})", now, stu_id)
                db.execute(sql, val)
                mydb.commit()
                return
        if len(results) == 0:
            sql = "INSERT INTO grade_book (stu_id, course_name, grade_1) VALUES (%s, %s, %s)"
            val = (stu_id, course_name, assignment_grade)
            db.execute(sql, val)
            mydb.commit()
             # SEND STUDENT A NOTIFICATION
            senderType = 'Professor'
            senderName = prof_name
            message = f"Your {course_name} Grade Has Been Updated To: {assignment_grade}"
            sql = "INSERT INTO student_notification (notification, received_from, date, stu_id) VALUES (%s, %s, %s, %s)"
            val = (message, f"{senderType} ({senderName})", now, stu_id)
            db.execute(sql, val)
            mydb.commit()
            return
    sql = "UPDATE grade_book SET grade_5 = %s WHERE stu_id = %s AND course_name = %s"
    val = (assignment_grade, stu_id, course_name)
    db.execute(sql, val)
    mydb.commit()
     # SEND STUDENT A NOTIFICATION
    senderType = 'Professor'
    senderName = prof_name
    message = f"Your {course_name} Grade Has Been Updated To: {assignment_grade}"
    sql = "INSERT INTO student_notification (notification, received_from, date, stu_id) VALUES (%s, %s, %s, %s)"
    val = (message, f"{senderType} ({senderName})", now, stu_id)
    db.execute(sql, val)
    mydb.commit()


# FILTER STUDENT NOTIFICATIONS
def filter_stu_notification_by_date(notifications):
    while True:
        print()
        date_to_filter = input("Enter The Date: ")
        if date_to_filter != '':
            break

    clear()
    total_found = 0
    print("-" * len(date_to_filter) + "--------------")
    print(f"Filtered by: {date_to_filter}")
    print("-" * len(date_to_filter) + "--------------")
    print()
    for i in range(len(notifications)):
        if date_to_filter in notifications[i][3]:
            print("-" * len(notifications[i][1]) + "---------")
            print(f"Id: {notifications[i][0]}")
            print(f"Date: {notifications[i][3]}")
            print(f"Received From: {notifications[i][2]}")
            print(f"Message: {notifications[i][1]}")
            print("-" * len(notifications[i][1]) + "---------")
            print()
            total_found += 1

    if total_found == 0:
        print()
        print("No Notifications Found")

    while True:
        print()
        back = input("Press (F) To Filter Again:\nPress (C) To Clear A Notification:\nPress (S) To Return To Student Menu: ").lower()
        if back == "f":
            student_inbox()
        if back == "c":
            clear_student_notification()
        elif back == "s":
            StudentMenu(None)
def filter_stu_notification_by_received_from(notifications):
    while True:
        print()
        person_to_filter = input("Enter The Name: ")
        person_to_filter = capitalize(person_to_filter)
        if person_to_filter != '':
            break

    clear()
    total_found = 0
    print("-" * len(person_to_filter) + "--------------")
    print(f"Filtered by: {person_to_filter}")
    print("-" * len(person_to_filter) + "--------------")
    print()
    for i in range(len(notifications)):
        if person_to_filter in notifications[i][2]:
            print("-" * len(notifications[i][1]) + "---------")
            print(f"Id: {notifications[i][0]}")
            print(f"Date: {notifications[i][3]}")
            print(f"Received From: {notifications[i][2]}")
            print(f"Message: {notifications[i][1]}")
            print("-" * len(notifications[i][1]) + "---------")
            print()
            total_found += 1

    if total_found == 0:
        print()
        print("No Notifications Found")

    while True:
        print()
        back = input("Press (F) To Filter Again:\nPress (C) To Clear A Notification:\nPress (S) To Return To Student Menu: ").lower()
        if back == "f":
            student_inbox()
        elif back == "c":
            clear_student_notification()
        elif back == "s":
            StudentMenu(None)
def filter_stu_notification_by_message(notifications):
    while True:
        print()
        message_to_filter = input("Enter The Message: ")
        if message_to_filter != '':
            break

    clear()
    total_found = 0
    print("-" * len(message_to_filter) + "--------------")
    print(f"Filtered by: {message_to_filter}")
    print("-" * len(message_to_filter) + "--------------")
    print()
    for i in range(len(notifications)):
        if message_to_filter in notifications[i][1]:
            print("-" * len(notifications[i][1]) + "---------")
            print(f"Id: {notifications[i][0]}")
            print(f"Date: {notifications[i][3]}")
            print(f"Received From: {notifications[i][2]}")
            print(f"Message: {notifications[i][1]}")
            print("-" * len(notifications[i][1]) + "---------")
            print()
            total_found += 1

    if total_found == 0:
        print()
        print("No Notifications Found")

    while True:
        print()
        back = input("Press (F) To Filter Again:\nPress (C) To Clear A Notification:\nPress (S) To Return To Student Menu: ").lower()
        if back == "f":
            student_inbox()
        elif back == "c":
            clear_student_notification()
        elif back == "s":
            StudentMenu(None)
def clear_student_notification():
    while True:
        print()
        notification_id = input("Enter The Id Of The Notification: ")
        if notification_id != '' and notification_id.isdigit():
            break

    while True:
        print()
        confirmation = input("CONFIRMATION: Are You Sure You Want To Clear This Notifications? ")
        if confirmation != '' and (confirmation == "yes" or confirmation == "no"):
            break

    if confirmation == "yes":
        sql = "DELETE FROM student_notification WHERE id = %s"
        val = (int(notification_id), )
        db.execute(sql, val)
        mydb.commit()

        while True:
            print()
            back = input("Notification Deleted. Press (M) To Return To Student Menu: ").lower()
            if back == "m":
                StudentMenu(None)
    else:
        StudentMenu(None)

def clear_all_student_notifications(stu_id):
    while True:
        print()
        confirmation = input("CONFIRMATION: Are You Sure You Want To Clear All Notifications? ")
        if confirmation != '' and (confirmation == "yes" or confirmation == "no"):
            break

    if confirmation == "yes":
        sql = "DELETE FROM student_notification WHERE stu_id = %s"
        val = (stu_id, )
        db.execute(sql, val)
        mydb.commit()

        while True:
            print()
            back = input("All Notifications Cleared. Press (M) To Return To Student Menu: ").lower()
            if back == "m":
                StudentMenu(None)
    else:
        StudentMenu(None)

# REQUEST MAJOR CHANGE
def request_major_change(student_id, student_name, current_major):
    clear()
    print("REQUEST MAJOR CHANGE")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    print(f"CURRENT MAJOR: {current_major}")
    print()
    while True:
        new_major = input("Major Request: ")
        if new_major != '':
            break
    # CHECKING IF C WAS ENTERED
    if len(new_major) == 1:
        new_major = new_major.lower()
    if new_major == "c":
        StudentMenu(student_name)

    new_major = capitalize(new_major)
    if not Student.checkIfMajorIsAvailableToSet(new_major):
        while True:
            print()
            error = input("Invalid Major. Press (T) To Try Again:\n"
                          "               Press (S) To See All Majors:\n"
                          "               Press (M) To Return To Student Menu: ").lower()
            if error == "t":
                request_major_change(student_id, student_name, current_major)
            elif error == "s":
                view_all_majors("Student")
            elif error == "m":
                StudentMenu(None)

    if new_major == current_major:
        while True:
            print()
            error = input("You Are Already In That Major. Press (T) To Try Again:\n"
                          "                               Press (M) To Return To Student Menu: ").lower()
            if error == "t":
                request_major_change(student_id, student_name, current_major)
            elif error == "m":
                StudentMenu(None)

    # REASON
    while True:
        reason = input("What Is Your Reason For Wanting To Change Major? ")
        if reason != '':
            break
    # CHECKING IF C WAS ENTERED
    if len(reason) == 1:
        reason = reason.lower()
    if reason == "c":
        StudentMenu(student_name)

    # CONFIRMATION
    while True:
        print()
        confirmation = input("CONFIRMATION: Are You Sure You Want To Request A Major Change? ").lower()
        if confirmation != '' and (confirmation == "yes" or confirmation == "no"):
            break

    if confirmation == "yes":
        # SET UP NOTIFICATION
        notification = f"Requesting Major Change From {current_major} To {new_major} Because: {reason}"
        received_from = f"Student ({student_name})"
        date = now
        stu_id = student_id

        sql = "INSERT INTO dean_notification (notification, received_from, date, person_id) VALUES (%s, %s, %s, %s)"
        val = (notification, received_from, date, stu_id)
        db.execute(sql, val)
        mydb.commit()

        while True:
            print()
            back = input("Your Request Has Been Successfully Sent. Press (M) To Return To Student Menu: ").lower()
            if back == "m":
                StudentMenu(student_name)

    else:
        StudentMenu(student_name)


# STU SEND NOTIFICATION
def stu_send_notification():
    clear()
    print("SEND NOTIFICATION")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    while True:
        print()
        to = input("To (Dean, Professor, Or Student): ").capitalize()
        if to == "C":
            StudentMenu(None)
            break
        if to != '' and (to == "Student" or to == "Professor" or to == "Dean"):
            break
        if to == '' or (to != "Student" or to != "Professor" or to != "Dean"):
            print("Messages Can Only Be Sent To: Dean, Professor Or Student")

    # STUDENT
    if to == "Student":
        while True:
            print()
            student_name = capitalize(input("Enter The Name Of The Student: "))
            if student_name.lower() == "c":
                StudentMenu(None)
            if student_name != '':
                break
        sql = "SELECT id FROM Student WHERE name = %s"
        val = (student_name, )
        db.execute(sql, val)
        stu_id = db.fetchall()
        if len(stu_id) == 0:
            no_person_found("Notification", "Stu", "Send_To_Stu")
        stu_id = stu_id[0][0]

        while True:
            message = input("Message: ")
            if message != '':
                break

        # CONFIRMATION
        while True:
            print()
            confirmation = input("CONFIRMATION: Are You Sure You Want To Send This Message? ").lower()
            if confirmation == "yes" or confirmation == "no":
                break

        if confirmation == "yes":
            # CREATE CONVERSATION
            conversationInfo = {
                'convoId': f'{stu_name}(Student) To {student_name}(Student)',
                'date': now,
                'senderType': "Student",
                'senderName': stu_name,
                'preMessage': None,
                'senderMessage': message,
                'receivedFrom': None
            }
            createConversation(conversationInfo)

            # SET UP NOTIFICATION
            sql = "INSERT INTO student_notification (notification, received_from, date, stu_id) VALUES (%s, %s, %s, %s)"
            val = (message, f"Student ({stu_name})", now, stu_id)
            db.execute(sql, val)
            mydb.commit()

            while True:
                print()
                back = input("Your Message Has Been Sent. Press (S) To Send Another Message:\n"
                             "                            Press (M) To Return To Student Menu: ").lower()
                if back == "s":
                    stu_send_notification()
                elif back == "m":
                    StudentMenu(stu_name)
        elif confirmation == "no":
            StudentMenu(stu_name)

    # PROFESSOR
    elif to == "Professor":
        while True:
            print()
            professor_name = capitalize(input("Enter The Name Of The Professor: "))
            if professor_name.lower() == "c":
                StudentMenu(None)
            if professor_name != '':
                break
        sql = "SELECT id FROM Professor WHERE name = %s"
        val = (professor_name, )
        db.execute(sql, val)
        prof_id = db.fetchall()
        if len(prof_id) == 0:
            no_person_found("Notification", "Stu", "Send_To_Prof")
        prof_id = prof_id[0][0]

        while True:
            message = input("Message: ")
            if message != '':
                break

        # CONFIRMATION
        while True:
            print()
            confirmation = input("CONFIRMATION: Are You Sure You Want To Send This Message? ").lower()
            if confirmation == "yes" or confirmation == "no":
                break
        if confirmation == "yes":
            # CREATE CONVERSATION
            conversationInfo = {
                'convoId': f'{stu_name}(Student) To {professor_name}(Professor)',
                'date': now,
                'senderType': "Student",
                'senderName': stu_name,
                'preMessage': None,
                'senderMessage': message,
                'receivedFrom': None
            }
            createConversation(conversationInfo)
            # SET UP NOTIFICATION
            sql = "INSERT INTO professor_notification (notification, received_from, date, prof_id) VALUES (%s, %s, %s, %s)"
            val = (message, f"Student ({stu_name})", now, prof_id)
            db.execute(sql, val)
            mydb.commit()

            while True:
                print()
                back = input("Your Message Has Been Sent. Press (S) To Send Another Message:\n"
                             "                            Press (M) To Return To Student Menu: ").lower()
                if back == "s":
                    stu_send_notification()
                    break
                elif back == "m":
                    StudentMenu(None)
                    break
        elif confirmation == "no":
            StudentMenu(stu_name)

    # DEAN
    elif to == "Dean":
        while True:
            print()
            deanName = capitalize(input("Enter The Name Of The Dean: "))
            if deanName.lower() == "c":
                StudentMenu(None)
            if deanName != '':
                break
        # CHECKING IF CORRECT NAME WAS ENTERED
        sql = "SELECT * FROM Dean WHERE name = %s"
        val = (deanName,)
        db.execute(sql, val)
        result = db.fetchall()
        if len(result) == 0:
            no_person_found("Notification", "Stu", "Send_To_Dean")

        # GETTING THE ID OF THE STUDENT
        sql = "SELECT id FROM Student WHERE name = %s"
        val = (stu_name, )
        db.execute(sql, val)
        stu_id = db.fetchall()[0][0]

        while True:
            message = input("Message: ")
            if message != '':
                break

        # CONFIRMATION
        while True:
            print()
            confirmation = input("CONFIRMATION: Are You Sure You Want To Send This Message? ").lower()
            if confirmation == "yes" or confirmation == "no":
                break

        if confirmation == "yes":
            # CREATE CONVERSATION
            conversationInfo = {
                'convoId': f'{stu_name}(Student) To {deanName}(Dean)',
                'date': now,
                'senderType': "Student",
                'senderName': stu_name,
                'preMessage': None,
                'senderMessage': message,
                'receivedFrom': None
            }
            createConversation(conversationInfo)

            # SET UP NOTIFICATION
            sql = "INSERT INTO dean_notification (notification, received_from, date, person_id) VALUES (%s, %s, %s, %s)"
            val = (message, f"Student ({stu_name})", now, stu_id)
            db.execute(sql, val)
            mydb.commit()

            while True:
                print()
                back = input("Your Message Has Been Sent. Press (S) To Send Another Message:\n"
                             "                            Press (M) To Return To Student Menu: ").lower()
                if back == "s":
                    stu_send_notification()
                    break
                elif back == "m":
                    StudentMenu(None)
                    break
        elif confirmation == "no":
            StudentMenu(stu_name)



def respondToNotification(senderName, senderType, receiverType, receiverName, previous_message):
    # Kim Lenny(Professor) To Jaheim Archibald(Student)
    convoID = f'{senderName}({senderType}) To {receiverName}({receiverType})'
    print()
    convo_view(convoID, senderType)
    print()
    print(f'[{receiverName}]: {previous_message}')
    while True:
        print()
        message = input("Enter Your Message: ")
        if message == "c":
            if senderType == "Student":
                student_inbox()
                break
            elif senderType == "Professor":
                professor_inbox()
                break
            elif senderType == "Dean":
                dean_inbox()
                break
        if message != '':
            break

    while True:
        confirmation = input("CONFIRMATION: Are You Sure You Want To Send This Message? ")
        if confirmation == "yes" or confirmation == "no":
            break


    if confirmation == "yes":
        if receiverType == "Dean":
            table_to_insert = "dean_notification"
            id_type = "person_id"
        elif receiverType == "Professor":
            table_to_insert = "professor_notification"
            id_type = "prof_id"
        elif receiverType == "Student":
            table_to_insert = "student_notification"
            id_type = "stu_id"
        else:
            return

        # MESSAGE BEING SENT TO THE DEAN
        if receiverType == "Dean" and receiverName == None:
            notification = message
            received_from = f"{senderType} ({senderName})"
            sql = f"SELECT id FROM {senderType} WHERE name = %s"
            val = (senderName,)
            db.execute(sql, val)
            person_id = db.fetchall()[0][0]

            sql = "INSERT INTO dean_notification (notification, received_from, date, person_id) VALUES (%s, %s, %s, %s)"
            val = (notification, received_from, now, person_id)
            db.execute(sql, val)
            mydb.commit()
        else:
            # SET UP REGULAR NOTIFICATION
            notification = message
            received_from = f"{senderType} ({senderName})"
            sql = f"SELECT id FROM {receiverType} WHERE name = %s"
            val = (receiverName,)
            db.execute(sql, val)
            person_id = db.fetchall()[0][0]

            sql = f"INSERT INTO {table_to_insert} (notification, received_from, date, {id_type}) VALUES (%s, %s, %s, %s)"
            val = (notification, received_from, now, person_id)
            db.execute(sql, val)
            mydb.commit()
            # CREATE CONVERSATION
            conversationInfo = {
                'convoId': f'{senderName}({senderType}) To {receiverName}({receiverType})',
                'date': now,
                'senderType': senderType,
                'senderName': senderName,
                'preMessage': previous_message,
                'senderMessage': message,
                'receivedFrom': f'{receiverName}'
            }


            createConversation(conversationInfo)

        while True:
            print()
            back = input("Message Sent. Press (B) To Go Back: ").lower()
            if back == "b":
                if senderType == "Student":
                    student_inbox()
                    break
                elif senderType == "Professor":
                    professor_inbox()
                    break
                elif senderType == "Dean":
                    dean_inbox()
                    break
                else:
                    return

    elif confirmation == "no":
        if senderType == "Student":
            student_inbox()
        elif senderType == "Professor":
            professor_inbox()
        elif senderType == "Dean":
            dean_inbox()
def extractNameFromNotification(notification: str):
    try:
        receiver_name = notification[indexOf(notification, '(') + 1: indexOf(notification, ')')]
    except:
        receiver_name = None
    try:
        type = notification.split()[0]
    except:
        type = None

    return {"receiverName": receiver_name, "Type": type}


# CREATE CONVERSATION
def createConversation(conversationInfo):
    # ADD CONVERSATION
    convoId = conversationInfo['convoId']
    date = conversationInfo['date']
    senderType = conversationInfo['senderType']
    senderName = conversationInfo['senderName']
    preMessage = conversationInfo['preMessage']
    senderMessage = conversationInfo['senderMessage']
    receivedFrom = conversationInfo['receivedFrom']



    sql = "INSERT INTO Conversations (convoId, date, preMessage, senderType, senderName, senderMessage, receivedFrom)" \
          "VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (convoId, date, preMessage, senderType, senderName, senderMessage, receivedFrom)
    db.execute(sql, val)
    mydb.commit()

def convo_view(convoId, user, respondOnOpen=False):
    print("CONVERSATION - Press (C) To Cancel")
    print("-" * len(convoId))
    print(convoId)
    print("-" * len(convoId))
    print()
    sql = "SELECT * FROM Conversations WHERE convoID = %s"
    val = (convoId,)
    db.execute(sql, val)
    results = db.fetchall()
    if len(results) == 0:
        return

    received_from = ''
    showDates = False
    seenMessages = set()
    for item in results:
        print()
        date = item[1]
        receivedFrom =  item[-1]
        receiverMessages = item[2]
        userMessages = item[5]
        if receivedFrom != None:
            received_from = receivedFrom
        if showDates:
            print(date)

        if receiverMessages != None and receiverMessages not in seenMessages:
            print(f'[{receivedFrom}]: {receiverMessages}')
        print()
        print(f"[You]: {userMessages}")
        seenMessages.add(receiverMessages)

    if respondOnOpen:
        if user == 'Dean':
            db_table = 'dean_notification'
        elif user == 'Professor':
            db_table = 'professor_notification'
        elif user == 'Student':
            db_table ='student_notification'

        senderName = getSenderInfo(convoId)['Name']
        senderType = getSenderInfo(convoId)['Type']
        receiverName = getReceiverInfo(convoId)['Name']
        receiverType = getReceiverInfo(convoId)['Type']         

        like_query = f'%{received_from}%'

        sql = f"SELECT notification FROM {db_table} WHERE received_from LIKE %s"
        val = (like_query, )
        db.execute(sql, val)
        results = db.fetchall()
        if len(results) == 0:
            print()
        print()
        if received_from != '':
            last_message = results[-1][0]
            if receiverMessages != last_message and showLastMessage(senderName, senderType, receiverName, receiverType, convoId):
                print(f'[{received_from}]: {last_message}')
        else:
            last_message = None
        while True:
            print()
            message = input("Enter Message: ")
            if message.lower() == 'c':
                clear()
                view_all_conversations(senderName, user)
                break
            if message != '':
                break
        while True:
            print()
            confirmation = input("CONFIRMATION: Are You Sure Want To Send This Message? ").lower()
            if confirmation == 'yes' or confirmation == 'no':
                break
        if confirmation == 'yes':
            # CREATE CONVERSATION
            conversationInfo = {
                'convoId': convoId,
                'date': now,
                'senderType': senderType,
                'senderName': senderName,
                'preMessage': last_message,
                'senderMessage': message,
                'receivedFrom': received_from if received_from != '' else None
            }
            createConversation(conversationInfo)

            
            if receiverType == 'Student':
                stu_id = get_student_id(receiverName)
                sql = "INSERT INTO student_notification (notification, received_from, date, stu_id) VALUES (%s, %s, %s, %s)"
                val = (message, f"{senderType} ({senderName})", now, stu_id)
                db.execute(sql, val)
                mydb.commit()
            elif receiverType == 'Professor':
                prof_id = get_professor_id(receiverName)
                sql = "INSERT INTO professor_notification (notification, received_from, date, prof_id) VALUES (%s, %s, %s, %s)"
                val = (message, f"{senderType} ({senderName})", now, prof_id)
                db.execute(sql, val)
                mydb.commit()
            elif receiverType == 'Dean':
                if senderType == 'Student':
                    person_id = get_student_id(stu_name)
                elif senderType == 'Professor':
                    person_id = get_professor_id(prof_name)
                elif senderType == 'Dean':
                    person_id = get_dean_id(dean_name)
                sql = "INSERT INTO dean_notification (notification, received_from, date, person_id) VALUES (%s, %s, %s, %s)"
                val = (message, f"{senderType} ({senderName})", person_id)
                db.execute(sql, val)
                mydb.commit()

            while True:
                print()
                back = input("Message Sent. Press (B) To Go Back: ").lower()
                if back == 'b':
                    if senderType == 'Student':
                        StudentMenu(stu_name)
                        break
                    elif senderType == 'Professor':
                        ProfessorMenu(prof_name)
                        break
                    elif senderType == 'Dean':
                        DeanMenu(dean_name)
                        break
        elif confirmation == 'no':
            if senderType == 'Student':
                StudentMenu(stu_name)
            elif senderType == 'Professor':
                ProfessorMenu(prof_name)
            elif senderType == 'Dean':
                DeanMenu(dean_name)


def getSenderInfo(convoID):
    senderInfo = {}
    name = f'{convoID.split()[0]}' + ' ' +  convoID.split()[1][:indexOf(convoID.split()[1],'(', 1)]
    senderInfo.update({'Name': name})
    type = convoID[indexOf(convoID, '(', 1)+1:indexOf(convoID, ')', 1)]
    senderInfo.update({'Type': type})
    return senderInfo

def getReceiverInfo(convoID):
    # Kim Roberts(Professor) To Jaheim Archibald(Dean)
    receiverInfo = {}

    receiverNameAndType = convoID.split('To')[1]

    receiverName = receiverNameAndType[:indexOf(receiverNameAndType, '(')].lstrip()
    receiverInfo.update({'Name': receiverName})

    receiverType = receiverNameAndType[indexOf(receiverNameAndType, '(')+1:indexOf(receiverNameAndType, ')')]
    receiverInfo.update({'Type': receiverType})
    return receiverInfo


def showLastMessage(senderName, senderType, receiverName, receiverType, convoId):
    # DETERMINE WHETHER THE PERSON HAS RESPONDED
    sql = "SELECT senderMessage FROM Conversations WHERE convoId = %s"
    val = (convoId, )
    db.execute(sql, val)
    results = db.fetchall()
    if len(results) == 0:
        return False

    lastSentMessage = results[0][-1]
    reverse_convo_id = f'{receiverName}({receiverType}) To {senderName}({senderType})'
    sql = "SELECT * FROM Conversations WHERE convoId = %s AND preMessage = %s"
    val = (reverse_convo_id, lastSentMessage)
    db.execute(sql, val)
    results2 = db.fetchall()
    if len(results2) == 0:
        return False
    return True
    

# VIEW ALL COURSES
def view_all_courses_stu():
    clear()
    print("----------------")
    print("VIEW ALL COURSES")
    print("----------------")
    print()
    all_courses = Course.getAll_Courses()
    db.execute("SELECT description FROM Course")

    description = db.fetchall()

    for i, course in enumerate(all_courses):
        index = 0
        # SEPARATE THE FULL COURSE NAME FROM THE DESCRIPTION
        for j in range(len(description)):
            if description[i][0][j] == ':':
                break
            index += 1

        print(f"{all_courses[i][0]} - {description[i][0][:index]}")
        print()

    while True:
        stu_choice = input("Press (S) To Select A Course:\nPress (M) To Return To Student Menu: ").lower()
        if stu_choice == "s":
            search_for_course_stu()
        elif stu_choice == "m":
            StudentMenu(None)

# SEARCH FOR COURSE
def search_for_course_stu(came_from=None):
    if came_from != None:
        pass
    while True:
        print()
        course_name = input("Enter The Name Of The Course: ").upper()
        if course_name != '':
            break
    # CHECK IF COURSE ENTERED IS IN THE LIST
    sql = "SELECT name FROM Course WHERE name = %s"
    val = (course_name,)
    db.execute(sql, val)
    result = db.fetchall()
    if len(result) == 0:
        course_not_found("Student Search For Course")

    # COURSE WAS FOUND
    select_course_stu(course_name)

# SELECT COURSE
def select_course_stu(course_name):
    clear()
    course = Course(course_name)

    print("-" * len(course_name) + "-------")
    print(f"{course_name.upper()} COURSE")
    print("-" * len(course_name) + "-------")
    print()
    print("<<<<<<<<<<<<<<<< DESCRIPTION >>>>>>>>>>>>>>>>")
    print()
    print(course.getDescription())
    print()


    try:
        print("-" * len(course) + "------------------")
        print(f"COURSE CANCELLED: {course.isCourseCancelled()}")
        print(f"Class Size: {course.getStudentCountInCourse()}")
        print("-" * len(course) + "------------------")
        print()
    except:
        print()
        print("An Error Occurred. Restart Application")
        sleep(1)
        exit()
    while True:
        print()
        print("Press (S) To Search Again:")
        print("Press (E) To Enroll In This Course:")  # TODO ONLY MAKE THIS AVAILABLE IF COURSE IS NOT CANCELLED
        print("Press (D) To Drop This Course:")   # TODO ONLY MAKE THIS OPTION AVAILABLE IF THE STUDENT IS ENROLLED IN THE COURSE
        back = input("Press (M) To Return To Student Menu: ").lower()
        if back == "s":
            search_for_course_stu("Search")
        elif back == "e":
            enroll_in_course(course_name)
        elif back == "d":
            sql = "SELECT CoursesEnrolledIn FROM Student WHERE name = %s"
            val = (stu_name, )
            db.execute(sql, val)
            courses_enrolled_in = db.fetchall()[0][0]

            Stu = Student(stu_name.split()[0], stu_name.split()[1], None, None, None, courses_enrolled_in, None, None)
            drop_class(Stu.getID(), Stu.getCoursesEnrolledIn(), course_name)
        elif back == "m":
            StudentMenu(None)

# ENROLL IN COURSE
def enroll_in_course(course_name):
    clear()
    print("----------------")
    print("ENROLL IN COURSE")
    print("----------------")
    print()
    # GET ALL THE COURSES CURRENTLY ENROLLED
    sql = "SELECT CoursesEnrolledIn From Student WHERE name = %s"
    val = (stu_name,)
    db.execute(sql, val)
    courses_enrolled_in = db.fetchall()[0][0]
    print(f"Courses You Are Currently Enrolled In: {courses_enrolled_in.split()}")

    # CHECK IF THE STUDENT IS ALREADY ENROLLED IN THE COURSE
    for course in courses_enrolled_in.split():
        if course_name == course:
            print()
            while True:
                print()
                back = input("You Are Already Enrolled In This Course. Press (S) To Return To All Courses:\n"
                             "                                         Press (M) To Return To Student Menu: ").lower()
                if back == "s":
                    view_all_courses_stu()
                elif back == "m":
                    StudentMenu(None)


    # CHECKING IF STUDENT CANT ENROLL IN ANY MORE COURSES
    if len(courses_enrolled_in.split()) == Student.MAX_COURSES_STUDENT_CAN_ENROLL_IN:
        while True:
            print()
            print(f"You Can't Enroll In More Than {Student.MAX_COURSES_STUDENT_CAN_ENROLL_IN} Courses.")
            print()
            back = input("Press (S) To Return To Courses\nPress (M) To Return To Student Menu: ").lower()
            if back == "s":
                view_all_courses_stu()
            elif back == "m":
                StudentMenu(None)

    while True:
        print()
        confirmation = input(
            f"CONFIRMATION: Are You Sure You Want To Enroll In {course_name}? ")
        if confirmation != '' and (confirmation == "yes" or confirmation == "no"):
            break
    if confirmation == "yes":
        Stu = Student(stu_name.split()[0], stu_name.split()[1], None, None, None, None, None, None)

        new_courses_to_add = courses_enrolled_in + " " + course_name
        sql = "UPDATE Student SET CoursesEnrolledIn = %s WHERE id = %s"
        val = (new_courses_to_add, Stu.getID())
        db.execute(sql, val)
        mydb.commit()

        # SET UP NOTIFICATION
        message = f"{stu_name} Enrolled In: {course_name}"
        sql = "INSERT INTO dean_notification (notification, received_from, date, person_id) VALUES (%s, %s, %s, %s)"
        val = (message, f"Student ({stu_name})", now, Stu.getID())
        db.execute(sql, val)
        mydb.commit()

        while True:
            print()
            print(f"You Have Successfully Enrolled In {course_name}")
            print()
            back = input(f"Press (S) To Return To All Courses:\nPress (M) To Return To Student Menu: ").lower()
            if back == "s":
                view_all_courses_stu()
            elif back == "m":
                StudentMenu(None)
    else:
        StudentMenu(None)


# DROP STUDENT FROM COURSE
def drop_class(student_id, courses_enrolled_in, name_of_class=None):
    clear()
    print("DROP CLASS")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    print(f"CURRENT COURSES ENROLLED IN: {courses_enrolled_in}")
    print()
    if courses_enrolled_in == None:
        while True:
            print()
            error = input("You Are Not Enrolled In Any Courses. Press (M) To Return To Student Menu: ").lower()
            if error == "m":
                StudentMenu(None)
    if name_of_class == None:
        while True:
            class_to_drop = input("Enter The Name Of Class To Drop: ").upper()
            if class_to_drop != '':
                break
    else:
        class_to_drop = name_of_class

    # CHECKING IF C WAS ENTERED
    if len(class_to_drop) == 1:
        class_to_drop = class_to_drop.lower()
    if class_to_drop == "c":
        StudentMenu(None)

    # CHECKING IF THEY ARE ENROLLED IN THE CLASS THEY TRIED TO DROP
    if class_to_drop not in courses_enrolled_in.split():
        while True:
            print()
            error = input("You Are Not Enrolled In That Class. Press (T) To Try Again:\n"
                          "                                    Press (M) To Return To Main Menu: ").lower()
            if error == "t":
                drop_class(student_id, courses_enrolled_in)
            elif error == "m":
                StudentMenu(None)

    # CONFIRMATION
    while True:
        print()
        confirmation = input("CONFIRMATION: Are You Sure You Want To Drop This Class? ")
        if confirmation != '' and (confirmation == "yes" or confirmation == "no"):
            break

    if confirmation == "yes":
        new_courses = ""
        for course in courses_enrolled_in.split():
            if course != class_to_drop:
                new_courses += course
                new_courses += " "
        new_courses = new_courses.rstrip()

        # UPDATE THEIR COURSES ENROLLED IN
        sql = "UPDATE Student SET CoursesEnrolledIn = %s WHERE id = %s"
        val = (new_courses, student_id)
        db.execute(sql, val)
        mydb.commit()

        # SET UP NOTIFICATION
        message = f"{stu_name} Dropped: {class_to_drop}"
        sql = "INSERT INTO dean_notification (notification, received_from, date, person_id) VALUES (%s, %s, %s, %s)"
        val = (message, f"Student ({stu_name})", now, student_id)
        db.execute(sql, val)
        mydb.commit()

        print()
        print(f"You Dropped {class_to_drop}")
        while True:
            print()
            back = input("Press (M) To Return To Student Menu: ").lower()
            if back == "m":
                StudentMenu(stu_name)

    else:
        StudentMenu(None)


# SANITIZE
def sanitize_password(password, name, came_from=None):
    if came_from == None:
        msg = "Your"
    else:
        msg = "Their"
    if " " in password:
        while True:
            while True:
                print()
                invalid_pwd = input("Invalid Password: Password Must Not Contain Spaces. Press (T) To Try Again: ").lower()
                if invalid_pwd != '':
                    break
            if invalid_pwd == "t":
                while True:
                    new_password = getpass(f"Enter {msg} Password: ")
                    if new_password != '':
                        break
                if " " in new_password:
                    new_password = sanitize_password(new_password, name)

                return new_password
                    # break

    # CHECKING FOR SHORT PASSWORD
    if len(password) <= 3:
        while True:
            while True:
                print()
                short_pwd = input(f"Weak Password: {msg} Password Is Too Short. Press (T) To Try Again:\n"
                                  "                                           Press (C) To Continue: ").lower()
                if short_pwd != '':
                    break

            if short_pwd == "t":
                while True:
                    print()
                    new_password = getpass(f"Enter {msg} Password: ")
                    if new_password != '':
                        break
                if len(new_password) <= 3:
                    new_password = sanitize_password(new_password, name)

                return new_password

            elif short_pwd == "c":
                return password

      # CHECKING IF PASSWORD IS SIMILAR TO USER NAME
    if password.lower() in name.lower():
        while True:
            while True:
                print()
                similar_pwd = input(f"Weak Password: {msg} Password Is Too Similar To {msg} Username. Press (T) To Try Again:\n"
                                    "                                                              Press (C) To Continue: ").lower()
                if similar_pwd != '':
                    break
            if similar_pwd == "t":
                while True:
                    print()
                    new_password = getpass(f"Enter {msg} Password: ")
                    if new_password != '':
                        break
                if new_password.lower() in name.lower():
                    new_password = sanitize_password(new_password, name)

                return new_password

            elif similar_pwd == "c":
                return password

    return password
def sanitize_phone_number(phone_number, came_from=None):
    if came_from == None:
        msg = "Your"
    else:
        msg = "Their"
    if "-" not in phone_number:
        while True:
            while True:
                print()
                tmp = input(f"Invalid Phone Number: {msg} Phone Number Must Be Formatted Like This: '829-647-1985'. Press (T) To Try Again: ").lower()
                if tmp != '':
                    break
            if tmp == "t":
                new_phone_number = input(f"Enter {msg} Phone Number: ")
                if "-" not in new_phone_number:
                    new_phone_number = sanitize_phone_number(new_phone_number)

                return new_phone_number
    return phone_number
def sanitize_courses(sub_courses, came_from):
    if not checkCourse(sub_courses):
        print()
        while True:
            tmp = input("INVALID COURSES. Press (V) To View All Courses:\n"
                        "                 Press (T) To Try Again: ").lower()
            if tmp == "v" or tmp == "t":
                break
        if tmp == "v":
             # PRINT ALL THE COURSES
            all_courses = Course.getAll_Courses()
            db.execute("SELECT description FROM Course")
            description = db.fetchall()

            for i, course in enumerate(all_courses):
                print(f"{all_courses[i][0]} - {description[i][0][:indexOf(description[i][0], ':')]}")
                print()

            return re_enter_courses(came_from)

        elif tmp == "t":
            return re_enter_courses(came_from)

    return sub_courses
def re_enter_courses(came_from):
    while True:
        print()
        if came_from == "Register_As_Prof":
            while True:
                new_courses_taught = input("Enter The Courses You Teach: ").upper()
                if new_courses_taught != '':
                    break
            new_courses_taught = sanitize_courses(new_courses_taught, came_from)
            return new_courses_taught
        elif came_from == "Prof_Change_Courses_Taught":
            while True:
                new_courses_taught = input("Enter The New Courses You Teach: ").upper()
                if new_courses_taught != '':
                    break
            new_courses_taught = sanitize_courses(new_courses_taught, came_from)
            return new_courses_taught
        elif came_from == "Dean_Register_Professor":
            while True:
                new_courses_taught = input("Enter Their Courses Taught: ").upper()
                if new_courses_taught != '':
                    break
            new_courses_taught = sanitize_courses(new_courses_taught, came_from)
            return new_courses_taught


def checkCourse(sub_courses):
    counter = 0
    all_courses = Course.getAll_Courses()
    sub_courses = sub_courses.split()
    for i in range(len(sub_courses)):
        for j in range(len(all_courses)):
            if sub_courses[i] == all_courses[j][0]:
                counter += 1

    return counter == len(sub_courses)
def checkAge(age):
    return age.isdigit()
def removeDuplicates(array):
    found_items = []
    for item in array:
        if item not in found_items:
            found_items.append(item)

    return found_items
def removeRightDuplicateAssignmentTypes(all_titles: list):
    all_assign_types = []
    for title in all_titles:
        sql = "SELECT assignment_type FROM assignments WHERE title = %s LIMIT 1"
        val = (title, )
        db.execute(sql, val)
        results = db.fetchall()
        if len(results) == 0:
            return
        all_assign_types.append(results[0][0])

    return all_assign_types

def view_all_course_general(came_from, args=None):
    clear()
    print("----------------")
    print("VIEW ALL COURSES")
    print("----------------")
    print()
    all_courses = Course.getAll_Courses()
    db.execute("SELECT description FROM Course")

    description = db.fetchall()

    for i, course in enumerate(all_courses):
        print(f"{all_courses[i][0]} - {description[i][0][:indexOf(description[i][0], ':')]}")
        print()

    while True:
        user_choice = input("Press (B) To Go Back: ").lower()
        if user_choice == "b":
            if came_from == "Dean_Update_Student_Courses":
                update_student(args[0], args[1], args[2])
                break
            elif came_from == "Dean_Update_Prof_Courses_Taught":
                update_professor(args[0], args[1], args[2])
                break


# CONFIRM PASSWORD ERROR
def confirm_password_error(name, came_from=None):
    if came_from == None:
        msg = "Your"
    else:
        msg = "Their"
    while True:
        while True:
            print()
            tmp = input(f"{msg} Passwords Do Not Match. Press (T) To Try Again: ").lower()
            if tmp != '':
                break
        if tmp == "t":
            print()
            while True:
                password = getpass(f"Enter {msg} Password: ")
                if password != '':
                    break
            password = sanitize_password(password, name)
            confirm_password = getpass(f"Confirm {msg} Password: ")
            if password != confirm_password:
                confirm_password = confirm_password_error(name)

            return confirm_password

# HASH PASSWORD
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_password_hash(password, hash):
    if hash_password(password) == hash:
        return True
    return False

# SPECIAL FUNCTIONS
def capitalize(word):
    word_to_return = ""
    all_words = [word.capitalize() for word in word.split()]

    for word in all_words:
        word_to_return += word
        word_to_return += " "

    word_to_return = word_to_return.rstrip()
    return word_to_return
def indexOf(string, index_of, specific_index=None):
    if specific_index != None:
        all_occurrences = []

        for i in range(len(string)):
            if string[i] == index_of:
                all_occurrences.append(i)

        return all_occurrences[specific_index - 1] if len(all_occurrences) != 0 else None
    for i in range(len(string)):
        if string[i] == index_of:
            return i

def permuteString(string):
    if len(string) == 1:
        return [string]
    perms = permuteString(string[1:])
    char = string[0]
    result = []
    for perm in perms:
        for i in range(len(perm)+1):
            result.append(perm[:i] + char + perm[i:])

    return result

# GET ID
def get_student_id(name):
    sql = "SELECT id FROM Student WHERE name = %s"
    val = (name, )
    db.execute(sql, val)
    results = db.fetchall()
    if len(results) == 0:
        return None
    student_id = results[0][0]
    return student_id
def get_professor_id(name):
    sql = "SELECT id FROM Professor WHERE name = %s"
    val = (name, )
    db.execute(sql, val)
    results = db.fetchall()
    if len(results) == 0:
        return None
    prof_id = results[0][0]
    return prof_id
def getProfessorName(prof_id):
    sql = "SELECT name FROM Professor WHERE id = %s"
    val = (prof_id, )
    db.execute(sql, val)
    results = db.fetchall()
    if len(results) == 0:
        return None
    return results[0][0]
def get_dean_id(name):
    sql = "SELECT id FROM Dean WHERE name = %s"
    val = (name, )
    db.execute(sql, val)
    results = db.fetchall()
    if len(results) == 0:
        return None
    dean_id = results[0][0]
    return dean_id
def reset_password(came_from):
    global password_attempts
    if came_from == "Dean":
        Table = "Dean"
        user_name = dean_name
        menuToReturn = DeanMenu
        loginToReturn = DeanLogin
    elif came_from == "Prof":
        Table = "Professor"
        user_name = prof_name
        menuToReturn = ProfessorMenu
        loginToReturn = ProfessorLogin
    elif came_from == "Stu":
        Table = "Student"
        user_name = stu_name
        menuToReturn = StudentMenu
        loginToReturn = StudentLogin
    else:
        return
    # GET THE USERS NAME AND SECURITY ANIMAL
    sql = f"SELECT security_animal FROM {Table} WHERE name = %s"
    val = (user_name, )
    db.execute(sql, val)
    results = db.fetchall()
    # NO SECURITY ANIMAL WAS FOUND
    if len(results) == 0:
        no_security_animal(came_from)
    user_security_animal = results[0][0]


    while True:
        print()
        error = input(f"You Entered Your Password Incorrect {password_attempts} Times. Would You Like To Reset Your Password? ").lower()
        if error == "yes" or error == "no":
            break
    if error == "yes":
        while True:
            print()
            entered_s_animal = input("SECURITY QUESTION: What Is The Name Of Your Favorite Animal? ").lower()
            if entered_s_animal != user_security_animal:
                print("Security Question Doesn't Match. Press (C) To Cancel")
                if entered_s_animal == "c":
                    loginToReturn()
            else:
                break
        # NEW PASSWORD
        while True:
            print()
            new_password = getpass("Enter Your New Password: ")
            if new_password != '':
                break
        new_password = sanitize_password(new_password, user_name)
        # CONFIRM PASSWORD
        while True:
            print()
            confirm_user_password = getpass("Confirm Your Password: ")
            if confirm_user_password != '':
                break
        if confirm_user_password != new_password:
            confirm_user_password = confirm_password_error(user_name)

        # HASH PASSWORD
        confirm_user_password = hash_password(confirm_user_password)

        # CONFIRMATION
        while True:
            print()
            confirmation = input("CONFIRMATION: Are You Sure You Want To Reset Your Password? ").lower()
            if confirmation == "yes" or confirmation == "no":
                break
        if confirmation == "yes":
            sql = f"UPDATE {Table} SET password = %s WHERE name = %s"
            val = (confirm_user_password, user_name)
            db.execute(sql, val)
            mydb.commit()

            # BACK
            while True:
                print()
                back = input("Your Password Has Been Reset. Press (R) To Re-Login: ").lower()
                if back == "r":
                    loginToReturn()
        elif confirmation == "no":
            loginToReturn()

    elif error == "no":
        loginToReturn()


def no_security_animal(came_from):
    while True:
        print()
        error = input("You Have Not Entered Your Security Animal So Your Password Cannot Be Reset. Press (L) To Return To Login: ").lower()
        if error == "l":
            if came_from == "Dean":
                DeanLogin()
                break
            elif came_from == "Prof":
                ProfessorLogin()
                break
            elif came_from == "Stu":
                StudentLogin()
                break





# UPDATE COURSE DATABASE
def update_course_database():
    # UPDATING studentsInCourse
    all_courses = Course.getAll_Courses()
    for i in range(len(all_courses)):
        # FIND ALL THE STUDENT THAT ARE ENROLLED IN EACH COURSE
        like_query = f"%{all_courses[i][0]}%"
        sql = "SELECT name FROM Student WHERE CoursesEnrolledIn LIKE %s"
        val = (like_query,)
        db.execute(sql, val)
        names = db.fetchall()
        # GENERATE A STRING THAT CAN BE ADDED TO THE DATABASE(BECAUSE TUPLES ARE RETURNED BACK)
        students_to_add_to_database = ""
        for j in range(len(names)):
            students_to_add_to_database += names[j][0]
            students_to_add_to_database += " "
        students_to_add_to_database = students_to_add_to_database.rstrip()
        # UPDATE THE DATABASE
        sql = "UPDATE Course SET studentsInCourse = %s WHERE name = %s"
        val = (students_to_add_to_database, all_courses[i][0])
        db.execute(sql, val)
        mydb.commit()

        # UPDATING studentsInCourse
        sql = "SELECT COUNT(name) FROM Student WHERE CoursesEnrolledIn LIKE %s"
        val = (like_query,)
        db.execute(sql, val)
        student_count = db.fetchall()
        # UPDATE THE DATABASE
        sql = "UPDATE Course SET studentsCount = %s WHERE name = %s"
        val = (student_count[0][0], all_courses[i][0])
        db.execute(sql, val)
        mydb.commit()

    # UPDATING teachedBy
    for i in range(len(all_courses)):
        # FIND ALL THE PROFESSORS THAT TEACH A COURSE
        like_query = f"%{all_courses[i][0]}%"
        sql = "SELECT name FROM Professor WHERE CoursesTaught LIKE %s"
        val = (like_query,)
        db.execute(sql, val)
        names = db.fetchall()
        # GENERATE A STRING THAT CAN BE ADDED TO THE DATABASE(BECAUSE TUPLES ARE RETURNED BACK)
        professors_to_add_to_database = ""
        for j in range(len(names)):
            professors_to_add_to_database += names[j][0]
            professors_to_add_to_database += " "
        professors_to_add_to_database = professors_to_add_to_database.rstrip()
        # UPDATE THE DATABASE
        sql = "UPDATE Course SET teachedBy = %s WHERE name = %s"
        val = (professors_to_add_to_database, all_courses[i][0])
        db.execute(sql, val)
        mydb.commit()
# UPDATE MAJOR DATABASE
def update_major_database():
    all_majors = Major.getAllMajors()
    # UPDATE STUDENT COUNT
    for major in all_majors:
        sql = "SELECT COUNT(major) FROM Student WHERE major = %s"
        val = (major,)
        db.execute(sql, val)
        major_count = int(db.fetchall()[0][0])
        sql = "UPDATE Major SET studentCount = %s WHERE name = %s"
        val = (major_count, major)
        db.execute(sql, val)
        mydb.commit()

    # UPDATE STUDENT NAMES
    for major in all_majors:
        sql = "SELECT name FROM Student WHERE major = %s"
        val = (major,)
        db.execute(sql, val)
        student_name = db.fetchall()
        # print(student_name, len(student_name))
        if len(student_name) == 0:
            sql = "UPDATE Major SET studentNames = 'None' WHERE name = %s"
            val = (major,)
            db.execute(sql, val)
            mydb.commit()
        else:
            if len(student_name) == 1:
                student_name = student_name[0][0]
                sql = "UPDATE Major SET studentNames = %s WHERE name = %s"
                val = (student_name, major)
                db.execute(sql, val)
                mydb.commit()
            else:
                all_student_names = ""
                for names in student_name:
                    all_student_names += names[0]
                    all_student_names += " "
                all_student_names = all_student_names.rstrip()
                sql = "UPDATE Major SET studentNames = %s WHERE name = %s"
                val = (all_student_names, major)
                db.execute(sql, val)
                mydb.commit()
# UPDATE STUDENT GRADES
def update_student_grades():
    # GET ALL STUDENT IDS
    db.execute("SELECT id, name FROM Student")
    all_stu_id = db.fetchall()
    all_stu_id = [all_stu_id[i][0] for i in range(len(all_stu_id))]

    for id in all_stu_id:
        course_grades = {}
        sql = "SELECT * FROM grade_book WHERE stu_id = %s"
        val = (id, )
        db.execute(sql, val)
        results = db.fetchall()
        stu_id = results[0][1] if len(results) != 0 else None
        course_names = [results[i][2] for i in range(len(results))]

        # RETRIEVE ONLY THE GRADES FROM THE RESULTS
        if stu_id != None:
            results = [results[i][3:] for i in range(len(results))]
            for i in range(len(course_names)):
                grades_to_avg = [grade for grade in results[i] if grade != None]
                # UPDATE course_grades USING THE COURSE NAME AND THE AVG OF THEIR 5 GRADES FOR THAT COURSE
                course_grades.update({course_names[i]: str(compute_average(grades_to_avg)) + "%"})

            # CONVERT THE DICT TO A STRING
            grades_to_add_to_database = ""
            for grade in course_grades:
                grades_to_add_to_database += f"{grade}: {course_grades[grade]}"
                grades_to_add_to_database += " "

           # COMPUTE THE STUDENT'S OVERALL AVG USING ALL THEIR COURSE AVERAGES
            student_grade_avg_for_each_grade_book = []
            for i in range(len(results)):
                grades_to_avg = [grade for grade in results[i] if grade != None]
                student_grade_avg_for_each_grade_book.append(compute_average(grades_to_avg))
            try:
                studentAverage = round(sum(student_grade_avg_for_each_grade_book) // len(student_grade_avg_for_each_grade_book))
            except ZeroDivisionError:
                studentAverage = None
            grades_to_add_to_database += f"AVG: {studentAverage}%"

            # UPDATE THE DATABASE
            sql = "UPDATE Student SET grades = %s WHERE id = %s"
            val = (grades_to_add_to_database, stu_id)
            db.execute(sql, val)
            mydb.commit()

        if stu_id == None:
            sql = "UPDATE Student SET grades = %s WHERE id = %s"
            val = (None, id)
            db.execute(sql, val)
            mydb.commit()

if __name__ == '__main__':
    login()















# student_1 = Person("Jaheim", "Archibald", "idk", 18, "574-883-2322")
#
#
#
# student_2 = Student("John", "Brown", "idkyet", 21, "917-456-2623", "MATH-06 MATH-21 CSI-13", "90 84 71")
# print(student_2.getEmail())
#
#
#
# student_2.setCoursesEnrolledIn("MATH-06 MATH-21 CSI-30")
#
#
# print(student_2.getCoursesEnrolledIn())



# print(Student.checkIfCourseIsAvailableToSet(Course.getAll_Courses(), student_2.getCoursesEnrolledIn()))

# print(student_2.getCoursesEnrolledIn())


#student_2.setCoursesEnrolledIn("CSI-45, DAT-46, MATH-30")

# print(student_2.getCoursesEnrolledIn())


# print(student_2.setGrades("80 91 98 67 91"))

# professor_1  = Professor("Jimmy", "Lue", "Address", 40, "156-636-8373", 90000, "CSI-30 CSI-32 CSI-35 MATH-33 MATH-13")
#
#
#
#
#
# course_1 = Course(50, "MATH-30", "Jimmy-Lue")


#print(course_1.isCourseCancelled())






