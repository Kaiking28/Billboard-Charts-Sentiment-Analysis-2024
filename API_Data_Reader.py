
import pandas as pd
import time
import lyricsgenius
import os
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import re
from typing import List, Optional

# Define file paths
BILLBOARD_FILE = 'hot-100-current.csv'
GENIUS_API_TOKEN = "c7cFWlvgeKoSep6rAxM6b3df8ptVlNhTHQHDiV_ASTBHm6KG4gNXw4j7cCQZSxLF"
SPOTIFY_CLIENT_ID = "cc518de4edf54b36be2a35a0f4ab738b"
SPOTIFY_CLIENT_SECRET = "fe3ceec7f1bb49a8a021d255561dca7c"

# Initialize APIs
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))
genius = lyricsgenius.Genius(GENIUS_API_TOKEN)
genius.remove_section_headers = True
genius.verbose = False  # Reduce verbose output


def get_spotify_genre(artist_name: str) -> List[str]:
    """Get genres for an artist from Spotify."""
    try:
        results = sp.search(q=f'artist:{artist_name}', type='artist', limit=1)
        if results['artists']['items']:
            return results['artists']['items'][0]['genres']
        return []
    except Exception as e:
        print(f"Error getting genre for {artist_name}: {str(e)}")
        return []


def load_billboard_data_year(year: int) -> pd.DataFrame:
    """Load and filter Billboard data for a specific year."""
    df = pd.read_csv(BILLBOARD_FILE)
    df['chart_week'] = pd.to_datetime(df['chart_week'])
    df['year'] = df['chart_week'].dt.year
    df = df[(df['year'] == year) & (df['current_week'] <= 10)]

    # Get unique songs with their chart performance
    song_stats = df.groupby(['performer', 'title']).agg(
        max_week=('current_week', 'max'),
        weeks_on_chart=('wks_on_chart', 'max'),
        first_chart_date=('chart_week', 'min')
    ).reset_index()
    return song_stats


def clean_lyrics(lyrics: str) -> str:
    """Clean lyrics by removing metadata and empty lines."""
    if not lyrics:
        return ""
    # Remove section headers like [Verse], [Chorus], etc.
    lyrics = re.sub(r'\[.*?\]', '', lyrics)
    # Remove empty lines
    lyrics = os.linesep.join([s for s in lyrics.splitlines() if s.strip()])
    return lyrics.strip()


def get_data_for_year(year: int, max_songs: Optional[int] = None) -> pd.DataFrame:
    """Get lyrics and genre data for Billboard songs in a given year."""
    songs_df = load_billboard_data_year(year)

    if max_songs:
        songs_df = songs_df.head(max_songs)

    lyrics_data = []
    genres_data = []

    for i, row in songs_df.iterrows():
        artist = row['performer']
        separators = ["&", ",", "Featuring", "feat.", "ft.", "with", "x", "X"]
        primary_artist = artist
        for sep in separators:
            primary_artist = primary_artist.split(sep)[0].strip()
        title = row['title']
        print(f'loading now {title}')
        lyrics = ""
        genres = []

        try:
            # Get lyrics
            song = genius.search_song(title, primary_artist)
            cleaned_lyrics = clean_lyrics(song.lyrics)
            lines = cleaned_lyrics.splitlines(True)
            lyrics = "".join(lines[1:]) if len(lines) > 1 else cleaned_lyrics
            print(lyrics[:20])

            # Get genre
            genres = get_spotify_genre(primary_artist)

            # Sleep to avoid rate limiting
            time.sleep(1)
        except Exception as e:
            print(f"Error processing {title} by {artist}: {str(e)}")

        lyrics_data.append(lyrics)
        genres_data.append(genres[0] if genres else "")
    songs_df['lyrics'] = lyrics_data
    songs_df['genre'] = genres_data
    return songs_df
if __name__ == "__main__":
    for year in range(1958, 2025):
        print(f"\n\n\n\n=== {year} ===")
        lyrics_df = get_data_for_year(year)
        print(f"\n=== done ===")
        print(lyrics_df[['performer', 'title', 'genre']])
        output_filename = f"billboard_top10_{year}.csv"
        lyrics_df.to_csv(output_filename, index=False)
        print(f"Data saved to {output_filename}")
