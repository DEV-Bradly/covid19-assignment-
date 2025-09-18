# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/metadata_sample.csv")
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
df['year'] = df['publish_time'].dt.year

st.title("CORD-19 Data Explorer")
st.write("A beginner-friendly app to explore COVID-19 research metadata.")

# Year range filter
years = df['year'].dropna().unique()
min_year, max_year = int(min(years)), int(max(years))
year_range = st.slider("Select year range:", min_year, max_year, (min_year, max_year))

filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

# Show sample
st.subheader("Sample Data")
st.write(filtered.head())

# Publications by year
st.subheader("Publications by Year")
year_counts = filtered['year'].value_counts().sort_index()
fig, ax = plt.subplots()
ax.bar(year_counts.index, year_counts.values)
ax.set_xlabel("Year")
ax.set_ylabel("Number of Papers")
st.pyplot(fig)

# Top Journals
st.subheader("Top Journals")
top_journals = filtered['journal'].value_counts().head(5)
fig, ax = plt.subplots()
ax.barh(top_journals.index, top_journals.values)
ax.set_xlabel("Number of Papers")
st.pyplot(fig)
