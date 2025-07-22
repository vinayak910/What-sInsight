import streamlit as st
from collections import Counter
import os
import re
import time
from datetime import datetime

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

# Page Config
st.set_page_config(page_title="What's Insight 🤔", page_icon="🤔")

# Initialize objects
chat_stats = ChatStatistics()
timeline_analysis = TimelineAnalysis()
activity_map = ActivityMap()
preprocess = Preprocessor()

# Title
st.markdown("""
<h1 style='text-align: center;text-shadow: 3px 3px 5px rgba(138, 43, 226, 0.7);'>
Welcome to <span style='color: violet;'>What's Insight 🤔</span>
</h1>
""", unsafe_allow_html=True)

# Upload chat file
st.subheader("📂 Upload your WhatsApp chat file (txt only)")
uploaded_file = st.file_uploader("Choose a file", type=["txt"])

if uploaded_file is not None:
    file_contents = uploaded_file.read().decode("utf-8")
    df = preprocess.preprocess(file_contents)

    # Sidebar
    st.sidebar.title("What'sInsight 🤔")
    st.sidebar.image("D:/Projects/SE-Project/What'sInsight/magnifying-glass.png", width=100)
    mode = st.sidebar.radio("Choose an option", ["Chat Statistics", "Timeline Analysis", "Activity Map", "Word Cloud", "Detective Mode"])

    st.markdown(f"""<h1 style='text-align: center;text-shadow: 3px 3px 5px rgba(255, 255, 0, 0.5);'>
        <span style='color: #FFEA00;'> Chat</span> 
        <span style='color: #FFAB40;'>Analysis</span> 
        <span style='color: #00E5FF;'>Playground</span>
        </h1>""" , unsafe_allow_html=True)
    
    st.write(f"🧠 Analysis started for mode: **{mode}**")
       

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


                st.markdown("""
### 🕵️‍♂️ Detective Mode Activated
This section detects and highlights users who frequently use abusive language in the group. It also shows sample messages and top bad words used by them.
""")

                
                st.markdown("""
                <h1 style='text-align: center; 
               color: #FFEA00;
               text-shadow: 3px 3px 5px rgba(255, 255, 0, 0.5);'>
               Top 1-5 abusive users
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
                    from collections import Counter
                    import re

                    # Hindi + English abuses
                    abusive_words = ["motherfucker", "bitch", "bastard", "asshole", "hell", "fuck", "shit", "harami", "suar", "suaro",
                                    "chutiya", "bhosdike", "madarchod", "behenchod", "gandu", "launde", "randi", "loda", "lodu",
                                    "bhenchod", "chod", "gaand", "gand", "lund", "randwe", "betichod", "kute", "mc", "bc", "bkl",
                                    "chodu", "gaandfad", "gaaaandfaaad", "raand", "chakke", "tatti" , "nigga", "nigger", "dumbass", "prick", "retard", "jerk", "douche", "piss", "slut", "whore" , "motherfuckers",
                                    "fuck", "shit", "bitch", "asshole", "nigga", "nigger", 
                                    "dumbass", "prick", "retard", "jerk", "douche", "slut", "whore", "cock", "dick",
                                    "pussy", "balls", "bollocks", "cunt", "screw", "damn", "piss", "crap", "hoe", 
                                    "twat", "wanker", "arse", "bugger", "bollock", "shithead", "fucker", "slutty", 
                                    "scumbag", "dipshit", "twatwaffle", "skank", "slag", "moron", "idiot", 'fuckers' , "motherfuckers" , "niggas" , "chutad" , "randiya", "suck", "stupid",
                                    "motherfucker", "motherfuckers", "fucker", "fuckers", "fucking", "fuck", "fucks",
                                    "bitch", "bitches", "bitchy",
                                    "bastard", "bastards",
                                    "asshole", "assholes", "asshat", "asshats",
                                    "hell", "damn", "damned",
                                    "shit", "shits", "shitty", "shithead",
                                    "harami", "haramis",
                                    "suar", "suaro", "suaron", "kutte", "kuttey", "kutta", "kutiya", "kuttiya",
                                    "chutiya", "chutiyon", "chutiyapa",
                                    "bhosdike", "bhosdika","bhosdiwala" , "bhosdiwali" ,
                                    "madarchod", "madarchodon", "mc",
                                    "behenchod", "bhenchod", "bc",
                                    "gandu", "gandus", "gandugiri",
                                    "launde", "launda", "laundey",
                                    "randi", "randis", "randiya", "raand", "raandiyan",
                                    "loda", "lodu", "lund", "lunds",
                                    "chod", "chodon", "chodu", "chudai", "chutad",
                                    "gaand", "gand", "gaandfad", "gaandfadi", "gaandfattu", "gaandfat",
                                    "randwe", "betichod",
                                    "chakke", "chakka", "chakkas",
                                    "tatti", "tatty", "tattiyan",
                                    "nigga", "niggas",
                                    "nigger", "niggers",
                                    "dumbass", "dumbasses", "dumb",
                                    "prick", "pricks",
                                    "retard", "retards", "retarded",
                                    "jerk", "jerks",
                                    "douche", "douches", "douchebag", "douchebags",
                                    "piss", "pissy",
                                    "slut", "sluts", "slutty",
                                    "whore", "whores", "whorish",
                                    "cock", "cocks", "cocky",
                                    "dick", "dicks", "dickhead", "dickheads",
                                    "pussy", "pussies",
                                    "balls", "ballsy",
                                    "bollocks", "bollock",
                                    "cunt", "cunts",
                                    "screw", "screwed", "screwing",
                                    "crap", "crappy",
                                    "hoe", "hoes",
                                    "twat", "twats", "twatwaffle",
                                    "wanker", "wankers",
                                    "arse", "arses", "arsehole", "arseholes",
                                    "bugger", "buggers",
                                    "shithead", "shitheads",
                                    "fucker", "fuckers",
                                    "scumbag", "scumbags",
                                    "dipshit", "dipshits",
                                    "skank", "skanks",
                                    "slag", "slags",    
                                    "moron", "morons",
                                    "idiot", "idiots", "idiotic",
                                    "suck", "sucks", "sucking",
                                    "stupid" , "mc" , "bc" , "mkl" , "bkl" , "gandfad" ,"gandfati", "fuddu" , "bund" , "mayova" , "mayo"
                                    "fuckboy " ,"rape" , "rapis"
                                ]



                    profanity.add_censor_words(abusive_words)

                    # Filter based on user
                    if selected_user != "Overall":
                        temp_df = new_df[new_df['user'] == selected_user]
                    else:
                        temp_df = new_df.copy()

                    # Detect abusive messages
                    temp_df['is_abusive'] = temp_df['message'].apply(lambda x: profanity.contains_profanity(str(x).lower()))
                    
                    # Count abusive messages by user
                    abusive_counts = temp_df[temp_df['is_abusive']].groupby('user')['message'].count().sort_values(ascending=False).head(5)

                    st.markdown("###  Abusive word counts of top 1-5 users")
                    st.bar_chart(abusive_counts)

                    # Show detailed analysis in expander
                    with st.expander("View abusive messages"):
                        for user in abusive_counts.index:
                            st.markdown(f"### 👤 {user}")

                            user_msgs = temp_df[(temp_df['user'] == user) & (temp_df['is_abusive'])]['message'].tolist()

                            # Count abusive words
                            word_counts = Counter()
                            for msg in user_msgs:
                                words = re.findall(r'\b\w+\b', msg.lower())  # Extract individual words
                                abusive_in_msg = [word for word in words if word in abusive_words]
                                word_counts.update(abusive_in_msg)

                            top_abuses = word_counts.most_common(5)

                            st.markdown("🧨 **Top 1-5 abusive words used by user:**")
                            if top_abuses:
                                for word, count in top_abuses:
                                    st.write(f"- {word} → {count} times")
                            else:
                                st.write("No abusive words found for this user.")

                            st.markdown("💬 **Sample Abusive Messages:**")
                            if user_msgs:
                                for msg in user_msgs[:5]:
                                    st.write(f"- {msg}")
                            else:
                                st.write("No abusive messages available for this user.")

                            st.markdown("---")  






