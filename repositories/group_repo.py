from repositories.db import get_pool
from psycopg.rows import dict_row
from typing import Any

def group_exists(group_name: str) -> bool:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                            SELECT
                                group_id
                            FROM
                                "group"
                            WHERE group_name = %s
                            ''', [group_name])
            group = cur.fetchone()
            return group is not None

def get_user_groups_from_user_id(user_id: str) -> dict[str: Any]:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                            SELECT
                                group_name, group_id
                            FROM
                                "group"
                            WHERE
                                user_id = %s
                            ''', [user_id])
            return cursor.fetchall()

def create_group(user_id: str, group_name: str, group_description: str, group_public: bool) -> dict[str: Any]:
    if group_exists(group_name):
        return False, "Group already exists."
    
    # creates and registers the new group
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        INSERT INTO "group" (user_id, group_name, group_description, group_public)
                        VALUES (%s, %s, %s, %s)
                        RETURNING group_id
                        ''', [user_id, group_name, group_description, group_public])
            group_id = cur.fetchone()
            if group_id is None:
                raise Exception('Failed to create group.')
            return {
                'group_id': group_id,
                'group_name': group_name
            }
            
def get_user_group_from_group_id(group_id: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                            SELECT
                                *
                            FROM
                                "group"
                            WHERE
                                group_id = %s
                            ''', [group_id])
            return cursor.fetchone()
        
def get_member_count_from_group_id(group_id: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                            SELECT
                                *
                            FROM
                                membership
                            WHERE
                                group_id = %s
                            ''', [group_id])
            return cursor.fetchone()

# TODO: Update group details

# TODO: Delete a group

# TODO: Add Member

# TODO: Remove Member

# TODO: Change a Member's role (owner, admin, member)