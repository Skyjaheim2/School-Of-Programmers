import os
import mysql.connector
from Main_School import ProfessorMenu, indexOf, createAssignmentPrompt, isDue
clear = lambda: os.system('cls')
db_user = os.environ.get("DB_USER")
db_password = os.environ.get('DB_PASSWORD')

mydb = mysql.connector.connect(host="localhost", user=db_user, passwd=db_password, database="student")

db = mydb.cursor()


class Assignment:
    def __init__(self):
        self.short_ans_questions = {}
        self.multiple_choice_questions = {}
        self.question_type_look_up = {}
        self.answer_prompts = {}
        self.correct_answers = {}
        self.answer_choices = ['a.', 'b.', 'c.', 'd.']

    # STATIC METHODS
    @staticmethod
    def assignmentAlreadyExist(assignment_title):
        sql = "SELECT * FROM assignments WHERE title = %s"
        val = (assignment_title,)
        db.execute(sql, val)
        results = db.fetchall()
        if len(results) == 0:
            return False
        return True
    @staticmethod
    def validateDueDate(due_date):
        tmp_date = due_date
        all_months = {"January", "February", "March", "April", "May", "June", "July", "August",
                      "September", "October", "November", "December"}

        try:
            due_date = due_date.split()
            due_date_month = due_date[0]
            due_date_day = int(due_date[1].replace(',', ''))
            due_date_year = int(due_date[2])
        except:
            return 0

        # INVALID MONTH
        if due_date_month not in all_months:
            return -1
        # INVALID DAY
        if due_date_day < 1 or due_date_day > 31 if due_date_month != "February" else 28:
            return -2
        # DATE HAS PASSED
        if isDue(tmp_date):
            return -3

        return 1
    @staticmethod
    def getProfessorID(name):
        sql = "SELECT id FROM Professor WHERE name = %s"
        val = (name, )
        db.execute(sql, val)
        results = db.fetchall()
        if len(results) == 0:
            return None
        prof_id = results[0][0]
        return prof_id

class MultipleChoiceAssignment(Assignment):
    def __init__(self, courseName, assignmentType, prof_name):
        super().__init__()
        self.__courseName = courseName
        self.__assignmentType = assignmentType
        self.__prof_name = prof_name

        print("--------" + "-" * len(self.__courseName) + "-" * len(self.__assignmentType) + "--")
        print(f"CREATING {self.__courseName} {self.__assignmentType.upper()}")
        print("--------" + "-" * len(self.__courseName) + "-" * len(self.__assignmentType) + "--")
        print()
        shortendAssignmentType = self.__assignmentType[:indexOf(self.__assignmentType, "(")]
        # TITLE
        while True:
            print()
            self.__assignment_title = input(f"{shortendAssignmentType} Title: ")
            if self.__assignment_title.lower() == "c":
                createAssignmentPrompt(self.__courseName)
                break

            if self.assignmentAlreadyExist(self.__assignment_title):
                print("That Assignment Has Already Been Created")
            else:
                if self.__assignment_title != '':
                    break
        # NUMBER OF QUESTIONS
        while True:
            print()
            self.__num_questions = input("Number Of Questions: ")
            if self.__num_questions.lower() == "c":
                createAssignmentPrompt(self.__courseName)
                break
            if not self.__num_questions.isdigit():
                print("Must Be A Number")
            else:
                self.__num_questions = int(self.__num_questions)
                break
        # DURATION
        while True:
            print()
            self.__duration = input("Duration(Mins): ").lower()
            if self.__duration == "c":
                createAssignmentPrompt(self.__courseName)
                break
            if not self.__duration.isdigit():
                print("Duration Must Be A Number")
            else:
                break
        # DUE DATE
        while True:
            formatError = False
            print()
            self.__due_date = input("Due Date(MM/DD/YYYY): ")
            if self.__due_date == "c":
                createAssignmentPrompt(self.__courseName)
                break
            if self.validateDueDate(self.__due_date) == 0:
                formatError = True
                print("Invalid Date Format")
            elif self.validateDueDate(self.__due_date) == -1:
                formatError = True
                print("Invalid Month")
            elif self.validateDueDate(self.__due_date) == -2:
                formatError = True
                print("Invalid Day")
            elif self.validateDueDate(self.__due_date) == -3:
                formatError = True
                print("That Date Has Already Passed")
            if not formatError:
                break
        # DESCRIPTION
        print()
        self.__assignment_description = input(f"{shortendAssignmentType} Description(Optional): ")
        if self.__assignment_description.lower() == "c":
            createAssignmentPrompt(self.__courseName)


    def createAssignment(self):
        clear()
        for i in range(1, self.__num_questions + 1):
            print()
            # GET THE QUESTION
            assigned_questions = input(f"Question: {i}: ")
            if assigned_questions.lower() == "c":
                ProfessorMenu(self.__prof_name)
            self.multiple_choice_questions.update({i: assigned_questions})
            tmp_prompt_answer = {}
            # GET THE ASSIGNED PROMPTS
            for choice in self.answer_choices:
                while True:
                    assigned_ans_prompt = input(f"{choice.replace('.', '')}: ")
                    if assigned_ans_prompt != '':
                        break
                if assigned_ans_prompt.lower() == "c":
                    ProfessorMenu(self.__prof_name)
                tmp_prompt_answer.update({choice: assigned_ans_prompt})
            # STORE ALL THE PROMPT ANSWERS
            prompt_ans_to_store = f"a. {tmp_prompt_answer['a.']}\nb. {tmp_prompt_answer['b.']}\nc. {tmp_prompt_answer['c.']}\nd. {tmp_prompt_answer['d.']}"
            self.answer_prompts.update({i: prompt_ans_to_store})
            # GET THE CORRECT ANSWER
            while True:
                correct_answer = input("Enter The Correct Answer: ").lower()
                correct_answer += '.'
                if correct_answer not in self.answer_choices:
                    print("Invalid Choice. Enter a, b, c, or d")
                    print()
                else:
                    self.correct_answers.update({i: correct_answer})
                    break

        clear()
        print("------------")
        print(f"{self.__assignmentType} CREATED")
        print("------------")
        print()
        if self.__assignment_description != '':
            print("-" * len(self.__assignment_description))
            print(self.__assignment_description)
            print("-" * len(self.__assignment_description))
            print()
        print(f"Duration: {self.__duration}")
        print(f"Due Date: {self.__due_date}")
        print()
        for i in range(1, self.__num_questions + 1):
            print(self.multiple_choice_questions[i])
            print(self.answer_prompts[i])
            print(f"Correct Answer: {self.correct_answers[i]}")
            print()

        # CONFIRMATION
        while True:
            print()
            confirmation = input(f"CONFIRMATION: Do You Want To Save This {self.__assignmentType}? ").lower()
            if confirmation == "yes" or confirmation == "no":
                break

        if confirmation == "yes":
            db.execute("SELECT id FROM assignments")
            results = db.fetchall()
            if len(results) == 0:
                assign_id = 1
            else:
                assign_id = results[len(results) - 1][0] + 1

            for question in self.multiple_choice_questions:
                # QUESTIONS
                question_num = question
                Questions = self.multiple_choice_questions[question]
                # ANSWERS
                answer_prompt_num = question
                answer_prompt = self.answer_prompts[question]
                # CORRECT ANSWERS
                correct_answer_num = question
                correct_answer = self.correct_answers[question]

                sql = "INSERT INTO assignments (id, assignment_type, title, description, question_num, questions, answer_prompts_num, answer_prompts, correct_answer_num, correct_answer, prof_id, duration, due_date, course_name)" \
                      "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (assign_id, self.__assignmentType, self.__assignment_title, self.__assignment_description, question_num, Questions,
                       answer_prompt_num, answer_prompt, correct_answer_num, correct_answer, self.getProfessorID(self.__prof_name), self.__duration,
                       self.__due_date, self.__courseName)
                db.execute(sql, val)
                mydb.commit()

            while True:
                print()
                back = input(f"{self.__assignmentType} Saved. Press (M) To Return To Professor Menu: ").lower()
                if back == "m":
                    ProfessorMenu(self.__prof_name)
        elif confirmation == "no":
            ProfessorMenu(self.__prof_name)

class ShortAnswerAssignment(Assignment):
    def __init__(self, courseName, assignmentType, prof_name):
        super().__init__()
        self.__courseName = courseName
        self.__assignmentType = assignmentType
        self.__prof_name = prof_name

        print("--------" + "-" * len(self.__courseName) + "-" * len(self.__assignmentType) + "--")
        print(f"CREATING {self.__courseName} {self.__assignmentType.upper()}")
        print("--------" + "-" * len(self.__courseName) + "-" * len(self.__assignmentType) + "--")
        print()
        shortendAssignmentType = self.__assignmentType[:indexOf(self.__assignmentType, "(")]
        # TITLE
        while True:
            print()
            self.__assignment_title = input(f"{shortendAssignmentType} Title: ")
            if self.__assignment_title.lower() == "c":
                createAssignmentPrompt(self.__courseName)
                break
            if self.assignmentAlreadyExist(self.__assignment_title):
                print("That Assignment Has Already Been Created")
            else:
                if self.__assignment_title != '':
                    break
        # NUMBER OF QUESTIONS
        while True:
            print()
            self.__num_questions = input("Number Of Questions: ")
            if self.__num_questions.lower() == "c":
                createAssignmentPrompt(self.__courseName)
                break
            if not self.__num_questions.isdigit():
                print("Must Be A Number")
            else:
                self.__num_questions = int(self.__num_questions)
                break
        # DURATION
        while True:
            print()
            self.__duration = input("Duration(Mins): ").lower()
            if self.__duration == "c":
                createAssignmentPrompt(self.__courseName)
                break
            if not self.__duration.isdigit():
                print("Duration Must Be A Number")
            else:
                break
        # DUE DATE
        while True:
            formatError = False
            print()
            self.__due_date = input("Due Date(MM/DD/YYYY): ")
            if self.__due_date == "c":
                createAssignmentPrompt(self.__courseName)
                break
            if self.validateDueDate(self.__due_date) == 0:
                formatError = True
                print("Invalid Date Format")
            elif self.validateDueDate(self.__due_date) == -1:
                formatError = True
                print("Invalid Month")
            elif self.validateDueDate(self.__due_date) == -2:
                formatError = True
                print("Invalid Day")
            elif self.validateDueDate(self.__due_date) == -3:
                formatError = True
                print("That Date Has Already Passed")
            if not formatError:
                break
        # DESCRIPTION
        print()
        self.__assignment_description = input(f"{shortendAssignmentType} Description(Optional): ")
        if self.__assignment_description.lower() == "c":
            createAssignmentPrompt(self.__courseName)

    def createAssignment(self):
        for i in range(1, self.__num_questions + 1):
            print()
            # GET THE QUESTION
            assigned_questions = input(f"Question: {i}: ")
            if assigned_questions.lower() == "c":
                ProfessorMenu(self.__prof_name)
            self.short_ans_questions.update({i: assigned_questions})

        clear()
        print("-" * len(self.__assignmentType) + "--------")
        print(f"{self.__assignmentType} CREATED")
        print("-" * len(self.__assignmentType) + "--------")
        print()
        if self.__assignment_description != '':
            print("-" * len(self.__assignment_description))
            print(self.__assignment_description)
            print("-" * len(self.__assignment_description))
            print()
        print(f"Duration: {self.__duration}")
        print(f"Due Date: {self.__due_date}")
        print()
        for i in range(1, self.__num_questions + 1):
            print(f"{i}.{self.short_ans_questions[i]}")
            print()

        # CONFIRMATION
        while True:
            print()
            confirmation = input(f"CONFIRMATION: Do You Want To Save This {self.__assignmentType}? ").lower()
            if confirmation == "yes" or confirmation == "no":
                break

        if confirmation == "yes":
            db.execute("SELECT id FROM assignments")
            results = db.fetchall()
            if len(results) == 0:
                assign_id = 1
            else:
                assign_id = results[len(results) - 1][0] + 1

            for question in self.short_ans_questions:
                # QUESTIONS
                question_num = question
                Questions = self.short_ans_questions[question]

                sql = "INSERT INTO assignments (id, assignment_type, title, description, question_num, questions, prof_id, duration, due_date, course_name)" \
                      "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (
                assign_id, self.__assignmentType, self.__assignment_title, self.__assignment_description, question_num, Questions, self.getProfessorID(self.__prof_name),
                self.__duration, self.__due_date, self.__courseName)
                db.execute(sql, val)
                mydb.commit()

            while True:
                print()
                back = input(f"{self.__assignmentType} Saved. Press (M) To Return To Professor Menu: ").lower()
                if back == "m":
                    ProfessorMenu(self.__prof_name)
        elif confirmation == "no":
            ProfessorMenu(self.__prof_name)

class MixedAssignment(Assignment):
    def __init__(self, courseName, assignmentType, prof_name):
        super().__init__()
        self.__courseName = courseName
        self.__assignmentType = assignmentType
        self.__prof_name = prof_name
        print("--------" + "-" * len(self.__courseName) + "-" * len(self.__assignmentType) + "--")
        print(f"CREATING {self.__courseName} {self.__assignmentType.upper()}")
        print("--------" + "-" * len(self.__courseName) + "-" * len(self.__assignmentType) + "--")
        print()
        shortenedAssignType = self.__assignmentType[:indexOf(self.__assignmentType, "(")]
        # TITLE
        while True:
            print()
            self.__assignment_title = input(f"{shortenedAssignType} Title: ")
            if self.__assignment_title.lower() == "c":
                createAssignmentPrompt(self.__courseName)
                break
            if self.assignmentAlreadyExist(self.__assignment_title):
                print("That Assignment Has Already Been Created")
            else:
                if self.__assignment_title != '':
                    break
        # NUMBER OF QUESTIONS
        while True:
            print()
            self.__num_questions = input("Number Of Questions: ")
            if self.__num_questions.lower() == "c":
                createAssignmentPrompt(self.__courseName)
                break
            if not self.__num_questions.isdigit():
                print("Must Be A Number")
            else:
                self.__num_questions = int(self.__num_questions)
                break
        # DURATION
        while True:
            print()
            self.__duration = input("Duration(Mins): ").lower()
            if self.__duration == "c":
                createAssignmentPrompt(self.__courseName)
                break
            if not self.__duration.isdigit():
                print("Duration Must Be A Number")
            else:
                break
        # DUE DATE
        while True:
            formatError = False
            print()
            self.__due_date = input("Due Date(MM/DD/YYYY): ")
            if self.__due_date == "c":
                createAssignmentPrompt(self.__courseName)
                break
            if self.validateDueDate(self.__due_date) == 0:
                formatError = True
                print("Invalid Date Format")
            elif self.validateDueDate(self.__due_date) == -1:
                formatError = True
                print("Invalid Month")
            elif self.validateDueDate(self.__due_date) == -2:
                formatError = True
                print("Invalid Day")
            elif self.validateDueDate(self.__due_date) == -3:
                formatError = True
                print("That Date Has Already Passed")
            if not formatError:
                break
        # DESCRIPTION
        print()
        self.__assignment_description = input(f"{shortenedAssignType} Description(Optional): ")
        if self.__assignment_description.lower() == "c":
            createAssignmentPrompt(self.__courseName)


    def createAssignment(self):
        clear()
        for i in range(1, self.__num_questions + 1):
            # QUESTION TYPE
            while True:
                print()
                question_type = input(f"Question {i} Type\nEnter 'S' For Short Answer And 'M' For Multiple Choice: ").lower()
                if question_type == 's' or question_type == 'm':
                    break

            # GET THE SHORT ANSWER QUESTION
            if question_type == 's':
                while True:
                    print()
                    assigned_short_ans_question = input("Enter Question: ")
                    if assigned_short_ans_question.lower() == 'c':
                        ProfessorMenu(self.__prof_name)
                        break
                    if assigned_short_ans_question != '':
                        break
                self.short_ans_questions.update({i: assigned_short_ans_question})
                self.question_type_look_up.update({i: question_type})

            # GET THE MULTIPLE CHOICE QUESTION
            elif question_type == 'm':
                while True:
                    print()
                    assigned_multiple_choice_question = input(f"Enter Question: {i}: ")
                    if assigned_multiple_choice_question.lower() == "c":
                        ProfessorMenu(self.__prof_name)
                        break
                    if assigned_multiple_choice_question != '':
                        break
                self.multiple_choice_questions.update({i: assigned_multiple_choice_question})
                self.question_type_look_up.update({i: question_type})
                tmp_prompt_answer = {}
                # GET THE ASSIGNED PROMPTS
                for choice in self.answer_choices:
                    assigned_ans_prompt = input(f"{choice}: ")
                    if assigned_ans_prompt.lower() == "c":
                        ProfessorMenu(self.__prof_name)
                    tmp_prompt_answer.update({choice: assigned_ans_prompt})
                # STORE ALL THE PROMPT ANSWERS
                prompt_ans_to_store = f"a. {tmp_prompt_answer['a.']}\nb. {tmp_prompt_answer['b.']}\nc. {tmp_prompt_answer['c.']}\nd. {tmp_prompt_answer['d.']}"
                self.answer_prompts.update({i: prompt_ans_to_store})
                # GET THE CORRECT ANSWER
                while True:
                    correct_answer = input("Enter The Correct Answer: ").lower()
                    correct_answer += '.'
                    if correct_answer not in self.answer_choices:
                        print("Invalid Choice. Enter a, b, c, or d")
                        print()
                    else:
                        self.correct_answers.update({i: correct_answer})
                        break

        clear()
        print("------------")
        print(f"{self.__assignmentType} CREATED")
        print("------------")
        print()
        if self.__assignment_description != '':
            print("-" * len(self.__assignment_description))
            print(self.__assignment_description)
            print("-" * len(self.__assignment_description))
            print()
        print(f"Duration: {self.__duration}")
        print(f"Due Date: {self.__due_date}")
        print()
        for i in range(1, self.__num_questions + 1):
            # DISPLAY THE SHORT ANSWER QUESTION
            if self.question_type_look_up[i] == 's':
                print(f"{i}.{self.short_ans_questions[i]}")
                print()
            # DISPLAY THE MULTIPLE CHOICE QUESTION
            else:
                print(f'{i}.{self.multiple_choice_questions[i]}')
                print(self.answer_prompts[i])
                print(f"Correct Answer: {self.correct_answers[i]}")
                print()

        # CONFIRMATION
        while True:
            print()
            confirmation = input(f"CONFIRMATION: Do You Want To Save This {self.__assignmentType}? ").lower()
            if confirmation == "yes" or confirmation == "no":
                break

        if confirmation == "yes":
            db.execute("SELECT id FROM assignments")
            results = db.fetchall()
            if len(results) == 0:
                assign_id = 1
            else:
                assign_id = results[len(results) - 1][0] + 1

            for i in range(1, self.__num_questions + 1):
                # ADD SHORT ANSWER
                if self.question_type_look_up[i] == 's':
                    question_num = i
                    Questions = self.short_ans_questions[i]
                    sql = "INSERT INTO assignments (id, assignment_type, title, description, question_num, questions, prof_id, duration, due_date, course_name)" \
                          "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    val = (
                    assign_id, self.__assignmentType, self.__assignment_title, self.__assignment_description, question_num, Questions,
                    self.getProfessorID(self.__prof_name), self.__duration, self.__due_date, self.__courseName)
                    db.execute(sql, val)
                    mydb.commit()
                # ADD MULTIPLE CHOICE
                else:
                    # QUESTIONS
                    question_num = i
                    Questions = self.multiple_choice_questions[i]
                    # ANSWERS
                    answer_prompt_num = i
                    answer_prompt = self.answer_prompts[i]
                    # CORRECT ANSWERS
                    correct_answer_num = i
                    correct_answer = self.correct_answers[i]

                    sql = "INSERT INTO assignments (id, assignment_type, title, description, question_num, questions, answer_prompts_num, answer_prompts, correct_answer_num, correct_answer, prof_id, duration, due_date, course_name)" \
                          "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    val = (
                    assign_id, self.__assignmentType, self.__assignment_title, self.__assignment_description, question_num, Questions,
                    answer_prompt_num, answer_prompt, correct_answer_num, correct_answer, self.getProfessorID(self.__prof_name), self.__duration,
                    self.__due_date, self.__courseName)
                    db.execute(sql, val)
                    mydb.commit()

            while True:
                print()
                back = input(f"{self.__assignmentType} Saved. Press (M) To Return To Professor Menu: ").lower()
                if back == "m":
                    ProfessorMenu(self.__prof_name)
        elif confirmation == 'no':
            ProfessorMenu(self.__prof_name)


# def Test():
#     Assignment = MultipleChoiceAssignment('MATH-30', 'Quiz(Multiple Choice)', 'Jaheim Archibald')
#
#     Assignment.createAssignment()


# Test()