#!/usr/bin/env python3
# lib/debug.py

from models.game import Game
from models.question import Question
from models.user import User
import ipdb

Game.create_table()
Question.create_table()

question1 = Question("Which sport would you prefer to coach?", 1.0, "Football", "Baseball", "Fencing", "Synchronized Swimming")
question2 = Question("Which museum would you prefer to visit?", 1.0, "Air and Space", "Science", "Military", "Art")
question3 = Question("Assuming money is equivalent, which would you prefer being?", 1.1, "Entrepreneur", "C-Suite Professional", "General", "Director")
question4 = Question("What type of professionals do you enjoy working with most?", 1.0, "Developer", "Businesspeople", "Lawyers", "Marketers")

# question1.save()
# question2.save()
# question3.save()
# question4.save()

user_1 = User.create("Tom", "tommy123", "t.edison@powersupply.com")
print(user_1)  # <User 1: Tom, tommy123, t.edison@powersupply.com>

user_2 = User.create("Albert", "Emc2", "einstein@princeton.edu")
print(user_2)  # <User 2: Albert, Emc2, einstein@princeton.edu>

user_1.name = 'Jefferson'
user_1.alias = 'jeff00'
user_1.update()
print(user_1)

print("Delete Einstein")
user_2.delete() # delete from db table, object still exists in memory
print(user_2)

ipdb.set_trace()

# Responsible for populating database
# initialization with all instances of data

# '''round_1 = Question(id = 1, question = "Which sport would you coach?", 
#                    answer_one ="Football", answer_one_value = "1",
#                     answer_two_value,
#                     answer_three, answer_three_value, 
#                     answer_four, answer_four_value):
#         )
# '''