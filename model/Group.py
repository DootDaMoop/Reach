from User import User
class Group:
    def __init__(self, group_name: str, group_id: int, group_description: str, group_owner: User):
        self.group_name = group_name
        self.group_id = group_id
        self.group_description = group_description
        self.group_owner = group_owner
        self.members = set() # set of Users
        self.admins = set() # set of Users
        self.events = dict() # dictionary of Events

    def add_member(self, member: User):
        self.members.add(member)

    def remove_member(self, member: User):
        self.members.remove(member)