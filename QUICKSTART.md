# Quick Start Guide - Google Cloud Deployment

## 🚀 Deploy to Google Cloud in 5 Minutes

### Prerequisites
- Google Cloud account
- `gcloud` CLI installed
- Docker installed (for testing)

### Option A: Deploy with Cloud Run (Fastest)

```bash
# 1. Set your project
gcloud config set project YOUR_PROJECT_ID

# 2. Build and deploy in one command
gcloud run deploy law8-accountant \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080

# 3. Set your secrets
gcloud run services update law8-accountant \
  --update-env-vars "SUPABASE_URL=your-url,SUPABASE_ANON_KEY=your-key" \
  --region us-central1

# 4. Get your URL
gcloud run services describe law8-accountant --region us-central1 --format 'value(status.url)'
```

### Option B: Using Dockerfile

```bash
# 1. Build
docker build -t gcr.io/YOUR_PROJECT_ID/law8-accountant .

# 2. Push
docker push gcr.io/YOUR_PROJECT_ID/law8-accountant

# 3. Deploy
gcloud run deploy law8-accountant \
  --image gcr.io/YOUR_PROJECT_ID/law8-accountant \
  --region us-central1
```

### Option C: App Engine

```bash
# 1. Update app.yaml with your settings
# 2. Deploy
gcloud app deploy
```

## 📚 Full Documentation

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete instructions, troubleshooting, and advanced configuration.

## 🔐 Environment Variables Required

- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `HCAPTCHA_SITE_KEY`
- `HCAPTCHA_SECRET_KEY`
- `OPENAI_API_KEY`

Copy `.env.example` to `.env` and fill in your values for local development.

## ✅ Verify Deployment

After deployment, test:
- Main page loads: `https://your-app-url.com`
- Health check: `https://your-app-url.com/_stcore/health`
- Authentication works

## 🆘 Need Help?

- View logs: `gcloud run logs read --service law8-accountant`
- Check status: `gcloud run services describe law8-accountant`
- See full guide: [DEPLOYMENT.md](DEPLOYMENT.md)
