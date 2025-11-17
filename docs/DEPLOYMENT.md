# 🚀 Deployment Guide

Complete step-by-step instructions to deploy the AI Resume Agent to production on Render, Vercel, AWS, or Netlify.

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Environment Setup](#environment-setup)
3. [Render (Backend + Database)](#render-backend--database)
4. [Vercel (Frontend)](#vercel-frontend)
5. [AWS (Alternative)](#aws-alternative)
6. [Netlify (Alternative Frontend)](#netlify-alternative-frontend)
7. [Post-Deployment Testing](#post-deployment-testing)
8. [Troubleshooting](#troubleshooting)

---

## Pre-Deployment Checklist

Before deploying, ensure:

- [ ] All code is committed and pushed to GitHub
- [ ] `.env` file is **NOT** tracked (check `.gitignore`)
- [ ] You have accounts for: GitHub, Render, Vercel, and any services you use
- [ ] API keys are ready: OpenAI, Stripe, Google OAuth, GitHub OAuth
- [ ] Database is configured (PostgreSQL)
- [ ] MinIO/S3 bucket is set up

---

## Environment Setup

### Required Environment Variables

#### Backend Services (.env)

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/resume_agent_db

# Security
SECRET_KEY=your-very-secret-key-here-change-in-production

# OpenAI (optional for dev, required for production)
OPENAI_API_KEY=sk-your-openai-key
LLM_PROVIDER=openai

# Stripe (optional for dev, required for payments)
STRIPE_API_KEY=sk_live_your-stripe-key
STRIPE_WEBHOOK_SECRET=whsec_your-webhook-secret

# MinIO / S3 (required for file uploads)
MINIO_ENDPOINT=s3.amazonaws.com  # or your MinIO host
MINIO_ACCESS_KEY=your-access-key
MINIO_SECRET_KEY=your-secret-key
MINIO_BUCKET=resume-uploads

# Redis (for Celery tasks)
CELERY_BROKER=redis://redis-host:6379/0
CELERY_BACKEND=redis://redis-host:6379/1

# OAuth (optional but recommended)
GOOGLE_OAUTH_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-google-client-secret

GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret

# App Settings
ENVIRONMENT=production
FRONTEND_URL=https://your-frontend-domain.com
DEBUG=false
```

---

## Render (Backend + Database)

**Render** offers a free tier for databases and web services. Perfect for MVP deployment.

### Step 1: Create PostgreSQL Database on Render

1. Go to [render.com](https://render.com) and sign in with GitHub
2. Click **"+ New"** → **"PostgreSQL"**
3. Configure:
   - **Name:** `ai-resume-db`
   - **Database:** `resume_agent_db`
   - **User:** `postgres`
   - **Region:** Same as your web service (us-east)
   - **Instance Type:** Free
4. Click **Create Database**
5. Copy the **Database URL** (save it for later)

### Step 2: Create Redis Instance (Optional but Recommended)

1. Go to Render dashboard → **"+ New"** → **"Redis"**
2. Configure:
   - **Name:** `ai-resume-redis`
   - **Region:** Same as database
   - **Instance Type:** Free
3. Click **Create Redis**
4. Copy the **Redis URL** (save it)

### Step 3: Deploy Backend to Render

1. Create `render.yaml` in your backend root:

```yaml
services:
  - type: web
    name: ai-resume-backend
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt && alembic upgrade head
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT --log-level info
    
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: ai-resume-db
          property: connectionString
      - key: REDIS_URL
        fromService:
          name: ai-resume-redis
          property: connectionString
      - key: ENVIRONMENT
        value: production
      - key: SECRET_KEY
        generateValue: true
      - key: OPENAI_API_KEY
        sync: false
      - key: STRIPE_API_KEY
        sync: false
      - key: MINIO_ENDPOINT
        value: s3.amazonaws.com  # or your MinIO host
      - key: MINIO_ACCESS_KEY
        sync: false
      - key: MINIO_SECRET_KEY
        sync: false
      - key: FRONTEND_URL
        value: https://your-frontend-url.vercel.app
```

2. Go to Render dashboard → **"+ New"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name:** `ai-resume-backend`
   - **Environment:** Python
   - **Build Command:** `pip install -r requirements.txt && alembic upgrade head`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT --log-level info`
   - **Plan:** Free
5. Add environment variables:
   - Copy all variables from `.env` except `DATABASE_URL`, `CELERY_BROKER`, `CELERY_BACKEND`
   - For those, use the URLs from your Render database/Redis
6. Click **Create Web Service**
7. Wait for deployment (5-10 minutes)
8. Copy the **Service URL** (e.g., `https://ai-resume-backend.onrender.com`)

### Step 4: Configure Environment Variables

On Render dashboard:

1. Go to your backend service → **Environment**
2. Add/update these variables:
   - `DATABASE_URL` → From PostgreSQL database
   - `REDIS_URL` → From Redis instance
   - `FRONTEND_URL` → `https://your-frontend.vercel.app`
   - `OPENAI_API_KEY` → Your OpenAI key
   - `STRIPE_API_KEY` → Your Stripe key
   - `MINIO_ENDPOINT` → S3 or MinIO URL
   - `MINIO_ACCESS_KEY` → S3/MinIO access key
   - `MINIO_SECRET_KEY` → S3/MinIO secret key

3. Click **Save** (triggers redeploy)

### Step 5: Verify Backend is Running

```bash
curl https://ai-resume-backend.onrender.com/health
```

Should return: `{"status": "ok", ...}`

---

## Vercel (Frontend)

**Vercel** is the easiest platform for Next.js and React apps. Free tier available.

### Step 1: Deploy Frontend to Vercel

1. Go to [vercel.com](https://vercel.com) and sign in with GitHub
2. Click **"Add New..."** → **"Project"**
3. Select your GitHub repo
4. Configure:
   - **Framework:** Vite (or detect automatically)
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
5. Add environment variables:
   ```
   VITE_API_URL=https://ai-resume-backend.onrender.com
   VITE_STRIPE_PUBLIC_KEY=your-stripe-public-key
   VITE_GOOGLE_CLIENT_ID=your-google-client-id
   ```
6. Click **Deploy**
7. Wait for deployment (2-5 minutes)
8. Copy your **Vercel URL** (e.g., `https://ai-resume.vercel.app`)

### Step 2: Update Backend Environment Variable

On Render backend service:

1. Go to **Environment**
2. Update `FRONTEND_URL` to your Vercel URL
3. Click **Save** (redeploy)

### Step 3: Configure CORS in Backend (if needed)

If you still get CORS errors, update `backend/app/main.py`:

```python
cors_origins = [settings.FRONTEND_URL]  # Restrict to your Vercel URL
```

---

## AWS (Alternative)

### Option A: AWS Elastic Beanstalk (Backend)

1. Install AWS CLI: `pip install awsebcli`
2. Initialize EB:
   ```bash
   eb init -p python-3.11 ai-resume-backend
   ```
3. Create environment:
   ```bash
   eb create ai-resume-backend-env
   ```
4. Set environment variables:
   ```bash
   eb setenv DATABASE_URL=... OPENAI_API_KEY=... STRIPE_API_KEY=...
   ```
5. Deploy:
   ```bash
   eb deploy
   ```

### Option B: AWS RDS + Lambda + API Gateway

For serverless approach, see [AWS Lambda Docs](https://docs.aws.amazon.com/lambda/latest/dg/).

---

## Netlify (Alternative Frontend)

If you prefer Netlify over Vercel:

1. Go to [netlify.com](https://netlify.com) and connect your GitHub
2. Create new site from your repo
3. Configure:
   - **Build Command:** `npm run build`
   - **Publish Directory:** `dist`
4. Add build environment variables:
   ```
   VITE_API_URL=https://ai-resume-backend.onrender.com
   VITE_STRIPE_PUBLIC_KEY=sk_live_...
   ```
5. Deploy

---

## Post-Deployment Testing

### 1. Test Backend Health

```bash
curl https://ai-resume-backend.onrender.com/health
curl https://ai-resume-backend.onrender.com/health/ready
curl https://ai-resume-backend.onrender.com/health/detailed
```

Expected response:
```json
{
  "status": "ok",
  "database": true,
  "minio": true,
  "timestamp": "2025-11-17T..."
}
```

### 2. Test API Documentation

Visit: `https://ai-resume-backend.onrender.com/docs`

Should show Swagger UI with all endpoints.

### 3. Test Frontend

Visit your Vercel/Netlify URL. Should load without errors.

### 4. Test Login (OAuth)

1. Click **Login** button
2. Try Google or GitHub OAuth
3. Verify you can log in and access dashboard

### 5. Test File Upload

1. Create a resume
2. Upload a file (tests MinIO/S3)
3. Should complete without errors

### 6. Check Logs

**Render Backend Logs:**
```
On Render dashboard → Backend Service → Logs
```

**Vercel Frontend Logs:**
```
On Vercel dashboard → Deployments → Logs
```

---

## Troubleshooting

### Backend won't start

**Error:** `Configuration error - missing DATABASE_URL`

**Fix:** On Render, go to **Environment** and add `DATABASE_URL` variable

---

### CORS errors on frontend

**Error:** `Access to XMLHttpRequest blocked by CORS`

**Fix:** Update `FRONTEND_URL` on Render backend to match your Vercel URL

---

### Database connection timeout

**Error:** `could not connect to database`

**Fix:** 
1. Check PostgreSQL service is running (Render dashboard)
2. Verify `DATABASE_URL` is correct
3. Check database firewall allows connections

---

### MinIO/S3 upload fails

**Error:** `S3Error: invalid credentials`

**Fix:**
1. Verify `MINIO_ACCESS_KEY` and `MINIO_SECRET_KEY` are correct
2. Check S3 bucket exists and is accessible
3. Verify IAM permissions (if using AWS)

---

### Migrations not running

**Error:** `Table not found` or `column does not exist`

**Fix:**
1. On Render, check deployment logs for migration errors
2. Manually run: `render-cli exec alembic upgrade head` 
3. Or redeploy from dashboard

---

### Redis connection fails

**Error:** `Cannot connect to Redis`

**Fix:**
1. If using Render Redis, check it's running
2. Verify `CELERY_BROKER` URL is correct
3. If no Redis needed, comment out Celery configuration

---

## Monitoring & Maintenance

### Set Up Alerts

**Render:**
- Dashboard → Service → Settings → Alerts
- Set up uptime monitoring

**Vercel:**
- Dashboard → Analytics
- Monitor deployment status

### Regular Maintenance

1. **Weekly:** Check logs for errors
2. **Monthly:** Review usage metrics
3. **Quarterly:** Update dependencies

---

## Next Steps

✅ Deployed to production!

Now:
1. Share your live URL with users
2. Set up error tracking (Sentry, Rollbar)
3. Configure analytics (Mixpanel, PostHog)
4. Monitor performance (New Relic, DataDog)
5. Set up backups for database

---

**Questions? Issues?** Open an issue on GitHub or check [Render Docs](https://render.com/docs) and [Vercel Docs](https://vercel.com/docs).
