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
        with conn.cursor() as cursor:
            cursor.execute('''
                            SELECT
                                count(user_id)
                            FROM
                                membership
                            WHERE
                                group_id = %s
                            ''', [group_id])
            return cursor.fetchone()[0]

def get_role_in_group_from_user_and_group_id(user_id: str, group_id: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                            SELECT
                                user_role
                            FROM
                                membership
                            WHERE
                                user_id = %s and group_id = %s
                            ''', [user_id, group_id])
            return cursor.fetchone()

def get_groups_from_user_id(user_id: str): # This returns all groups a user is a part of, in comparison to turning in groups a user is owner of
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                            SELECT 
                                *
                            FROM 
                                "group" user_group
                            JOIN 
                                membership on user_group.group_id = membership.group_id
                            JOIN 
                                "user" usr on usr.user_id = membership.user_id
                            WHERE 
                                usr.user_id = %s;
                            ''', [user_id])
            return cursor.fetchall()

def get_group_and_user_from_group_and_user_id(user_id: str, group_id: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                            SELECT 
                                *
                            FROM 
                                "group" user_group
                            JOIN 
                                membership on user_group.group_id = membership.group_id
                            JOIN 
                                "user" usr on usr.user_id = membership.user_id
                            WHERE 
                                usr.user_id = %s and user_group.group_id = %s;
                            ''', [user_id, group_id])
            return cursor.fetchone()

# Returns all members from a group using group_id
def get_all_members_from_group_id(group_id: int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                            SELECT 
                                user_id
                            FROM 
                                membership
                            WHERE 
                                group_id = %s;
                            ''', [group_id])
            return cursor.fetchall()

# TODO: Update group details

# TODO: Delete a group

# TODO: Add Member

# TODO: Remove Member

# TODO: Change a Member's role (owner, admin, member)