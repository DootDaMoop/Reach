from repositories.db import get_pool
from repositories.group_repo import get_all_members_from_group_id
from psycopg.rows import dict_row
from typing import Any

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
            group = cur.fetchone()
            
            if group is None:
                raise Exception('Failed to get event details')
            return group

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
                                event.event_id, group_id, event_name, event_description, event_public, event_start_timestamp, event_end_timestamp
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
                                event.event_id, group_id, event_name, event_description, event_public, event_start_timestamp, event_end_timestamp
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
            members = get_all_members_from_group_id(group_id)
            
            for member in members:
                user_id = member['user_id']
                cur.execute('''
                        INSERT INTO pending (user_id, event_id, attending)
                        VALUES (%s, %s, NULL)
                        RETURNING event_id
                        ''', [user_id, event_id['event_id']])
                event = cur.fetchall()

                if event is None:
                    raise Exception('Failed to send pending invites.')

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

def delete_event(event_id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        DELETE FROM
                            event
                        WHERE event_id = %s
                        ''', [event_id])
