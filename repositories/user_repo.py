from repositories.db import get_pool
from psycopg.rows import dict_row
from typing import Any
import re

# Regular expression for validating an Email
email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

def get_all_users_for_table():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''SELECT
                                *
                            FROM
                                "user"''')
            return cursor.fetchall()

def is_valid_email(email: str) -> bool:
        """Check if the email address is valid using regex."""
        return bool(re.match(email_regex, email))

def validate_user(username: str, email: str, password: str) -> bool:
    if user_exists(username):
        user = get_user_from_username(username)
        if password == user['user_password'] and is_valid_email(email):
            return True, "User authenticated successfully."
    else:
        return False, "Invalid username, email, or password."

def user_exists(username: str) -> bool:
    """Check if the user already exists."""
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                            SELECT
                                user_id
                            FROM
                                "user"
                            WHERE user_name = %s
                            ''', [username])
            user = cur.fetchone()
            return user is not None

def register_user(username: str, email: str, password: str, first_name: str, last_name: str) -> dict[str, Any]:
    """Register a new user if the email is valid and not already taken."""
    if not is_valid_email(email):
        return False, "Invalid email format."
    if user_exists(username):
        return False, "User already exists."
    
    # creates and registers the new user
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        INSERT INTO "user" (user_name, user_password, user_email, user_first_name, user_last_name)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING user_id
                        ''', [username, password, email, first_name, last_name])
            user_id = cur.fetchone()
            if user_id is None:
                raise Exception('Failed to create user.')
            return {
                'user_id': user_id,
                'username': username
            }

# Can use as singleton
def get_user_from_username(username: str) -> dict[str, Any] | None:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT
                            *
                        FROM
                            "user"
                        WHERE user_name = %s
                        ''', [username])
            user = cur.fetchone()
            if user is None:
                return None
            return user