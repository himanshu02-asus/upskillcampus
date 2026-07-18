"""
Quiz Game
---------
A command-line quiz game that reads questions from a JSON file,
asks the user multiple-choice questions, tracks their score,
and shows the final result at the end.

Run:
    python quiz_game.py
(make sure questions.json is in the same folder)
"""

import json
import os
import random

QUESTIONS_FILE = "questions.json"


def load_questions(filename):
    if not os.path.exists(filename):
        print(f"'{filename}' not found. Creating a sample question file...")
        create_sample_questions(filename)

    with open(filename, "r") as f:
        return json.load(f)


def create_sample_questions(filename):
    """Create a starter questions.json file if one doesn't exist."""
    sample_questions = [
        {
            "question": "What does CPU stand for?",
            "options": ["Central Processing Unit", "Computer Personal Unit",
                        "Central Process Utility", "Control Processing Unit"],
            "answer": "Central Processing Unit"
        },
        {
            "question": "Which language is primarily used for this quiz program?",
            "options": ["Java", "Python", "C++", "JavaScript"],
            "answer": "Python"
        },
        {
            "question": "What is the output of 2 ** 3 in Python?",
            "options": ["6", "8", "9", "5"],
            "answer": "8"
        },
        {
            "question": "Which data structure uses FIFO (First In, First Out)?",
            "options": ["Stack", "Queue", "Tree", "Graph"],
            "answer": "Queue"
        },
        {
            "question": "What is the capital of India?",
            "options": ["Mumbai", "Kolkata", "New Delhi", "Chennai"],
            "answer": "New Delhi"
        }
    ]
    with open(filename, "w") as f:
        json.dump(sample_questions, f, indent=4)


def ask_question(question_data):
    print("\n" + question_data["question"])

    options = question_data["options"][:]
    random.shuffle(options)

    for i, option in enumerate(options, start=1):
        print(f"  {i}. {option}")

    while True:
        choice = input("Your answer (enter the number): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            selected = options[int(choice) - 1]
            return selected == question_data["answer"]
        print("Invalid input. Please enter a valid option number.")


def run_quiz(questions):
    score = 0
    total = len(questions)

    # Shuffle question order each time for replayability
    shuffled_questions = questions[:]
    random.shuffle(shuffled_questions)

    for i, q in enumerate(shuffled_questions, start=1):
        print(f"\nQuestion {i}/{total}")
        correct = ask_question(q)
        if correct:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct answer was: {q['answer']}")

    return score, total


def show_result(score, total):
    percentage = (score / total) * 100
    print("\n" + "=" * 30)
    print(f"Quiz finished! Your score: {score}/{total} ({percentage:.1f}%)")

    if percentage == 100:
        print("Perfect score! Excellent work!")
    elif percentage >= 70:
        print("Great job!")
    elif percentage >= 40:
        print("Not bad, keep practicing!")
    else:
        print("Keep studying and try again!")
    print("=" * 30)


def main():
    print("=== Welcome to the Python Quiz Game ===")
    questions = load_questions(QUESTIONS_FILE)

    if not questions:
        print("No questions available. Add some to questions.json and try again.")
        return

    score, total = run_quiz(questions)
    show_result(score, total)

    again = input("\nPlay again? (y/n): ").strip().lower()
    if again == "y":
        main()


if __name__ == "__main__":
    main()
