# Deploy BeatRec to Hugging Face Spaces

Hugging Face Spaces offers **16 GB RAM** and **2 vCPU** for free - perfect for BeatRec after optimizations.

## Prerequisites

1. Create a free account at [huggingface.co](https://huggingface.co)
2. Install Git LFS: `git lfs install`

## Step-by-Step Deployment

### 1. Create a New Space

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Choose:
   - **Space name**: `beatrec` (or your preferred name)
   - **License**: MIT
   - **Space SDK**: Docker
   - **Visibility**: Public (or Private)
4. Click "Create Space"

### 2. Prepare Your Repository

```bash
# Clone your space (replace YOUR_USERNAME with your HF username)
git clone https://huggingface.co/spaces/YOUR_USERNAME/beatrec
cd beatrec

# Copy BeatRec app files
cp /path/to/your/app_v2/* .

# Required files for Docker deployment:
# - Dockerfile
# - requirements.txt
# - main.py
# - model_manager.py
# - data_loader.py
# - recommender.py
# - templates/
# - static/
# - embeddings/ (all .pkl files)
# - data/ (spotify_songs.csv, optional)

# Add .gitignore
cat > .gitignore << EOF
__pycache__/
*.pyc
*.pyo
*.git
.env
*.log
feedback_results.csv
EOF

# Git LFS for large files (embeddings)
git lfs install
git lfs track "*.pkl"
git lfs track "*.csv"

# Commit and push
git add .
git commit -m "Deploy BeatRec music recommender"
git push
```

### 3. Configure Space Settings

In your Space settings page:
- **Hardware**: Choose "CPU Basic" (free tier)
- **Storage**: Keep default
- **Variables**: Add if needed:
  - `SECRET_KEY`: Your secret key
  - `SUBPATH`: Leave empty for root deployment

### 4. Wait for Build

The Docker image will build automatically (~3-5 minutes):
1. Building dependencies
2. Copying application files
3. Starting Gunicorn server

### 5. Access Your App

Once deployed, your app will be available at:
```
https://YOUR_USERNAME-beatrec.hf.space
```

---

## Troubleshooting

### Build Fails: "No such file or directory"

Ensure all files are copied correctly:
```bash
ls -la
# Should see: Dockerfile, requirements.txt, main.py, etc.
```

### Memory Errors

The optimizations should prevent this, but if you see OOM:
1. Check Space hardware: should be "CPU Basic" (16 GB RAM)
2. Verify embeddings are loaded lazily (check logs)

### Port Binding Errors

Hugging Face Spaces uses port 7860 by default. The Dockerfile handles this automatically.

---

## Alternative: Deploy to Fly.io

If you prefer Fly.io (~$2/month):

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Initialize (from app_v2 directory)
fly launch --name beatrec --dockerfile ./Dockerfile

# Set environment variables
fly secrets set SECRET_KEY=your-secret-key

# Deploy
fly deploy

# Open app
fly open
```

---

## Alternative: Deploy to Railway

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project (from app_v2 directory)
railway init

# Add Docker support
railway up

# Set environment variables
railway variables set SECRET_KEY=your-secret-key

# Deploy
railway up
```

---

## Performance Comparison

| Platform | RAM | CPU | Boot Time | Monthly Cost |
|----------|-----|-----|-----------|--------------|
| Hugging Face Spaces | 16 GB | 2 vCPU | ~30s | Free |
| Fly.io | 256 MB-2 GB | Shared | ~10s | ~$2 |
| Railway | 512 MB | Shared | ~15s | ~$5 |
| Render (Free) | 512 MB | Shared | ~20s | Free |

**Recommendation**: Start with Hugging Face Spaces (free, most resources), then consider Fly.io for production if you need custom domains and lower latency.

---

## Monitoring

### View Logs

**Hugging Face Spaces:**
- Go to your Space page
- Click "Logs" tab
- Real-time logs shown

**Check for:**
```
Loading dataset and embedding metadata...
Dataset loaded: XXXXX tracks, 10 columns
Memory usage: XX.XX MB
Registered embedding model: MiniLM (all-MiniLM-L6-v2)
Initialized ModelManager with X models
```

### Test Endpoints

```bash
# Test API health
curl https://YOUR_USERNAME-beatrec.hf.space/api/genres

# Test recommendations
curl -X POST https://YOUR_USERNAME-beatrec.hf.space/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"ratings":[], "valence":0.5, "energy":0.5, "mainstream":0.5, "diversity":0.5, "genres":["pop"], "decade":"Mixed", "model":"hybrid", "embedding_model":"MiniLM"}'
```

---

## Updating Your Deployment

```bash
# Make changes locally
git add .
git commit -m "Fix: description of changes"
git push

# Hugging Face Spaces will auto-redeploy
```

---

## Cost Optimization Tips

1. **Use CPU only** - GPU is unnecessary for inference
2. **Enable auto-sleep** - Hugging Face Spaces sleeps after inactivity
3. **Monitor usage** - Check Space metrics in settings
4. **Optimize embeddings** - Consider removing unused models

---

## Security Notes

1. **Never commit secrets** - Use Space variables
2. **Rate limiting** - Add if experiencing abuse
3. **HTTPS** - Enabled by default on all platforms
4. **CORS** - Configure if exposing API

Example rate limiting in `main.py`:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(app, key_func=get_remote_address)

@app.route("/api/recommend", methods=["POST"])
@limiter.limit("10 per minute")
def recommend():
    # ...
```
