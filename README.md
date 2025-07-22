# 📊 Whats Insight – WhatsApp Chat Analyzer

A full-stack analytics app built using Python and Streamlit to extract deep insights from exported WhatsApp group chats. From basic stats to advanced sentiment and abuse detection, Whats Insight helps you understand group activity patterns in a few clicks.

## 🔍 Features

- 📈 **Group Statistics**: Total messages, word count, media shared, links, etc.
- 🗓️ **Activity Timeline**: Monthly and daily trends of group activity.
- 🔥 **User Heatmaps**: Visualize user activity by time and day.
- 👤 **Most Active Users**: Rank participants by their contribution.
- ☁️ **Word Cloud**: Highlight frequently used words in the chat.
- 😀 **Sentiment Analysis**: Detect positive, negative, or neutral tone using NLP.
- 🕵️ **Detective Module**: 
  - Detect abusive, threatening, and vulgar messages.
  - Custom classifier for identifying toxic Hinglish text.
- 🇮🇳 **Hinglish Handling**: 
  - Supports Hinglish chat files.
  - Removes Hinglish stopwords and normalizes informal spelling for NLP tasks.

## 💻 Tech Stack

- **Frontend**: Streamlit
- **Backend & Logic**: Python, Pandas, Regex
- **Data Visualization**: Plotly, WordCloud
- **NLP & Classification**: NLTK, TextBlob, Scikit-learn

## How to Run This Project

If you want to run this project locally, follow these steps:

1. **Clone the repository**
2. **Install the required libraries**
3. **Run the project**

Use Streamlit to run the app:
streamlit run app.py

