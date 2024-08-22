from helpers import (
    exit_program,
    play_game,
    find_by,
    add_new_question,
    setup_default_questions
)
from models.question import Question
from models.game import Game
from models.user import User

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
            Game.view_results()
        elif choice == "5":
            add_new_question()
        elif choice == "6":
            User.delete()
        elif choice == "7":
            Question.drop_table()
            print("All questions have been deleted.")
        elif choice == "8":
            Game.drop_table()
            print("All games have been deleted.")
        elif choice == "8":
            Game.find_by_id()
        elif choice == "9":
            Game.view_my_games()  # <-- WE NEED TO ADD VIEW RELATED OBJECTS FOR THE CURRENT USER
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
    print("8. Find user by ID")
    print("9. View my games")
    print("10. Get all users")


def delete_user():
    id = input("Enter user ID to delete: ")
    user = User.find_by_id(id)
    if user:
        user.delete()
        print(f"User with ID {id} has been deleted.")
    else:
        print(f"User with ID {id} not found.")

def get_all_users():
    users = User.get_all()
    for user in users:
        print(f"ID={user.id}, Name={user.name}, Alias={user.alias}, Email={user.email}")
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