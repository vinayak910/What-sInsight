import firebase_admin  
from firebase_admin import credentials, auth
import os
import requests

class AuthManager:
    def __init__(self):
        self.initialize_firebase()
        self.api_key = os.getenv("FIREBASE_API_KEY")  # Firebase Web API Key
        if self.api_key:
            print(f"✅ API Key Found: {self.api_key}")
        else:
            print("❌ API Key Not Found!")

    def initialize_firebase(self):
        json_path = os.getenv("FIREBASE_KEY_PATH")
        if not firebase_admin._apps and json_path:
            cred = credentials.Certificate(json_path)
            firebase_admin.initialize_app(cred)

    def login(self, email, password):
        """Logs in user using Firebase REST API (email + password verification)"""
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.api_key}"
        data = {"email": email, "password": password, "returnSecureToken": True}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            user_data = response.json()
            return {"uid": user_data["localId"], "email": user_data["email"]}
        else:
            return False  # Invalid credentials

    def signup(self, email, password):
        """Creates a new user account in Firebase."""
        if len(password) < 6:
            return 0  # Password too short
        try:
            auth.get_user_by_email(email)
            return 1  # Email already exists
        except auth.UserNotFoundError:
            auth.create_user(email=email, password=password)
            return 2  # Success

    def logout(self):
        """Logs out the user."""
        return None
