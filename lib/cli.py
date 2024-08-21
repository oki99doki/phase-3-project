# lib/cli.py

from helpers import (
    exit_program,
    play_game
)
# from models.users import Users
from models.question import Question
from models.game import Game
from models.user import User

def main():
    
    # User.create_table()
    Game.create_table() 
    Question.initialize_all()
    
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            play_game()
        elif choice == "2":
            Game.view_results()
        elif choice == "3":
            Question.create_question()
        elif choice == "4":
            User.delete() #(need to include the current user id)
        else:
            print("Invalid choice")


def menu():
    print("Welcome to Career Chooser! Please select an option:")
    print("0. Exit the program")
    print("1. Start game")
    print("2. View results")
    print("3. Add a new question")
    print("4. Delete current user")


if __name__ == "__main__":
    main()
    