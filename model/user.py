class User:
    def __init__(self, email, password = None, google_id = None, first_name=None, last_name=None, pfp=None, first_and_last=None):
        self.google_id = google_id
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.pfp = pfp  
        self.first_and_last = first_and_last
        
    def __init__(self):
        self.google_id = None
        self.email = None
        self.first_name = None
        self.last_name = None
        self.pfp = None 
        self.first_and_last = None
    
    def update_from_session(self, session: dict):
        self.google_id = session.get("google_id")
        self.email = session.get("email")
        self.first_name = session.get("first_name")
        self.last_name = session.get("last_name")
        self.pfp = session.get("pfp")
        self.first_and_last = session.get("first_and_last")

    def update_from_registration(self, email, password, first_name, last_name):
        self.email = email
        self.set_password(password)  # Assuming you might have some password hashing here
        self.first_name = first_name
        self.last_name = last_name




    def set_password(self, new_password):
        self.password = new_password
    
