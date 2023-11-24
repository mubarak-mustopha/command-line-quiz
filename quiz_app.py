import os
import re
import json
import random

def remove_space(string):
    return re.sub(" ","",string)

def get_questions(num_question = 40):
    QUESTIONS = [question for question in json.load(open("gns-pq.json")) if question != None]
    random.shuffle(QUESTIONS)
    return QUESTIONS[:num_question]

def clear_screen():
    clear = "cls" if os.name == 'nt' else "clear"
    return os.system(clear)

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
        clear_screen()
        print("Result to each question shows immediately after you answer it.")
        for q_num,question in enumerate(self._questions):
            is_multiple_choice = self._is_multiple_choice(question)
            print(f"\nQuestion number {q_num}")
            print(question["question"])
            if is_multiple_choice:
                options = '\n'.join(question['options'])
                print(f"\n{options}")
            answer = input("Type in your answer: ")
            print()
            if self._is_correct(question,answer, is_multiple_choice):
                print("You got that right")
                self._increment_score()
                clear_screen()
            else:
                print(f"You missed.\nCorrect answer is {question['answer']}")    
                self._missed_questions.append(question)

        self._print_score()        

    def _print_score(self):
        print(f"You got {self._score} questions right out of {len(self._questions)}")
     
        
gns_questionniare = Questionniare(get_questions(10))
gns_questionniare.start()
