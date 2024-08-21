# lib/cli.py

from helpers import (
    exit_program,
    play_game,
    add_new_question,
    setup_default_questions
)
# from models.users import Users
from models.question import Question
from models.game import Game
from models.user import User

def main():
    
    # User.create_table()
    # Game.create_table() 
    # Question.create_table()
    # Question.initialize_all()
    
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            setup_default_questions()
        elif choice == "2":
            play_game()
        elif choice == "3":
            Game.view_results()
        elif choice == "4":
            add_new_question()
        elif choice == "5":
            User.delete() #(need to include the current user id)
        elif choice == "6":
            Question.drop_table()
        elif choice == "7":
            Game.drop_table()
        else:
            print("Invalid choice")


def menu():
    print("Welcome to Career Chooser! Please select an option:")
    print("0. Exit the program")
    print("1. Seed with default questions")
    print("2. Start game")
    print("3. View results")
    print("4. Add a new question")
    print("5. Delete current user")
    print("6. Delete all questions")
    print("7. Delete all games")


if __name__ == "__main__":
    main()
    