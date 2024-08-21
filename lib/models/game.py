# lib/models/game.py
import sqlite3
import datetime
from . import CURSOR, CONN

CONN = sqlite3.connect('resources.db', timeout=10)
CURSOR = CONN.cursor()

class Game:
    all = {}
    # current_game = {}

    def __init__(self, user_id=None, outcome=None, created_at=None, id=None):
        self.id = id
        self._user_id = None
        self._outcome = None
        self._created_at = None

        # Set attributes using property setters to ensure constraints
        self.user_id = user_id
        self.outcome = outcome
        self.created_at = created_at or datetime.datetime.now().date().strftime("%m/%d/%y")

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        if isinstance(value, int) and value > 0:
            self._user_id = value
        else:
            raise ValueError("user_id must be a positive integer")

    @property
    def outcome(self):
        return self._outcome

    @outcome.setter
    def outcome(self, value):
        if isinstance(value, int):
            self._outcome = value
        else:
            raise ValueError("outcome must be a positive integer")

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, value):
        try:
            datetime.datetime.strptime(value, "%m/%d/%y")
            self._created_at = value
        except ValueError:
            raise ValueError("created_at must be in the format MM/DD/YY")

    @classmethod 
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS games
                (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    outcome INTEGER,
                    created_at TEXT
                );
        """
        CURSOR.execute(sql)
        CONN.commit()
        
    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS games;"
        CURSOR.execute(sql)
        CONN.commit()
        
    def save(self):
        sql = """
            INSERT INTO games (user_id, outcome, created_at) VALUES (?, ?, ?);
        """
        CURSOR.execute(sql, (self.user_id, self.outcome, self.created_at))
        CONN.commit()
        
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self
        
    @classmethod
    def create(cls, user_id, outcome, created_at=None):
        game = cls(user_id, outcome, created_at)
        game.save()
        cls.all[game.id] = game
        return game
    
    def update(self):
        sql = """
        UPDATE games
        SET outcome=?, created_at=?
        WHERE id=?;
        """
        CURSOR.execute(sql, (self.outcome, self.created_at, self.id))
        CONN.commit()
        
    def delete(self):
        sql = """
        DELETE FROM games WHERE id=?;
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        del type(self).all[self.id]
        self.id = None
        
    @classmethod
    def view_results(cls):
        # Aggregate the results of the dictionary and display each outcome with its count
        sql = """
        SELECT outcome, COUNT(*) as count
        FROM games
        GROUP BY outcome
        ORDER BY COUNT(*) DESC;
        """
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        for row in rows:
            outcome = row[0]
            count = row[1]
            
            if outcome == 1:
                print(f"\033[32mSoftware Engineering: {count}\033[0m")
            elif outcome == 2:
                print(f"\033[32mData Science: {count}\033[0m")
            elif outcome == 3:
                print(f"\033[32mCybersecurity: {count}\033[0m")
            else:
                print(f"\033[32mUX/UI Product Design: {count}\033[0m")