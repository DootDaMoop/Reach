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

def get_group_by_id(group_id: str) -> dict:
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

def get_group_description_by_id(group_id: str) -> str:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                            SELECT
                                group_description
                            FROM
                                "group"
                            WHERE
                                group_id = %s
                            ''', [group_id])
            description = cursor.fetchone()
            if description:
                return description[0]
            else:
                return "Group description not found."
            

def get_group_public_status(group_id: str) -> bool:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                            SELECT
                                group_public
                            FROM
                                "group"
                            WHERE
                                group_id = %s
                            ''', [group_id])
            result = cursor.fetchone()
            if result is not None:
                return result[0]  # Assuming 'group_public' is the first column returned
            else:
                raise ValueError("Group not found with the specified ID")


def get_group_name_by_id(group_id: str) -> str:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                            SELECT
                                group_name
                            FROM
                                "group"
                            WHERE
                                group_id = %s
                            ''', [group_id])
            result = cursor.fetchone()
            if result:
                return result[0]  # Assuming 'group_name' is the first column returned
            else:
                return "No group found with this ID."
            


def get_members_and_roles(group_id: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                SELECT 
                    usr.user_name, mem.user_role
                FROM 
                    "user" usr
                JOIN 
                    membership mem ON usr.user_id = mem.user_id
                WHERE 
                    mem.group_id = %s;
            ''', [group_id])
            members = cursor.fetchall()
            if members:
                return members
            else:
                return "No members found for this group."



def update_group_description(group_id: str, new_description: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                UPDATE "group"
                SET group_description = %s
                WHERE group_id = %s;
            ''', [new_description, group_id])
            conn.commit()
            return cursor.rowcount > 0 


def update_group_name(group_id: str, new_name: str = None):

    if not new_name:
        return True  

    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                UPDATE "group"
                SET group_name = %s
                WHERE group_id = %s;
            ''', [new_name, group_id])
            conn.commit()
            return cursor.rowcount > 0  # Returns True if at least one row was updated



def update_group_status(group_id: str, new_status: bool):

    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                UPDATE "group"
                SET group_public = %s
                WHERE group_id = %s;
            ''', [new_status, group_id])
            conn.commit()
            return cursor.rowcount > 0  # Returns True if at least one row was updated


def get_members_from_group_id(group_id: str):
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
#group_is has cascade delete on it so it should delete everything from collaboration, membership, event 
def delete_group(group_id: int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        DELETE FROM
                            "group"
                        WHERE group_id = %s
                        RETURNING group_id
                        ''', [group_id])
            group_id = cur.fetchone()
            if group_id is None:
                raise Exception('Failed to delete group.')
            return {
                'group_id': group_id
            }

# TODO: Add Member



# TODO: Remove Member
def remove_member_from_group(user_id: str, group_id: str) -> bool:

    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                DELETE FROM membership
                WHERE user_id = %s AND group_id = %s;
            ''', [user_id, group_id])
            conn.commit()
            return cursor.rowcount > 0  # Returns True if at least one row was affected




# TODO: Change a Member's role (owner, admin, member)
def change_member_role(user_id: str, group_id: str, new_role: str) -> bool:

    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                UPDATE membership
                SET user_role = %s
                WHERE user_id = %s AND group_id = %s;
            ''', [new_role, user_id, group_id])
            conn.commit()
            return cursor.rowcount > 0  # Returns True if at least one row was updated

#Finding all admins in a group
def get_admin_member_and_role(group_id: int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                SELECT 
                    usr.user_id, mem.user_role
                FROM 
                    "user" usr
                JOIN 
                    membership mem ON usr.user_id = mem.user_id
                WHERE 
                    mem.group_id = %s AND mem.user_role = 1;
            ''', [group_id])
            members = cursor.fetchone()
            if members:
                return members
            else:
                return "No admins found for this group."

