import sqlite3 
from __init__ import CURSOR, CONN

CONN = sqlite3.connect('resources.db', timeout=10) 
CURSOR = CONN.cursor()

class User:

    def __init__(self, id, name, alias, email):
        self.id = id
        self.name = name
        self.alias = alias # add alias attribute
        self.email = email # add email attribute


    # Implmenet CRUD = Create, Read, Update, Delete

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
        """ Insert a new row with the name and location values of the current Department instance.
        Update object id attribute using the primary key value of new row.
        """
        sql = '''
            INSERT INTO departments (name, alias, email)
            VALUES (?, ?, ?)
        '''
        CURSOR.execute(sql, (self.name, self.alias, self.email))
        CONN.commit()

        self.id = CURSOR.lastrowid
    

    # C as Create (CRUD)
    @classmethod
    def create(cls, name, alias, email):
        """ Initialize a new User instance and save the object to the database """
        user = cls(name, alias, email)
        user.save()
        return user


    # U as Update (CRUD)
    def update(self):
        """Update the table row corresponding to the current User instance."""
        sql = """
            UPDATE users
            SET name = ?, alias = ?, email = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.alias, self.email, self.id))
        CONN.commit()


    # D as Delete (CRUD)
    def delete(self):
        """Delete the table row corresponding to the current User instance"""
        sql = """
            DELETE FROM users
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()