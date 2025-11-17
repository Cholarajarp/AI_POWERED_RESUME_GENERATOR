# ✅ DEPLOYMENT CHECKLIST

## Pre-Deployment (Before You Start)

- [ ] Read QUICK_DEPLOY.md
- [ ] Have GitHub account ready (already have)
- [ ] Have free email for Render/Vercel
- [ ] Docker services verified locally ✅
- [ ] All 8 fixes confirmed working ✅

---

## Backend Deployment to Render (15 minutes)

### Step 1: Create Render Account
- [ ] Go to https://render.com
- [ ] Sign up with GitHub
- [ ] Authorize access to repos

### Step 2: Deploy PostgreSQL
- [ ] Click "New +" → "PostgreSQL"
- [ ] Name: `resume-agent-db`
- [ ] Click "Create Database"
- [ ] ⏳ Wait 2-5 minutes
- [ ] Copy **Internal Database URL**
- [ ] Note the URL somewhere safe

### Step 3: Deploy Backend Service
- [ ] Click "New +" → "Web Service"
- [ ] Select: `AI_POWERED_RESUME_GENERATOR` repo
- [ ] Root Directory: `backend`
- [ ] Build Command: `pip install -r requirements.txt`
- [ ] Start Command: `./scripts/start.sh`
- [ ] Click "Create Web Service"
- [ ] ⏳ Wait 3-5 minutes for build

### Step 4: Set Environment Variables
In Render dashboard, add these:
- [ ] `DATABASE_URL` = (from Step 2)
- [ ] `MINIO_ENDPOINT` = `minio:9000`
- [ ] `MINIO_ACCESS_KEY` = `minioadmin`
- [ ] `MINIO_SECRET_KEY` = `minioadmin`
- [ ] `REDIS_URL` = `redis://redis:6379`
- [ ] (Optional) `STRIPE_API_KEY`
- [ ] (Optional) `GOOGLE_CLIENT_ID`
- [ ] (Optional) `GOOGLE_CLIENT_SECRET`

### Step 5: Verify Backend
- [ ] Copy Backend URL from Render
- [ ] Test: `https://your-backend.onrender.com/health`
- [ ] Should see: `{"status":"ok",...}`
- [ ] ✅ Backend is live!

**Estimated Time:** 15-20 minutes

---

## Frontend Deployment to Vercel (10 minutes)

### Step 1: Create Vercel Account
- [ ] Go to https://vercel.com
- [ ] Sign up with GitHub
- [ ] Authorize access to repos

### Step 2: Import Project
- [ ] Click "Add New" → "Project"
- [ ] Select: `AI_POWERED_RESUME_GENERATOR` repo
- [ ] Click "Import"

### Step 3: Configure Project
- [ ] Root Directory: `frontend`
- [ ] Framework: `Vite`
- [ ] Build Command: `npm run build`
- [ ] Output Directory: `dist`
- [ ] Click "Deploy"
- [ ] ⏳ Wait 1-2 minutes

### Step 4: Set Environment Variables
In Vercel dashboard:
- [ ] Go to Settings → Environment Variables
- [ ] Add: `VITE_API_URL` = `https://your-backend.onrender.com`
- [ ] Save and redeploy

### Step 5: Verify Frontend
- [ ] Copy Frontend URL from Vercel
- [ ] Open in browser: `https://your-frontend.vercel.app`
- [ ] Should see your React app
- [ ] ✅ Frontend is live!

**Estimated Time:** 10-15 minutes

---

## Post-Deployment Verification (5 minutes)

### Check Backend Health
- [ ] Open: `https://your-backend.onrender.com/health`
- [ ] See: `{"status":"ok"}`
- [ ] ✅ Backend responding

### Check Frontend Loading
- [ ] Open: `https://your-frontend.vercel.app`
- [ ] See: Your React app loads
- [ ] ✅ Frontend rendering

### Check API Communication
- [ ] Open frontend URL
- [ ] Open DevTools (F12)
- [ ] Click Network tab
- [ ] Try any API action (if available)
- [ ] Check that request goes to `your-backend.onrender.com`
- [ ] Should see 2xx response
- [ ] ✅ Frontend talking to Backend

### Check for CORS Errors
- [ ] Open DevTools Console
- [ ] Should NOT see "CORS error"
- [ ] ✅ CORS configured correctly

---

## Troubleshooting

### Backend won't start
**Check:**
- [ ] Render logs show error message
- [ ] DATABASE_URL is correct
- [ ] All required env vars are set
- [ ] PostgreSQL database exists

**Fix:**
- [ ] Add missing env var to Render
- [ ] Redeploy from Render dashboard
- [ ] Check logs again

### Frontend shows blank page
**Check:**
- [ ] Browser console for errors
- [ ] DevTools Network tab
- [ ] `VITE_API_URL` is set correctly

**Fix:**
- [ ] Update `VITE_API_URL` in Vercel
- [ ] Redeploy from Vercel dashboard
- [ ] Clear browser cache (Cmd+Shift+Delete)

### Frontend can't reach Backend
**Check:**
- [ ] `VITE_API_URL` matches backend URL
- [ ] Test backend directly: `https://backend.onrender.com/health`
- [ ] Check DevTools Console for CORS errors

**Fix:**
- [ ] Update environment variable
- [ ] Redeploy frontend
- [ ] Check that backend is running

---

## Success Criteria

You'll know it works when:

✅ All checkboxes above are checked
✅ Frontend loads without errors
✅ Backend health endpoint responds
✅ No CORS errors in browser console
✅ Can navigate frontend app
✅ Health check shows all dependencies ready

---

## After Success

1. **Save Your URLs**
   - Frontend: `https://...`
   - Backend: `https://...`

2. **Test Core Features**
   - Create test account
   - Upload test file
   - Test all functionality

3. **Monitor Deployment**
   - Check Render logs daily first week
   - Check Vercel analytics
   - Monitor error rates

4. **Upgrade Later**
   - Add custom domain
   - Connect database to better service
   - Add S3 storage
   - Set up error tracking

---

## Total Deployment Time

- Pre-deployment checks: 2 min ✓
- Backend to Render: 15 min
- Frontend to Vercel: 10 min
- Verification: 5 min
- **Total: 32 minutes**

---

## Common Commands

**To view Render logs:**
1. Go to Render Dashboard
2. Click your Web Service
3. Go to "Logs" tab
4. See real-time logs

**To restart service:**
1. Go to Render Dashboard
2. Click your service
3. Click "Restart service"
4. Wait for restart

**To update environment variables:**
1. Go to Render/Vercel Dashboard
2. Go to Settings → Environment Variables
3. Update value
4. Redeploy

---

**Status:** Ready for deployment ✅
**Difficulty:** Easy
**Assistance:** Follow QUICK_DEPLOY.md step by step
