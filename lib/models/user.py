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