# Billboard Charts Sentiment Analysis

### Tracking the evolution of popular music through lyric sentiment and audio features over time

---

## Overview

This project analyzes how Billboard Hot 100 charts have evolved by examining lyric sentiment, audio characteristics, and musical trends across decades. By integrating data from Spotify, Genius, Last.FM, and Kaggle databases, we uncover patterns in popular music that reflect cultural shifts, emotional trends, and changing listener preferences over time.

## Features

### Lyric Sentiment Analysis
Natural language processing of song lyrics to track emotional trends in chart-topping music

### Audio Feature Tracking
Analysis of musical characteristics like tempo, energy, valence, and danceability across eras

### Temporal Trend Visualization
Interactive charts and word clouds showing how music has changed decade by decade

### Multi-Source Data Integration
Combines Spotify audio features, Genius lyrics, Last.FM metadata, and Billboard chart positions with real time APIs

---

## Project Structure

```
Billboard-Charts-Sentiment-Analysis-2024/
├── API_Data_Analysis.py            # Core analysis and sentiment processing
├── API_Data_Reader.py              # API integration for data collection
├── Billboard_Analysis_Paper.pdf    # Complete research paper and findings
├── Visualizations.pdf              # Charts and graphs of temporal trends
├── wordclouds.gif                  # Animated word clouds across decades
├── hot-100-current.csv             # Billboard Hot 100 chart data
├── sub genres.csv                  # Genre classification data
└── README.md                       # Project documentation
```

---

## Getting Started

```bash
git clone https://github.com/Kaiking28/Billboard-Charts-Sentiment-Analysis-2024.git
cd Billboard-Charts-Sentiment-Analysis-2024
python API_Data_Reader.py  # Collect data from APIs
python API_Data_Analysis.py  # Run sentiment analysis
```

## Research Outputs

View the complete analysis in `Billboard_Analysis_Paper.pdf` and explore visualizations in `Visualizations.pdf`. The animated `wordclouds.gif` shows the most common lyrical themes across different time periods. This research reveals how sentiment in popular music has shifted over time, tracks the rise and fall of different genres, identifies patterns in lyrical themes, and correlates musical characteristics with chart performance.

