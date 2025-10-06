# Render Deployment Guide

## Overview
This guide covers deploying the Multi-Sport Lineup Manager to Render's free tier.

## Prerequisites
- GitHub repository with your code
- Render account (free)
- TeamSnap API credentials

## Step 1: Prepare TeamSnap OAuth Application

1. Go to your TeamSnap OAuth application settings
2. Update the redirect URI to: `https://your-app-name.onrender.com/auth/callback`
   - Replace `your-app-name` with your actual Render service name
3. Save the changes

## Step 2: Deploy to Render

### Option A: Using render.yaml (Recommended)
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New" → "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect the `render.yaml` file
5. Click "Apply" to deploy

### Option B: Manual Setup
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `multisport-lineup-app` (or your preferred name)
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: `Free`

## Step 3: Set Environment Variables

In your Render service settings, add these environment variables:

### Required Variables
```
TEAMSNAP_CLIENT_ID=your_actual_teamsnap_client_id
TEAMSNAP_CLIENT_SECRET=your_actual_teamsnap_client_secret
SECRET_KEY=your_secure_random_secret_key_here
FLASK_ENV=production
```

### How to Generate SECRET_KEY
Run this in Python to generate a secure key:
```python
import secrets
print(secrets.token_hex(32))
```

## Step 4: Update TeamSnap Redirect URI

After your app is deployed, update your TeamSnap OAuth application:
1. Get your app URL from Render (e.g., `https://multisport-lineup-app.onrender.com`)
2. Update redirect URI to: `https://your-app-name.onrender.com/auth/callback`

## Step 5: Test Your Deployment

1. Visit your Render app URL
2. Test the OAuth login flow
3. Verify lineup generation works
4. Test with multiple users

## Important Notes

### Free Tier Limitations
- App sleeps after 15 minutes of inactivity
- 750 hours per month usage limit
- Cold start delay (10-30 seconds) when waking up

### App URLs
- Your app will be available at: `https://your-service-name.onrender.com`
- Render automatically provides SSL certificates

### Automatic Deployments
- Render automatically deploys when you push to your main branch
- Monitor deployments in the Render dashboard

## Troubleshooting

### Common Issues
1. **Build fails**: Check that all dependencies are in `requirements.txt`
2. **App won't start**: Verify `gunicorn app:app` can find your Flask app
3. **OAuth fails**: Ensure redirect URI exactly matches your Render URL
4. **Environment variables**: Make sure all required variables are set in Render dashboard

### Logs
- View real-time logs in the Render dashboard
- Check for startup errors or runtime issues

## Monitoring Usage

### Staying Within Free Limits
- Monitor usage in Render dashboard
- 750 hours ≈ 25 hours per day
- Typical baseball team usage: ~50-100 hours/month

### Performance Tips
- App wakes faster with lighter startup process
- Consider implementing keep-alive if needed (but uses more hours)

## Support

If you encounter issues:
1. Check Render documentation
2. Review app logs in Render dashboard
3. Verify TeamSnap API credentials are correct
4. Test locally first to isolate deployment issues