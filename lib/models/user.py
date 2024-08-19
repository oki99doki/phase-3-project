import sqlite3 
from __init__ import CURSOR, CONN

CONN = sqlite3.connect('resources.db', timeout=10) 
CURSOR = CONN.cursor()

class User:

    def __init__(self, id, name):
        self.id = id
        self.name = name


    @classmethod 
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS users
                (
                    id INTEGER PRIMARY KEY,
                    name TEXT
                );
        """
        CURSOR.execute(sql)
        CONN.commit()