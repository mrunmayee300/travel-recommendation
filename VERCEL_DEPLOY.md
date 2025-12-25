# 🚀 Deploy to Vercel - Step by Step Guide

## Prerequisites
- GitHub account
- Code pushed to a GitHub repository
- Vercel account (free)
- Railway account (free) for backend

---

## PART 1: Deploy Backend (Choose One)

### Option A: Railway (Original)
See steps below.

### Option B: Render.com (Recommended Alternative)
See `BACKEND_ALTERNATIVES.md` for full guide, or:

1. Go to https://render.com
2. New Web Service → Connect GitHub
3. Build Command: `pip install -r requirements.txt && python scripts/import_india_data.py`
4. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add env var: `CORS_ALLOW_ORIGINS=https://your-app.vercel.app,https://*.vercel.app`
6. Deploy!

### Option C: Other Alternatives
See `BACKEND_ALTERNATIVES.md` for Fly.io, PythonAnywhere, Heroku, DigitalOcean, Cloud Run.

---

## PART 1A: Deploy Backend to Railway

### Step 1: Push Code to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/your-repo.git
git push -u origin main
```

### Step 2: Deploy on Railway

1. **Go to Railway**: https://railway.app
2. **Sign up** with GitHub
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your repository**
6. **Railway will auto-detect Python**

### Step 3: Configure Railway

1. **Go to Settings** → **Variables**
2. **Add environment variable**:
   ```
   CORS_ALLOW_ORIGINS=https://your-app.vercel.app,https://*.vercel.app
   ```
   (We'll update this after deploying frontend)

3. **Go to Settings** → **Deploy**
4. **Set Start Command** (if not auto-detected):
   ```
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

### Step 4: Initialize Database

1. **Go to your Railway project**
2. **Click "View Logs"** → **Open Shell/Console**
3. **Run**:
   ```bash
   python scripts/import_india_data.py
   ```
   Or use the init script:
   ```bash
   python scripts/init_db.py
   ```

### Step 5: Get Backend URL

1. **Railway provides a URL** like: `https://your-app.up.railway.app`
2. **Copy this URL** - you'll need it for frontend
3. **Test it**: Visit `https://your-backend-url.up.railway.app/api/health`

---

## PART 2: Deploy Frontend to Vercel

### Step 1: Prepare Frontend

1. **Make sure** `frontend/vercel.json` exists (already created ✅)
2. **Check** that `frontend/package.json` has build script (already has ✅)

### Step 2: Deploy via Vercel Dashboard

1. **Go to Vercel**: https://vercel.com
2. **Sign up/Login** with GitHub
3. **Click "Add New Project"**
4. **Import your GitHub repository**
5. **Configure Project**:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend` ⚠️ **IMPORTANT**
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `dist` (auto-detected)
   - **Install Command**: `npm install` (auto-detected)

### Step 3: Add Environment Variable

1. **Before deploying**, click **"Environment Variables"**
2. **Add**:
   - **Name**: `VITE_API_BASE`
   - **Value**: `https://your-backend-url.up.railway.app/api`
   - **Select**: Production, Preview, Development ✅
3. **Click "Add"**

### Step 4: Deploy

1. **Click "Deploy"**
2. **Wait for build** (2-3 minutes)
3. **Get your frontend URL**: `https://your-app.vercel.app`

### Step 5: Update Backend CORS

1. **Go back to Railway**
2. **Settings** → **Variables**
3. **Update** `CORS_ALLOW_ORIGINS`:
   ```
   https://your-app.vercel.app,https://*.vercel.app
   ```
4. **Redeploy** backend (Railway auto-redeploys on env var change)

---

## PART 3: Test Your Deployment

1. **Open frontend URL**: `https://your-app.vercel.app`
2. **Test the flow**:
   - Select preferences
   - Get recommendations
   - Select destination
   - Customize trip
   - Generate itinerary
   - Check map view

3. **If errors**, check:
   - Browser console (F12)
   - Vercel deployment logs
   - Railway deployment logs

---

## 🔧 Troubleshooting

### Frontend shows "API unavailable"
- ✅ Check `VITE_API_BASE` in Vercel environment variables
- ✅ Verify backend URL is correct (test `/api/health`)
- ✅ Check CORS settings in Railway

### Backend returns 404
- ✅ Check Railway logs for errors
- ✅ Verify database was initialized
- ✅ Check that `travel_india.db` exists

### Build fails on Vercel
- ✅ Check Root Directory is set to `frontend`
- ✅ Verify all dependencies in `package.json`
- ✅ Check Vercel build logs for specific errors

### Database not found
- ✅ Run `python scripts/import_india_data.py` in Railway shell
- ✅ Check file paths in production

---

## 📝 Quick Reference

### Backend URL Format
```
https://your-app.up.railway.app
```

### Frontend URL Format
```
https://your-app.vercel.app
```

### Environment Variables Needed

**Railway (Backend)**:
- `CORS_ALLOW_ORIGINS` = `https://your-app.vercel.app,https://*.vercel.app`

**Vercel (Frontend)**:
- `VITE_API_BASE` = `https://your-backend-url.up.railway.app/api`

---

## 🎉 You're Done!

Your app is now live:
- **Frontend**: https://your-app.vercel.app
- **Backend**: https://your-backend.up.railway.app/api

Both platforms provide:
- ✅ Free HTTPS
- ✅ Auto-deployments on git push
- ✅ Free tier (with limits)
- ✅ Easy scaling

---

## 🔄 Updating Your App

After making changes:

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Your changes"
   git push
   ```

2. **Auto-deploy**:
   - Vercel auto-deploys frontend
   - Railway auto-deploys backend
   - Both take 2-3 minutes

3. **Check deployments**:
   - Vercel: Dashboard → Deployments
   - Railway: Dashboard → Deploys

---

## 💡 Pro Tips

1. **Use Railway's PostgreSQL** (free) instead of SQLite for production
2. **Set up custom domains** in both Vercel and Railway
3. **Monitor logs** in both platforms for debugging
4. **Use preview deployments** in Vercel for testing before production

