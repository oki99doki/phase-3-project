# lib/helpers.py
from models.question import Question
from models.game import Game
from models.user import User
import random
        
def play_game():
    
    # load questions from the database
    Question.initialize_all()
    
    # let user know to seed questions first if there are none
    if not Question.all:
        print("No questions available. Please seed questions first.")
        return
    
    # a dictionary is created with four keys and four values, each value initialized to 0
    answer_scores = {
        1: 0,
        2: 0,
        3: 0,
        4: 0
    }
    
    # display question 1 with its four answers below it and then repeat the process for questions 2-4
    questions = Question.all.values()
    for question in questions:
        while True:
            print("\033[34m" f"Question {question.id}. {question.question}" + "\033[0m")
            print(f"1. {question.answer_one}")
            print(f"2. {question.answer_two}")
            print(f"3. {question.answer_three}")
            print(f"4. {question.answer_four}\n")
            
            # user selects 1, 2, 3, or 4 to answer the question
            user_choice = input("Select one of the four answers (1-4): ")
            
            # whichever answer the user chooses, the key corresponding to that answer has its value increased by the question_value
            if user_choice in ["1", "2", "3", "4"]:
                user_choice = int(user_choice)
                answer_scores[user_choice] += question.question_value
                break
            else:
                print("Invalid input. Please select 1-4.")
    
    # after all questions are answered, the key corresponding to the max question_value is the winner
    max_score = max(answer_scores.values())
    winners = [key for key, value in answer_scores.items() if value == max_score]
    # print(winners)
    # print the result based on the winner
    if 1 in winners:
        print("\033[31m" + "You matched to Software Engineering!" + "\033[0m" + "\n")
    elif 2 in winners:
        print("\033[31m" + "You matched to Data Science!" + "\033[0m" + "\n")
    elif 3 in winners:
        print("\033[31m" + "You matched to Cybersecurity!" + "\033[0m" + "\n")
    else:
        print("\033[31m" + "You matched to UX/UI Product Design!" + "\033[0m" + "\n")
        
    # save the result to the database
    user_id = random.randint(1, 1000)
    outcome = winners[0]
    game = Game(user_id, outcome)
    game.save()
    
    
def add_new_question():
    question = input("Enter a question: ")
    question_value = int(input("Enter the question value (integer): "))
    answer_one = input("Enter answer one: ")
    answer_two = input("Enter answer two: ")
    answer_three = input("Enter answer three: ")
    answer_four = input("Enter answer four: ")
    
    Question.create_question(question, question_value, answer_one, answer_two, answer_three, answer_four)
    print("\033[36m" + "Question added successfully!" + "\033[0m" + "\n")
    
def setup_default_questions():
    Question.drop_table()
    Question.create_table()
    Question.initialize_all()
    Question.seed_questions()
    Game.create_table()


def exit_program():
    print("Goodbye!")
    exit()
