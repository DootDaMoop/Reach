from repositories.db import get_pool
from repositories.group_repo import get_members_from_group_id
from repositories import group_repo, email_repo, user_repo
from psycopg.rows import dict_row
from typing import Tuple, Union, Dict, Any
from werkzeug.datastructures import FileStorage
import re
import bcrypt
import logging
from flask import Response


def event_exists_by_name(event_name: str) -> bool:
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

def get_event_by_event_id(event_id: int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                            SELECT
                                *
                            FROM
                                event
                            WHERE event_id = %s
                            ''', [event_id])
            event = cur.fetchone()
            
            if event is None:
                raise Exception('Failed to get event details')
            return event

def create_event(user_id: int, group_id: int, event_name:str, event_description: str, event_public: bool, event_start_timestamp: str, event_end_timestamp: str) -> dict[str: Any]:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        INSERT INTO event (user_id, group_id, event_name, event_description, event_public, event_start_timestamp, event_end_timestamp)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        RETURNING event_id
                        ''', [user_id, group_id, event_name, event_description, event_public, event_start_timestamp, event_end_timestamp])
            event_id = cur.fetchone()
            if event_id is None:
                raise Exception('Failed to create group.')
            return {
                'event_id': event_id,
                'event_name': event_name,
                'event_public': event_public
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


def get_all_selected_group_events(group_id: int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                            SELECT
                                *
                            FROM
                                event
                            WHERE
                                group_id = %s
                            ''', [group_id])
            return cursor.fetchall()

# This method is used for getting ALL EVENTS FOR THE LOGGED IN USER; FOR HOME PAGE.
def get_all_user_group_events(user_id: int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                            SELECT
                                event.event_id, group_id, event_name, event_description, event_public, event_start_timestamp, event_end_timestamp, attending
                            FROM
                                pending
                            INNER JOIN
                                event ON pending.event_id = event.event_id
                            WHERE
                                pending.user_id = %s
                            ORDER BY
                                event_start_timestamp ASC
                            ''', [user_id])
            return cursor.fetchall()

# This method is used for getting ALL EVENTS FOR THE LOGGED IN USER AND FOR THE SPECIFIC GROUP PAGE THEY'RE IN.
def get_all_user_group_events_for_selected_group(user_id: int, group_id: int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                            SELECT
                                event.event_id, group_id, event_name, event_description, event_public, event_start_timestamp, event_end_timestamp, attending
                            FROM
                                pending
                            JOIN
                                event ON pending.event_id = event.event_id
                            WHERE
                                pending.user_id = %s AND event.group_id = %s
                            ORDER BY
                                event_start_timestamp ASC
                            ''', [user_id, group_id])
            return cursor.fetchall()

# This method is used for inviting all users in a group for a PUBLIC EVENT.
def invite_all_users_in_group_to_event(group_id: int, event_id: int) -> dict[str: Any]:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            members = group_repo.get_members_from_group_id(group_id)
            
            for member in members:
                user_id = member['user_id']
                cur.execute('''
                        INSERT INTO pending (user_id, event_id, attending)
                        VALUES (%s, %s, NULL)
                        RETURNING event_id
                        ''', [user_id, event_id['event_id']])
                invites = cur.fetchall()
                if invites is None:
                    raise Exception('Failed to send pending invites.')
                
                event = get_event_by_event_id(event_id['event_id'])

                subject = f"Reach: You've been invited to {event['event_name']}!"
                html = f"""
                        <html>
                            <body>
                                <h1>Event Name: {event['event_name']}</h1>
                                <h2>Public Event: {event['event_public']}</h2>
                                <p><b>Description: {event['event_description']}</b></p>
                                <p><b>Event Start Time: {event['event_start_timestamp'].strftime('%Y-%m-%d %I:%M:%S %p')}</b></p>
                                <p><b>Event End Time: {event['event_end_timestamp'].strftime('%Y-%m-%d %I:%M:%S %p')}</b></p>
                                <br>
                                <p>Hope to see you there!</p>
                            </body>
                        </html>
                        """
                email_repo.send_email(member['user_email'],subject, html)

def verify_user_admin_for_event(user_id: int, group_id: int, event_id: int) -> bool:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                            SELECT
                                user_role
                            FROM
                                membership
                            JOIN
                                event ON membership.group_id = event.group_id
                            WHERE
                                membership.user_id = %s AND membership.group_id = %s AND event_id = %s
                            ''', [user_id, group_id, event_id])
            user_role = cursor.fetchone()

            if user_role is None:
                raise Exception('Failed to get user_role')
            return user_role

def edit_event(event_id: int, event_name: str, event_description: str, event_public, event_start_timestamp, event_end_timestamp):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        UPDATE
                            event
                        SET
                            event_name = %s,
                            event_description = %s,
                            event_public = %s,
                            event_start_timestamp = %s,
                            event_end_timestamp = %s
                        WHERE event_id = %s
                        ''', [event_name, event_description, event_public, event_start_timestamp, event_end_timestamp, event_id])
            event_id = cur.fetchone()
            if event_id is None:
                raise Exception('Failed to delete event.')
            return {
                'event_id': event_id
            }


#event_id has cascade delete on it so it should delete everythig from pending and collaboration
def delete_event(event_id: int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        DELETE FROM
                            event
                        WHERE event_id = %s
                        RETURNING event_id
                        ''', [event_id])
            event_id = cur.fetchone()
            if event_id is None:
                raise Exception('Failed to delete event.')
            return {
                'event_id': event_id
            }

def accept_event(event_id: int, user_id: int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        UPDATE
                            pending
                        SET
                            attending = true
                        WHERE event_id = %s AND user_id = %s
                        ''', [event_id, user_id])

def decline_event(event_id: int, user_id: int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        UPDATE
                            pending
                        SET
                            attending = false
                        WHERE event_id = %s AND user_id = %s
                        ''', [event_id, user_id])

def revert_event_choice(event_id: int, user_id: int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        UPDATE
                            pending
                        SET
                            attending = null
                        WHERE event_id = %s AND user_id = %s
                        ''', [event_id, user_id])

def get_user_events_for_day(user_id: int, year: int, month: int, day: int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT
                            *
                        FROM
                            event
                        WHERE user_id = %s AND DATE(event_start_timestamp) = %s
                        ''', [user_id, f'{year}-{month:02}-{day:02}'])
            events = cur.fetchall()

            if events is None:
                raise Exception('Failed to get events for day')
            return events

def get_members_for_edit_event_page(group_id: int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                            SELECT
                                user_name, user_role, profile_picture, u.user_id
                            FROM
                                membership
                            JOIN
                                "user" u on membership.user_id = u.user_id
                            WHERE
                                group_id = %s
                            ''', [group_id])
            return cursor.fetchall()

def verify_member_is_invited_to_event(user_id: int, event_id: int) -> bool:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                            SELECT
                                *
                            FROM
                                pending
                            WHERE
                                user_id = %s AND event_id = %s
                            ''', [user_id, event_id])
            user = cursor.fetchone()
            if user:
                return True
            else:
                return False

def invite_user_to_event(user_id: int, event_id: int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                    INSERT INTO pending (user_id, event_id, attending)
                    VALUES (%s, %s, NULL)
                    RETURNING event_id
                    ''', [user_id, event_id])
            event_id = cur.fetchone()

            if event_id is None:
                raise Exception('Failed to send invite.')
            
            event = get_event_by_event_id(event_id['event_id'])

            subject = f"Reach: You've been invited to {event['event_name']}!"
            html = f"""
                    <html>
                        <body>
                            <h1>Event Name: {event['event_name']}</h1>
                            <h2>Public Event: {event['event_public']}</h2>
                            <p><b>Description: {event['event_description']}</b></p>
                            <p><b>Event Start Time: {event['event_start_timestamp'].strftime('%Y-%m-%d %I:%M:%S %p')}</b></p>
                            <p><b>Event End Time: {event['event_end_timestamp'].strftime('%Y-%m-%d %I:%M:%S %p')}</b></p>
                            <br>
                            <p>Hope to see you there!</p>
                        </body>
                    </html>
                    """
            user = user_repo.get_user_from_user_id(user_id)
            email_repo.send_email(user['user_email'],subject, html)

def remove_invited_user_from_event(user_id: int, event_id: int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                    DELETE FROM pending WHERE user_id = %s AND event_id = %s
                    ''', [user_id, event_id])

def get_attending_status(user_id, event_id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                            SELECT
                                attending
                            FROM
                                pending
                            WHERE
                                user_id = %s AND event_id = %s
                            ''', [user_id, event_id])
            attending = cursor.fetchone()
            return attending
