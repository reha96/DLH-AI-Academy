# BeatRec Deployment Guide

Deploy your BeatRec music recommender to **Render** (free tier) at `rehatuncer.com/beatrec`.

---

## 📋 Prerequisites

- GitHub account
- Render account (free)
- Domain: `rehatuncer.com` (you already own this)
- Pre-computed embeddings in `embeddings/` folder

---

## 🚀 Step-by-Step Deployment

### Step 1: Create Render Account

1. Go to **[https://render.com](https://render.com)**
2. Click **"Get Started for Free"**
3. Sign up with **GitHub** (recommended) or email
   - Using GitHub makes deployment easier

---

### Step 2: Push Code to GitHub

Ensure your repository contains the `app_v2` folder with all files:

```
Course 3 - BY/
├── app_v2/
│   ├── main.py              # ✅ Updated with subpath support
│   ├── data_loader.py       # ✅ Updated with flexible embedding paths
│   ├── recommender.py       # Music recommendation algorithms
│   ├── requirements.txt     # ✅ Includes gunicorn
│   ├── render.yaml          # ✅ Render deployment config
│   ├── web.sh               # ✅ Startup script
│   ├── .renderignore        # Exclude unnecessary files
│   ├── embeddings/          # ✅ Pre-computed embeddings (9 models)
│   │   ├── all-MiniLM-L6-v2.pkl
│   │   ├── all-mpnet-base-v2.pkl
│   │   ├── BAAI-bge-m3.pkl
│   │   ├── colbert-ir-colbertv2.0.pkl
│   │   ├── mixedbread-ai-mxbai-embed-large-v1.pkl
│   │   ├── multi-qa-MiniLM-L6-cos-v1.pkl
│   │   ├── naver-splade-cocondenser-ensembledistil.pkl
│   │   ├── Snowflake-snowflake-arctic-embed-l-v2.0.pkl
│   │   └── thenlper-gte-large.pkl
│   ├── static/
│   │   ├── css/
│   │   └── profile-utils.js
│   └── templates/
│       ├── welcome.html
│       ├── page1_profile_material.html
│       ├── genre_selection.html
│       ├── page2_preferences.html
│       └── page3_recommendations.html
└── embeddings/
    └── (original embeddings - kept for local development)
```

**Note**: The `app_v2/embeddings/` folder contains all 9 pre-computed embedding models required for recommendations. These are automatically included in deployment.

**Commit and push:**

```bash
git add app_v2/
git commit -m "Prepare BeatRec for Render deployment"
git push origin main
```

---

### Step 3: Create New Web Service on Render

1. **Log in to Render Dashboard**
   - Go to [dashboard.render.com](https://dashboard.render.com)

2. **Create New Service**
   - Click **"New +"** button (top right)
   - Select **"Web Service"**

3. **Connect Repository**
   - Choose **"Connect a repository"**
   - Select your GitHub repo: `DLH-AI-Academy/Course 3 - BY`
   - If you don't see it, click **"Configure account"** to grant access

4. **Configure Service Settings**

| Field | Value |
|-------|-------|
| **Name** | `beatrec` (or any name you prefer) |
| **Region** | `Frankfurt` (closest to Turkey) |
| **Branch** | `main` (or your default branch) |
| **Root Directory** | `app_v2` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `./web.sh` |
| **Instance Type** | `Free` |
| **Environment Variables** | Add these: |

**Environment Variables:**

| Key | Value |
|-----|-------|
| `SUBPATH` | `/beatrec` |
| `FLASK_ENV` | `production` |
| `SECRET_KEY` | (generate a random string, e.g., use [randomkeygen.com](https://randomkeygen.com)) |

> **Note**: `PYTHON_VERSION` is auto-detected by Render, no need to set it manually.

5. **Advanced Settings** (optional but recommended)
   - **Auto-Deploy**: ✅ Enabled (auto-deploy on git push)
   - **Health Check Path**: `/api/genres`

6. **Click "Create Web Service"**

---

### Step 4: Wait for Deployment

- Render will now build your app (~3-5 minutes)
- You'll see logs in real-time
- Wait for status: **"Live"**

**Your app is now accessible at:**
```
https://beatrec-xyz.onrender.com/beatrec
```

(The `xyz` is a unique ID assigned by Render)

---

### Step 5: Configure Custom Domain

#### Option A: Subdomain (`beatrec.rehatuncer.com`)

**Easiest option - recommended for first-time setup**

1. **In Render Dashboard:**
   - Go to your service → **Settings** → **Custom Domains**
   - Click **"Add Custom Domain"**
   - Enter: `beatrec.rehatuncer.com`
   - Click **"Add Domain"**

2. **Render will show DNS records to add:**
   - CNAME record: `beatrec` → `beatrec-xyz.onrender.com`

3. **Go to your domain registrar** (where you bought rehatuncer.com):
   - Add a **CNAME record**:
     - **Host/Name**: `beatrec`
     - **Value/Target**: `beatrec-xyz.onrender.com` (replace xyz with your actual ID)
     - **TTL**: Automatic or 3600

4. **Wait for DNS propagation** (5-30 minutes)

5. **SSL Certificate:**
   - Render automatically provisions a free SSL certificate via Let's Encrypt
   - Takes ~5-10 minutes after DNS propagation

6. **Final URL:**
   ```
   https://beatrec.rehatuncer.com
   ```

---

#### Option B: Subpath (`rehatuncer.com/beatrec`)

**Requires DNS A record access to your root domain**

1. **In Render Dashboard:**
   - Go to your service → **Settings** → **Custom Domains**
   - Click **"Add Custom Domain"**
   - Enter: `rehatuncer.com`
   - Click **"Add Domain"**

2. **Render will show DNS records:**
   - **A record**: `@` → `76.76.21.21` (Render's IP)
   - **OR CNAME**: `www` → `custom.onrender.com`

3. **Go to your domain registrar:**
   - Add **A record** for root domain:
     - **Host/Name**: `@`
     - **Value/Target**: `76.76.21.21`
   
   - Or update existing nameservers if you're using a DNS provider

4. **Wait for DNS propagation** (5-30 minutes)

5. **Configure redirect** (optional):
   - Set up redirect from `rehatuncer.com` → `rehatuncer.com/beatrec`
   - This depends on your hosting provider

6. **Final URL:**
   ```
   https://rehatuncer.com/beatrec
   ```

---

## ✅ Verify Deployment

1. **Test the app:**
   - Visit your deployed URL
   - Create a profile
   - Rate songs
   - Get recommendations

2. **Test API endpoints:**
   ```bash
   # Replace YOUR_URL with your actual deployment URL
   curl https://YOUR_URL/beatrec/api/genres
   curl https://YOUR_URL/beatrec/api/decades
   ```

3. **Check logs:**
   - Render Dashboard → Your Service → **Logs**
   - View real-time logs for debugging

---

## 🔧 Troubleshooting

### App shows 502 Bad Gateway
- **Cause**: App failed to start
- **Fix**: Check logs for errors, ensure `web.sh` is executable

### Embeddings not found
- **Cause**: Missing embedding file
- **Fix**: Ensure `embeddings/all-MiniLM-L6-v2.pkl` is in your repo or mounted disk

### Cold start delays (~30 seconds)
- **Normal behavior** on free tier
- App sleeps after 15 minutes of inactivity
- **Upgrade to paid plan** ($7/month) for always-on service

### Custom domain not working
- **Wait**: DNS propagation can take up to 24 hours
- **Check**: Verify DNS records are correct using [whatsmydns.net](https://whatsmydns.net)
- **SSL**: Wait additional 5-10 minutes for certificate provisioning

---

## 💰 Cost Breakdown

| Resource | Free Tier | Your Usage | Cost |
|----------|-----------|------------|------|
| Web Service | 750 hours/month | ~750 hours | $0 |
| Bandwidth | 100 GB/month | ~1-2 GB | $0 |
| SSL Certificate | Included | Included | $0 |
| Custom Domain | Included | 1 domain | $0 |
| **Total** | | | **$0/month** |

**Note**: Free tier includes sleep after 15 minutes of inactivity. First request after sleep takes ~30 seconds (cold start).

---

## 🔄 Updating Your App

After initial deployment, updates are automatic:

1. **Make changes** to `app_v2/` files
2. **Commit and push** to GitHub:
   ```bash
   git add app_v2/
   git commit -m "Update recommender logic"
   git push origin main
   ```
3. **Render auto-deploys** (~2-3 minutes)
4. **Done!** Your changes are live

---

## 📊 Monitoring

- **Dashboard**: [dashboard.render.com](https://dashboard.render.com)
- **Logs**: Real-time logs in Render dashboard
- **Metrics**: CPU, memory, request count
- **Alerts**: Email notifications for failures

---

## 🎯 Next Steps

1. **Share your app** with friends/classmates
2. **Collect feedback** for improvements
3. **Monitor usage** in Render dashboard
4. **Consider upgrading** to paid plan ($7/month) if:
   - You want to avoid cold starts
   - You exceed free tier limits
   - You need more resources

---

## 📞 Support

- **Render Docs**: [render.com/docs](https://render.com/docs)
- **Render Community**: [community.render.com](https://community.render.com)
- **This Project**: Check `app_v2/README.md` for local development

---

**🎉 Congratulations! Your BeatRec app is now live on the internet!**
