import os
clear = lambda: os.system("cls")
import hashlib
from stdiomask import getpass
try:
    import mysql.connector
except ImportError:
    print("Import Error: Do pip install mysql.connector-python To Use This Program")
from datetime import date

current_date = date.today()
now = current_date.strftime("%B %d, %Y")

# CLASSES
from Professor import Professor
from Course import Course
from Major import Major
from Person import Person
from Student import Student

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


# DEAN LOGIN
def DeanLogin():
    clear()
    global dean_name
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
        incorrect_password("Dean")

    update_course_database()
    update_major_database()
    DeanMenu(dean_name)


# PROFESSOR LOGIN
def ProfessorLogin():
    global prof_password, prof_name
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
        incorrect_password("Professor")

    update_course_database()
    update_major_database()
    ProfessorMenu(prof_name)



# STUDENT LOGIN
def StudentLogin():
    clear()
    global stu_name, stu_password
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
    print()
    while True:
        dean_name = input("Enter Your Full Name: ")
        if dean_name != '':
            break
    # CHECKING IF C WAS ENTERED
    if len(dean_name) == 1:
        dean_name = dean_name.lower()
    if dean_name == "c":
        login()

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
        if dean_s_animal != '':
            break

    # PASSWORD
    while True:
        dean_password = input("Enter Your Password: ")
        if dean_password != '':
            break

    # SANITIZE PASSWORD
    dean_password = sanitize_password(dean_password, dean_name)


    # CONFIRM PASSWORD
    while True:
        confirm_dean_password = input("Confirm Your Password: ")
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
    print()
    while True:
        prof_name = input("Enter Your Full Name: ")
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
        already_registered()

    # SECURITY ANIMAL
    while True:
        prof_s_animal = input("SECURITY QUESTION: What Is The Name Of Your Favorite Animal? ").lower()
        if prof_s_animal != '':
            break

    # PASSWORD
    while True:
        prof_password = input("Enter Your Password: ")
        if prof_password != '':
            break

    # SANITIZE PASSWORD
    prof_password = sanitize_password(prof_password, prof_name)

    # CONFIRM PASSWORD
    while True:
        confirm_prof_password = input("Confirm Your Password: ")
        if confirm_prof_password != '':
            break

    if prof_password != confirm_prof_password:
        confirm_prof_password = confirm_password_error(prof_name)

    # HASH PASSWORD
    confirm_prof_password = hash_password(confirm_prof_password)

    # ADDRESS
    while True:
        prof_address = input("Enter Your Address: ")
        if prof_address != '':
            break

    # AGE
    while True:
        try:
            prof_age = int(input("Enter Your Age: "))
        except ValueError:
            prof_age = age_not_num()
        if prof_age != '':
            break


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
    prof_courses_taught = sanitize_courses(prof_courses_taught)



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




# REGISTER AS PROFESSOR
def register_as_student():
    clear()
    print("REGISTER AS STUDENT")
    print(now)
    print("-------------------")
    print("Press (C) To Cancel")
    print("-------------------")
    print()
    while True:
        student_name = input("Enter Your Full Name: ")
        if student_name != '':
            break
    # CHECKING IF C WAS ENTERED
    if len(student_name) == 1:
        student_name = student_name.lower()
    if student_name == "c":
        login()

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
        if student_s_animal != '':
            break

    # PASSWORD
    while True:
        student_password = input("Enter Your Password: ")
        if student_password != '':
            break

    # SANITIZE PASSWORD
    student_password = sanitize_password(student_password, student_name)

    # CONFIRM PASSWORD
    while True:
        confirm_student_password = input("Confirm Your Password: ")
        if confirm_student_password != '':
            break

    if student_password != confirm_student_password:
        confirm_student_password = confirm_password_error(student_name)

    # HASH PASSWORD
    confirm_student_password = hash_password(confirm_student_password)

    # ADDRESS
    while True:
        student_address = input("Enter Your Address: ")
        if student_address != '':
            break

    # AGE
    while True:
        try:
            student_age = int(input("Enter Your Age: "))
        except ValueError:
            student_age = age_not_num()
        if student_age != '':
            break


    # PHONE NUMBER
    while True:
        student_phone_number = input("Enter Your Phone Number: ")
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




# DEAN MENU
def DeanMenu(name):
    clear()
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
        major_description = results[0][0]
        students_names = results[0][1]
        student_count = results[0][2]

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
                             "Press (V) To View All Students In Major:\nPress (A) To Admin Options: ").lower()
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
    print("5 -> Search By Courses Enrolled In")
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
    like_query = f"%{where_val}%"
    sql = f"SELECT * FROM Student WHERE {column_name} LIKE %s"
    val = (like_query,)

    db.execute(sql, val)

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
                error = input("Can't Set Course Check If All Courses Entered Are Available. Press (T) To Try Again:\n"
                              "                                                             Press (V) To View All Courses:\n"
                              "                                                             Press (M) To Return To Dean Menu: ").lower()
                if error == "t":
                    update_student('Courses Enrolled In', 'CoursesEnrolledIn', student_name)
                elif error == "v":
                    view_all_courses_dean()
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
def no_person_found(came_from=None, argv=None):
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
            menu = "Dean Menu"
            who = "Dean"
        elif argv == "Prof":
            menu = "Professor Menu"
            who = "Professor"
        elif argv == "Stu":
            menu = "Student Menu"
            who = "Student"
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
        index = 0
        # SEPARATE THE FULL COURSE NAME FROM THE DESCRIPTION
        for j in range(len(description)):
            if description[i][0][j] == ':':
                break
            index += 1

        print(f"{all_courses[i][0]} - {description[i][0][:index]}")
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

    print("-" * len(course) + "------------------")
    print(f"COURSE CANCELLED: {course.isCourseCancelled()}")
    print(f"Class Size: {course.getStudentCountInCourse()}")
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
        if course.getStudentCountInCourse() != 0:
            print("Press (V) To View All Students Enrolled In This Course: ")
        back = input("Press (A) To Return To Admin Options: ").lower()
        if back == "s":
            search_for_course_dean("Search")
        elif back == "e":
            enroll_student_in_course(course_name)
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
    students_in_course = [result[i] + " " + result[i + 1] for i in range(len(result) // 2)]

    print(students_in_course)

    while True:
        print()
        tmp = input("Press (V) To View Students Grades:\nPress (A) To Return To Admin Options: ").lower()
        if tmp == "v":
            all_names = course.getStudentNamesInCourse().split()
            num_students_in_course = course.getStudentCountInCourse()
            view_student_grade_for_course(all_names, num_students_in_course, course_name, "Dean")
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
        login()

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
        try:
            student_age = int(input("Enter Their Age: "))
        except ValueError:
            student_age = age_not_num('Student')
        if student_age != '':
            break


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


    for i in range(len(all_notifications)):
        if len(all_notifications[i][1]) <= 188:
            print("-" * len(all_notifications[i][1]) + "---------")
        else:
            print("-" * 109 + "---------\n")
        print(f"Id: {all_notifications[i][0]}")
        print(f"Date: {all_notifications[i][3]}")
        print(f"Received From: {all_notifications[i][2]} Id: {all_notifications[i][4]}")
        print(f"Message: {all_notifications[i][1]}")
        if len(all_notifications[i][1]) <= 188:
            print("-" * len(all_notifications[i][1]) + "---------")
        else:
            print("-" * 109 + "---------")
        print()

    while True:
        print()
        print("Press (D) To Filter By Date:              |  Press (C) To Clear A Notification:")
        print("Press (F) To Filter By Received From:     |  Press (CA) To Clear All Notifications:")
        print("Press (M) To Filter By Message:           |  Press (S) To Return To Dean Menu:")
        print()
        filter = input("Choose An Option: ")
        if filter == "d":
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
    if len(to) == 1:
        to = to.lower()
    if to == "c":
        DeanMenu(None)

    # STUDENT
    if to == "Student":
        while True:
            print()
            stu_name = capitalize(input("Enter The Name Of The Student: "))
            if stu_name != '':
                break
        sql = "SELECT id FROM Student WHERE name = %s"
        val = (stu_name, )
        db.execute(sql, val)
        stu_id = db.fetchall()
        if len(stu_id) == 0:
            no_person_found("Notification", "Dean")
        stu_id = stu_id[0][0]

        while True:
            message = input("Message: ")
            if message != '':
                break

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

    # PROFESSOR
    elif to == "Professor":
        while True:
            print()
            professor_name = capitalize(input("Enter The Name Of The Professor: "))
            if professor_name != '':
                break
        sql = "SELECT id FROM Professor WHERE name = %s"
        val = (professor_name, )
        db.execute(sql, val)
        prof_id = db.fetchall()
        if len(prof_id) == 0:
            no_person_found("Notification", "Dean")
        prof_id = prof_id[0][0]

        while True:
            message = input("Message: ")
            if message != '':
                break

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

    # DEAN
    elif to == "Dean":
        while True:
            print()
            deanName = capitalize(input("Enter The Name Of The Dean: "))
            if deanName != '':
                break
        # CHECKING IF CORRECT NAME WAS ENTERED
        sql = "SELECT * FROM Dean WHERE name = %s"
        val = (deanName,)
        db.execute(sql, val)
        result = db.fetchall()
        if len(result) == 0:
            no_person_found("Notification", "Dean")

        # GETTING THE ID OF THE DEAN
        sql = "SELECT id FROM Dean WHERE name = %s"
        val = (dean_name, )
        db.execute(sql, val)
        dean_id = db.fetchall()[0][0]

        while True:
            message = input("Message: ")
            if message != '':
                break

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
                              "                                                             Press (M) To Return To Dean Menu: ").lower()
                if error == "t":
                    update_professor('Courses Taught', 'CoursesTaught', professor_name)
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
        prof_password = input("Enter Their Password: ")
        if prof_password != '':
            break

    # SANITIZE PASSWORD
    prof_password = sanitize_password(prof_password, prof_name, "Professor")

    # CONFIRM PASSWORD
    while True:
        confirm_prof_password = input("Confirm Their Password: ")
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
        try:
            prof_age = int(input("Enter Their Age: "))
        except ValueError:
            prof_age = age_not_num("Professor")
        if prof_age != '':
            break


    # PHONE NUMBER
    while True:
        prof_phone_number = input("Enter Their Phone Number: ")
        if prof_phone_number != '':
            break


    # SANITIZE PHONE NUMBER
    prof_phone_number = sanitize_phone_number(prof_phone_number, "Professor")


    # COURSES TAUGHT
    while True:
        prof_courses_taught = input("Enter The Courses You Teach: ")
        if prof_courses_taught != '':
            break

    # CHECKING IF THE COURSES ARE AVAILABLE
    prof_courses_taught = sanitize_courses(prof_courses_taught, "Professor")



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
    clear()
    print("DEAN ADMIN OPTIONS")
    print(now)
    print("--------------------------------")
    print("Press (M) To Return To Dean Menu")
    print("--------------------------------")
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
        delete_all_prof_data()
    elif dean_choice == "7":
        delete_all_stu_data()
    elif dean_choice == "8":
        delete_all_data()
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
        sql = "INSERT INTO Course (name, description) VALUES (%s, %s)"
        val = (new_course_number, full_description)
        db.execute(sql, val)
        mydb.commit()

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
        print("Application Needs To Be Restarted To View New Course")
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
    if len(course_name) == 1:
        course_name = course_name.lower()
    if course_name == "c":
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
            edit_to_make = input("Would You Like To Edit The Name Of The Course Or The Description? ").lower()
            if edit_to_make != '' and (edit_to_make == "name" or edit_to_make == "description"):
                break
    else:
        edit_to_make = courseDescriptionOrName

    if edit_to_make == "name":
        while True:
            print()
            new_course_name = input("Enter The New Name Of The Course: ").upper()
            if new_course_name != '':
                break


        # CONFIRMATION
        while True:
            confirmation = input("CONFIRMATION: Are You Sure You Want To Edit The Name Of This Course? ").lower()
            if confirmation != '' and (confirmation == "yes" or confirmation == "no"):
                break
        if confirmation == "yes":
            sql = "UPDATE Course SET name = %s WHERE name = %s"
            val = (new_course_name, course_name)
            db.execute(sql, val)
            mydb.commit()

            # SET UP NOTIFICATION
            notification = f"{course_name} Name Has Been Changed To - {new_course_name}"
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

    elif edit_to_make == "description":
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
        elif dean_choice == "2":
            change_minimum_math_level(major_name, major_details)
        elif dean_choice == "3":
            change_minimum_eng_level(major_name, major_details)
        elif dean_choice == "4":
            change_major_requirements(major_name, major_details)

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
        if not checkCourse(new_minimum_english_level):
            print("Invalid English Course. Try Again")
        if checkCourse(new_minimum_english_level):
            break

    # CHECKING IF C WAS ENTERED
    if len(new_minimum_english_level) == 1:
        new_minimum_english_level = new_minimum_english_level.lower()
    if new_minimum_english_level == "c":
        view_all_majors("Dean")

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
        new_major_requirements = input("New Major Requirements: ")
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










# CHECK MAJOR
def checkMajor(major_name):
    db.execute("SELECT name FROM Major")
    all_majors = db.fetchall()

    all_majors = [all_majors[i][0] for i in range(len(all_majors))]

    return major_name in all_majors








# PROFESSOR MENU
def ProfessorMenu(name):
    clear()
    # GETTING INBOX COUNT
    Prof = Professor(prof_name.split()[0], prof_name.split()[1], None, None, None, None, None)
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
    print("Press (A) To Open Inbox")
    print("-----------------------")
    print()
    print(f"INBOX: {inbox_count}")
    print()
    print("AVAILABLE OPTIONS")
    print()
    print("1 - View Profile")
    print("2 - View All Courses")
    print("3 - View Courses Taught")
    print()
    while True:
        prof_choice = input("Choose An Option: ").lower()
        if prof_choice != '':
            break

    if prof_choice == "l":
        login()
    elif prof_choice == "a":
        professor_inbox()
    elif prof_choice == "s":
        prof_send_notification()
    elif prof_choice == "1":
        view_prof_profile()
    elif prof_choice == "2":
        view_all_courses_prof()
    elif prof_choice == "3":
        view_courses_taught()

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

    print("<" * (len(Prof.getAddress()) // 2), "PROFILE", ">" * (len(Prof.getAddress()) // 2 + 1))

    print("-" * len(Prof.getAddress()) + "---------")
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
    print("-" * len(Prof.getAddress()) + "---------")
    print()
    while True:
        back = input("Press (C) To Change Your Password:\nPress (M) To Return To Professor Menu: ").lower()
        if back == "m":
            ProfessorMenu(Prof.getFullName())
        elif back == "c":
            change_professor_password(prof_name, Prof.getID())


# VIEW ALL COURSES
def view_all_courses_prof():
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
    new_courses = sanitize_courses(new_courses)

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
        error = input("That Course Was Not Found. Press (T) To Try Again:\n"
                      "                           Press (M) To Return To Professor Menu: ").lower()
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
        elif error == "m":
            if came_from == "Edit_Course":
                DeanMenu(None)
            elif came_from == "Student Search For Course":
                StudentMenu(None)
            elif came_from == "Dean Search For Course":
                DeanMenu(None)
            elif came_from == "Prof Search For Course":
                ProfessorMenu(None)
            elif came_from == "Dean Remove Course":
                dean_admin_options()


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
    print()

    print("-" * len(course) + "------------------")
    print(f"COURSE CANCELLED: {course.isCourseCancelled()}")
    print("-" * len(course) + "------------------")
    print()
    # GET THE NAMES OF THE STUDENTS ENROLLED
    names = course.getStudentNamesInCourse()
    if names != None:
        names = names.split()
        students_in_course = [names[i] + " " + names[i+1] for i in range(len(names) // 2)]
    else:
        students_in_course = None

    print(f"Students In Course: {students_in_course}")
    # IF NO STUDENTS ARE IN THE COURSE THEN THE studentsCount IS NOT SHOWN
    if course.getStudentNamesInCourse() != None:
        # GET THE STUDENT COUNT
        print(f"Number Of Students Enrolled: {course.getStudentCountInCourse()}")
        # COMPUTE THE CLASS AVERAGE
        all_grades = []
        all_names  = course.getStudentNamesInCourse().split()
        for i in range(course.getStudentCountInCourse()):
            # GETTING STUDENTS INFO
            sql = "SELECT CoursesEnrolledIn, grades FROM Student WHERE name = %s"
            val = (all_names[i+i] + " " + all_names[i+i+1], )
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
                drop_student_from_course(course_name)
            elif back == "v":
                view_student_grade_for_course(all_names, course.getStudentCountInCourse(), course_name)
            elif back == "m":
                ProfessorMenu(None)

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
        ProfessorMenu(None)
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
def view_student_grade_for_course(students_in_course, num_students_in_course, course_name, came_from=None):
    clear()
    print("-------------------")
    print("VIEW STUDENT GRADES")
    print("-------------------")
    print()
    grades_for_course = {}
    for i in range(num_students_in_course):
        # GETTING STUDENTS INFO
        sql = "SELECT name, grades FROM Student WHERE name = %s"
        val = (students_in_course[i+i] + " " + students_in_course[i+i+1],)
        db.execute(sql, val)
        result = db.fetchall()
        for j, grade  in enumerate(result[0][1].split()):
            if grade.replace(':', '') == course_name:
                grades_for_course.update({result[0][0].split()[0] + " " + result[0][0].split()[1]: result[0][1].split()[j+1]})

    # PRINT THE DICTIONARY
    for key in grades_for_course:
        print(f"{key}: {grades_for_course[key]}")

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
    print(f"CURRENT PASSWORD: {prof_password}")
    print()
    while True:
        new_pwd = input("Enter Your New Password: ")
        if new_pwd != '':
            break

    # CHECKING IF C WAS ENTERED
    if len(new_pwd) == 1:
        new_pwd = new_pwd.lower()
    if new_pwd == "c":
        ProfessorMenu(prof_name)
    new_pwd = sanitize_password(new_pwd, prof_name)

    confirm_new_pwd = input("Confirm Your Password: ")

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
        if len(to) == 1:
            to = to.lower()
        if to == "c":
            ProfessorMenu(None)

        # CHECKING IF A WAS ENTERED
        if len(to) == 1:
            to = to.lower()
        if to == "a":
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
            if stu_name != '':
                break
        sql = "SELECT id FROM Student WHERE name = %s"
        val = (stu_name, )
        db.execute(sql, val)
        stu_id = db.fetchall()
        if len(stu_id) == 0:
            no_person_found("Notification", "Prof")
        stu_id = stu_id[0][0]

        while True:
            message = input("Message: ")
            if message != '':
                break

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

    # PROFESSOR
    elif to == "Professor":
        while True:
            print()
            professor_name = capitalize(input("Enter The Name Of The Professor: "))
            if professor_name != '':
                break
        sql = "SELECT id FROM Professor WHERE name = %s"
        val = (professor_name, )
        db.execute(sql, val)
        prof_id = db.fetchall()
        if len(prof_id) == 0:
            no_person_found("Notification", "Prof")
        prof_id = prof_id[0][0]

        while True:
            message = input("Message: ")
            if message != '':
                break

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

    # DEAN
    elif to == "Dean":
        while True:
            print()
            deanName = capitalize(input("Enter The Name Of The Dean: "))
            if deanName != '':
                break
        # CHECKING IF CORRECT NAME WAS ENTERED
        sql = "SELECT * FROM Dean WHERE name = %s"
        val = (deanName,)
        db.execute(sql, val)
        result = db.fetchall()
        if len(result) == 0:
            no_person_found("Notification", "Prof")

        # GETTING THE ID OF THE PROFESSOR
        sql = "SELECT id FROM Professor WHERE name = %s"
        val = (prof_name, )
        db.execute(sql, val)
        prof_id = db.fetchall()[0][0]

        while True:
            message = input("Message: ")
            if message != '':
                break

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

# PROF SEND ANNOUNCEMENT
def prof_send_announcement():
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


    for i in range(len(all_notifications)):
        print("-" * len(all_notifications[i][1]) + "---------")
        print(f"Id: {all_notifications[i][0]}")
        print(f"Date: {all_notifications[i][3]}")
        print(f"Received From: {all_notifications[i][2]}")
        print(f"Message: {all_notifications[i][1]}")
        print("-" * len(all_notifications[i][1]) + "---------")
        print()

    while True:
        print()
        print("Press (D) To Filter By Date:              |  Press (C) To Clear A Notification:")
        print("Press (F) To Filter By Received From:     |  Press (CA) To Clear All Notifications:")
        print("Press (M) To Filter By Message:           |  Press (S) To Return To Professor Menu:")
        print()
        filter = input("Choose An Option: ")
        if filter == "d":
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


# STUDENT MENU
def StudentMenu(name):
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
    print("Press (A) To Open Inbox")
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
    elif stu_choice == "a":
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
    print(f"Courses Enrolled In: {Stu.getCoursesEnrolledIn()}")
    print(f"Grades: {Stu.getGrades()}")
    print(f"GPA: {Stu.getGPA()}")
    print(f"Major: {Stu.getMajor()}")
    print("-" * len(Stu.getAddress()) + "---------")
    print()
    while True:
        back = input("Press (C) To Change Your Password:\nPress (D) To Drop A Class:\nPress (R) To Request Major Change:\nPress (M) To Return To Student Menu: ").lower()
        if back == "m":
            StudentMenu(Stu.getFullName())
        elif back == "r":
            request_major_change(Stu.getID(), Stu.getFullName(), Stu.getMajor())
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
    print()
    print(f"CURRENT PASSWORD: {stu_password}")
    print()
    while True:
        new_pwd = input("Enter Your New Password: ")
        if new_pwd != '':
            break

    # CHECKING IF C WAS ENTERED
    if len(new_pwd) == 1:
        new_pwd = new_pwd.lower()
    if new_pwd == "c":
        StudentMenu(stu_name)
    new_pwd = sanitize_password(new_pwd, stu_name)

    confirm_new_pwd = input("Confirm Your Password: ")

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


    for i in range(len(all_notifications)):
        # AUTO FIT THE BROKEN LINES
        max_len_of_attributes = max([len(all_notifications[i][1]), len(all_notifications[i][2])])
        if max_len_of_attributes == len(all_notifications[i][1]):
            broken_line_added = "-" * len("Message: ")
        else:
            broken_line_added = "-" * len("Received From: ")

        print("-" * max_len_of_attributes + broken_line_added)
        print(f"Id: {all_notifications[i][0]}")
        print(f"Date: {all_notifications[i][3]}")
        print(f"Received From: {all_notifications[i][2]}")
        print(f"Message: {all_notifications[i][1]}")
        print("-" * max_len_of_attributes + broken_line_added)
        print()

    while True:
        print()
        print("Press (D) To Filter By Date:              |  Press (C) To Clear A Notification:")
        print("Press (F) To Filter By Received From:     |  Press (CA) To Clear All Notifications:")
        print("Press (M) To Filter By Message:           |  Press (S) To Return To Student Menu:")
        print()
        filter = input("Choose An Option: ")
        if filter == "d":
            filter_stu_notification_by_date(all_notifications)
        elif filter == "f":
            filter_stu_notification_by_received_from(all_notifications)
        elif filter == "m":
            filter_stu_notification_by_message(all_notifications)
        elif filter == "c":
            clear_student_notification()
        elif filter == "ca":
            clear_all_student_notifications(Stu.getID())
        elif filter == "s":
            StudentMenu(None)

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
        if to != '' and (to == "Student" or to == "Professor" or to == "Dean"):
            break
        if to == '' or (to != "Student" or to != "Professor" or to != "Dean"):
            print("Messages Can Only Be Sent To: Dean, Professor Or Student")

    # CHECKING IF C WAS ENTERED
    if len(to) == 1:
        to = to.lower()
    if to == "c":
        ProfessorMenu(None)

    # STUDENT
    if to == "Student":
        while True:
            print()
            student_name = capitalize(input("Enter The Name Of The Student: "))
            if student_name != '':
                break
        sql = "SELECT id FROM Student WHERE name = %s"
        val = (student_name, )
        db.execute(sql, val)
        stu_id = db.fetchall()
        if len(stu_id) == 0:
            no_person_found("Notification", "Stu")
        stu_id = stu_id[0][0]

        while True:
            message = input("Message: ")
            if message != '':
                break

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
                StudentMenu(None)

    # PROFESSOR
    elif to == "Professor":
        while True:
            print()
            professor_name = capitalize(input("Enter The Name Of The Professor: "))
            if professor_name != '':
                break
        sql = "SELECT id FROM Professor WHERE name = %s"
        val = (professor_name, )
        db.execute(sql, val)
        prof_id = db.fetchall()
        if len(prof_id) == 0:
            no_person_found("Notification", "Stu")
        prof_id = prof_id[0][0]

        while True:
            message = input("Message: ")
            if message != '':
                break

        # SET UP NOTIFICATION
        sql = "INSERT INTO professor_notification (notification, received_from, date, prof_id) VALUES (%s, %s, %s, %s)"
        val = (message, f"Professor ({prof_name})", now, prof_id)
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

    # DEAN
    elif to == "Dean":
        while True:
            print()
            deanName = capitalize(input("Enter The Name Of The Dean: "))
            if deanName != '':
                break
        # CHECKING IF CORRECT NAME WAS ENTERED
        sql = "SELECT * FROM Dean WHERE name = %s"
        val = (deanName,)
        db.execute(sql, val)
        result = db.fetchall()
        if len(result) == 0:
            no_person_found("Notification", "Stu")

        # GETTING THE ID OF THE STUDENT
        sql = "SELECT id FROM Student WHERE name = %s"
        val = (stu_name, )
        db.execute(sql, val)
        stu_id = db.fetchall()[0][0]

        while True:
            message = input("Message: ")
            if message != '':
                break

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
        clear()
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
    print()

    print("-" * len(course) + "------------------")
    print(f"COURSE CANCELLED: {course.isCourseCancelled()}")
    print(f"Class Size: {course.getStudentCountInCourse()}")
    print("-" * len(course) + "------------------")
    print()

    while True:
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
        sql = "INSERT INTO dean_notification (notification, received_from, date, person_id) VALUES (%s, %s, %s, %s)"
        val = (f"{stu_name} Enrolled In: {course_name}", "Student", now, Stu.getID())
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
        sql = "INSERT INTO dean_notification (notification, received_from, date, person_id) VALUES (%s, %s, %s, %s)"
        val = (f"{stu_name} Dropped: {class_to_drop}", "Student", now, student_id)
        db.execute(sql, val)
        mydb.commit()

        print()
        print(f"You Dropped {class_to_drop}")
        while True:
            print()
            back = input("Press (M) To Return To Student Menu: ").lower()
            if back == "m":
                StudentMenu(None)

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
                    new_password = input(f"Enter {msg} Password: ")
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
                    new_password = input(f"Enter {msg} Password: ")
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
                    new_password = input(f"Enter {msg} Password: ")
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
def sanitize_courses(sub_courses, came_from=None):
    if came_from == None:
        msg = "You"
    else:
        msg = "They"

    if not checkCourse(sub_courses):
        print()
        print(f"AVAILABLE COURSES:")
        print()
        print(Course.getAll_Courses()) # TODO
        while True:
            while True:
                print()
                tmp = input("INVALID COURSES. Check To See If All Courses You Entered Are Available. Press (T) To Try Again: ").lower()
                if tmp != '':
                    break
            if tmp == "t":
                print()
                new_courses = input(f"Enter The Courses {msg} Teach: ").upper()

                if not checkCourse(new_courses):
                    new_courses = sanitize_courses(new_courses)

                return new_courses

    return sub_courses
def checkCourse(sub_courses):
    counter = 0
    all_courses = Course.getAll_Courses()
    sub_courses = sub_courses.split()
    for i in range(len(sub_courses)):
        for j in range(len(all_courses)):
            if sub_courses[i] == all_courses[j][0]:
                counter += 1

    return counter == len(sub_courses)
def age_not_num(came_from=None):
    if came_from == None:
        msg = "Your"
    else:
        msg = "Their"
    while True:
        while True:
            print()
            tmp = input(f"Invalid Input. {msg} Age Must Be A Number. Press (T) To Try Again: ").lower()
            if tmp != '':
                break
        if tmp == "t":
            try:
                print()
                new_age = int(input(f"Enter {msg} Age: "))

            except ValueError:
                new_age = age_not_num()

            return new_age


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
                password = input(f"Enter {msg} Password: ")
                if password != '':
                    break
            password = sanitize_password(password, name)
            confirm_password = input(f"Confirm {msg} Password: ")
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
def indexOf(string, index_of):
    for i in range(len(string)):
        if string[i] == index_of:
            return i

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






