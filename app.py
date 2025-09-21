#streamlit app
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Load data
@st.cache
def load_data():
    df = pd.read_csv('ncr_ride_bookings.csv')
    df = df.dropna(subset=['title', 'publish_time'])
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['year'] = df['publish_time'].dt.year
    return df

df = load_data()

# Layout
st.title("Uber Data Analytics Explorer")
st.write("Explore ride booking data from the Uber Data Analytics dataset.")

# Year filter
year_range = st.slider("Select Year Range", int(df['year'].min()), int(df['year'].max()), (2020, 2021))
df_filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

# Show sample data
if st.checkbox("Show Sample Data"):
    st.write(df_filtered[['title', 'journal', 'publish_time']].head())

# Bookings per year
year_counts = df_filtered['year'].value_counts().sort_index()
st.subheader("Bookings by Year")
st.bar_chart(year_counts)

# Top journals (if journal column exists)
st.subheader("Top Journals")
if 'journal' in df_filtered.columns:
    top_journals = df_filtered['journal'].value_counts().head(10)
    st.bar_chart(top_journals)
else:
    st.write("No 'journal' column in dataset.")

# Word cloud
st.subheader("Word Cloud of Titles")
titles = ' '.join(df_filtered['title'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(titles)
st.image(wordcloud.to_array())