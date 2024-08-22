import sqlite3 
from . import CURSOR, CONN
import re

CONN = sqlite3.connect('resources.db', timeout=10)
CURSOR = CONN.cursor()

class User:
    def __init__(self, name, alias, email, id=None):
        self._id = id
        self._name = None
        self._alias = None
        self._email = None

        # Use property setters to validate data
        self.name = name
        self.alias = alias
        self.email = email

    def __repr__(self):
        return (
            f"<User {self.id}, {self.name}, {self.alias}, {self.email}>"
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
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._name = value
        else:
            raise ValueError("Name must be a non-empty string")

    @property
    def alias(self):
        return self._alias

    @alias.setter
    def alias(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._alias = value
        else:
            raise ValueError("Alias must be a non-empty string")

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if isinstance(value, str) and re.match(r"[^@]+@[^@]+\.[^@]+", value):
            self._email = value
        else:
            raise ValueError("Email must be a valid email address")

    @classmethod 
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS users
                (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    alias TEXT,
                    email TEXT
                );
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists User instances """
        sql = '''
            DROP TABLE IF EXISTS users;
        '''
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """Insert a new row into the users table and update the instance id."""
        if self.id is None:
            sql = '''
                INSERT INTO users (name, alias, email)
                VALUES (?, ?, ?)
            '''
            CURSOR.execute(sql, (self.name, self.alias, self.email))
            CONN.commit()
            self._id = CURSOR.lastrowid
        else:
            self.update()  # If ID exists, update the existing record

    @classmethod
    def create(cls, name, alias, email):
        """ Initialize a new User instance and save the object to the database """
        user = cls(name, alias, email)
        user.save()
        return user

    def update(self):
        """ Update the table row corresponding to the current User instance """
        if self.id is None:
            raise ValueError("Cannot update a user that has not been saved to the database")
        
        sql = """
            UPDATE users
            SET name = ?, alias = ?, email = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.alias, self.email, self.id))
        CONN.commit()

    def delete(self):
        """ Delete the table row corresponding to the current User instance """
        if self.id is None:
            raise ValueError("Cannot delete a user that has not been saved to the database")

        sql = """
            DELETE FROM users
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        self._id = None
    
    # SK: add this block of code (games-method) to compute associated Game instances
    def games(self):
        """Return list of games associated with current user"""
        from game import Game
        sql = """
            SELECT * FROM games
            WHERE user_id = ?
        """
        CURSOR.execute(sql, (self.id,),)

        rows = CURSOR.fetchall()
        return [
            Game.instance_from_db(row) for row in rows
        ]
    

    # SK: added this class method for Find Usewr by ID functionality
    @classmethod 
    def find_by_name(cls, name):
        sql = """
                SELECT * FROM users WHERE name=?;
            """
        row = CURSOR.execute(sql,(name,)).fetchone()
        if not row: 
            return None 
        else: 
            return cls.create_instance(row)
            #return User(row)
    
    '''
    BACKUP original
    @classmethod 
    def find_by_id(cls, id):
        sql = """
                SELECT * FROM users WHERE id=?;
            """
        row = CURSOR.execute(sql,(id,)).fetchone()
        if not row: 
            return None 
        else: 
            return cls.create_instance(row)
    '''
    
        

    @classmethod 
    def find_or_create_by(cls, name=None, high_score=0):
        select_sql = """ 
            SELECT * FROM users WHERE 
            name = ?;
        """
        row = CURSOR.execute(select_sql, (name,)).fetchone()
        if not row: 
            insert_sql = """ INSERT INTO users (name, high_score) VALUES (?, ?);"""
            CURSOR.execute(insert_sql, (name, high_score))
            CONN.commit()
            return cls.find_by_id(CURSOR.lastrowid)
        else:
            return cls.create_instance(row)
        
    
    @classmethod 
    def create_instance(cls, row):
        #row = ['id', 'name', 'alias, 'email']
        user = cls(
            name=row[1],
            alias=row[2],
            email=row[3],
            id=row[0]
        )
        return user
    

    def get_recent_user():
        #conn = sqlite3.connect('your_database.db')
        #cur = conn.cursor()

        # Execute a query to retrieve the ID of the last row from the users table
        CURSOR.execute("SELECT id FROM users ORDER BY id DESC LIMIT 1")
        row = CURSOR.fetchone()

        # Check if a row was returned
        if row:
            # Assign the ID to cur_user
            return row[0]
        else:
            print("No users found.")
