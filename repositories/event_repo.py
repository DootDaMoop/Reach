from repositories.db import get_pool
from psycopg.rows import dict_row
from typing import Tuple, Union, Dict, Any
from werkzeug.datastructures import FileStorage
import re
import bcrypt
import logging
from flask import Response


def event_exists(event_name: str) -> bool:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                            SELECT
                                event_id
                            FROM
                                event
                            WHERE event_name = %s
                            ''', [event_name])
            group = cur.fetchone()
            return group is not None

def create_event(user_id: str, group_id: str, event_name:str, event_description: str, event_public: bool, event_start_timestamp: str, event_end_timestamp: str) -> dict[str: Any]:
    #if event_exists(event_name):
    #    return False, "Group already exists."

    # creates and registers the new group
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        INSERT INTO event (user_id, group_id, event_name, event_description, event_public, event_start_timestamp, event_end_timestamp)
                        VALUES (%s, %s, %s, %s)
                        RETURNING group_id
                        ''', [user_id, group_id, event_name, event_description, event_public, event_start_timestamp, event_end_timestamp])
            event_id = cur.fetchone()
            if event_id is None:
                raise Exception('Failed to create group.')
            return {
                'event_id': event_id,
                'event_name': event_name
            }
        

def update_event_picture(event_id: int, event_picture: FileStorage) -> bool:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            try:
                # Read the bytes from the FileStorage object
                picture_bytes = event_picture.read()
                #double quotes might affect
                cur.execute('''
                    UPDATE "event"
                    SET event_picture = %(event_picture)s
                    WHERE event_id = %(event_id)s
                ''', {'profile_picture': picture_bytes, 'event_id': event_id})
                conn.commit()
                return True
            except Exception as e:
                logging.error("Error updating event picture: %s", e)
                conn.rollback()
                return False
            

def get_event_picture(event_id: int):
    """Retrieve and send the profile picture for a given user."""
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:  # Ensure dict_row is used
            cur.execute('SELECT event_picture FROM "event" WHERE event_id = %s', (event_id,))
            row = cur.fetchone()
            if row and row['event_picture']:
                return Response(row['event_picture'], mimetype='image/jpeg')
            else:
                return "No event picture found", 404
            

def get_event_start_time(event_id: int) -> Union[str, Tuple[str, int]]:
    """Retrieve the start timestamp for a given event and return it in 24-hour format."""
        #hour = formatted_time.split(':')[0]
        #minute = formatted_time.split(':')[1]

    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT event_start_timestamp
                        FROM event
                        WHERE event_id = %s
                        ''', (event_id,))
            event_time = cur.fetchone()
            if event_time:
                # Format the timestamp to 24-hour time format HH:MM:SS
                formatted_time = event_time['event_start_timestamp'].strftime('%H:%M:%S')
                return formatted_time
            else:
                return "No event found", 404
            

def get_event_by_id(event_id: int) -> Union[dict, Tuple[str, int]]:
    """Retrieve an event by its ID from the database."""
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT *
                        FROM event
                        WHERE event_id = %s
                        ''', (event_id,))
            event = cur.fetchone()
            if event:
                return event
            else:
                return "No event found", 404