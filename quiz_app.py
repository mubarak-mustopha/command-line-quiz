#! /usr/bin/env python3
import sys
import re
import json
import random


def remove_whitespace(text):
    """
    Remove all whitespace characters from a string.

    Used for flexible answer matching where spacing shouldn't matter.

    Args:
        text (str): String to process

    Returns:
        str: String with all whitespace removed

    Example:
        >>> remove_whitespace("Analytic method")
        'Analyticmethod'
    """
    return re.sub(r"\s+", "", text)


def load_questions(filepath, num_questions=40):
    """
    Load and randomly sample questions from a JSON file.

    Args:
        filepath (str): Path to JSON file containing questions
        num_questions (int, optional): Number of questions to sample.
            Defaults to 40

    Returns:
        list: Random sample of questions (dicts with 'question', 'options', 'answer')

    Example:
        >>> questions = load_questions("quiz.json", 10)
        >>> len(questions)
        10
    """
    with open(filepath, "r", encoding="utf-8") as f:
        all_questions = json.load(f)

    # Filter out None values (malformed questions from PDF extraction)
    valid_questions = [q for q in all_questions if q is not None]

    random.shuffle(valid_questions)
    return valid_questions[:num_questions]


class Questionnaire:
    """
    Manages quiz administration, scoring, and tracking missed questions.

    Supports both multiple-choice and fill-in-the-blank question formats.

    Attributes:
        _questions (list): Questions to be asked
        _missed_questions (list): Questions answered incorrectly
        _score (int): Number of correct answers
    """

    def __init__(self, questions) -> None:
        """
        Initialize questionnaire with a list of questions.

        Args:
            questions (list): List of question dicts, each containing:
                - question (str): The question text
                - options (list or str): Answer choices or blank for fill-in
                - answer (str): Correct answer
        """
        self._questions = questions
        self._missed_questions = []
        self._score = 0

    def _increment_score(self):
        self._score += 1

    def _is_multiple_choice(self, question):
        """
        Determine if a question is multiple-choice format.

        Args:
            question (dict): Question data

        Returns:
            bool: True if question has multiple choice options, False otherwise
        """
        return isinstance(question["options"], list)

    def _is_correct_answer(self, question, user_answer):
        """
        Check if the user's answer matches the correct answer.

        For multiple-choice: Compares first character (a, b, c, d)
        For fill-in: Case-insensitive comparison with whitespace removed

        Args:
            question (dict): Question data containing the correct answer
            user_answer (str): User's submitted answer

        Returns:
            bool: True if answer is correct, False otherwise
        """
        is_multiple_choice = self._is_multiple_choice(question)
        correct_answer = question["answer"]
        if is_multiple_choice:
            # Compare just the letter choice (a, b, c, or d)
            return correct_answer[0].lower() == user_answer.lower()
        else:
            # For fill-in questions, ignore case and whitespace
            return remove_whitespace(correct_answer.lower()) == remove_whitespace(
                user_answer.lower()
            )

    def start(self):
        """
        Administer the quiz, displaying questions and collecting answers.

        Provides immediate feedback after each question and tracks the score.
        Stores missed questions for optional review.
        """
        print("Result to each question shows immediately after you answer it.\n")

        for question_num, question in enumerate(self._questions, start=1):
            is_multiple_choice = self._is_multiple_choice(question)

            # Display question
            print(f"Question number {question_num}")
            print(question["question"])

            # Display options if multiple choice
            if is_multiple_choice:
                options_text = "\n".join(question["options"])
                print(f"\n{options_text}")

            user_answer = input("\nType in your answer: ")

            if self._is_correct_answer(question, user_answer):
                print("Correct!\n")
                self._increment_score()
            else:
                print(f"Incorrect. The correct answer is: {question['answer']}")
                self._missed_questions.append(question)

            print("=" * 50)  # visual separator between questions
        self._print_final_score()

    def _print_final_score(self):
        total = len(self._questions)
        print(f"\n{'='*50}")
        print(f"FINAL SCORE: {self._score}/{total}")
        print(f"{'='*50}\n")

    def get_missed_questions(self):
        return self._missed_questions


class QuizApp:
    """
    Main application class for managing the quiz workflow.

    Handles user interaction, quiz initialization, and optional practice
    sessions for missed questions.

    Attributes:
        quiz_filepath (str): Path to the JSON file containing questions
        questions (list): Current set of questions being used
        missed_questions (list): Questions answered incorrectly in the main quiz
    """

    def __init__(self, quiz_filepath):
        self.quiz_filepath = quiz_filepath
        self.questions = []
        self.missed_questions = []

    def start_quiz(self):
        num_questions = self._get_question_count()

        self.questions = load_questions(self.quiz_filepath, num_questions)
        print(f"\nStarting quiz with {len(self.questions)} questions...\n")

        questionniare = Questionnaire(self.questions)
        questionniare.start()

        self.missed_questions = questionniare.get_missed_questions()

        if self.missed_questions:
            self._offer_practice_session()
        else:
            print("Perfect score! You didn't miss any questions. 🎉")

    def _get_question_count(self):
        """
        Prompt user for the number of questions they want to practice.

        Returns:
            int: Number of questions requested by user
        """
        while True:
            try:
                count = int(input("How many questions would you like to practice? "))
                if count > 0:
                    return count
                else:
                    print("Please enter a positive number.")
            except ValueError:
                print("Please enter a valid number.")

    def _offer_practice_session(self):
        """
        Ask if user wants to practice missed questions and start if yes.
        """
        num_missed = len(self.missed_questions)
        print(f"\nYou missed {num_missed} question(s).")

        response = (
            input("Would you like to practice your missed questions? (yes/no): ")
            .strip()
            .lower()
        )

        if response in ["yes", "y"]:
            print(f"\nStarting practice session with {num_missed} question(s)...\n")
            practice_questionnaire = Questionnaire(self.missed_questions)
            practice_questionnaire.start()
        else:
            print("Quiz session complete. Good job!")


def main():
    """
    Entry point for the quiz application.

    Accepts an optional command-line argument for the quiz file path.
    If no argument is provided, defaults to 'gns-pq.json'.
    """
    # Determine quiz file from command-line argument or use default
    if len(sys.argv) > 1:
        quiz_filepath = sys.argv[1]

        # Validate file extension
        if not quiz_filepath.endswith(".json"):
            print("Error: Quiz file must be a JSON file (.json extension)")
            sys.exit(1)
    else:
        quiz_filepath = "gns-pq.json"

    # Check if file exists
    try:
        with open(quiz_filepath, "r") as f:
            pass
    except FileNotFoundError:
        print(f"Error: Quiz file '{quiz_filepath}' not found")
        sys.exit(1)

    # Start the quiz application
    print(f"Loading quiz from: {quiz_filepath}\n")
    app = QuizApp(quiz_filepath)
    app.start_quiz()


if __name__ == "__main__":
    main()
