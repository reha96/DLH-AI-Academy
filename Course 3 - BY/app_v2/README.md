# BeatRec v2 - Music Recommender Web App

A 3-page Flask web application for personalized music recommendations.

## Quick Start

### Prerequisites
- Python 3.8+
- Pre-computed embeddings in `../embeddings/all-MiniLM-L6-v2.pkl`

### Installation

```bash
cd app_v2
pip install -r requirements.txt
```

### Run the App

```bash
python main.py
```

Then open http://localhost:5000 in your browser.

## App Flow

### Page 1: Profile Creation
- Enter your name
- Listen to 10 sample songs (with iTunes previews)
- Rate each song 1-5 stars

### Page 2: Preferences
- **Valence/Energy Grid**: Interactive XY pad to set mood preferences
- **Mainstream Slider**: Underground (1) to Chart-Topper (10)
- **History Match Slider**: Balance between slider preferences vs. rating history
- **Genre Selection**: Multi-select from available genres
- **Decade Dropdown**: Filter by era (1970s-2020s)

### Page 3: Recommendations
- View 5 personalized song recommendations
- **Model Dropdown**: Choose between:
  - **Hybrid**: Full model combining embeddings, audio features, popularity, and genre
  - **Content-Based**: Pure embedding similarity
  - **Popularity-Weighted**: Collaborative-style recommendations
- Audio previews for each recommendation
- Match percentage scores

## Architecture

```
app_v2/
├── main.py              # Flask routes and API endpoints
├── data_loader.py       # Music data and embeddings loader
├── recommender.py       # Recommendation algorithms
├── requirements.txt     # Python dependencies
└── templates/
    ├── page1_profile.html
    ├── page2_preferences.html
    └── page3_recommendations.html
```

## API Endpoints

- `GET /` - Page 1: Profile creation
- `GET /preferences` - Page 2: Preferences
- `GET /recommendations` - Page 3: Results
- `GET /api/sample-songs` - Get 10 songs for rating
- `GET /api/genres` - Get available genres
- `GET /api/decades` - Get available decades
- `POST /api/recommend` - Get recommendations

## Features

- **Persona-based**: User profile with name and rating history
- **Audio Features**: Valence (mood) and Energy preferences via XY pad
- **Multi-model Support**: Switch between recommendation strategies
- **Constraint Filtering**: Genre and decade filters
- **iTunes Integration**: 30-second audio previews
