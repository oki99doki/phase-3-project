from helpers import (
    exit_program,
    play_game,
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
            setup_default_questions()
        elif choice == "2":
            play_game()
        elif choice == "3":
            Game.view_results()
        elif choice == "4":
            add_new_question()
        elif choice == "5":
            User.delete()
        elif choice == "6":
            Question.drop_table()
            print("All questions have been deleted.")
        elif choice == "7":
            Game.drop_table()
            print("All games have been deleted.")
        elif choice == "8":
            Game.find_by_id()
        elif choice == "9":
            Game.view_my_games()
        elif choice == "10":
            get_all_users()
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

if __name__ == "__main__":
    main()