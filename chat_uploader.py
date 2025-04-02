from pathlib import Path
import datetime

class ChatUploader:
    def __init__(self, base_dir="uploads/"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save_file(self, uploaded_file, user_email):
        "Saves chat file inside a user-specific folder with a unique timestamped name."
        
        # 🔹 Create user-specific folder
        user_folder = self.base_dir / user_email.replace("@", "_").replace(".", "_")
        user_folder.mkdir(parents=True, exist_ok=True)

        # 🔹 Generate unique filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = user_folder / f"chat_{timestamp}.txt"

        # 🔹 Save uploaded file
        file_path.write_bytes(uploaded_file.getbuffer())

        return str(file_path)  # Returning file path

    def get_user_chats(self, user_email):
        """Returns list of uploaded chat files for a user."""
        user_folder = self.base_dir / user_email.replace("@", "_").replace(".", "_")
        return list(user_folder.glob("*.txt")) if user_folder.exists() else []
