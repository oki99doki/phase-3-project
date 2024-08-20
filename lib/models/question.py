import sqlite3 
from __init__ import CURSOR, CONN

CONN = sqlite3.connect('resources.db', timeout=10) 
CURSOR = CONN.cursor()

class Question:

    all = {}

    def init(self, question, question_value, answer_one, answer_two, answer_three, answer_four, id=None):
        self.id = id
        self.question = question
        self.question_value = question_value
        self.answer_one = answer_one
        self.answer_two = answer_two
        self.answer_three = answer_three
        self.answer_four = answer_four


    @classmethod 
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS games98
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
        
    def save(self):
        sql = """
            INSERT INTO questions (question, question_value, answer_one, answer_two, answer_three, answer_four) VALUES (?, ?, ?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.question, self.question_value, self.answer_one, self.answer_two, self.answer_three, self.answer_four))
        CONN.commit()
        
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

                
    def update(self):
        sql = """
            UPDATE questions
            SET question=?, question_value=?, answer_one=?, answer_two=?, answer_three=?, answer_four=? WHERE id=?
        """
        CURSOR.execute(sql, (self.question, self.question_value, self.answer_one, self.answer_two, self.answer_three, self.answer_four, self.id))
        CONN.commit()

    # Add save mthod here...

    # @classmethod
    # def initialize_table(cls):
    #     sql = '''
    #         ALTER TABLE games


        
    #     '''


    #     CURSOR.execute(sql)
    #     CONN.commit()






    # '''
    # def __init__(self, id, question, answer_one, answer_one_value, answer_two, answer_two_value,
    #              answer_three, answer_three_value, answer_four, answer_four_value):
        
    #     self.id = id
    #     self.question = question
        
    #     self.answer_one = answer_one
    #     self.question_one_value = answer_one_value
    #     self.answer_two = answer_two
    #     self.question_two_value = answer_two_value
    #     self.answer_three = answer_three
    #     self.question_three_value = answer_three_value
    #     self.answer_four = answer_four
    #     self.question_four_value = answer_four_value
    # '''