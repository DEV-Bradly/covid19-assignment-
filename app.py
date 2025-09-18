#app.py

import streamlit as st
import pandas as pd
import os

st.title("CORD-19 Data Explorer")

file_path = "data/metadata_sample.csv"

if not os.path.exists(file_path):
    st.error("⚠️ Dataset file not found! Please make sure `metadata_sample.csv` is uploaded in the `data/` folder of your GitHub repo.")
else:
    df = pd.read_csv(file_path)
    st.write("Sample of the dataset:", df.head())


# Load dataset
df = pd.read_csv("data/metadata_sample.csv")

# Convert publish_time to datetime
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
df['year'] = df['publish_time'].dt.year

# Drop rows without title/abstract
df = df.dropna(subset=['title', 'abstract'])

# Abstract word count
df['abstract_word_count'] = df['abstract'].apply(lambda x: len(str(x).split()))

# --- Streamlit App ---
st.title("CORD-19 Data Explorer")
st.write("Simple exploration of COVID-19 research papers")

# Filter by year
year_range = st.slider("Select year range:",
                       int(df['year'].min()),
                       int(df['year'].max()),
                       (2020, 2021))

filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

# Show sample
st.subheader("Sample Data")
st.dataframe(filtered[['title', 'authors', 'journal', 'year']].head(10))

# Publications by year
st.subheader("Publications by Year")
year_counts = filtered['year'].value_counts().sort_index()
fig, ax = plt.subplots()
ax.bar(year_counts.index, year_counts.values)
ax.set_xlabel("Year")
ax.set_ylabel("Count")
st.pyplot(fig)

# Top journals
st.subheader("Top Journals")
top_journals = filtered['journal'].value_counts().head(10)
fig, ax = plt.subplots()
top_journals.plot(kind="bar", ax=ax)
ax.set_ylabel("Count")
st.pyplot(fig)

