import streamlit as st
from collections import Counter
from email.message import EmailMessage
import smtplib


import re 
import os
import time
from datetime import datetime
from auth import AuthManager
from chat_stats import ChatStatistics
from time_analysis import TimelineAnalysis
import preprocessor
import helper
from activity_map_analysis import ActivityMap
from preprocessor import Preprocessor
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import word_cloud
import matplotlib.font_manager as fm

# Set font for emojis
plt.rcParams['font.family'] = 'Segoe UI Emoji'



st.set_page_config(page_title="What's Insight 🤔", page_icon="🤔")

auth_manager = AuthManager()
chat_stats = ChatStatistics()
timeline_analysis = TimelineAnalysis()
activity_map = ActivityMap()
preprocess = Preprocessor()
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
    user_role = st.session_state.user["role"]
    # **Show File Uploader Only If No File Is Uploaded**
    if not st.session_state.file_uploaded:
        st.markdown("""
        <h1 style='text-align: center;'><span style='color: #FFEA00;'>We missed you! 😍</h1>
        <h2 style='text-align: center;'>Are you ready to witness the insights?</h2>
            """, unsafe_allow_html=True)

        st.subheader("Upload your chat file")
        uploaded_file = st.file_uploader("Drag and drop file here", type=["txt"], help="Limit 200MB per file")
        if st.button("Sign out"):
                st.session_state.user = None
                st.session_state.uploaded_file_path = None
                st.session_state.df = None
                st.session_state.file_uploaded = False
                st.rerun()

        if uploaded_file is not None:
            file_contents = uploaded_file.read().decode("utf-8")  # Decode file content
            df = preprocess.preprocess(file_contents)
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
            mode = st.radio("Choose an option", ["Chat Statistics", "Timeline Analysis","Activity Map", "Word Cloud", "Detective Mode"], index=0)

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


        st.markdown(f"""<h1 style='text-align: center;text-shadow: 3px 3px 5px rgba(255, 255, 0, 0.5);'>
        <span style='color: #FFEA00;'> Chat</span> 
        <span style='color: #FFAB40;'>Analysis</span> 
        <span style='color: #00E5FF;'>Playground</span>
        </h1>""" , unsafe_allow_html=True)
        st.write(f"Analysis started for mode: **{mode}**")

        df = st.session_state.df
        #fetch unique users
       

        if mode == "Chat Statistics":
            user_list = df['user'].unique().tolist()
            user_list.sort()
            user_list.insert(0,"Overall")
            selected_user = st.selectbox("Show analysis wrt",user_list)

            if st.button("Show Analysis") or selected_user== 'Overall':
                st.write("📊 Chat Statistics are being analyzed...")
            # Stats Area
                num_messages, words, num_media_messages, num_links = chat_stats.fetch_stats(selected_user,df)
                st.markdown("""
    <h1 style='text-align: center; 
               color: #FFEA00;
               text-shadow: 3px 3px 5px rgba(255, 255, 0, 0.5);'>
               Top Statistics 
                </h1>
               """, unsafe_allow_html=True)

                col1, col2, col3, col4 = st.columns(4)


                with col1:
                    st.markdown(f"<h3 style='color: #00FFFF;'>Total Messages</h3>", unsafe_allow_html=True)
                    st.subheader(num_messages)

                with col2:
                    st.markdown(f"<h3 style='color: #00FFFF;'>Total Words</h3>", unsafe_allow_html=True)
                    st.subheader(words)

                with col3:
                    st.markdown(f"<h3 style='color: #00FFFF;'>Media Shared</h3>", unsafe_allow_html=True)
                    st.subheader(num_media_messages)

                with col4:
                    st.markdown(f"<h3 style='color: #00FFFF;'>Links Shared</h3>", unsafe_allow_html=True)
                    st.subheader(num_links)

                avg_msg_per_day, avg_msg_length, pareto_valid, media_msg_ratio = chat_stats.fetch_math_stats(selected_user, df)

                # Heading
                st.markdown("""
                <h1 style='text-align: center; 
                        color: #FFEA00;
                        text-shadow: 3px 3px 5px rgba(255, 255, 0, 0.5);'>
                        Mathematical Statistics
                            </h1>
                        """, unsafe_allow_html=True)

                # Columns for layout
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.markdown(f"<h2 style='color: #00FFFF;'>Avg. Messages/Day</h2>", unsafe_allow_html=True)
                    st.header(avg_msg_per_day)

                with col2:
                    st.markdown(f"<h2 style='color: #00FFFF;'>Avg. Msg Length</h2>", unsafe_allow_html=True)
                    st.header(avg_msg_length)

                with col3:
                    st.markdown(f"<h2 style='color: #00FFFF;'>Pareto Valid?</h2>", unsafe_allow_html=True)
                    st.header(pareto_valid)

                with col4:
                    st.markdown(f"<h2 style='color: #00FFFF;'>Media Msg Ratio</h2>", unsafe_allow_html=True)
                    st.header(media_msg_ratio)


 
                    
                most_word, longest_msg_length, most_emoji, active_period = chat_stats.fetch_interesting_stats(selected_user, df)
 
                
                st.markdown("""
    <h1 style='text-align: center; 
               color: #FFEA00;
               text-shadow: 3px 3px 5px rgba(255, 255, 0, 0.5);'>
               Interesting Statistics
                </h1>
               """, unsafe_allow_html=True)

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.markdown(f"<h3 style='color: #00FFFF;'>Most Used Word</h3>", unsafe_allow_html=True)
                    st.subheader(most_word)  

                with col2:
                    st.markdown(f"<h3 style='color: #00FFFF;'>Longest Message Length</h3>", unsafe_allow_html=True)
                    st.subheader(longest_msg_length)  

                with col3:
                    st.markdown(f"<h3 style='color: #00FFFF;'>Most Used Emoji</h3>", unsafe_allow_html=True)
                    st.subheader(most_emoji)  

                with col4:
                    st.markdown(f"<h3 style='color: #00FFFF;'>Most Active Period</h3>", unsafe_allow_html=True)
                    st.subheader(active_period)
        elif mode == "Timeline Analysis":
            user_list = df['user'].unique().tolist()
            user_list.sort()
            user_list.insert(0,"Overall")
            selected_user = st.selectbox("Show analysis wrt",user_list)

            if st.button("Show Analysis") or selected_user== 'Overall':
                st.markdown(
                    """
                    <style>
                    .title {
                        color: yellow;
                        font-size: 28px;
                        font-weight: bold;
                        text-shadow: 2px 2px 5px black;
                        text-align: center;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )
                st.write("📅 Generating Timeline Insights...")

                # Monthly Timeline
                st.markdown("""
    <h1 style='text-align: center; 
               color: #FFEA00;
               text-shadow: 3px 3px 5px rgba(255, 255, 0, 0.5);'>
               Monthly Timeline
                </h1>
               """, unsafe_allow_html=True)                
                timeline = timeline_analysis.monthly_timeline(selected_user, df)

                fig = px.line(timeline, x='time', y='message', 
                            title="",  # Removed title from Plotly (Handled by HTML)
                            line_shape='linear', 
                            markers=True)

                fig.update_layout(height=350, width=600, xaxis_title="Month", yaxis_title="Messages", template="plotly_white")

                st.plotly_chart(fig, use_container_width=True)

                # Daily Timeline
                st.markdown("""
    <h1 style='text-align: center; 
               color: #FFEA00;
               text-shadow: 3px 3px 5px rgba(255, 255, 0, 0.5);'>
               Daily Timeline
                </h1>
               """, unsafe_allow_html=True)                
                daily_timeline = timeline_analysis.daily_timeline(selected_user, df)

                fig2 = px.line(daily_timeline, x='date', y='message', 
                            title="",  # Removed title from Plotly
                            line_shape='linear', 
                            markers=True)

                fig2.update_layout(height=350, width=600, xaxis_title="Date", yaxis_title="Messages", template="plotly_white")

                st.plotly_chart(fig2, use_container_width=True)



        elif mode == "Activity Map":
            user_list = df['user'].unique().tolist()
            user_list.sort()
            user_list.insert(0,"Overall")
            selected_user = st.selectbox("Show analysis wrt",user_list)
                        
            if st.button("Show Analysis") or selected_user== 'Overall':

                st.markdown(
                    """
                    <style>
                    .title {
                        color: yellow;
                        font-size: 28px;
                        font-weight: bold;
                        text-shadow: 2px 2px 5px black;
                        text-align: center;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown("""
    <h1 style='text-align: center; 
               color: #FFEA00;
               text-shadow: 3px 3px 5px rgba(255, 255, 0, 0.5);'>
               Activity Map
                </h1>
               """, unsafe_allow_html=True)

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown('<p class="title">📅 Most Busy Day</p>', unsafe_allow_html=True)
                    busy_day = activity_map.week_activity_map(selected_user, df)

                    fig = px.bar(
                        x=busy_day.index, 
                        y=busy_day.values, 
                        labels={'x': 'Day of Week', 'y': 'Message Count'},
                        title="",  # Removed title (Handled by HTML)
                        color_discrete_sequence=['purple']
                    )
                    fig.update_layout(height=350, width=350, template="plotly_white")
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    st.markdown('<p class="title">📆 Most Busy Month</p>', unsafe_allow_html=True)
                    busy_month = activity_map.month_activity_map(selected_user, df)

                    fig2 = px.bar(
                        x=busy_month.index, 
                        y=busy_month.values, 
                        labels={'x': 'Month', 'y': 'Message Count'},
                        title="",  # Removed title (Handled by HTML)
                        color_discrete_sequence=['orange']
                    )
                    fig2.update_layout(height=350, width=350, template="plotly_white")
                    st.plotly_chart(fig2, use_container_width=True)

                st.markdown("""
    <h1 style='text-align: center; 
               color: #FFEA00;
               text-shadow: 3px 3px 5px rgba(255, 255, 0, 0.5);'>
               Weekly Activity Map
                </h1>
               """, unsafe_allow_html=True)
                user_heatmap = activity_map.activity_heatmap(selected_user,df)
                fig,ax = plt.subplots()
                ax = sns.heatmap(user_heatmap)
                st.pyplot(fig)


        elif mode == "Word Cloud":

            st.markdown("""
    <h1 style='text-align: center; 
               color: #FFEA00;
               text-shadow: 3px 3px 5px rgba(255, 255, 0, 0.5);'>
               Word Cloud
                </h1>
               """, unsafe_allow_html=True)
            new_df = df[~df['message'].str.contains('media omitted', case=False, na=False)]
            new_df = new_df[new_df['message']!='null']
            user_list = new_df['user'].unique().tolist()
            user_list.sort()
            user_list.insert(0,"Overall")
            selected_user = st.selectbox("Show analysis wrt",user_list)
            if st.button("Show Analysis") or selected_user== 'Overall':


            
                df_wc = word_cloud.create_wordcloud(selected_user,new_df)
                fig,ax = plt.subplots()
                ax.imshow(df_wc)
                st.pyplot(fig)
            
                most_common_df = word_cloud.most_common_words(selected_user,new_df)

                fig,ax = plt.subplots()

                ax.barh(most_common_df[0],most_common_df[1])
                plt.xticks(rotation='vertical')

                st.markdown("""
        <h1 style='text-align: center; 
                color: #FFEA00;
                text-shadow: 3px 3px 5px rgba(255, 255, 0, 0.5);'>
                Most Common Words
                    </h1>
                """, unsafe_allow_html=True)
                st.pyplot(fig)

                st.markdown("""
        <h1 style='text-align: center; 
                color: #FFEA00;
                text-shadow: 3px 3px 5px rgba(255, 255, 0, 0.5);'>
                Emoji Analysis
                    </h1>
                """, unsafe_allow_html=True)

            emoji_df = word_cloud.emoji_helper(selected_user , new_df)


            col1,col2 = st.columns(2)

            with col1:
                st.dataframe(emoji_df)
            with col2:
                top_emojis = emoji_df.head(5)
                other_count = emoji_df['count'][5:].sum()

                labels = top_emojis['emoji'].tolist()
                sizes = top_emojis['count'].tolist()

                if other_count > 0:
                    labels.append("Others")
                    sizes.append(other_count)

                # Set emoji-supporting font
                import matplotlib.font_manager as fm
                emoji_font_path = "C:\\Windows\\Fonts\\seguiemj.ttf"
                emoji_font = fm.FontProperties(fname=emoji_font_path)
                plt.rcParams['font.family'] = emoji_font.get_name()

                fig, ax = plt.subplots(figsize=(6, 6))  # Slightly bigger
                wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.2f%%',
                                                startangle=90, textprops={'fontsize': 12})
                plt.setp(autotexts, size=10, weight='bold')
                ax.axis('equal')
                plt.title("Top Emojis", fontsize=14)                
                st.pyplot(fig)


        elif mode == "Detective Mode":
            if user_role == "investigator":

                st.markdown("""
### 🕵️‍♂️ Detective Mode Activated
This section detects and highlights users who frequently use abusive language in the group. It also shows sample messages and top bad words used by them.
""")

                
                st.markdown("""
                <h1 style='text-align: center; 
               color: #FFEA00;
               text-shadow: 3px 3px 5px rgba(255, 255, 0, 0.5);'>
               Top 5 abusive users
                </h1>
               """, unsafe_allow_html=True)
                new_df = df[~df['message'].str.contains('media omitted', case=False, na=False)]
                new_df = new_df[new_df['message']!='null']

                # Step 2: Optional smart filtering if dataset is large
                threshold = 5000  # you can change this based on your testing
                if len(new_df) > threshold:
                    st.info("🔍 Large dataset detected. Optimizing for performance...")

                    # 1. Remove duplicate messages
                    new_df = new_df.drop_duplicates(subset='message')

                    # 2. Remove very short messages
                    new_df = new_df[new_df['message'].str.split().str.len() > 5]

                    # 3. Focus on top 10 active users
                    top_users = new_df['user'].value_counts().head(10).index.tolist()
                    new_df = new_df[new_df['user'].isin(top_users)]

                    # 4. Sample 50% randomly
                    new_df = new_df.sample(frac=0.5, random_state=42)

                # Step 3: User selection
                user_list = new_df['user'].unique().tolist()
                user_list.sort()
                user_list.insert(0, "Overall")
                selected_user = st.selectbox("Show analysis wrt", user_list)

                # Step 4: Profanity Detection
                if st.button("Show Analysis") or selected_user == 'Overall':
                    from better_profanity import profanity

                    # Hindi + English abuses
                    abusive_words = ["motherfucker", "bitch", "bastard", "asshole", "hell", "fuck", "shit",
                        "chutiya", "bhosdike", "madarchod", "behenchod", "gandu", "launde", "randi", 
                        "loda", "lodu",  "bhenchod", "chod", "gaand", "gand" , "lund" , "randwe" ,"betichod" , "kute" , "mc" , "bc" ,"bkl" ,"chodu", "gaandfad" , "gaaaandfaaad", 'raand' , "chakke", 'tatti']
                    profanity.add_censor_words(abusive_words)

                    if selected_user != "Overall":
                        temp_df = new_df[new_df['user'] == selected_user]
                    else:
                        temp_df = new_df.copy()

                    temp_df['is_abusive'] = temp_df['message'].apply(lambda x: profanity.contains_profanity(str(x).lower()))
                    abusive_counts = temp_df[temp_df['is_abusive']].groupby('user')['message'].count().sort_values(ascending=False).head(5)

                    st.markdown("### 🔥 Top 5 Users Sending Abusive Messages")
                    st.bar_chart(abusive_counts)

                    # Expander for messages + top 3 abusive words
                    with st.expander("View abusive messages"):
                        for user in abusive_counts.index:
                            st.markdown(f"**{user}**")

                            user_msgs = temp_df[(temp_df['user'] == user) & (temp_df['is_abusive'])]['message'].tolist()

                            # Count abusive words
                            word_counts = Counter()
                            for msg in user_msgs:
                                words = re.findall(r'\b\w+\b', msg.lower())  # Extract words
                                abusive_in_msg = [word for word in words if word in abusive_words]
                                word_counts.update(abusive_in_msg)

                            top_abuses = word_counts.most_common(5)

                            st.markdown("🧨 **Top 5 abusive words used by user:**")
                            for word, count in top_abuses:
                                st.write(f"- {word} → {count} times")

                            st.markdown("💬 **Sample Abusive Messages:**")
                            for msg in user_msgs[:5]:
                                st.write(f"- {msg}")                
            else:
                st.warning("🚫 You do not have access to Detective Mode!")
                st.markdown("""
### 🕵️‍♂️ About Detective Mode
This section detects and highlights users who frequently use abusive language in the group. It also shows sample messages and top bad words used by them.
""")
                

                st.markdown("## 🔐 Request Access to Detective Mode")
                st.info("""
                This mode helps detect and visualize abusive content in chats. 
                Access is limited to trusted users for privacy and safety reasons.

                📩 **To request access**, please send an email to  
                **vinayakchhabra545.vc@gmail.com**  
                with the following details:
                - The email ID you used to sign up on **What'sInsight**
                - A short reason why you need access to this feature

                We’ll review your request and get back to you shortly.
                """)



# Login UI (If User Not Logged In)
else:
    st.markdown("""
    <h1 style='text-align: center;
            text-shadow: 3px 3px 5px rgba(138, 43, 226, 0.7);'>
            Welcome to <span style='color: violet;'>What's Insight 🤔</span>
    </h1>
    """, unsafe_allow_html=True)

    auth_option = st.radio("Select an option:", ["Login", "Sign Up"])

    if auth_option == "Login":
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            try:
                st.session_state.user = auth_manager.login(email, password)
                if st.session_state.user:
                    st.success("Login Successful! 🎉")
                    time.sleep(1)
                    st.rerun() 
                else:
                    st.error("Incorrect username or password. Please try again!")
            except Exception as e:
                st.error(f"An error occurred during login: {str(e)}")

    elif auth_option == "Sign Up":
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        if st.button("Signup"):
            try:
                signup_status = auth_manager.signup(email, password)

                if signup_status == 0:
                    st.error("Password too short! It must be at least 6 characters.")
                elif signup_status == 1:
                    st.warning("This email is already registered. Try logging in instead.")
                elif signup_status == 2:
                    st.success("Account created successfully! 🎉 Please login.")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Sign-up failed due to an unknown error. Please try again.")
            except Exception as e:
                st.error(f"An error occurred during signup: {str(e)}")

    



