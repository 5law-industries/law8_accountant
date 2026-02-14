# Deploying 8law Accountant to Google Cloud

This guide provides step-by-step instructions for deploying the 8law Accountant application to Google Cloud Platform (GCP).

## Table of Contents
- [Prerequisites](#prerequisites)
- [Deployment Options](#deployment-options)
- [Option 1: Google Cloud Run (Recommended)](#option-1-google-cloud-run-recommended)
- [Option 2: Google App Engine](#option-2-google-app-engine)
- [Option 3: Using Cloud Build for CI/CD](#option-3-using-cloud-build-for-cicd)
- [Environment Variables](#environment-variables)
- [Post-Deployment](#post-deployment)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before deploying, ensure you have:

1. **Google Cloud Account**: Create one at [cloud.google.com](https://cloud.google.com)
2. **Google Cloud Project**: Create a new project or use an existing one
3. **Google Cloud SDK**: Install from [cloud.google.com/sdk](https://cloud.google.com/sdk/docs/install)
4. **Docker** (for local testing): Install from [docker.com](https://www.docker.com/get-started)
5. **Required API Keys**:
   - Supabase URL and anon key
   - hCaptcha site and secret keys
   - OpenAI API key
   - Pinecone API key (if using vector features)

### Initial Setup

1. **Authenticate with Google Cloud**:
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```

2. **Set your project**:
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **Enable required APIs**:
   ```bash
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable run.googleapis.com
   gcloud services enable containerregistry.googleapis.com
   gcloud services enable secretmanager.googleapis.com
   ```

---

## Deployment Options

### Option 1: Google Cloud Run (Recommended)

**Best for**: Auto-scaling, serverless deployment with minimal management

#### Step 1: Build the Docker Image

```bash
# Build the Docker image locally (optional, for testing)
docker build -t law8-accountant .

# Test locally (optional)
docker run -p 8080:8080 \
  -e SUPABASE_URL=your-url \
  -e SUPABASE_ANON_KEY=your-key \
  law8-accountant
```

#### Step 2: Push to Google Container Registry

```bash
# Tag the image for GCR
docker tag law8-accountant gcr.io/YOUR_PROJECT_ID/law8-accountant:latest

# Configure Docker to use gcloud as credential helper
gcloud auth configure-docker

# Push to GCR
docker push gcr.io/YOUR_PROJECT_ID/law8-accountant:latest
```

#### Step 3: Deploy to Cloud Run

```bash
gcloud run deploy law8-accountant \
  --image gcr.io/YOUR_PROJECT_ID/law8-accountant:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 2Gi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 10 \
  --timeout 300 \
  --set-env-vars "STREAMLIT_SERVER_PORT=8080,STREAMLIT_SERVER_ADDRESS=0.0.0.0,STREAMLIT_SERVER_HEADLESS=true"
```

#### Step 4: Set Secrets via Secret Manager (Recommended)

```bash
# Create secrets
echo -n "your-supabase-url" | gcloud secrets create supabase-url --data-file=-
echo -n "your-supabase-key" | gcloud secrets create supabase-anon-key --data-file=-
echo -n "your-openai-key" | gcloud secrets create openai-api-key --data-file=-
echo -n "your-hcaptcha-site-key" | gcloud secrets create hcaptcha-site-key --data-file=-
echo -n "your-hcaptcha-secret" | gcloud secrets create hcaptcha-secret-key --data-file=-

# Grant Cloud Run access to secrets
gcloud secrets add-iam-policy-binding supabase-url \
  --member="serviceAccount:YOUR_PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# Repeat for other secrets...

# Update Cloud Run to use secrets
gcloud run services update law8-accountant \
  --update-secrets="SUPABASE_URL=supabase-url:latest" \
  --update-secrets="SUPABASE_ANON_KEY=supabase-anon-key:latest" \
  --update-secrets="OPENAI_API_KEY=openai-api-key:latest" \
  --update-secrets="HCAPTCHA_SITE_KEY=hcaptcha-site-key:latest" \
  --update-secrets="HCAPTCHA_SECRET_KEY=hcaptcha-secret-key:latest" \
  --region us-central1
```

#### Alternative: Set Environment Variables Directly

```bash
gcloud run services update law8-accountant \
  --update-env-vars "SUPABASE_URL=your-url,SUPABASE_ANON_KEY=your-key,OPENAI_API_KEY=your-key" \
  --region us-central1
```

⚠️ **Warning**: Direct environment variables are visible in the Cloud Console. Use Secret Manager for sensitive data.

---

### Option 2: Google App Engine

**Best for**: Traditional managed hosting with less configuration

#### Step 1: Update app.yaml

Edit `app.yaml` and add your environment variables (or use Secret Manager).

#### Step 2: Deploy

```bash
gcloud app deploy app.yaml
```

#### Step 3: View Your Application

```bash
gcloud app browse
```

---

### Option 3: Using Cloud Build for CI/CD

**Best for**: Automated deployments from Git repository

#### Step 1: Connect Your Repository

1. Go to [Cloud Build Triggers](https://console.cloud.google.com/cloud-build/triggers)
2. Click "Connect Repository"
3. Select your Git provider (GitHub, GitLab, etc.)
4. Authorize and select your repository

#### Step 2: Create a Build Trigger

1. Click "Create Trigger"
2. Configure:
   - **Name**: `deploy-law8-accountant`
   - **Event**: Push to a branch
   - **Branch**: `^main$` (or your production branch)
   - **Build Configuration**: Cloud Build configuration file
   - **Cloud Build configuration file location**: `/cloudbuild.yaml`

#### Step 3: Set Up Substitution Variables

Add these substitution variables in the trigger:
- `_REGION`: `us-central1`
- `_SERVICE_NAME`: `law8-accountant`

#### Step 4: Push to Trigger Deployment

```bash
git push origin main
```

Cloud Build will automatically:
1. Build the Docker image
2. Push to Container Registry
3. Deploy to Cloud Run

---

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SUPABASE_URL` | Your Supabase project URL | `https://xxx.supabase.co` |
| `SUPABASE_ANON_KEY` | Supabase anonymous/public key | `eyJhbG...` |
| `HCAPTCHA_SITE_KEY` | hCaptcha site key for CAPTCHA | `10000000-...` |
| `HCAPTCHA_SECRET_KEY` | hCaptcha secret key | `0x...` |
| `OPENAI_API_KEY` | OpenAI API key for AI features | `sk-...` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PINECONE_API_KEY` | Pinecone API key for vector DB | - |
| `PINECONE_ENVIRONMENT` | Pinecone environment | - |
| `DEBUG` | Enable debug mode | `false` |

### Streamlit Variables (Usually Auto-Set)

These are typically set in the Dockerfile:
- `STREAMLIT_SERVER_PORT=8080`
- `STREAMLIT_SERVER_ADDRESS=0.0.0.0`
- `STREAMLIT_SERVER_HEADLESS=true`
- `STREAMLIT_BROWSER_GATHER_USAGE_STATS=false`

---

## Post-Deployment

### 1. Get Your Application URL

**Cloud Run:**
```bash
gcloud run services describe law8-accountant --region us-central1 --format 'value(status.url)'
```

**App Engine:**
```bash
gcloud app browse
```

### 2. Set Up Custom Domain (Optional)

#### For Cloud Run:

```bash
gcloud beta run domain-mappings create --service law8-accountant --domain your-domain.com --region us-central1
```

Then add DNS records as instructed by GCP.

#### For App Engine:

1. Go to [App Engine Settings](https://console.cloud.google.com/appengine/settings/domains)
2. Click "Add a custom domain"
3. Follow the verification and DNS setup instructions

### 3. Configure HTTPS/SSL

Both Cloud Run and App Engine automatically provide HTTPS with managed certificates for custom domains.

### 4. Set Up Monitoring

```bash
# Enable Cloud Monitoring
gcloud services enable monitoring.googleapis.com

# Create uptime check
gcloud monitoring uptime create law8-accountant-uptime \
  --resource-type=uptime-url \
  --resource-url="https://your-app-url.com/_stcore/health"
```

### 5. View Logs

**Cloud Run:**
```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=law8-accountant" --limit 50 --format json
```

**App Engine:**
```bash
gcloud app logs tail -s default
```

Or view in [Cloud Console Logs Explorer](https://console.cloud.google.com/logs).

---

## Troubleshooting

### Common Issues

#### 1. Container Fails to Start

**Symptoms**: Deployment succeeds but service won't start

**Solutions**:
- Check logs: `gcloud run logs read --service law8-accountant --region us-central1`
- Verify port 8080 is exposed and Streamlit is binding to it
- Check environment variables are set correctly
- Ensure all required dependencies are in requirements.txt

#### 2. "Module Not Found" Errors

**Solution**: Verify all imports in main.py are correct and dependencies are in requirements.txt

#### 3. Authentication Not Working

**Solutions**:
- Verify Supabase credentials are correct
- Check hCaptcha keys are properly configured
- Ensure secrets are accessible by the service account

#### 4. Memory/CPU Limits Exceeded

**Solution**: Increase resources in deployment:
```bash
gcloud run services update law8-accountant \
  --memory 4Gi \
  --cpu 2 \
  --region us-central1
```

#### 5. Slow Cold Starts

**Solutions**:
- Set minimum instances: `--min-instances 1`
- Use Cloud Run second generation execution environment
- Optimize Docker image size

### Getting Help

- Check [Cloud Run documentation](https://cloud.google.com/run/docs)
- View [Streamlit deployment guides](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)
- Search [Stack Overflow](https://stackoverflow.com/questions/tagged/google-cloud-run)

---

## Cost Optimization

### Cloud Run Pricing Tips

1. **Use minimum instances**: Set to 0 for development, 1+ for production
2. **Right-size resources**: Start with 1 CPU / 2GB RAM, adjust based on usage
3. **Enable request timeout**: Use `--timeout` to prevent long-running requests
4. **Use Cloud CDN**: Cache static assets for faster delivery

### Estimated Costs (as of 2026)

**Cloud Run**:
- First 2 million requests/month: Free
- After that: ~$0.40 per million requests
- CPU: ~$0.00002400 per vCPU-second
- Memory: ~$0.00000250 per GB-second

**App Engine** (Flexible):
- ~$0.05 per core-hour
- Minimum 1 instance = ~$36/month

👉 Use [GCP Pricing Calculator](https://cloud.google.com/products/calculator) for accurate estimates.

---

## Security Best Practices

1. ✅ Use Secret Manager for all sensitive credentials
2. ✅ Enable Cloud Armor for DDoS protection
3. ✅ Configure VPC Service Controls if handling sensitive data
4. ✅ Set up Cloud IAM with least-privilege access
5. ✅ Enable Cloud Audit Logs
6. ✅ Use HTTPS only (default for Cloud Run and App Engine)
7. ✅ Implement rate limiting in your Streamlit app
8. ✅ Regularly update dependencies: `pip list --outdated`

---

## Quick Reference

### Essential Commands

```bash
# Deploy to Cloud Run
gcloud run deploy law8-accountant --image gcr.io/PROJECT_ID/law8-accountant --region us-central1

# View logs
gcloud run logs read --service law8-accountant --region us-central1

# Update environment variables
gcloud run services update law8-accountant --update-env-vars KEY=VALUE --region us-central1

# Scale service
gcloud run services update law8-accountant --min-instances 1 --max-instances 10 --region us-central1

# Get service URL
gcloud run services describe law8-accountant --region us-central1 --format 'value(status.url)'

# Delete service
gcloud run services delete law8-accountant --region us-central1
```

---

## Next Steps

After successful deployment:

1. ✅ Test all application features
2. ✅ Configure monitoring and alerting
3. ✅ Set up automated backups for Supabase
4. ✅ Implement CI/CD pipeline with Cloud Build
5. ✅ Configure custom domain and SSL
6. ✅ Set up staging and production environments
7. ✅ Document your deployment process

---

**Need Help?** Create an issue in the repository or contact the development team.

**Last Updated**: February 2026
