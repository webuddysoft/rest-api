# Railway Deployment Guide

## Quick Start

### 1. Prepare Your Repository
Make sure your code is pushed to GitHub with the following files:
- `railway.json` ✅
- `Procfile` ✅
- `requirements.txt` ✅
- `database.py` (updated for Railway) ✅

### 2. Deploy to Railway

1. **Visit Railway**: Go to [railway.app](https://railway.app) and sign in with GitHub

2. **Create New Project**: Click "New Project" → "Deploy from GitHub repo"

3. **Select Repository**: Choose your `rest-api` repository

4. **Add MySQL Database**:
   - In your project, click "New Service" → "Database" → "MySQL"
   - Wait for the database to be created
   - Copy the `DATABASE_URL` from the MySQL service variables

5. **Configure Environment Variables**:
   - Go to your application service settings
   - Add these variables:
     ```
     MYSQL_PUBLIC_URL=mysql://username:password@host:port/database
     SECRET_KEY=your-super-secure-secret-key-here
     ```
   - Note: You can also use `DATABASE_URL` as an alternative

6. **Deploy**: Railway will automatically build and deploy your application

### 3. Test Your Deployment

Once deployed, you can test your API:

```bash
# Health check
curl https://your-app-name.railway.app/health

# Create a user
curl -X POST "https://your-app-name.railway.app/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

### 4. Access API Documentation

- **Swagger UI**: `https://your-app-name.railway.app/docs`
- **ReDoc**: `https://your-app-name.railway.app/redoc`

## Troubleshooting

### Common Issues

1. **Database Connection Error**:
   - Ensure `MYSQL_PUBLIC_URL` (or `DATABASE_URL`) is correctly set
   - Check that the MySQL service is running
   - Verify SSL configuration in `database.py`

2. **Build Failures**:
   - Check that all dependencies are in `requirements.txt`
   - Ensure Python version compatibility

3. **Environment Variables**:
   - Make sure `MYSQL_PUBLIC_URL` (or `DATABASE_URL`) and `SECRET_KEY` are set
   - Check for typos in variable names

### Railway CLI (Optional)

You can also deploy using Railway CLI:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Deploy
railway up
```

## Monitoring

- **Logs**: View application logs in Railway dashboard
- **Metrics**: Monitor performance and usage
- **Database**: Access MySQL database through Railway dashboard

## Scaling

Railway automatically scales your application based on traffic. You can also manually adjust resources in the dashboard. 