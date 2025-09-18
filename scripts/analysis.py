# scripts/analysis.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# -----------------------
# Part 1: Load & Explore
# -----------------------
df = pd.read_csv("data/metadata_sample.csv")

print("Data shape:", df.shape)
print("\nColumn info:")
print(df.info())
print("\nMissing values per column:")
print(df.isnull().sum())

# -----------------------
# Part 2: Cleaning
# -----------------------
# Convert publish_time to datetime
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')

# Extract year
df['year'] = df['publish_time'].dt.year

# Word count in abstract
df['abstract_word_count'] = df['abstract'].fillna("").apply(lambda x: len(x.split()))

# -----------------------
# Part 3: Analysis
# -----------------------

# Papers by year
year_counts = df['year'].value_counts().sort_index()
print("\nPublications per year:\n", year_counts)

plt.figure(figsize=(6,4))
sns.barplot(x=year_counts.index, y=year_counts.values)
plt.title("Publications by Year")
plt.xlabel("Year")
plt.ylabel("Number of Papers")
plt.tight_layout()
plt.savefig("results/papers_per_year.png")
plt.close()

# Top journals
top_journals = df['journal'].value_counts().head(5)
print("\nTop Journals:\n", top_journals)

plt.figure(figsize=(6,4))
sns.barplot(y=top_journals.index, x=top_journals.values)
plt.title("Top Journals")
plt.xlabel("Number of Papers")
plt.tight_layout()
plt.savefig("results/top_journals.png")
plt.close()

# Word cloud of titles
titles = " ".join(df['title'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(titles)

plt.figure(figsize=(8,4))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Word Cloud of Titles")
plt.tight_layout()
plt.savefig("results/wordcloud_titles.png")
plt.close()

# Papers by source
source_counts = df['source_x'].value_counts()
plt.figure(figsize=(6,4))
sns.barplot(y=source_counts.index, x=source_counts.values)
plt.title("Papers by Source")
plt.xlabel("Number of Papers")
plt.tight_layout()
plt.savefig("results/papers_by_source.png")
plt.close()

print("\nAnalysis completed. Results saved in 'results/' folder.")
