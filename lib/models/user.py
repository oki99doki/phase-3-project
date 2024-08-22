import sqlite3 
from . import CURSOR, CONN
import re

CONN = sqlite3.connect('resources.db', timeout=10)
CURSOR = CONN.cursor()

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
        sql = """
            CREATE TABLE IF NOT EXISTS users (
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
        sql = "DROP TABLE IF EXISTS users;"
        cursor.execute(sql)
        conn.commit()
        conn.close()

    @classmethod
    def create(cls, name, alias, email):
        """Initialize a new User instance and save the object to the database."""
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
        """Insert a new row into the users table and update the instance id."""
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

        conn = get_connection()
        cursor = get_cursor(conn)
        sql = f"DELETE FROM {self.table_name} WHERE id = ?"
        cursor.execute(sql, (self.id,))
        conn.commit()
        conn.close()
        self._id = None