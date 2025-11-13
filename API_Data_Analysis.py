import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
import numpy as np
from collections import Counter
from wordcloud import WordCloud
import nltk
nltk.download('punkt_tab')

all_years = []
for year in range(1958, 2025):
    file_path = f"billboard_top10_{year}.csv"
    df = pd.read_csv(file_path)
    df['year'] = year
    all_years.append(df)

combined_df = pd.concat(all_years).reset_index(drop=True)
combined_df.to_csv("billboard_top10_all_years.csv", index=False)
subgenres_df = pd.read_csv("sub genres.csv", header=0)


subgenres_df.columns = subgenres_df.columns.str.lower().str.strip()
subgenres_df = subgenres_df.apply(lambda x: x.str.lower().str.strip())

# Build genre mapping dictionary
subgenre_to_main = {}
for main_genre in subgenres_df.columns:
    subgenres = subgenres_df[main_genre].dropna()
    for sub in subgenres:
        subgenre_to_main[sub] = main_genre

# Apply mapping to combined data (with fallback for unknown genres)
combined_df['main_genre'] = (
    combined_df['genre']
    .str.lower()
    .str.strip()
    .map(subgenre_to_main)
    .fillna('other')  # Handle unmapped genres
)

def get_sentiment(text):
    if pd.isna(text) or text.strip() == "":
        return 0
    return TextBlob(text).sentiment.polarity

def generate_wordcloud(text, title):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(title)
    plt.axis('off')
    plt.savefig(f'wordcloud_{start_year}_{end_year}.png')
    plt.close()

# Create word clouds for different decades
for decade in [1960, 1970, 1980, 1990, 2000, 2010, 2020]:
    start_year = decade
    end_year = decade + 9
    if end_year > 2024:
        end_year = 2024
    decade_text = ' '.join(combined_df[(combined_df['year'] >= start_year) &
                                     (combined_df['year'] <= end_year)]['lyrics'].dropna())
    generate_wordcloud(decade_text, f'Most Common Words in Billboard Top 10 ({start_year}-{end_year})')




# Calculate sentiment for each song
combined_df['sentiment'] = combined_df['lyrics'].apply(get_sentiment)
yearly_sentiment = combined_df.groupby('year')['sentiment'].mean().reset_index()

# Plot sentiment over time line graph
plt.figure(figsize=(14, 7))
sns.lineplot(data=yearly_sentiment, x='year', y='sentiment')
sns.regplot(
    data=yearly_sentiment,
    x='year',
    y='sentiment',
    scatter=False,
    color='red',
    label='Trend Line'
)
plt.title('Average Song lyric Sentiment Over Time scraped from billboard charts (1958-2024)')
plt.xlabel('Year')
plt.ylabel('Sentiment Polarity (-1 to 1)')
plt.grid(True)
plt.savefig('sentiment_over_time.png')
plt.close()

# Plot Sentiment Distribution by Genre box plot
combined_df = combined_df[combined_df['main_genre'] != 'other']
plt.figure(figsize=(12, 6))
sns.boxplot(data=combined_df, x='main_genre', y='sentiment')
plt.title('Sentiment Distribution by Genre')
plt.xlabel('Main Genre')
plt.ylabel('Sentiment')
plt.savefig('sentiment_by_genre_boxplot.png')
plt.close()

avg_sentiment_by_genre = combined_df.groupby('main_genre')['sentiment'].mean().sort_values(ascending=False)

# Print the average sentiment for each genre
print("Average Sentiment by Genre:")
print(avg_sentiment_by_genre.to_string())


# Plot Average Weeks on Chart by Genre bar graph
avg_weeks_by_genre = combined_df.groupby('main_genre')['weeks_on_chart'].mean().reset_index()
'''
plt.figure(figsize=(12, 6))
sns.barplot(data=avg_weeks_by_genre, x='main_genre', y='weeks_on_chart', palette='viridis')
plt.title('Average Weeks on Chart by Genre')
plt.xlabel('Main Genre')
plt.ylabel('Average Weeks on Chart')
plt.savefig('avg_weeks_by_genre.png')
plt.show()
'''

include_genres = ['pop', 'hip hop', 'blues', 'country', 'rock', 'r&b', 'folk']
top_genres_filtered = (
    combined_df[combined_df['main_genre'].isin(include_genres)]
    .groupby(['year', 'main_genre'])
    .size()
    .reset_index(name='count')
)


#plot genres in billboard over time
plt.figure(figsize=(14, 7))
sns.lineplot(
    data=top_genres_filtered,
    x='year',
    y='count',
    hue='main_genre',
    palette='tab10',
    linewidth=2.5
)
plt.title('Genre occurance in billboard overtime', fontsize=14, pad=20)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Number of Songs', fontsize=12)
plt.legend(title='Genre')
plt.grid(True)
plt.savefig('Genre occurance in billboard overtime.png', bbox_inches='tight', dpi=300)
plt.close()



# Plot line graph of subgenre counts over time
subgenre_diversity = combined_df.groupby('year')['genre'].nunique().reset_index(name='num_subgenres')
plt.figure(figsize=(14, 7))
sns.lineplot(data=subgenre_diversity, x='year', y='num_subgenres', marker='o', linewidth=2)
plt.title('Number of Unique Subgenres in Billboard Top 10 Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Subgenres')
plt.savefig('subgenre_diversity_over_time.png')
plt.close()


# sorry for the language this is just for data
profanity_words = {
    'fuck', 'fucking', 'fucked', 'shit', 'shitting', 'bitch', 'bitches',
    'ass', 'asses', 'hell', 'crap', 'dick', 'piss', 'cock',
    'pussy', 'whore', 'slut', 'bastard', 'motherfucker', 'motherfucking','nigga'
}

def count_profanity(text):
    if pd.isna(text) or text.strip() == "":
        return 0
    words = TextBlob(text).words
    return sum(1 for word in words if word.lower() in profanity_words)

# Calculate profanity counts
combined_df['profanity_count'] = combined_df['lyrics'].apply(count_profanity)
combined_df['has_profanity'] = combined_df['profanity_count'] > 0

# Calculate yearly profanity metrics
yearly_profanity = combined_df.groupby('year').agg(
    songs_with_profanity=('has_profanity', 'sum'),
    total_songs=('year', 'count')
).reset_index()

yearly_profanity['pct_songs_with_profanity'] = (yearly_profanity['songs_with_profanity'] / yearly_profanity['total_songs']) * 100

# Plot only the percentage of songs with profanity
plt.figure(figsize=(14, 6))
plt.plot(yearly_profanity['year'], yearly_profanity['pct_songs_with_profanity'],
         label='% of Songs with Profanity', color='red', linewidth=2)
sns.regplot(x='year', y='pct_songs_with_profanity', data=yearly_profanity,
            scatter=False, color='blue', label='Trend Line', ci=None)
plt.title('Percentage of Billboard Top 10 Songs Containing Profanity (1958-2024)', fontsize=14)
plt.xlabel('Year')
plt.ylabel('Percentage of Songs')
plt.legend()
plt.grid(True)
plt.show()