from repositories.db import get_pool
from psycopg.rows import dict_row
from typing import Any

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
        
def delete_event(event_id: str) -> dict[str: Any]:
    
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        DELETE FROM event WHERE event_id = %s
                        ''', event_id)
            event_id = cur.fetchone()
            if event_id is None:
                raise Exception('Failed to delete event.')
            return {
                'event_id': event_id
            }