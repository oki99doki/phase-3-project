# lib/cli.py

from helpers import (
    exit_program,
    play_game
)
# from models.users import Users
from models.question import Question
from models.game import Game


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
    