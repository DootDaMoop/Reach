class user:
    def __init__(self, user_id, email, name=None, profile_pic=None, access_token=None, refresh_token=None):
        self.user_id = user_id  # Unique identifier for the user
        self.email = email  # User's email address
        self.name = name  # User's full name (optional)
        self.profile_pic = profile_pic  # URL to the user's profile picture (optional)
        self.access_token = access_token  # OAuth Access Token (optional)
        self.refresh_token = refresh_token  # OAuth Refresh Token (optional)

    def __repr__(self):
        return f"<user {self.email}>"
