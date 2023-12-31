import re
import json
import random

def remove_space(string):
    return re.sub(" ","",string)

def get_questions(num_question = 40):
    QUESTIONS = [question for question in json.load(open("gns-pq.json")) if question != None]
    random.shuffle(QUESTIONS)
    return QUESTIONS[:num_question]

class Questionniare:
    def __init__(self, questions) -> None:
        self._questions = questions
        self._missed_questions = []
        self._score = None

    def _increment_score(self):
        if not self._score:
            self._score = 1
        else:
            self._score += 1        

    def _is_multiple_choice(self,question):
        return isinstance(question['options'], list)

    def _is_correct(self, question, option, is_multiple_choice=False):
        if is_multiple_choice:
            return question['answer'][0] == option
        return remove_space(question['answer'].lower()) == remove_space(option.lower())#Analytic method --> analyticmethod        

    def start(self):
        print("Result to each question shows immediately after you answer it.")
        for q_num,question in enumerate(self._questions):
            is_multiple_choice = self._is_multiple_choice(question)
            print(f"Question number {q_num}")
            print(question["question"])
            if is_multiple_choice:
                options = '\n'.join(question['options'])
                print(f"\n{options}")
            answer = input("Type in your answer: ")
            if self._is_correct(question,answer, is_multiple_choice):
                print("You got that right")
                self._increment_score()
            else:
                print(f"You missed.\nCorrect answer is {question['answer']}")    
                self._missed_questions.append(question)
            print("*"*50)#indicate new question    
        self._print_score()        

    def _print_score(self):
        print(f"You got {self._score} questions right out of {len(self._questions)}")

    def get_missed_questions(self):
        return self._missed_questions    
     
class Quiz_app:
    def __init__(self):
        self.questions = []
        self.missed_questions = []

    def start_quiz(self):
        num_questions = int(input("How many questions would you like to practice with? "))

        self.questions = get_questions(num_questions)
        questionniare = Questionniare(self.questions)
        questionniare.start()

        self.missed_questions = questionniare.get_missed_questions()
        practice_missed_questions = input("Type 'yes' you want to practice yr missed questions? ")

        #practice-missed questions
        if practice_missed_questions == "yes" :
            questionniare = Questionniare(self.missed_questions)
            questionniare.start()

# gns_questionniare = Questionniare(get_questions(10))
# gns_questionniare.start()
gns_quiz_app = Quiz_app()
gns_quiz_app.start_quiz()