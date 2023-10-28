import re

QUESTIONS = [
            {
                "question": "Oneof theseis not astatement",

                "options": [
                        "a. Kayodeis tall",

                        "b. Femiis short",

                        "c. Ifeis not too short",

                        "d. Get methetallstudent "
                ],

                "answer": "d. Get methetallstudent +++"
        },

        {
                "question": "Oneof theseis not astatement",

                "options": [
                        "a. Iam finished!",

                        "b. What happened?",

                        "c. Relax.",

                        "d. Allof theabove "
                ],

                "answer": "d. Allof theabove +++"
        },

        {
                "question": "Anorganizedwayof doingsomethinginphilosophyis called+++ inphilosophy",

                "options": " ",

                "answer": "Methods"
        },

        {
                "question": "+++methodis theoldest method inphilosophy?",

                "options": " ",

                "answer": "Socratic"
        },

        {
                "question": "+++methodapplies theart of debatebymeans of questions andanswers",

                "options": " ",

                "answer": "Socratic"
        },
]

def remove_space(string):
    return re.sub(" ","",string)


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

    def _is_correct(self, question, option, is_multiple_choice):
        if is_multiple_choice:
            return question['answer'][0] == option
        return remove_space(question['answer'].lower()) == remove_space(option.lower())#Analytic method --> analyticmethod        

    def start(self):
        for question in self._questions:
            is_multiple_choice = self._is_multiple_choice(question)
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
        self._print_score()        

    def _print_score(self):
        print(f"You got {self._score} questions right out of {len(self._questions)}")
        
gns_questionniare = Questionniare(QUESTIONS)
gns_questionniare.start()
