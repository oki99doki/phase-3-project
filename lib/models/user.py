import sqlite3 
from . import CURSOR, CONN
import re

    # Database connection utility functions
def get_connection():
    return sqlite3.connect('resources.db', timeout=10)

def get_cursor(conn):
    return conn.cursor()

class User:
    table_name = 'users'

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
        """Create the table if it does not exist."""
        conn = get_connection()
        cursor = get_cursor(conn)
        sql = f"""
            CREATE TABLE IF NOT EXISTS {cls.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                alias TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            );
        """
        cursor.execute(sql)
        conn.commit()
        conn.close()

    @classmethod
    def drop_table(cls):
        """Drop the table that persists User instances."""
        conn = get_connection()
        cursor = get_cursor(conn)
        sql = f"DROP TABLE IF EXISTS {cls.table_name};"
        cursor.execute(sql)
        conn.commit()
        conn.close()

    @classmethod
    def create(cls, name, alias, email):
        """Initialize a new User instance and save it to the database."""
        user = cls(name, alias, email)
        user.save()
        return user

    @classmethod
    def find_by_id(cls, id):
        """Find a User instance by ID."""
        conn = get_connection()
        cursor = get_cursor(conn)
        sql = f"SELECT * FROM {cls.table_name} WHERE id = ?"
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(name=row[1], alias=row[2], email=row[3], id=row[0])
        return None

    @classmethod
    def get_all(cls):
        """Get all User instances."""
        conn = get_connection()
        cursor = get_cursor(conn)
        sql = f"SELECT * FROM {cls.table_name}"
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return [cls(name=row[1], alias=row[2], email=row[3], id=row[0]) for row in rows]

    def save(self):
        """Insert a new row into the users table or update the existing record."""
        if self.id is None:
            self._insert()
        else:
            self.update()  # If ID exists, update the existing record

    def _insert(self):
        """Insert a new row into the users table."""
        conn = get_connection()
        cursor = get_cursor(conn)
        sql = f"""
            INSERT INTO {self.table_name} (name, alias, email)
            VALUES (?, ?, ?)
        """
        cursor.execute(sql, (self.name, self.alias, self.email))
        conn.commit()
        self._id = cursor.lastrowid
        conn.close()

    def update(self):
        """Update the table row corresponding to the current User instance."""
        if self.id is None:
            raise ValueError("Cannot update a user that has not been saved to the database")

        conn = get_connection()
        cursor = get_cursor(conn)
        sql = f"""
            UPDATE {self.table_name}
            SET name = ?, alias = ?, email = ?
            WHERE id = ?
        """
        cursor.execute(sql, (self.name, self.alias, self.email, self.id))
        conn.commit()
        conn.close()

    def delete(self):
        """Delete the table row corresponding to the current User instance."""
        if self.id is None:
            raise ValueError("Cannot delete a user that has not been saved to the database")

<<<<<<< HEAD
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
=======
        conn = get_connection()
        cursor = get_cursor(conn)
        sql = f"DELETE FROM {self.table_name} WHERE id = ?"
        cursor.execute(sql, (self.id,))
        conn.commit()
        conn.close()
        self._id = None
>>>>>>> 8ecdfdad8b7050f204d342671450cdc6098230b6
