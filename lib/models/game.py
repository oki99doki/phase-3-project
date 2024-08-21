# lib/models/game.py
import sqlite3
import datetime
from . import CURSOR, CONN

CONN = sqlite3.connect('resources.db', timeout=10) 
CURSOR = CONN.cursor()
 
class Game:
    
    all = {}
    current_game = {}

    def __init__(self, user_id=None, outcome=None, created_at = datetime.datetime.now().date().strftime("%m/%d/%y"), id=None):
        self.user_id = user_id
        self.outcome = outcome
        self.created_at = created_at
        self.id = id

    @classmethod 
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS games
                (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER
                    outcome TEXT,
                    created_at TEXT
                );
        """
        # FOREIGN KEY (user_id) REFERENCES users(id),
        CURSOR.execute(sql)
        CONN.commit()
        
    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS games;"
        CURSOR.execute(sql)
        CONN.commit()
        
    def save(self):
        sql = """
            INSERT INTO games (user_id, outcome, created_at) VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (self.user_id, self.outcome, self.created_at))
        CONN.commit()
        
        self.id = CURSOR.lastrowid
        
    @classmethod
    def create(cls, user_id, outcome, created_at = datetime.datetime.now().date().strftime("%m/%d/%y")):
        game = cls(user_id, outcome)
        game.save()
        cls.all[game.id] = game
        return game
    
    def update(self):
        sql = """
        UPDATE games
        SET outcome=?, created_at=?
        HERE id=?
        """
        CURSOR.execute(sql, (self.outcome, self.created_at, self.id))
        CONN.commit()
        
    def delete(self):
        sql = """
        DELETE FROM games WHERE id=?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        del type(self).all[self.id]
        self.id = None
        
    @classmethod
    def view_results(self):
        #aggregate the results of the dictionary and display each of the four programs with its number of outcomes
        sql = """
        SELECT outcome, COUNT(*) as count
        FROM games
        GROUP BY outcome
        ORDER BY COUNT(*) DESC
        """
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        for row in rows:
            print(f"{row[0]}: {row[1]}")