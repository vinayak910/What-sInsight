import firebase_admin  
from firebase_admin import credentials, auth,firestore
import os
import requests

class AuthManager:
    def __init__(self):
        self.initialize_firebase()
        self.api_key = os.getenv("FIREBASE_API_KEY")  # Firebase Web API Key
        if self.api_key:
            print(f"API Key Found: {self.api_key}")
        else:
            print("API Key Not Found!")

    def initialize_firebase(self):
        json_path = os.getenv("FIREBASE_KEY_PATH")
        if not firebase_admin._apps and json_path:
            cred = credentials.Certificate(json_path)
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()
    def login(self, email, password):
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.api_key}"
        data = {"email": email, "password": password, "returnSecureToken": True}
        response = requests.post(url, json=data)

        if response.status_code == 200:
            user_data = response.json()
            uid = user_data["localId"]
            email = user_data["email"]

            # Check if user exists in Firestore, if not then create
            user_role = self.get_user_role(uid)
            if user_role is None:
                self.create_user(uid, email)

            return {"uid": uid, "email": email, "role": self.get_user_role(uid)}
        else:
            return False  # Invalid credentials

    def create_user(self, uid, email):
        """Creates a new user document in Firestore if not exists"""
        user_ref = self.db.collection("users").document(uid)
        user_ref.set({
            "email": email,
            "role": "standard"  # Default role
        })

    def get_user_role(self, uid):
        """Fetches user role from Firestore"""
        user_ref = self.db.collection("users").document(uid)
        user_doc = user_ref.get()
        if user_doc.exists:
            return user_doc.to_dict().get("role", "standard")  # Default role = "standard"
        return None

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
