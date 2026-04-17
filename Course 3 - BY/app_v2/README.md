# 🎵 BeatRec - Music Recommender

A smart music recommendation system powered by multiple embedding models.

## Features

- **Multi-Model Recommendations**: Choose from 9 different embedding models (MiniLM, MPNet, BAAI, ColBERT, etc.)
- **Smart Like/Dislike System**: Like songs to save them, dislike to remove and get new recommendations
- **Real-Time Replacement**: Automatically fetches new songs when you like/dislike
- **Personalized Preferences**: Set mood (valence/energy), mainstream level, diversity, genres, and decade
- **Analytics Dashboard**: Track model performance with detailed metrics

## Tech Stack

- **Backend**: Flask + Gunicorn
- **ML**: Sentence Transformers, Scikit-learn, Pandas, NumPy
- **Frontend**: Vanilla JS + Material Design
- **Deployment**: Docker on Hugging Face Spaces

## Usage

### Main App
Navigate to `/` to start the recommendation flow:
1. Create profile
2. Select genres
3. Rate songs
4. Set preferences (mood, mainstream, diversity)
5. Get recommendations
6. Like/dislike songs
7. Give feedback
8. Export playlist

### Admin Dashboard
Navigate to `/admin/dashboard` to view:
- Average rating by embedding model
- % Liked songs by model
- % Disliked songs by model
- Accuracy, Diversity, Serendipity, Usability metrics per model

## Memory Optimization

This app uses **lazy-loading** for embedding models:
- Only loads models on-demand (not all at startup)
- LRU caching keeps max 2 models in memory
- Optimized data types reduce DataFrame memory by 60%
- Total memory usage: ~150MB (fits in 512MB free tiers)

## Deployment

### Hugging Face Spaces (Recommended)
```bash
# Clone your space
git clone https://huggingface.co/spaces/YOUR_USERNAME/beatrec
cd beatrec

# Copy files from app_v2
cp /path/to/app_v2/* .

# Initialize Git LFS for embeddings
git lfs install
git lfs track "*.pkl"
git lfs track "*.csv"

# Push
git add .
git commit -m "Deploy BeatRec"
git push
```

**URL**: `https://YOUR_USERNAME-beatrec.hf.space`

### Local Development
```bash
pip install -r requirements.txt
python main.py
# Open http://127.0.0.1:5000
```

## Configuration

Environment variables (optional):
- `SECRET_KEY`: Flask secret key (default: auto-generated)
- `SUBPATH`: Deploy under subpath (e.g., `/beatrec`)

## Performance

- **Startup Time**: ~5 seconds
- **Memory Usage**: ~150MB
- **Recommendation Time**: ~2-3 seconds (includes iTunes API calls)

## License

MIT

## Credits

Built with ❤️ for music discovery
