# BeatRec v2 - Music Recommender Web App

A Material Design 3 Flask web application for personalized music recommendations.

## Quick Start

### Prerequisites
- Python 3.8+
- Pre-computed embeddings in `../embeddings/`

### Installation

```bash
cd app_v2
pip install -r requirements.txt
```

### Run the App

```bash
python main.py
```

Then open **http://localhost:5000** in your browser.

---

## App Flow (4 Steps)

### Welcome Page (`/`)
- **Description**: Explains the app's purpose
- **4-Step Stepper**: Visual journey through the process
- **Name Input**: User enters their name
- **Feature Cards**: Profile → Rate Songs → Preferences → Recommendations
- **M3 Progress Indicator**: Shows overall completion

### Step 1: Rate Songs (`/rate-songs`)
- **10 songs** presented one-by-one
- **Album artwork** from iTunes (600x600)
- **Material UI audio player**:
  - Play/Pause button
  - Seek slider (0:00 → 0:30)
  - 30-second preview limit
- **5-star rating** system
- **M3 Linear Progress**: Song-by-song progress
- **Navigation**: Previous/Next (must rate before continuing)
- **Dark mode** toggle

### Step 2: Preferences (`/preferences`)
- **Valence/Energy Grid**: Interactive XY pad for mood
- **Mainstream Slider**: Underground (1) ↔ Chart-Topper (10)
- **History Match**: Balance preferences vs. rating history
- **Genre Multi-select**: Choose favorite genres
- **Decade Dropdown**: Filter by era (1970s-2020s)

### Step 3: Recommendations (`/recommendations`)
- **5 personalized songs** with album art
- **Model Selector**:
  - **Hybrid**: Full model (embeddings + features + popularity)
  - **Content-Based**: Embedding similarity only
  - **Popularity-Weighted**: Collaborative-style
- **Match scores** for each recommendation
- **Audio previews** from iTunes
- **Export options** (save playlist)

---

## Architecture

```
app_v2/
├── main.py                      # Flask routes & API endpoints
├── data_loader.py               # Music data & embeddings loader
├── recommender.py               # Recommendation algorithms (3 models)
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── templates/
    ├── welcome.html             # Welcome page with 4-step stepper
    ├── page1_profile_material.html  # Song rating (M3 design)
    ├── page2_preferences.html   # Mood/genre preferences
    └── page3_recommendations.html  # Results with model selector
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Welcome page |
| `/rate-songs` | GET | Song rating page |
| `/preferences` | GET | Preferences page |
| `/recommendations` | GET | Results page |
| `/api/sample-songs` | GET | Get 10 songs for rating |
| `/api/genres` | GET | Get available genres |
| `/api/decades` | GET | Get available decades |
| `/api/embedding-models` | GET | Get embedding models |
| `/api/recommend` | POST | Get recommendations |

---

## Features

### Material Design 3
- **M3 Color System**: Primary (`#1DB954`), Error (`#ef5350`)
- **M3 Components**: Stepper, Linear Progress, Cards, Buttons
- **M3 Typography**: Roboto font family
- **M3 Icons**: Inline SVG icons (no font dependencies)

### User Experience
- **Dark Mode**: Persistent theme toggle
- **Responsive**: Viewport-scaled design (`min(400px, 95vw)`)
- **Progress Tracking**: Visual feedback at each step
- **Toast Notifications**: Success/error snackbars
- **LocalStorage**: Saves progress across sessions

### Music Features
- **iTunes Integration**: 30-second previews + album artwork
- **Multi-Model AI**: 9 embedding models available
- **Audio Features**: Valence, Energy, Tempo, Popularity
- **Constraint Filtering**: Genre, decade, mainstream level
- **Hybrid Scoring**: Combines multiple signals

---

## Technology Stack

- **Backend**: Flask (Python)
- **ML**: scikit-learn, sentence-transformers
- **Frontend**: Vanilla JS + Material Design 3 CSS
- **Data**: Spotify Songs dataset (5000 tracks)
- **Embeddings**: all-MiniLM-L6-v2 (384 dimensions)

---

## User Journey

```
┌─────────────┐
│   Welcome   │ Enter name
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Rate Songs  │ 10 songs × 1-5 stars
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Preferences │ Mood, genre, decade
└──────┬──────┘
       │
       ▼
┌─────────────┐
│Recommendations│ 5-song playlist
└─────────────┘
```

---

## Screenshots

### Welcome Page
- 4-step vertical stepper
- Feature grid (2×2)
- Name input with M3 TextField
- M3 Linear Progress indicator

### Rating Page
- Full-width album artwork
- Material FAB play button
- Star rating with animations
- M3 progress bar

---

## Development

### Add New Embedding Models
```python
# In data_loader.py, add to EMBEDDING_MODELS dict
"your-model-name": "sentence-transformers/model-path"
```

### Customize Genres
```python
# In recommender.py, modify GENRE_ALIASES dict
```

### Change Color Theme
```css
/* In templates, update CSS variables */
--mui-primary-main: #1DB954;  /* Spotify green */
```
