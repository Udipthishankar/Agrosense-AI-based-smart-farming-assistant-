# 🚀 HEROKU DEPLOYMENT - QUICK START

## ✅ Prerequisites
- Heroku account (free at https://www.heroku.com)
- Heroku CLI installed
- Git installed
- Your code on GitHub or ready to push

## 📝 Step-by-Step Deployment (5 minutes)

### 1. Login to Heroku
```bash
heroku login
```
This opens browser for authentication. Approve and return to terminal.

### 2. Create Your App on Heroku
```bash
cd "path/to/Agrosense-AI-based-smart-farming-assistant-"
heroku create your-agrosense-app
```
Replace `your-agrosense-app` with your desired app name.

### 3. Initialize Git (if not already done)
```bash
git init
git add .
git commit -m "Prepare AgroSense for Heroku deployment"
```

### 4. Deploy to Heroku
```bash
git push heroku main
```
If your main branch is called `master`, use:
```bash
git push heroku master
```

### 5. Watch Deployment
```bash
heroku logs --tail
```
This shows real-time logs. Look for "Deployed successfully" message.

### 6. Open Your App
```bash
heroku open
```
Or visit: `https://your-agrosense-app.herokuapp.com`

## ✨ Your App is Live!

### Test Your Deployment
1. Open https://your-agrosense-app.herokuapp.com
2. Go to Crop AI - Enter soil data and test recommendation
3. Go to Weather - Check weather for your location
4. Go to Disease Detection - Upload a leaf image

### View Logs Anytime
```bash
heroku logs --tail
heroku logs --lines 50
```

### Check App Status
```bash
heroku ps
heroku config
```

## 🔧 Common Issues & Fixes

### Issue: "Module not found: backend"
**Fix:** Ensure `.` current directory is in Procfile:
```
web: gunicorn backend.app:app
```

### Issue: "Application Error" on Heroku
**Check logs:**
```bash
heroku logs --tail
```

### Issue: CORS Errors
**Verify:** Flask-CORS is in requirements.txt and `CORS(app)` is in app.py

### Issue: Static Files Not Loading
**Verify:** Frontend HTML files are in root directory accessible at:
- https://your-app.herokuapp.com/index.html
- https://your-app.herokuapp.com/crop.html

## 📊 Monitor Your App

### Set Custom Domain (Optional - Paid)
```bash
heroku domains:add www.yourdomain.com
```

### Setup Error Tracking
```bash
heroku addons:create sentry:free
```

### View Metrics
```bash
heroku metrics
```

## 💾 Data Persistence Issue

**Important:** Heroku has ephemeral storage. Files in `data/records.json` will be lost!

**Solution:** Migrate to PostgreSQL
```bash
# Add free Postgres
heroku addons:create heroku-postgresql:hobby-dev

# Update app.py to use PostgreSQL
# See DEPLOYMENT.md for database migration guide
```

## 🚀 Advanced: Setup CI/CD (Auto-Deploy)

### Enable GitHub Integration
1. In Heroku Dashboard
2. Go to Deploy tab
3. Connect to GitHub
4. Select your repository
5. Enable "Automatic deploys"

Now every push to GitHub automatically deploys!

## 📞 Need Help?

Check Heroku documentation: https://devcenter.heroku.com/

---

**Your App URL:** https://your-agrosense-app.herokuapp.com
**Dashboard:** https://dashboard.heroku.com/apps/your-agrosense-app

Happy Farming! 🌾
