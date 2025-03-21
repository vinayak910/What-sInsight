import streamlit as st
import os
import time
from datetime import datetime
from auth import AuthManager
import preprocessor

auth_manager = AuthManager()
# Ensure session state is initialized
if "user" not in st.session_state:
    st.session_state.user = None
if "mode" not in st.session_state:
    st.session_state.mode = "Chat Statistics"
if "uploaded_file_path" not in st.session_state:
    st.session_state.uploaded_file_path = None
if "df" not in st.session_state:
    st.session_state.df = None
if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False  # Track file upload status

def save_uploaded_file(uploaded_file, user_email):
    """Saves the uploaded file in a user-specific folder with timestamp."""
    user_folder = f"uploads/{user_email.replace('@', '_').replace('.', '_')}"
    os.makedirs(user_folder, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_path = os.path.join(user_folder, f"chat_{timestamp}.txt")

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path

# **User Logged In UI**
if st.session_state.user:
    # **Show Welcome Message Only If No File Is Uploaded**

    # **Show File Uploader Only If No File Is Uploaded**
    if not st.session_state.file_uploaded:
        st.markdown("""
        <h1 style='text-align: center;'>We missed you! 😍</h1>
        <h2 style='text-align: center;'>Are you ready to witness the insights?</h2>
            """, unsafe_allow_html=True)

        st.subheader("Upload your chat file")
        uploaded_file = st.file_uploader("Drag and drop file here", type=["txt"], help="Limit 200MB per file")
        if st.button("Sign out"):
                st.session_state.user = None
                st.session_state.uploaded_file_path = None
                st.session_state.chat_text = None
                st.session_state.file_uploaded = False
                st.rerun()

        if uploaded_file is not None:
            file_contents = uploaded_file.read().decode("utf-8")  # Decode file content
            df = preprocessor.preprocess(file_contents)
            st.session_state.df = df
            file_path = save_uploaded_file(uploaded_file, st.session_state.user["email"])
            st.session_state.uploaded_file_path = file_path
            st.session_state.file_uploaded = True  # Hide upload UI
            st.success(f"✅ File saved: {file_path}")
            st.rerun()  # Refresh UI to hide welcome message and uploader

    # **Show Sidebar & Analysis Only After File Upload**
    if st.session_state.file_uploaded:
        with st.sidebar:
            st.title("What'sInsight 🤔")
            st.sidebar.image("D:\Projects\SE-Project\What'sInsight\magnifying-glass.png")
            st.text("Select Analysis Mode")
            mode = st.radio("Choose an option", ["Chat Statistics", "Timeline Analysis", "Word Cloud", "Sentiment Analysis"], index=0)

            if mode != st.session_state.mode:
                st.session_state.mode = mode
                st.rerun()  # Refresh UI to show only selected mode

            st.markdown(f"<h4>🔍 Mode Selected: {mode}</h4>", unsafe_allow_html=True)
            
            # **Sign Out Button in Sidebar**
            if st.button("Sign out"):
                st.session_state.user = None
                st.session_state.uploaded_file_path = None
                st.session_state.df = None
                st.session_state.file_uploaded = False
                st.rerun()

        # 🎯 **Display Analysis Based on Selected Mode**
        st.subheader(f"{mode} Analysis")
        st.write(f"Analysis started for mode: **{mode}** on file: **{st.session_state.uploaded_file_path}**")

        if mode == "Chat Statistics":
            st.write("📊 Chat Statistics are being analyzed...")
            st.dataframe(st.session_state.df)
        elif mode == "Timeline Analysis":
            st.write("📅 Generating Timeline Insights...")
        elif mode == "Word Cloud":
            st.write("☁️ Creating Word Cloud...")
        elif mode == "Sentiment Analysis":
            st.write("😊 Analyzing Sentiments...")

# **Login UI (If User Not Logged In)**
else:
    st.title("Welcome to What's Insight 🤔")
    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        st.session_state.user = auth_manager.login(email , password)
        if st.session_state.user:
            st.success("Login Successful! 🎉")
            time.sleep(1)
            st.rerun() 
        else:
            st.error("Incorrect username or password. Try again!")

