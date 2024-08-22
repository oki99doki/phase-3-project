# lib/models/game.py
import sqlite3
import datetime
from . import CURSOR, CONN

CONN = sqlite3.connect('resources.db', timeout=10)
CURSOR = CONN.cursor()

class Game:
    all = {}
    current_game = {}

    def __init__(self, user_id=None, outcome=None, created_at=None, id=None):
        self._id = id
        self._user_id = None
        self._outcome = None
        self._created_at = None

        # Set attributes using property setters to ensure constraints
        self.user_id = user_id
        self.outcome = outcome
        self.created_at = created_at or datetime.datetime.now().date().strftime("%m/%d/%y")

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
        if isinstance(value, str) and len(value) > 0:
            self._outcome = value
        else:
            raise ValueError("outcome must be a non-empty string")

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
        """Create the games table if it does not exist."""
        sql = """
            CREATE TABLE IF NOT EXISTS games
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    outcome TEXT,
                    created_at TEXT
                );
        """
        CURSOR.execute(sql)
        CONN.commit()
        
    @classmethod
    def drop_table(cls):
        """Drop the games table."""
        sql = "DROP TABLE IF EXISTS games;"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """Insert or update the game record."""
        if self.id is None:
            sql = """
                INSERT INTO games (user_id, outcome, created_at) VALUES (?, ?, ?)
            """
            CURSOR.execute(sql, (self.user_id, self.outcome, self.created_at))
            CONN.commit()
            self.id = CURSOR.lastrowid
            type(self).all[self.id] = self
        else:
            self.update()  # Update if ID exists

    @classmethod
    def create(cls, user_id, outcome, created_at=None):
        """Create and save a new game instance."""
        game = cls(user_id, outcome, created_at)
        game.save()
        return game

    def update(self):
        """Update the existing game record."""
        if self.id is None:
            raise ValueError("Cannot update a game that has not been saved to the database")

        sql = """
            UPDATE games
            SET user_id=?, outcome=?, created_at=?
            WHERE id=?
        """
        CURSOR.execute(sql, (self.user_id, self.outcome, self.created_at, self.id))
        CONN.commit()

    def delete(self):
        """Delete the game record."""
        if self.id is None:
            raise ValueError("Cannot delete a game that has not been saved to the database")

        sql = "DELETE FROM games WHERE id=?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        del type(self).all[self.id]
        self.id = None

    @classmethod
    def find_by_id(cls, id):
        """Find a game instance by its ID."""
        sql = "SELECT * FROM games WHERE id=?"
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        if row:
            return cls(
                user_id=row[1],
                outcome=row[2],
                created_at=row[3],
                id=row[0]
            )
        return None

    @classmethod
    def get_all(cls):
        """Retrieve all game instances."""
        sql = "SELECT * FROM games"
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        return [cls(
            user_id=row[1],
            outcome=row[2],
            created_at=row[3],
            id=row[0]
        ) for row in rows]

    @classmethod
    def view_results(cls):
        """Aggregate the results and display each outcome with its count."""
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