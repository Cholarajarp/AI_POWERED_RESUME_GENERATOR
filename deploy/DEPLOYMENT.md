# Deployment Guide

This guide covers deploying the AI Resume Agent to various platforms.

## 1. Deploy Backend to Render

### Prerequisites
- Render account (free tier available)
- PostgreSQL database (can use Render's managed Postgres)
- Redis instance (can use Render's managed Redis)

### Steps

1. **Connect GitHub Repository**
   - Go to https://dashboard.render.com
   - Click "New Web Service"
   - Connect your GitHub repository
   - Select the `main` branch

2. **Configure Environment Variables**
   ```
   DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database>
   SECRET_KEY=<generate-strong-random-key>
   OPENAI_API_KEY=<your-api-key>
   STRIPE_API_KEY=<your-stripe-key>
   STRIPE_WEBHOOK_SECRET=<your-webhook-secret>
   GITHUB_CLIENT_ID=<your-github-client-id>
   GITHUB_CLIENT_SECRET=<your-github-client-secret>
   REDIS_URL=redis://<host>:<port>
   MINIO_ENDPOINT=<minio-endpoint>
   FRONTEND_URL=https://<your-frontend-domain>
   ```

3. **Configure Build & Deploy Settings**
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port 8080`
   - Root Directory: `backend`

4. **Deploy**
   - Click "Create Web Service"
   - Render will automatically deploy on each push to main

## 2. Deploy Frontend to Vercel

### Prerequisites
- Vercel account (free tier available)
- GitHub repository connected

### Steps

1. **Import Project**
   - Go to https://vercel.com/new
   - Import your GitHub repository
   - Select `frontend` directory

2. **Configure Environment Variables**
   ```
   VITE_API_URL=https://<your-render-backend>.onrender.com
   VITE_GITHUB_CLIENT_ID=<your-github-client-id>
   VITE_GOOGLE_CLIENT_ID=<your-google-client-id>
   ```

3. **Deploy**
   - Click "Deploy"
   - Vercel will automatically deploy on each push

## 3. Deploy to AWS

### Prerequisites
- AWS account
- AWS CLI configured
- Docker installed
- ECR repository created

### Backend Deployment (ECS Fargate)

1. **Create ECR Repository**
   ```bash
   aws ecr create-repository --repository-name ai-resume-backend --region us-east-1
   ```

2. **Build and Push Docker Image**
   ```bash
   cd backend
   docker build -t ai-resume-backend .
   docker tag ai-resume-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/ai-resume-backend:latest
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
   docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/ai-resume-backend:latest
   ```

3. **Deploy to ECS**
   - Create ECS Cluster
   - Create Task Definition using ECR image
   - Create Service and specify task definition
   - Configure Application Load Balancer

### Frontend Deployment (S3 + CloudFront)

1. **Build Frontend**
   ```bash
   cd frontend
   npm run build
   ```

2. **Create S3 Bucket**
   ```bash
   aws s3 mb s3://ai-resume-frontend --region us-east-1
   ```

3. **Upload to S3**
   ```bash
   aws s3 sync dist s3://ai-resume-frontend --delete
   ```

4. **Create CloudFront Distribution**
   - Create distribution pointing to S3 bucket
   - Configure SSL/TLS certificate
   - Add custom domain

## 4. Deploy to Netlify

### Prerequisites
- Netlify account
- GitHub repository connected

### Steps

1. **Connect Repository**
   - Go to https://app.netlify.com
   - Click "Add new site"
   - Select "Import an existing project"
   - Choose GitHub and your repository

2. **Configure Build Settings**
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `dist`

3. **Set Environment Variables**
   - Go to Site Settings > Build & Deploy > Environment
   - Add required environment variables

4. **Deploy**
   - Save settings
   - Netlify will automatically deploy

## Database Setup

### PostgreSQL on Render
1. Create new Postgres instance from Render dashboard
2. Copy connection string to `DATABASE_URL`

### PostgreSQL on AWS RDS
```bash
aws rds create-db-instance \
  --db-instance-identifier ai-resume-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username postgres \
  --master-user-password <password>
```

## Monitoring & Logs

### Render
- Logs available in Render dashboard under service logs
- Use Render's integrated metrics for monitoring

### Vercel
- Logs available in Vercel dashboard
- Real-time monitoring and analytics

### AWS
- CloudWatch for logs
- CloudWatch Alarms for monitoring
- X-Ray for distributed tracing

## Domain Setup

### Point Domain to Deployed Services
1. Update DNS records to point to your deployed services
2. For Render backend: use the render.com domain
3. For Vercel/Netlify frontend: use the provided domain or CNAME

## Security Checklist

- [ ] Change all default secrets and API keys
- [ ] Enable HTTPS/SSL everywhere
- [ ] Set up WAF rules
- [ ] Configure CORS properly
- [ ] Enable database encryption
- [ ] Set up rate limiting
- [ ] Enable API authentication
- [ ] Configure backup strategies
- [ ] Set up monitoring and alerts
- [ ] Review security group rules
