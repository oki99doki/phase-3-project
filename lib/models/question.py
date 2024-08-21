# lib/models/question.py
import sqlite3 
from . import CURSOR, CONN

CONN = sqlite3.connect('resources.db', timeout=10) 
CURSOR = CONN.cursor()

class Question:

    all = {}

    def __init__(self, question, question_value, answer_one, answer_two, answer_three, answer_four, id=None):
        self.id = id
        self.question = question
        self.question_value = question_value
        self.answer_one = answer_one
        self.answer_two = answer_two
        self.answer_three = answer_three
        self.answer_four = answer_four
        
    def __repr__(self):
        return (
            f"<Question {self.id}, {self.question}, {self.question_value}, {self.answer_one}, {self.answer_two}, {self.answer_three}, {self.answer_four}>"
        )

    @property
    def question(self):
        return self._question

    @question.setter
    def question(self, question):
        if isinstance(question, str) and len(question) > 0:
            self._question = question
        else:
            raise ValueError(
                "Question must be a non-empty string"
            )

    @classmethod 
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS questions
                (
                    id INTEGER PRIMARY KEY,
                    question TEXT,
                    question_value FLOAT,
                    answer_one TEXT,
                    answer_two TEXT,
                    answer_three TEXT,
                    answer_four TEXT
                );
        """
        CURSOR.execute(sql)
        CONN.commit()
        
    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS questions;"
        CURSOR.execute(sql)
        CONN.commit()
        
    def save(self):
        sql = """
            INSERT INTO questions (question, question_value, answer_one, answer_two, answer_three, answer_four) VALUES (?, ?, ?, ?, ?, ?);
        """
        CURSOR.execute(sql, (self.question, self.question_value, self.answer_one, self.answer_two, self.answer_three, self.answer_four))
        CONN.commit()
        
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

                
    def update(self):
        sql = """
            UPDATE questions
            SET question=?, question_value=?, answer_one=?, answer_two=?, answer_three=?, answer_four=? WHERE id=?;
        """
        CURSOR.execute(sql, (self.question, self.question_value, self.answer_one, self.answer_two, self.answer_three, self.answer_four, self.id))
        CONN.commit()
        
    def delete(self):
        sql = "DELETE FROM questions WHERE id=?;"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        
    @classmethod
    def seed_questions(cls):
        question1 = Question("Which sport would you prefer to coach?", 1.0, "Football", "Baseball", "Fencing", "Synchronized Swimming")
        question2 = Question("Which museum would you prefer to visit?", 1.0, "Air and Space", "Science", "Military", "Art")
        question3 = Question("Assuming money is equivalent, which would you prefer being?", 1.1, "Entrepreneur", "C-Suite Professional", "General", "Director")
        question4 = Question("What type of professionals do you enjoy working with most?", 1.0, "Developer", "Businesspeople", "Lawyers", "Marketers")

        question1.save()
        question2.save()
        question3.save()
        question4.save()
        
        print("\033[36m" + "Seeded" + "\033[0m" + "\n")
        
    @classmethod
    def initialize_all(cls):
        cls.all = {}
        sql = "SELECT * FROM questions;"
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        for row in rows:
            question = cls(
                question=row[1],
                question_value=row[2],
                answer_one=row[3],
                answer_two=row[4],
                answer_three=row[5],
                answer_four=row[6],
                id=row[0]
            )
            cls.all[question.id] = question
            
    @classmethod
    def create_question(cls, question, question_value, answer_one, answer_two, answer_three, answer_four):
        newQuestion = Question(question, question_value, answer_one, answer_two, answer_three, answer_four)
        newQuestion.save()
        return newQuestion
    