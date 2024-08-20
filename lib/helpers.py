# lib/helpers.py
from models.question import Question
from models.game import Game

def play_game():
    # a dictionary is created with four keys and four values, each value initialized to 0
    answer_scores = {
        1 : 0,
        2 : 0,
        3 : 0,
        4 : 0
    }
    # display question 1 with its four answers below it and then repeat the process for questions 2-4
    questions = Question.all.values()
    for question in questions:
        print(f"{question.id}. {question.question}")
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
        else:
            print("Invalid input. Please select 1-4.")
    # after all questions are answered, the key corresponding to the max question_value is the winner
    max_score = max(answer_scores.values())
    winners = [key for key, value in answer_scores.items() if value == max_score]
    # if key_one is the winner, print("You matched to Software Engineering"), elif key_two is the winner, print("You matched to Data Science"),
    # elif key_three is the winner, print("You matched to Cybersecurity"), else print("You matched to UX/UI Product Design")
    if 1 in winners:
        print("You matched to Software Engineering!")
    elif 2 in winners:
        print("You matched to Data Science!")
    elif 3 in winners:
        print("You matched to Cybersecurity!")
    else:
        print("You matched to UX/UI Product Design!")
        
    # # save the result to the database
    # user_id = user_id
    # outcome = max(answer_scores, key=answer_scores.get())
    # Game.create(user_id, outcome)


def exit_program():
    print("Goodbye!")
    exit()
    
    
# def display_questions():
#     questions = Question.all.values()
#     for question in questions:
#         print(f"{question.id}. {question.question}")
#         print(f"1. {question.answer_one}")
#         print(f"2. {question.answer_two}")
#         print(f"3. {question.answer_three}")
#         print(f"4. {question.answer_four}\n")