import os
clear = lambda: os.system("cls")
import hashlib
try:
    import mysql.connector
except ImportError:
    print("Import Error: Do pip install mysql.connector-python To Use This Program")
import datetime
from datetime import date
from time import sleep
import random
current_date = date.today()
now = current_date.strftime("%B %d, %Y")

# CLASSES
from Professor import Professor
from Course import Course
from Person import Person
from Student import Student


mydb = mysql.connector.connect(host="localhost", user="root", passwd="jaheimSQL18", database="student")

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

    dean_password = input("Enter Your Password: ")
    # CHECKING IF THE PASSWORD MATCHES
    if not check_password_hash(dean_password, hashed_password):
        incorrect_password("Dean")

    update_course_database()
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


    prof_password = input("Enter Your Password: ")
    # CHECKING IF THE PASSWORD MATCHES
    if not check_password_hash(prof_password, hashed_password):
        incorrect_password("Professor")

    update_course_database()
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

    stu_password = input("Enter Your Password: ")
    # CHECKING IF THE PASSWORD MATCHES
    if not check_password_hash(stu_password, hashed_password):
        incorrect_password("Student")

    update_course_database()
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
    print("DEAN MENU")
    if name != None:
        print(f"Welcome {name}")
    print(now)
    print("--------------------")
    print("Press (L) To Log Out")
    print("--------------------")
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
        user_choice  = input("Choose An Option: ")
        # CHECKING IF L WAS ENTERED
        if len(user_choice) == 1:
            user_choice = user_choice.lower()
        if user_choice == "l":
            login()
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
def view_all_majors(came_from):
    clear()
    print("---------------")
    print("VIEW ALL MAJORS")
    print("---------------")
    print()
    all_majors = Student.getAllMajors()
    for i, major in enumerate(all_majors):
        if major != all_majors[-1]:
            print(major, end=", ")
        else:
            print(major, end="")
        if i == 4:
            print("\n")

    print()
    print()
    while True:
        back = input("Press (D) To Get The Description Of A Major:\n"
                     "Press (B) To Go Back: ")
        if back == "b":
            if came_from == "Update Student":
                update_student_info()

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
        update_student_info(name=student_name)
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
        print(f"CURRENT COURSES ENROLLED IN: {Stu.getCoursesEnrolledIn()}")
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
                              "                                                             Press (M) To Return To Dean Menu: ").lower()
                if error == "t":
                    update_student('Courses Enrolled In', 'CoursesEnrolledIn', name)
                elif error == "m":
                    DeanMenu(None)

        elif Stu.setCoursesEnrolledIn(new_courses) == -2:
            while True:
                print()
                error = input(f"Cant Enroll In More Than {Stu.MAX_COURSES_STUDENT_CAN_ENROLL_IN} Courses. Press (T) To Try Again:\n"
                              f"                                               Press (M) To Return To Dean Menu: ").lower()

                if error == "t":
                    update_student('Courses Enrolled In', 'CoursesEnrolledIn', name)
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
            print()
            print(f"You Changed {student_name} Courses Enrolled From {before_change} To {Stu.getCoursesEnrolledIn()}")
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
        if Stu.getGrades() != None:
            print("-" * len(Stu.getGrades()) + "----------------")
        print(f"CURRENT GRADES: {Stu.getGrades()}")
        print(f"GPA: {Stu.getGPA()}")
        if Stu.getGrades() != None:
            print("-" * len(Stu.getGrades()) + "----------------")
        before_change = Stu.getGrades()
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
        else:
            update_student_info(name=student_name)

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
                    update_student('Courses Enrolled In', 'CoursesEnrolledIn', name)
                elif error == "s":
                    view_all_majors("Update Student")
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
        update_professor_info(name=name)

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
                    f"Cant Enroll In More Than {Prof.MAX_COURSES_A_PROFESSOR_CAN_TEACH} Courses. Press (T) To Try Again:\n"
                    f"                                    Press (M) To Return To Dean Menu: ").lower()

                if error == "t":
                    update_professor('Courses Taught', 'CoursesTaught', name)
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



# PROFESSOR MENU
def ProfessorMenu(name):
    clear()
    print("PROFESSOR MENU")
    if name != None:
        print(f"Welcome {name}")
    print(now)
    print("--------------------")
    print("Press (L) To Log Out")
    print("--------------------")
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
        course_not_found()

    # COURSE WAS FOUND
    select_course_prof(course_name)


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

        while True:
            print()
            back = input("Courses Taught Successfully Updated. Press (M) To Return To Professor Menu: ").lower()
            if back == "m":
                ProfessorMenu(None)
    else:
        ProfessorMenu(None)

def course_not_found():
    print()
    while True:
        print()
        error = input("That Course Was Not Found. Press (T) To Try Again:\n"
                      "                           Press (M) To Return To Professor Menu: ").lower()
        if error == "t":
            search_for_course_prof()
        elif error == "m":
            ProfessorMenu(None)


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
    print(f"Students In Course: {course.getStudentNamesInCourse()}")
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

        while True:
            print()
            back = input("Course Successfully Added. Press (S) To Return To All Courses:\n"
                         "                           Press (M) To Return To Professor Menu: ").lower()
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

        new_names_to_add_to_database = students_in_course.replace(name_to_drop, '').strip()
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

        update_course_database()
        print()
        while True:
            back = input(f"You Have Dropped {name_to_drop} From {course_name} Press (M) To Return To Professor Menu: ").lower()
            if back == "m":
                ProfessorMenu(None)

    else:
        view_all_courses_prof()
# VIEW STUDENT GRADE FOR COURSE
def view_student_grade_for_course(students_in_course, num_students_in_course, course_name):
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
        back = input("Press (B) To Go Back:\nPress (M) To Return To Professor Menu: ").lower()
        if back == "b":
            select_course_prof(course_name)
        elif back == "m":
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



# STUDENT MENU
def StudentMenu(name):
    clear()
    clear()
    print("STUDENT MENU")
    if name != None:
        print(f"Welcome {name}")
    print(now)
    print("--------------------")
    print("Press (L) To Log Out")
    print("--------------------")
    print()
    print(f"INBOX: 0")
    print()
    print("AVAILABLE OPTIONS")
    print()
    print("1 - View Profile")
    print("2 - View All Courses") # TODO - Enroll And Drop Classes
    print("3 - View All Majors")  # TODO - View And Request Major Change

    print()
    while True:
        stu_choice = input("Choose An Option: ").lower()
        if stu_choice != '':
            break

    if stu_choice == "l":
        login()
    elif stu_choice == "1":
        view_student_profile()
    elif stu_choice == "2":
        view_all_courses_stu()
    elif stu_choice == "3":
        view_courses_taught()


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
        back = input("Press (C) To Change Your Password:\nPress (R) To Request Major Change:\nPress (M) To Return To Student Menu: ").lower()
        if back == "m":
            StudentMenu(Stu.getFullName())
        elif back == "r":
            request_major_change(Stu.getID(), Stu.getFullName(), Stu.getMajor())
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

    # TODO - CHECK IF MAJOR IS AVAILABLE BEFORE REQUESTING

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
        received_from = "Student"
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
        course_not_found()

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
            pass
        elif back == "m":
            StudentMenu(None)


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
        new_courses_to_add = courses_enrolled_in + " " + course_name
        sql = "UPDATE Student SET CoursesEnrolledIn = %s WHERE name = %s"
        val = (new_courses_to_add, stu_name)
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



# SANITIZE
def sanitize_password(password, name, came_from=None):
    if came_from == None:
        msg = "Your"
    else:
        msg = "Their"
    # TODO - Check Password Strength By The Amount Of Characters Or If It Is Similar To Name
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






