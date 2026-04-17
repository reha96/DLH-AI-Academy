# 🚀 Deploying BeatRec to Hugging Face Spaces

## Quick Start (5 minutes)

### Step 1: Create Hugging Face Account
1. Go to https://huggingface.co
2. Click "Sign Up" (free)
3. Complete registration

### Step 2: Create New Space
1. Click your profile picture → **"New Space"**
2. Fill in:
   - **Space name**: `beatrec` (or your preferred name)
   - **License**: MIT
   - **Space SDK**: **Docker** ⚠️ (Important!)
   - **Visibility**: Public (or Private)
3. Click **"Create Space"**

### Step 3: Prepare Files Locally

Open PowerShell/CMD in your app_v2 directory:

```powershell
# Navigate to app_v2
cd "C:\Users\LetzPC Gaming\Documents\GitHub\DLH-AI-Academy\Course 3 - BY\app_v2"

# Install Git LFS (if not already installed)
git lfs install
```

### Step 4: Clone Your Space

```powershell
# Clone your space (replace YOUR_USERNAME)
git clone https://huggingface.co/spaces/YOUR_USERNAME/beatrec
cd beatrec
```

### Step 5: Copy All Files

```powershell
# Copy all files from app_v2 to your space
# (Adjust the path as needed)
Copy-Item "..\*" -Destination "." -Recurse -Force
```

### Step 6: Track Large Files with Git LFS

```powershell
# Track embedding files (.pkl)
git lfs track "*.pkl"

# Track CSV files
git lfs track "*.csv"

# Create .gitattributes if not exists
echo "*.pkl filter=lfs diff=lfs merge=lfs -text" > .gitattributes
echo "*.csv filter=lfs diff=lfs merge=lfs -text" >> .gitattributes
```

### Step 7: Commit and Push

```powershell
# Add all files
git add .

# Commit
git commit -m "Deploy BeatRec music recommender with lazy-loading embeddings"

# Push to Hugging Face
git push
```

### Step 8: Wait for Build

1. Go to your Space page: https://huggingface.co/spaces/YOUR_USERNAME/beatrec
2. Click **"Logs"** tab
3. Wait for Docker build (~3-5 minutes)
4. App will be live when you see: `Running on http://0.0.0.0:7860`

### Step 9: Test Your App

- **Main URL**: https://YOUR_USERNAME-beatrec.hf.space
- **Admin Dashboard**: https://YOUR_USERNAME-beatrec.hf.space/admin/dashboard

---

## Troubleshooting

### Build Fails with "No such file"
**Solution**: Ensure all files are copied:
```powershell
# Check files
ls

# Required files: Dockerfile, main.py, requirements.txt, templates/, static/, embeddings/
```

### Memory Error
**Should NOT happen** - app uses only ~150MB with lazy-loading.

If it occurs:
1. Check Logs tab for details
2. Verify embeddings are loading on-demand (look for "Loading embedding model:" messages)

### Port Binding Error
**Solution**: Dockerfile already configured for port 7860 (HF Spaces default).

### Build Timeout
**Solution**: 
- Free tier builds can take 5-10 minutes
- Wait patiently, don't restart
- If still failing, try upgrading to Pro ($9/month)

---

## Configuration (Optional)

### Set Environment Variables

In your Space Settings → **"Variables"**:

| Key | Value | Description |
|-----|-------|-------------|
| `SECRET_KEY` | `your-secret-key` | Flask security (auto-generated if missing) |
| `SUBPATH` | `/beatrec` | Deploy under subpath (optional) |

### Upgrade Hardware

Free tier is sufficient (16 GB RAM), but you can upgrade:

1. Go to Settings → **"Hardware"**
2. Choose:
   - **CPU Basic** (free) - 16 GB RAM, 2 vCPU ✅ Recommended
   - **CPU Upgrade** ($5/mo) - 32 GB RAM, 4 vCPU
   - **GPU** ($30+/mo) - For faster inference

---

## Post-Deployment Checklist

- [ ] Homepage loads: `https://YOUR_USERNAME-beatrec.hf.space`
- [ ] Can create profile
- [ ] Can rate songs
- [ ] Can set preferences
- [ ] Recommendations appear
- [ ] Like button works (heart icon)
- [ ] Dislike button works (minus icon)
- [ ] New songs appear after like/dislike
- [ ] Admin dashboard works: `/admin/dashboard`
- [ ] Charts show model performance

---

## URLs After Deployment

| Page | URL |
|------|-----|
| Main App | `https://huggingface.co/spaces/YOUR_USERNAME/beatrec` |
| Direct App | `https://YOUR_USERNAME-beatrec.hf.space` |
| Admin Dashboard | `https://YOUR_USERNAME-beatrec.hf.space/admin/dashboard` |
| API (Genres) | `https://YOUR_USERNAME-beatrec.hf.space/api/genres` |
| API (Recommend) | `https://YOUR_USERNAME-beatrec.hf.space/api/recommend` |

---

## Updating Your Deployment

```powershell
# Make your changes locally
# Then:

cd beatrec
git add .
git commit -m "Update: describe your changes"
git push

# Auto-deploys in ~2 minutes
```

---

## Cost

- **Free Tier**: 16 GB RAM, 2 vCPU, unlimited storage ✅ Sufficient for BeatRec
- **Pro Tier**: $9/month - More build minutes, private spaces
- **Upgrades**: Starting at $5/month for more CPU/RAM

---

## Support

If you encounter issues:

1. Check **"Logs"** tab in your Space
2. Review **Troubleshooting** section above
3. Check Hugging Face status: https://status.huggingface.co
4. Ask in Hugging Face Discord: https://discord.gg/huggingface

---

## Next Steps After Deployment

1. **Share your app**: Post the URL on social media
2. **Collect feedback**: Use the built-in feedback form
3. **Monitor analytics**: Check `/admin/dashboard` for model performance
4. **Export data**: Use admin dashboard to export feedback CSV

Enjoy your deployed BeatRec app! 🎵
