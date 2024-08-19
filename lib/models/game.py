import sqlite3 
from __init__ import CURSOR, CONN

CONN = sqlite3.connect('resources.db', timeout=10) 
CURSOR = CONN.cursor()
 
class Game:

    def __init__(self, outcome, updated_at, created_at, user_id = None, id=None, ):

        self.outcome = outcome
        self.updated_at = updated_at
        self.created_at = created_at

        self.user_id = user_id
        self.id = id
        
        

    @classmethod 
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS games
                (
                    id INTEGER PRIMARY KEY,
                    outcome TEXT,
                    updated_at TEXT,
                    created_at TEXT,
                    user_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );
        """
        CURSOR.execute(sql)
        CONN.commit()