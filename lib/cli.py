# lib/cli.py

from helpers import (
    exit_program,
    play_game,
    find_by,
    add_new_question,
    setup_default_questions
)
# from models.users import Users
from models.question import Question
from models.game import Game
from models.user import User

import ipdb


def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            #User.create_table()
            global cur_user
            #global cur_alias
            #global cur_email
        
            print("Enter your name:")
            cur_user = input('> ')
        
            print("Enter your alias:")
            cur_alias = input('> ')
            print("Enter your email:")
            cur_email = input('> ')
            User.create(cur_user, cur_alias, cur_email)
        
            '''
            global cur_user
            print("Enter your username:")
            username = input('> ')
            cur_user = User.find_or_create_by(username.upper())
            print(f"Welcome, {cur_user.name}!")
            '''

            #cur_user = Users.find_or_create_by(username.upper())
            #cur_user = username
            #User.name = username

            print(f"Welcome, {cur_user}!")
            #ipdb.set_trace()
        elif choice == "2":
            setup_default_questions()
        elif choice == "3":

            #cur_user = 12 # User.id
            cur_user = User.get_recent_user()
            #ipdb.set_trace()
            play_game(cur_user)
            
        elif choice == "4":
            Game.view_results()   # display all objects/results of games requirement
        elif choice == "5":
            add_new_question()    # create object requirement
        elif choice == "6":
            User.delete() #(need to include the current user id)
        elif choice == "7":
            Question.drop_table()    # delete object requirement
        elif choice == "8":
            Game.drop_table()
        elif choice == "9":
            find_by()  # <-- WE NEED TO ADD FIND OBJECT BY ID/ name # SK added function in helper.py
        elif choice == "10":
            Game.view_my_games()  # <-- WE NEED TO ADD VIEW RELATED OBJECTS FOR THE CURRENT USER
        else:
            print("Invalid choice")
                    

def menu():
    print("Welcome to Career Chooser! Please select an option:")
    print("0. Exit the program")
    print("1. Enter user name")
    print("2. Seed with default questions")
    print("3. Start game")
    print("4. View results")
    print("5. Add a new question")
    print("6. Delete current user")
    print("7. Delete all questions")
    print("8. Delete all games")
    print("9. Find user by name")


if __name__ == "__main__":
    main()
    