import csv
import re
import os

# Regular expression for validating an Email
email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

class User_management:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.users = self.load_users()

    def is_valid_email(self, email):
        """Check if the email address is valid using regex."""
        return bool(re.match(email_regex, email))

    def load_users(self):
        """Load users from the CSV file."""
        if not os.path.exists(self.csv_file_path):
            return {}
        with open(self.csv_file_path, mode='r', newline='') as file:
            csv_reader = csv.DictReader(file)
            return {row['email']: row for row in csv_reader}
        
    def validate_user(self, email, password):
        user = self.users.get(email)
        if user and user['password'] == password:
            return True, "User authenticated successfully."
        else:
            return False, "Invalid email or password."

    def user_exists(self, email):
        """Check if the user already exists."""
        return email in self.users

    def register_user(self, email, password, first_name, last_name):
        """Register a new user if the email is valid and not already taken."""
        if not self.is_valid_email(email):
            return False, "Invalid email format."
        if self.user_exists(email):
            return False, "User already exists."

        # Save the new user
        self.users[email] = {'email': email, 'password': password, 'first_name': first_name, 'last_name': last_name}
        self.save_user(email, password, first_name, last_name)  # Updated call to match save_user's new signature
        return True, "User registered successfully."

    def save_user(self, email, password, first_name, last_name):
        """Save the user to the CSV file."""
        with open(self.csv_file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['email', 'password', 'first_name', 'last_name'])
            if file.tell() == 0:  # This checks if the file is empty and writes the header if true.
                writer.writeheader()
            writer.writerow({'email': email, 'password': password, 'first_name': first_name, 'last_name': last_name})
    
    def get_first_name_from_email(self, email):
        """Get the first name of the user with the given email."""
        user = self.users.get(email)
        if user:
            return user['first_name']
        else:
            return None

    def get_last_name_from_email(self, email):
        """Get the last name of the user with the given email."""
        user = self.users.get(email)
        if user:
            return user['last_name']
        else:
            return None
