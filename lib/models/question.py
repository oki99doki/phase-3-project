# lib/models/question.py
import sqlite3 
from . import CURSOR, CONN

CONN = sqlite3.connect('resources.db', timeout=10)
CURSOR = CONN.cursor()

class Question:
    all = {}

    def __init__(self, question, question_value, answer_one, answer_two, answer_three, answer_four, id=None):
        self._id = id
        self._question = None
        self._question_value = None
        self._answer_one = None
        self._answer_two = None
        self._answer_three = None
        self._answer_four = None

        # Set attributes using property setters
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
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if value is None or isinstance(value, int):
            self._id = value
        else:
            raise ValueError("ID must be an integer or None")

    @property
    def question(self):
        return self._question

    @question.setter
    def question(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._question = value
        else:
            raise ValueError("Question must be a non-empty string")

    @property
    def question_value(self):
        return self._question_value

    @question_value.setter
    def question_value(self, value):
        if isinstance(value, (int, float)) and value >= 0:
            self._question_value = float(value)
        else:
            raise ValueError("Question value must be a non-negative number")

    @property
    def answer_one(self):
        return self._answer_one

    @answer_one.setter
    def answer_one(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._answer_one = value
        else:
            raise ValueError("Answer one must be a non-empty string")

    @property
    def answer_two(self):
        return self._answer_two

    @answer_two.setter
    def answer_two(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._answer_two = value
        else:
            raise ValueError("Answer two must be a non-empty string")

    @property
    def answer_three(self):
        return self._answer_three

    @answer_three.setter
    def answer_three(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._answer_three = value
        else:
            raise ValueError("Answer three must be a non-empty string")

    @property
    def answer_four(self):
        return self._answer_four

    @answer_four.setter
    def answer_four(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._answer_four = value
        else:
            raise ValueError("Answer four must be a non-empty string")

    @classmethod 
    def create_table(cls):
        """Create the table if it does not exist."""
        sql = """
            CREATE TABLE IF NOT EXISTS questions
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT NOT NULL,
                    question_value FLOAT NOT NULL,
                    answer_one TEXT NOT NULL,
                    answer_two TEXT NOT NULL,
                    answer_three TEXT NOT NULL,
                    answer_four TEXT NOT NULL
                );
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """Drop the table that persists Question instances."""
        sql = "DROP TABLE IF EXISTS questions;"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """Insert a new row into the questions table and update the instance id."""
        if self.id is None:
            sql = """
                INSERT INTO questions (question, question_value, answer_one, answer_two, answer_three, answer_four)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            CURSOR.execute(sql, (self.question, self.question_value, self.answer_one, self.answer_two, self.answer_three, self.answer_four))
            CONN.commit()
            self._id = CURSOR.lastrowid
        else:
            self.update()  # If ID exists, update the existing record

    @classmethod
    def create(cls, question, question_value, answer_one, answer_two, answer_three, answer_four):
        """Initialize a new Question instance and save the object to the database."""
        new_question = cls(question, question_value, answer_one, answer_two, answer_three, answer_four)
        new_question.save()
        return new_question

    def update(self):
        """Update the table row corresponding to the current Question instance."""
        if self.id is None:
            raise ValueError("Cannot update a question that has not been saved to the database")

        sql = """
            UPDATE questions
            SET question=?, question_value=?, answer_one=?, answer_two=?, answer_three=?, answer_four=?
            WHERE id=?
        """
        CURSOR.execute(sql, (self.question, self.question_value, self.answer_one, self.answer_two, self.answer_three, self.answer_four, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Question instance."""
        if self.id is None:
            raise ValueError("Cannot delete a question that has not been saved to the database")

        sql = "DELETE FROM questions WHERE id=?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        self._id = None

    @classmethod
    def find_by_id(cls, id):
        """Find a Question instance by ID."""
        sql = "SELECT * FROM questions WHERE id=?"
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        if row:
            return cls(
                question=row[1],
                question_value=row[2],
                answer_one=row[3],
                answer_two=row[4],
                answer_three=row[5],
                answer_four=row[6],
                id=row[0]
            )
        return None

    @classmethod
    def get_all(cls):
        """Get all Question instances."""
        sql = "SELECT * FROM questions"
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        return [cls(
            question=row[1],
            question_value=row[2],
            answer_one=row[3],
            answer_two=row[4],
            answer_three=row[5],
            answer_four=row[6],
            id=row[0]
        ) for row in rows]

    @classmethod
    def seed_questions(cls):
        """Seed some initial questions into the database."""
        question1 = cls("Which sport would you prefer to coach?", 1.0, "Football", "Baseball", "Fencing", "Synchronized Swimming")
        question2 = cls("Which museum would you prefer to visit?", 1.0, "Air and Space", "Science", "Military", "Art")
        question3 = cls("Assuming money is equivalent, which would you prefer being?", 1.1, "Entrepreneur", "C-Suite Professional", "General", "Director")
        question4 = cls("What type of professionals do you enjoy working with most?", 1.0, "Developer", "Businesspeople", "Lawyers", "Marketers")

        question1.save()
        question2.save()
        question3.save()
        question4.save()

        print("\033[36m" + "Seeded" + "\033[0m" + "\n")

    @classmethod
    def initialize_all(cls):
        """Initialize all Question instances and store them in the `all` dictionary."""
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