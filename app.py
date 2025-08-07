import streamlit as st
import pandas as pd
import json
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime

# Load processed data
DATA_PATH = "data/processed_data.json"

@st.cache_data
def load_data(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df.dropna(subset=['date'], inplace=True)
    return df

df = load_data(DATA_PATH)

# Page config
st.set_page_config(page_title="Civic Narrative Monitoring", layout="wide")
st.title("🛰️ Civic Narrative Monitoring Dashboard")
st.markdown("Track civic discourse, toxicity, and sentiment trends across platforms.")

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filters")
    platforms = st.multiselect("Platform", df['platform'].unique(), default=df['platform'].unique())
    sentiment = st.multiselect("Sentiment", df['sentiment'].apply(lambda x: x['label']).unique())
    toxicity = st.multiselect("Toxicity", df['toxicity'].apply(lambda x: x['label']).unique())
    keyword = st.text_input("Keyword search")
    date_range = st.date_input("Date Range", [])

# Apply filters
filtered = df[df['platform'].isin(platforms)]

if sentiment:
    filtered = filtered[filtered['sentiment'].apply(lambda x: x['label'] in sentiment)]
if toxicity:
    filtered = filtered[filtered['toxicity'].apply(lambda x: x['label'] in toxicity)]
if keyword:
    filtered = filtered[filtered['content'].str.contains(keyword, case=False, na=False)]
if len(date_range) == 2:
    filtered = filtered[(filtered['date'] >= pd.to_datetime(date_range[0])) & (filtered['date'] <= pd.to_datetime(date_range[1]))]

# Line Chart: Volume over Time
st.subheader("📈 Volume Over Time")
trend = filtered.groupby(filtered['date'].dt.date).size().reset_index(name="count")
fig_trend = px.line(trend, x='date', y='count', title='Posts Over Time')
st.plotly_chart(fig_trend, use_container_width=True)

# Pie Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("🧭 Sentiment Distribution")
    sentiment_counts = filtered['sentiment'].apply(lambda x: x['label']).value_counts()
    fig_sentiment = px.pie(names=sentiment_counts.index, values=sentiment_counts.values)
    st.plotly_chart(fig_sentiment, use_container_width=True)

with col2:
    st.subheader("☣️ Toxicity Distribution")
    toxicity_counts = filtered['toxicity'].apply(lambda x: x['label']).value_counts()
    fig_toxicity = px.pie(names=toxicity_counts.index, values=toxicity_counts.values)
    st.plotly_chart(fig_toxicity, use_container_width=True)

# WordCloud of Named Entities
st.subheader("🧠 Named Entity Word Cloud")
entities = sum(filtered['entities'], [])
if entities:
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(" ".join(entities))
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot(plt)
else:
    st.write("No named entities found in filtered data.")

# Data Table
st.subheader("📄 Annotated Data Table")
st.dataframe(filtered[['date', 'platform', 'content', 'sentiment', 'toxicity', 'entities']])
