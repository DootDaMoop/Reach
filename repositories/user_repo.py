from repositories.db import get_pool
from psycopg.rows import dict_row
from typing import Tuple, Union, Dict, Any
from werkzeug.datastructures import FileStorage
import re
import bcrypt
import logging
from flask import Response



# Regular expression for validating an Email
email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

def hash_value(value: str) -> str:
    if value is None:
        return None
    return bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def check_password_against_hash(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

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
    if user_exists(username, email):
        user = get_user_from_username(username)
        if bcrypt.checkpw(password.encode('utf-8'), user['user_password'].encode('utf-8')) and is_valid_email(email):
            return True, "User authenticated successfully."
    else:
        return False, "Invalid username, email, or password."

def user_exists(username: str, email: str) -> bool:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                            SELECT
                                user_id
                            FROM
                                "user"
                            WHERE user_name = %s OR user_email = %s
                            ''', [username, email])
            user = cur.fetchone()
            return user is not None


def register_user(username: str, email: str, password: str, first_name: str, last_name: str, google_id: Union[str, None]) -> Tuple[bool, Dict[str, Any]]:
    """Register a new user if the email is valid and not already taken."""
    if not is_valid_email(email):
        return False, {"error": "Invalid email format."}
    if user_exists(username, email):
        return False, {"error": "User already exists."}
    hashed_password = hash_value(password) if password is not None else None
    hashed_google_id = hash_value(google_id) if google_id else None
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                INSERT INTO "user" 
                (user_name, user_password, user_email, user_first_name, user_last_name, google_id) 
                VALUES (%s, %s, %s, %s, %s, %s) 
                RETURNING user_id
                ''', [username, hashed_password, email, first_name, last_name, hashed_google_id])
            user_id = cur.fetchone()
            if user_id is None:
                return False, {"error": "Failed to create user."}
            return True, {
                'user_id': user_id['user_id'],
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
        

def get_user_from_user_id(user_id: int) -> dict[str, Any] | None:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT
                            *
                        FROM
                            "user"
                        WHERE user_id = %s
                        ''', [user_id])
            user = cur.fetchone()
            if user is None:
                return None
            return user

def get_user_from_user_email(email: str) -> dict[str, Any] | None:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT
                            *
                        FROM
                            "user"
                        WHERE user_email = %s
                        ''', [email])
            user = cur.fetchone()
            if user is None:
                return None
            return user

def edit_user(user_id: int, username: str, email: str, password: str | None, first_name: str | None, last_name: str | None) -> dict[str, Any]:
    #make password optional if user has a google id
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        UPDATE
                            "user"
                        SET
                            user_name = %s,
                            user_email = %s,
                            user_password = %s,
                            user_first_name = %s,
                            user_last_name = %s
                        WHERE user_id = %s;
                        ''', [username, email, password, first_name, last_name, user_id])
            cur.execute(''' 
                        SELECT * FROM "user" WHERE user_id = %s
                        ''', [user_id])
            user = cur.fetchone()
            if user is None:
                return None
            return user

def check_if_user_id_is_using_google_account(user_id: int) -> Tuple[bool, Dict[str, Any]]:
    user = get_user_from_user_id(user_id)
    if user:
        if user.get('google_id'):
            return True, {'message': 'User is linked to a Google account.', 'google_id': user['google_id']}
        else:
            return False, {'message': 'User is not linked to a Google account.'}
    return False, {'error': 'User does not exist.'}

def delete_user(user_id: str) -> dict[str: Any]:
    
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        DELETE FROM "user" WHERE user_id = %s
                        ''', user_id)
            user_id = cur.fetchone()
            if user_id is None:
                raise Exception('Failed to delete user.')
            return {
                'user_id': user_id
            }

def get_user_role_by_group_id(user_id: str, group_id: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                SELECT 
                    user_role
                FROM 
                    membership
                WHERE 
                    user_id = %s AND group_id = %s;
            ''', [user_id, group_id])
            result = cursor.fetchone()
            if result:
                return result['user_role']
            else:
                return "User role not found in this group."

#Delete user 
#cascades down to membership, event and pending 
#RUN AFTER CHANGING OWNERSHIP
def delete_user(user_id: int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                    DELETE FROM
                        "user"
                    WHERE user_id = %s
                    RETURNING user_id
                    ''', [user_id])
            group_id = cur.fetchone()
            if group_id is None:
                raise Exception('Failed to delete User.')
            return {
                'user_id': user_id
            }

def update_profile_picture(user_id: int, profile_picture: FileStorage) -> bool:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            try:
                # Read the bytes from the FileStorage object
                picture_bytes = profile_picture.read()
                cur.execute('''
                    UPDATE "user"
                    SET profile_picture = %s
                    WHERE user_id = %s
                ''', [picture_bytes, user_id])
                return True
            except Exception as e:
                logging.error("Error updating profile picture: %s", e)
                conn.rollback()
                return False

def get_profile_picture(user_id: int):
    """Retrieve and send the profile picture for a given user."""
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:  # Ensure dict_row is used
            cur.execute('SELECT profile_picture FROM "user" WHERE user_id = %s', [user_id])
            row = cur.fetchone()
            if row and row['profile_picture']:
                return Response(row['profile_picture'], mimetype='image/jpeg')
            else:
                return "No profile picture found", 404




