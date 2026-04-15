# 🚀 Quick Start: Deploy BeatRec to Render

This is a condensed checklist for deploying BeatRec. For detailed instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md).

---

## ✅ Pre-Deployment Checklist

- [ ] GitHub account created
- [ ] Code pushed to GitHub with `app_v2/` folder
- [ ] `app_v2/embeddings/` contains all 9 embedding models (already done ✅)
- [ ] `app_v2/static/` and `app_v2/templates/` folders exist (already done ✅)

---

## 📝 Deployment Steps (15 minutes)

### 1. Create Render Account (2 min)
- Go to https://render.com
- Sign up with GitHub

### 2. Create Web Service (5 min)
- Dashboard → **New +** → **Web Service**
- Connect repo: `DLH-AI-Academy/Course 3 - BY`
- Settings:
  - **Root Directory**: `app_v2`
  - **Build Command**: `pip install -r requirements.txt`
  - **Start Command**: `./web.sh`
  - **Environment Variables**:
    - `SUBPATH` = `/beatrec`
    - `FLASK_ENV` = `production`
    - `SECRET_KEY` = (generate random string)

### 3. Deploy (3-5 min)
- Click **Create Web Service**
- Wait for status: **Live**
- Test: `https://beatrec-xyz.onrender.com/beatrec`

### 4. Add Custom Domain (5 min + wait time)
- Render Dashboard → Settings → **Custom Domains**
- Add: `beatrec.rehatuncer.com`
- Go to your domain registrar
- Add CNAME: `beatrec` → `beatrec-xyz.onrender.com`
- Wait 5-30 minutes for DNS propagation

---

## 🎉 Done!

Your app is live at: **https://beatrec.rehatuncer.com**

---

## 💰 Cost: $0/month

- Free tier includes 750 hours/month
- App sleeps after 15 min inactivity (30s cold start)
- Upgrade to $7/month for always-on

---

## 🔄 Updates

```bash
# Make changes to app_v2/
git add app_v2/
git commit -m "Update"
git push origin main
# Auto-deploys in 2-3 minutes
```

---

## 📞 Need Help?

- Full guide: [DEPLOYMENT.md](./DEPLOYMENT.md)
- Render docs: https://render.com/docs
- Logs: Render Dashboard → Your Service → Logs

---

## 🎵 App Features

- **9 Embedding Models**: Users can switch between different ML models at runtime
- **Material UI**: Modern, responsive design
- **iTunes Integration**: 30-second audio previews + album artwork
- **Smart Fallback**: Automatically replaces songs without iTunes previews
