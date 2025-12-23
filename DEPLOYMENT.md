# Deployment Guide: Travel Recommendation App

This guide covers deploying your full-stack app with:
- **Frontend**: React + Vite → Vercel
- **Backend**: FastAPI → Railway/Render (recommended) or Vercel Serverless

---

## 🎯 Option 1: Frontend on Vercel + Backend on Railway/Render (Recommended)

### Step 1: Deploy Backend (Railway - Easiest)

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your repository

3. **Configure Backend**
   - Railway auto-detects Python
   - Add these environment variables in Railway dashboard:
     ```
     PYTHON_VERSION=3.10
     ```
   - Railway will run `pip install -r requirements.txt` automatically

4. **Add Startup Command**
   - In Railway, go to Settings → Deploy
   - Add start command:
     ```
     uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```
   - Or create `Procfile`:
     ```
     web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```

5. **Initialize Database**
   - Railway provides a shell/console
   - Run:
     ```bash
     python scripts/import_india_data.py
     ```
   - Or add this to a startup script

6. **Get Backend URL**
   - Railway provides a URL like: `https://your-app.up.railway.app`
   - Copy this URL

---

### Step 2: Deploy Frontend on Vercel

1. **Install Vercel CLI** (optional, or use web UI)
   ```bash
   npm i -g vercel
   ```

2. **Prepare Frontend**
   - Ensure `frontend/vercel.json` exists (already created)
   - Create `.env.production` in `frontend/` directory:
     ```env
     VITE_API_BASE=https://your-backend-url.up.railway.app/api
     ```
   - **Don't commit `.env.production`** - we'll add it in Vercel dashboard

3. **Deploy via Vercel Dashboard** (Easiest)
   - Go to [vercel.com](https://vercel.com)
   - Sign up/login with GitHub
   - Click "Add New Project"
   - Import your GitHub repository
   - Configure:
     - **Root Directory**: `frontend`
     - **Framework Preset**: Vite
     - **Build Command**: `npm run build`
     - **Output Directory**: `dist`
     - **Install Command**: `npm install`

4. **Add Environment Variables**
   - In Vercel project settings → Environment Variables
   - Add:
     ```
     VITE_API_BASE=https://your-backend-url.up.railway.app/api
     ```
   - Select "Production", "Preview", and "Development"

5. **Deploy**
   - Click "Deploy"
   - Vercel will build and deploy your frontend
   - You'll get a URL like: `https://your-app.vercel.app`

---

### Step 3: Update CORS in Backend

Make sure your backend allows requests from Vercel domain:

```python
# In app/main.py, update CORS origins:
origins = [
    "http://localhost:5173",
    "https://your-app.vercel.app",  # Add your Vercel URL
    "https://*.vercel.app",  # Or allow all Vercel previews
]
```

---

## 🎯 Option 2: Everything on Vercel (Serverless Functions)

If you want everything on Vercel, you'll need to convert FastAPI to Vercel serverless functions.

### Step 1: Create Vercel API Functions

Create `api/` directory in project root:

```
api/
  index.py  # Main handler
```

### Step 2: Install Vercel Python Runtime

```bash
pip install vercel
```

### Step 3: Create `vercel.json` in root:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    },
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "frontend/$1"
    }
  ]
}
```

**Note**: This approach requires significant refactoring. Option 1 is recommended.

---

## 📋 Quick Checklist

### Backend (Railway/Render)
- [ ] Backend deployed and accessible
- [ ] Database initialized (`python scripts/import_india_data.py`)
- [ ] CORS configured for frontend domain
- [ ] Environment variables set
- [ ] Backend URL copied

### Frontend (Vercel)
- [ ] Repository connected to Vercel
- [ ] Root directory set to `frontend`
- [ ] Build command: `npm run build`
- [ ] Output directory: `dist`
- [ ] Environment variable `VITE_API_BASE` set to backend URL
- [ ] Deployed successfully

---

## 🔧 Troubleshooting

### Frontend can't reach backend
- Check `VITE_API_BASE` environment variable in Vercel
- Verify backend CORS allows Vercel domain
- Check backend logs in Railway/Render

### Database not found
- Ensure `travel_india.db` is created
- Run import script: `python scripts/import_india_data.py`
- Check file paths in production

### Build fails
- Check Node.js version (Vercel auto-detects)
- Ensure all dependencies in `package.json`
- Check build logs in Vercel dashboard

---

## 🚀 Alternative: Render.com (Backend)

If Railway doesn't work, use Render:

1. Go to [render.com](https://render.com)
2. Create "Web Service"
3. Connect GitHub repo
4. Settings:
   - **Build Command**: `pip install -r requirements.txt && python scripts/import_india_data.py`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables
6. Deploy

---

## 📝 Notes

- **Database**: SQLite (`travel_india.db`) works for small apps. For production, consider PostgreSQL (Railway/Render provide free PostgreSQL).
- **Environment Variables**: Never commit `.env` files. Use platform environment variable settings.
- **CORS**: Always configure CORS to allow your frontend domain.
- **HTTPS**: Both Vercel and Railway/Render provide HTTPS automatically.

---

## 🎉 After Deployment

Your app will be live at:
- **Frontend**: `https://your-app.vercel.app`
- **Backend**: `https://your-backend.up.railway.app`

Test the full flow:
1. Open frontend URL
2. Select preferences
3. Get recommendations
4. Generate itinerary
5. Check map view

