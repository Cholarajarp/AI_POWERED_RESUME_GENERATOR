# 🚀 QUICK DEPLOYMENT GUIDE (5-30 minutes)

**Goal:** Deploy backend to Render + frontend to Vercel

---

## 📋 Prerequisites

✅ GitHub account (already have)
✅ Docker Desktop running (already verified)
✅ Code pushed to GitHub main branch (done)

---

## 🎯 OPTION 1: Deploy Backend to Render (15 minutes)

### Step 1: Create Render Account
1. Go to https://render.com
2. Click "Sign Up" 
3. Choose "Sign up with GitHub"
4. Authorize render.com to access your repos
5. Click "Create Account"

### Step 2: Create PostgreSQL Database
1. Click "New +" button → "PostgreSQL"
2. Name: `resume-agent-db`
3. Database: `resume_agent_db`
4. User: `postgres`
5. Keep other defaults
6. Click "Create Database"
7. **Wait ~2-5 minutes for database to initialize**
8. Copy the **Internal Database URL** (you'll need this)

### Step 3: Create Web Service for Backend
1. Click "New +" button → "Web Service"
2. Choose "Public Git repository"
3. Connect your GitHub repo: `AI_POWERED_RESUME_GENERATOR`
4. Fill in:
   - **Name:** `resume-agent-backend`
   - **Root Directory:** `backend`
   - **Runtime:** `Python 3.11`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `./scripts/start.sh`

### Step 4: Set Environment Variables
Click "Environment" and add:

```
DATABASE_URL = postgresql+asyncpg://postgres:PASSWORD@HOSTNAME:5432/resume_agent_db
MINIO_ENDPOINT = minio:9000
MINIO_ACCESS_KEY = minioadmin
MINIO_SECRET_KEY = minioadmin
REDIS_URL = redis://redis:6379
STRIPE_API_KEY = sk_test_... (or leave blank for dev)
GOOGLE_CLIENT_ID = (your Google OAuth ID or leave blank)
GOOGLE_CLIENT_SECRET = (your Google OAuth secret or leave blank)
GITHUB_CLIENT_ID = (your GitHub OAuth ID or leave blank)
GITHUB_CLIENT_SECRET = (your GitHub OAuth secret or leave blank)
```

**Where to get these:**
- `DATABASE_URL`: From PostgreSQL database page (Internal URL)
- MinIO: Use defaults for now
- Others: Optional - leave blank if you don't have

### Step 5: Deploy
1. Click "Create Web Service"
2. **Wait ~3-5 minutes for deployment**
3. You'll see a URL like: `https://resume-agent-backend-xyz.onrender.com`
4. Click on it to test `/health` endpoint

✅ **Backend is live!**

---

## 🎯 OPTION 2: Deploy Frontend to Vercel (10 minutes)

### Step 1: Create Vercel Account
1. Go to https://vercel.com
2. Click "Sign Up"
3. Choose "Continue with GitHub"
4. Authorize Vercel
5. Click "Create Account"

### Step 2: Import Project
1. Click "Add New..." → "Project"
2. Select your `AI_POWERED_RESUME_GENERATOR` repo
3. Click "Import"

### Step 3: Configure Project
1. **Root Directory:** Select `frontend`
2. **Framework Preset:** Select `Vite`
3. **Build Command:** `npm run build`
4. **Output Directory:** `dist`

### Step 4: Set Environment Variables
Click "Environment Variables" and add:

```
VITE_API_URL = https://resume-agent-backend-xyz.onrender.com
```

(Replace `xyz` with your Render backend URL)

### Step 5: Deploy
1. Click "Deploy"
2. **Wait ~1-2 minutes for deployment**
3. You'll see a URL like: `https://ai-powered-resume-generator-xyz.vercel.app`
4. Click it to see your app live!

✅ **Frontend is live!**

---

## ✅ Verify Both Are Working

1. Go to your Vercel URL (frontend)
2. Open browser Developer Tools (F12)
3. Go to Network tab
4. Try to access any API feature (login, upload resume, etc.)
5. Check that requests go to your Render URL
6. Should see successful responses (no CORS errors!)

---

## 🐛 Troubleshooting

### Backend shows "Service Unavailable"
1. Check Render Dashboard → Logs
2. Look for error messages
3. Common issues:
   - Missing environment variables → Add them in Render
   - Database not connected → Wait 5 more minutes
   - PORT env var → Render sets it automatically

### Frontend shows blank page
1. Check browser Console (F12)
2. Look for error messages
3. Common issues:
   - `CORS error` → Backend URL is wrong in `VITE_API_URL`
   - `404` → Backend URL is wrong
   - `Cannot GET /` → Frontend not deployed

### Both working but API calls fail
1. Check that `VITE_API_URL` matches your Render backend URL
2. Check backend health: `https://your-render-url.onrender.com/health`
3. Check CORS in backend logs

---

## 💾 Backup Your URLs

Save these for later:
- **Backend URL:** `https://resume-agent-backend-xyz.onrender.com`
- **Frontend URL:** `https://ai-powered-resume-generator-xyz.vercel.app`
- **Database:** `postgresql+asyncpg://...` (Render shows it)

---

## 🎓 What You've Built

✅ FastAPI backend with async SQLAlchemy
✅ React frontend with Vite
✅ PostgreSQL database
✅ MinIO S3 storage (local in backend, can upgrade later)
✅ Production health monitoring
✅ CORS-enabled API
✅ Zero-downtime deployment

---

## 📊 Cost

**Render (Free Tier):**
- PostgreSQL: $7/month (after free trial)
- Web Service: Free ($0 - sleeps after 15 mins of inactivity)
- Total: ~$7/month

**Vercel (Free Tier):**
- Frontend: Free ($0)
- Serverless functions: Free

---

## 🚀 Next Steps After Deployment

1. **Test in Production**
   - Go to your Vercel URL
   - Create a test account
   - Upload a resume
   - Check all features work

2. **Monitor Performance**
   - Check Render Dashboard every few days
   - Check Vercel Analytics
   - Monitor error logs

3. **Add Domain**
   - Buy domain from Namecheap / GoDaddy / Route53
   - Point to your deployed app
   - Add SSL certificate (automatic on Vercel/Render)

4. **Upgrade Storage**
   - Replace MinIO with AWS S3 ($0.023/GB)
   - Update `MINIO_ENDPOINT` to S3 endpoint
   - Add AWS credentials

---

**Estimated Time:** 15-30 minutes
**Difficulty:** Easy ✅
**Result:** Production-ready application live on internet! 🎉

