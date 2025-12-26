# 🔧 Fix: Frontend API Connection Issue

## Problem
The frontend can't reach the backend APIs because:
1. Missing `VITE_API_BASE` environment variable in Vercel
2. API path duplication in RecommendationsPage.tsx
3. CORS configuration needs update

## ✅ Fixes Applied

### 1. Created Shared API Config (`frontend/src/config/api.ts`)
- Centralized API base URL configuration
- Helper function to build API URLs correctly
- Prevents path duplication issues

### 2. Fixed API Calls
- Updated `RecommendationsPage.tsx` to use correct API path
- Updated `ItineraryPage.tsx` to use shared config
- Removed duplicate `/api` in paths

### 3. Updated Backend CORS
- Made CORS configurable via environment variable
- Allows Vercel preview deployments
- Supports wildcard for Vercel domains

---

## 🚀 Steps to Deploy Fix

### Step 1: Update Backend CORS (Render)

1. Go to your Render dashboard: https://dashboard.render.com
2. Select your backend service: `travel-recommendation-xx47`
3. Go to **Environment** tab
4. Add/Update environment variable:
   ```
   CORS_ALLOW_ORIGINS=https://travel-frontend-murex-rho.vercel.app,https://*.vercel.app
   ```
5. **Save** and wait for redeploy (2-3 minutes)

### Step 2: Set Frontend Environment Variable (Vercel)

1. Go to Vercel dashboard: https://vercel.com
2. Select your project: `travel-frontend`
3. Go to **Settings** → **Environment Variables**
4. Add new variable:
   - **Name**: `VITE_API_BASE`
   - **Value**: `https://travel-recommendation-xx47.onrender.com/api`
   - **Environment**: Select all (Production, Preview, Development) ✅
5. **Save**

### Step 3: Redeploy Frontend

**Option A: Auto-redeploy (if code is pushed to GitHub)**
- Push the fixed code to GitHub
- Vercel will auto-deploy

**Option B: Manual redeploy**
1. Go to Vercel dashboard
2. Click **Deployments**
3. Click **⋯** (three dots) on latest deployment
4. Click **Redeploy**

### Step 4: Test

1. Open your frontend: https://travel-frontend-murex-rho.vercel.app/preferences
2. Fill preferences and click "Continue to places"
3. Check browser console (F12) for any errors
4. Verify destinations load correctly

---

## 🔍 Verify Backend is Working

Test your backend directly:

```bash
# Health check
curl https://travel-recommendation-xx47.onrender.com/api/health

# Test recommendations endpoint
curl -X POST https://travel-recommendation-xx47.onrender.com/api/recommend-destinations \
  -H "Content-Type: application/json" \
  -d '{"tags":["culture","food"],"budget_level":"mid","climate":"warm","top_k":3}'
```

---

## 🐛 Troubleshooting

### Frontend still shows "Could not reach API"

1. **Check Environment Variable**:
   - Go to Vercel → Settings → Environment Variables
   - Verify `VITE_API_BASE` is set correctly
   - Make sure it's enabled for Production ✅

2. **Check Browser Console**:
   - Open browser DevTools (F12)
   - Go to Network tab
   - Try the flow again
   - Look for failed requests
   - Check the actual URL being called

3. **Verify Backend CORS**:
   - Check Render logs for CORS errors
   - Verify `CORS_ALLOW_ORIGINS` includes your Vercel URL

4. **Test Backend Directly**:
   - Visit: https://travel-recommendation-xx47.onrender.com/api/health
   - Should return: `{"status":"ok"}`
   - If not, backend might be down

### CORS Errors in Browser Console

If you see CORS errors:
1. Update `CORS_ALLOW_ORIGINS` in Render to include exact Vercel URL
2. Remove wildcards (FastAPI CORS doesn't support them well)
3. Use exact URL: `https://travel-frontend-murex-rho.vercel.app`

### Environment Variable Not Working

Vite environment variables:
- Must start with `VITE_`
- Must be set before build
- Require rebuild after adding/changing

**Solution**: After adding `VITE_API_BASE` in Vercel, trigger a new deployment.

---

## 📝 Quick Checklist

- [ ] Backend CORS updated in Render
- [ ] `VITE_API_BASE` set in Vercel
- [ ] Frontend code pushed to GitHub (with fixes)
- [ ] Frontend redeployed on Vercel
- [ ] Tested in browser
- [ ] Checked browser console for errors
- [ ] Verified backend is accessible

---

## 🎯 Expected Behavior After Fix

1. **Preferences Page**: Works (no API calls)
2. **Recommendations Page**: ✅ Loads destinations from backend
3. **Customize Page**: Works (no API calls)
4. **Itinerary Page**: ✅ Generates itinerary from backend

---

## 🔗 Your URLs

- **Backend**: https://travel-recommendation-xx47.onrender.com
- **Frontend**: https://travel-frontend-murex-rho.vercel.app
- **Backend API Base**: https://travel-recommendation-xx47.onrender.com/api

Make sure `VITE_API_BASE` in Vercel is set to: `https://travel-recommendation-xx47.onrender.com/api`

