from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)


def fetch_interesting_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Most used word (Ignoring media messages)
    words = []
    for message in df['message']:
        if message != "<Media omitted>":
            words.extend(message.split())

    most_common_word = Counter(words).most_common(1)[0][0] if words else "None"

    # Longest message length (Ignoring media messages)
    longest_message_length = max((len(msg.split()) for msg in df['message'] if msg != "<Media omitted>"), default=0)

    # Most used emoji
    all_emojis = []
    for message in df['message']:
        all_emojis.extend([char for char in message if char in emoji.EMOJI_DATA])

    most_used_emoji = Counter(all_emojis).most_common(1)[0][0] if all_emojis else "None"

    # Categorizing active time slots
    df['hour'] = df['date'].dt.hour
    time_slots = {
        "Morning": df[(df['hour'] >= 5) & (df['hour'] < 11)].shape[0],
        "Afternoon": df[(df['hour'] >= 11) & (df['hour'] < 17)].shape[0],
        "Evening": df[(df['hour'] >= 17) & (df['hour'] < 24)].shape[0],
        "Late Night": df[(df['hour'] >= 0) & (df['hour'] < 5)].shape[0]
    }

    most_active_period = max(time_slots, key=time_slots.get) if time_slots else "Unknown"

    return most_common_word, longest_message_length, most_used_emoji, most_active_period

import numpy as np

def fetch_math_stats(df):
    # Avg. Messages per Day
    df['date_only'] = df['date'].dt.date  # Extract only date part
    messages_per_day = df.groupby('date_only').size()
    avg_messages_per_day = round(messages_per_day.mean(), 2)

    # Avg. Message Length (in words)
    message_lengths = df['message'].apply(lambda x: len(x.split()))
    avg_message_length = round(message_lengths.mean(), 2)

    # Pareto Rule Validity (Checking if top 20% users send 80% messages)
    user_message_counts = df['user'].value_counts()
    top_20_percent_users = int(0.2 * len(user_message_counts)) or 1  # At least 1 user
    top_20_percent_messages = user_message_counts.iloc[:top_20_percent_users].sum()
    total_messages = len(df)
    pareto_valid = "Yes" if (top_20_percent_messages / total_messages) >= 0.7 else "No"

    # Media-to-Message Ratio
    num_media_messages = df[df['message'] == '<Media omitted>'].shape[0]
    media_message_ratio = f"1 in {round(total_messages / num_media_messages, 1)} msgs" if num_media_messages else "No media"

    return avg_messages_per_day, avg_message_length, pareto_valid, media_message_ratio

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x,df

def create_wordcloud(selected_user,df):

    f = open('Hinglish_stop_words.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):

    f = open('Hinglish_stop_words.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap















