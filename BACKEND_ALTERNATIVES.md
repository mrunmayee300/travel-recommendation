# Backend Deployment Alternatives to Railway

Here are the best alternatives for deploying your FastAPI backend:

---

## 🚀 Option 1: Render.com (Recommended Alternative)

### Why Render?
- ✅ Free tier with 750 hours/month
- ✅ Auto-deploy from GitHub
- ✅ Easy PostgreSQL database
- ✅ Simple configuration
- ✅ Similar to Railway

### Step-by-Step:

1. **Go to Render**: https://render.com
2. **Sign up** with GitHub
3. **Click "New +"** → **"Web Service"**
4. **Connect your GitHub repository**
5. **Configure**:
   - **Name**: `travel-recommendation-api`
   - **Environment**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt && python scripts/import_india_data.py
     ```
   - **Start Command**: 
     ```bash
     uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```
   - **Plan**: Free

6. **Add Environment Variables**:
   - `CORS_ALLOW_ORIGINS`: `https://your-app.vercel.app,https://*.vercel.app`
   - `APP_ENV`: `production`

7. **Click "Create Web Service"**
8. **Wait for deployment** (5-10 minutes)
9. **Get your URL**: `https://your-app.onrender.com`

### Render Notes:
- Free tier spins down after 15 min inactivity (first request may be slow)
- Upgrade to paid ($7/month) for always-on
- Auto-deploys on git push

---

## 🚀 Option 2: Fly.io

### Why Fly.io?
- ✅ Generous free tier
- ✅ Global edge deployment
- ✅ Fast cold starts
- ✅ Great for Python apps

### Step-by-Step:

1. **Install Fly CLI**:
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   
   # Or download from: https://fly.io/docs/getting-started/installing-flyctl/
   ```

2. **Sign up**: https://fly.io
   - Run: `fly auth signup`

3. **Create Fly App**:
   ```bash
   cd your-project-root
   fly launch
   ```
   - Follow prompts
   - Select region
   - Don't deploy yet

4. **Create `fly.toml`** (I'll create this for you):
   ```toml
   app = "your-app-name"
   primary_region = "iad"  # or your preferred region
   
   [build]
     builder = "paketobuildpacks/builder:base"
   
   [http_service]
     internal_port = 8000
     force_https = true
     auto_stop_machines = true
     auto_start_machines = true
     min_machines_running = 0
     processes = ["app"]
   
   [[services]]
     http_checks = []
     internal_port = 8000
     processes = ["app"]
     protocol = "tcp"
     script_checks = []
   
     [services.concurrency]
       hard_limit = 25
       soft_limit = 20
       type = "connections"
   
     [[services.ports]]
       force_https = true
       handlers = ["http"]
       port = 80
   
     [[services.ports]]
       handlers = ["tls", "http"]
       port = 443
   
     [[services.tcp_checks]]
       grace_period = "1s"
       interval = "15s"
       restart_limit = 0
       timeout = "2s"
   
   [[processes]]
     name = "app"
     command = "uvicorn app.main:app --host 0.0.0.0 --port 8000"
   ```

5. **Create `Dockerfile`** (for Fly.io):
   ```dockerfile
   FROM python:3.10-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   # Initialize database
   RUN python scripts/import_india_data.py || true
   
   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

6. **Deploy**:
   ```bash
   fly deploy
   ```

7. **Set secrets**:
   ```bash
   fly secrets set CORS_ALLOW_ORIGINS="https://your-app.vercel.app,https://*.vercel.app"
   ```

8. **Get URL**: `https://your-app.fly.dev`

---

## 🚀 Option 3: PythonAnywhere

### Why PythonAnywhere?
- ✅ Free tier available
- ✅ Simple Python hosting
- ✅ Good for beginners
- ⚠️ Limited free tier

### Step-by-Step:

1. **Sign up**: https://www.pythonanywhere.com
2. **Create new Web App**:
   - Go to "Web" tab
   - Click "Add a new web app"
   - Select "Manual configuration" → Python 3.10
3. **Upload code**:
   - Use "Files" tab to upload your code
   - Or use Git: `git clone https://github.com/yourusername/your-repo.git`
4. **Install dependencies**:
   - Open Bash console
   - Run: `pip3.10 install --user -r requirements.txt`
5. **Configure WSGI**:
   - Go to "Web" tab → WSGI configuration file
   - Edit and add:
   ```python
   import sys
   path = '/home/yourusername/your-repo'
   if path not in sys.path:
       sys.path.insert(0, path)
   
   from app.main import app
   application = app
   ```
6. **Initialize database**:
   - In Bash console: `python3.10 scripts/import_india_data.py`
7. **Reload web app**
8. **Get URL**: `https://yourusername.pythonanywhere.com`

---

## 🚀 Option 4: Heroku

### Why Heroku?
- ✅ Well-established platform
- ✅ Easy deployment
- ⚠️ No free tier anymore (paid only)

### Step-by-Step:

1. **Sign up**: https://heroku.com
2. **Install Heroku CLI**:
   ```bash
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```
3. **Login**:
   ```bash
   heroku login
   ```
4. **Create app**:
   ```bash
   heroku create your-app-name
   ```
5. **Set environment variables**:
   ```bash
   heroku config:set CORS_ALLOW_ORIGINS="https://your-app.vercel.app,https://*.vercel.app"
   ```
6. **Deploy**:
   ```bash
   git push heroku main
   ```
7. **Initialize database**:
   ```bash
   heroku run python scripts/import_india_data.py
   ```
8. **Get URL**: `https://your-app-name.herokuapp.com`

**Note**: Heroku requires paid plan ($5-7/month minimum)

---

## 🚀 Option 5: DigitalOcean App Platform

### Why DigitalOcean?
- ✅ Simple deployment
- ✅ Good pricing
- ✅ Reliable infrastructure

### Step-by-Step:

1. **Sign up**: https://www.digitalocean.com
2. **Go to App Platform**
3. **Create App** → **GitHub**
4. **Select repository**
5. **Configure**:
   - **Type**: Web Service
   - **Build Command**: `pip install -r requirements.txt && python scripts/import_india_data.py`
   - **Run Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**: Add `CORS_ALLOW_ORIGINS`
6. **Deploy**
7. **Get URL**: `https://your-app.ondigitalocean.app`

**Pricing**: ~$5/month for basic plan

---

## 🚀 Option 6: Google Cloud Run (Free Tier)

### Why Cloud Run?
- ✅ Generous free tier
- ✅ Pay per use
- ✅ Auto-scaling

### Step-by-Step:

1. **Install Google Cloud SDK**
2. **Create project** in Google Cloud Console
3. **Enable Cloud Run API**
4. **Create `Dockerfile`** (same as Fly.io)
5. **Deploy**:
   ```bash
   gcloud run deploy travel-api \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```
6. **Set environment variables** in Cloud Console
7. **Get URL**: `https://your-app-xxxxx.run.app`

---

## 📊 Comparison Table

| Platform | Free Tier | Ease of Use | Best For |
|----------|-----------|-------------|----------|
| **Render** | ✅ 750 hrs/month | ⭐⭐⭐⭐⭐ | Best Railway alternative |
| **Fly.io** | ✅ Generous | ⭐⭐⭐⭐ | Global edge deployment |
| **PythonAnywhere** | ✅ Limited | ⭐⭐⭐ | Beginners |
| **Heroku** | ❌ Paid only | ⭐⭐⭐⭐⭐ | Established apps |
| **DigitalOcean** | ❌ Paid | ⭐⭐⭐⭐ | Production apps |
| **Cloud Run** | ✅ Generous | ⭐⭐⭐ | Enterprise scale |

---

## 🎯 Recommendation

**For most users**: **Render.com** is the best Railway alternative:
- ✅ Free tier
- ✅ Easy setup
- ✅ Auto-deploy
- ✅ Similar to Railway

**For global apps**: **Fly.io** for edge deployment

**For production**: **DigitalOcean** or **Cloud Run**

---

## 🔧 Quick Setup for Render (Recommended)

I'll create the necessary files for Render deployment:

