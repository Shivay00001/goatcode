import sqlite3
from dataclasses import dataclass
from typing import List, Optional
import re
import datetime

class UserError(Exception):
    """Base class for custom exceptions."""
    pass

class InvalidEmailError(UserError):
    """Raised when the email address is invalid."""
    pass

@dataclass
class User:
    """Represents a user with id, username, email, and created_at."""
    id: int
    username: str
    email: str
    created_at: datetime.datetime

class UserRepository:
    """Handles user data storage and retrieval."""
    def __init__(self, db_name: str):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Creates the users table if it doesn't exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users
            (id INTEGER PRIMARY KEY, username TEXT, email TEXT, created_at DATETIME)
        ''')
        self.conn.commit()

    def save_user(self, user: User) -> None:
        """Saves a user to the database."""
        try:
            self.cursor.execute('''
                INSERT INTO users (username, email, created_at)
                VALUES (?, ?, ?)
            ''', (user.username, user.email, user.created_at))
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            raise UserError(f"User with username '{user.username}' already exists.") from e

    def fetch_user(self, id: int) -> Optional[User]:
        """Fetches a user by ID."""
        try:
            self.cursor.execute('SELECT * FROM users WHERE id = ?', (id,))
            row = self.cursor.fetchone()
            if not row:
                return None
            return User(
                id=row[0],
                username=row[1],
                email=row[2],
                created_at=datetime.datetime.fromtimestamp(row[3])
            )
        except sqlite3.Error as e:
            raise UserError(f"Failed to fetch user with ID {id}") from e

    def list_users(self) -> List[User]:
        """Lists all users."""
        try:
            self.cursor.execute('SELECT * FROM users')
            rows = self.cursor.fetchall()
            return [User(
                id=row[0],
                username=row[1],
                email=row[2],
                created_at=datetime.datetime.fromtimestamp(row[3])
            ) for row in rows]
        except sqlite3.Error as e:
            raise UserError(f"Failed to list users") from e

    def validate_email(self, email: str) -> bool:
        """Validates an email address using regex."""
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return bool(re.match(pattern, email))

# Example usage
if __name__ == "__main__":
    db_name = "users.db"
    user_repo = UserRepository(db_name)

    # Create a new user
    user = User(
        id=1,
        username="john_doe",
        email="johndoe@example.com",
        created_at=datetime.datetime.now()
    )
    user_repo.save_user(user)

    # Fetch a user by ID
    fetched_user = user_repo.fetch_user(1)
    print(fetched_user)

    # List all users
    users = user_repo.list_users()
    for user in users:
        print(user)

    # Validate an email address
    try:
        if not user_repo.validate_email("invalid_email"):
            raise InvalidEmailError
    except InvalidEmailError as e:
        print(e)