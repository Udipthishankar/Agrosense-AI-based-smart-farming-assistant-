# 🚀 AGROSENSE DEPLOYMENT GUIDE

Complete guide to deploy AgroSense to production.

---

## **📋 TABLE OF CONTENTS**
1. [Heroku Deployment (EASIEST)](#heroku-deployment)
2. [Railway Deployment](#railway-deployment)
3. [Render Deployment](#render-deployment)
4. [AWS Deployment](#aws-deployment)
5. [DigitalOcean VPS](#digitalocean-vps)
6. [Local Ngrok (Testing)](#local-ngrok)
7. [Production Checklist](#production-checklist)

---

## **🟣 HEROKU DEPLOYMENT** (RECOMMENDED - EASIEST)

### **Step 1: Prerequisites**
```bash
# Install Heroku CLI
# Windows: Download from https://devcenter.heroku.com/articles/heroku-cli
# Or use chocolatey: choco install heroku-cli

# Verify installation
heroku --version
```

### **Step 2: Prepare Your App**

**A) Update Python Runtime (Create `runtime.txt` in root)**
```
python-3.11.0
```

**B) Add Procfile (in root directory)**
```
web: gunicorn backend.app:app
```

**C) Create `.gitignore` (in root)**
```
__pycache__/
*.pyc
.DS_Store
.env
venv/
*.log
.pytest_cache/
.vscode/
node_modules/
```

**D) Initialize Git Repository**
```bash
git init
git add .
git commit -m "Initial commit for AgroSense"
```

### **Step 3: Update Backend for Production**

**Edit `backend/app.py` - Change last line:**
```python
# OLD:
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# NEW:
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

**Edit `backend/requirements.txt` - Add gunicorn:**
```
Flask==2.3.3
Flask-CORS==4.0.0
python-dotenv==1.0.0
numpy==1.24.3
requests==2.31.0
Pillow==10.0.0
scikit-learn==1.3.0
gunicorn==21.2.0
```

### **Step 4: Update Frontend for Production**

**Edit all HTML files (crop.html, weather.html, disease.html)**

Replace:
```javascript
const API_URL = 'http://localhost:5000';
```

With:
```javascript
const API_URL = window.location.origin;
// This automatically uses the same domain as frontend
```

### **Step 5: Deploy to Heroku**

```bash
# Login to Heroku
heroku login

# Create app on Heroku
heroku create your-agrosense-app

# Deploy
git push heroku main
# (or 'master' if your main branch is called master)

# View logs
heroku logs --tail

# Open app in browser
heroku open
```

### **Step 6: Verify Deployment**
```bash
# Check app status
heroku ps:scale web=1

# View environment variables
heroku config
```

**✅ Your app is live at:** `https://your-agrosense-app.herokuapp.com`

---

## **🚂 RAILWAY DEPLOYMENT** (SIMPLE ALTERNATIVE)

### **Step 1: Prerequisites**
- GitHub account
- Push code to GitHub

### **Step 2: Connect to Railway**

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub"
4. Authorize GitHub
5. Select your `Agrosense-AI-based-smart-farming-assistant-` repository

### **Step 3: Configure**

1. Add `Procfile` (same as Heroku):
```
web: gunicorn backend.app:app
```

2. Add `runtime.txt`:
```
python-3.11.0
```

3. Set environment variables in Railway dashboard:
   - `FLASK_ENV = production`
   - `PYTHON_VERSION = 3.11.0`

### **Step 4: Deploy**
- Railway automatically deploys on push to GitHub
- View logs in dashboard
- Get your production URL from Railway dashboard

---

## **🎨 RENDER DEPLOYMENT**

### **Step 1: Connect GitHub**
1. Go to https://render.com
2. Sign up and connect GitHub

### **Step 2: Create Web Service**
1. Click "New +"
2. Select "Web Service"
3. Connect your GitHub repo

### **Step 3: Configure**
```
Name: agrosense
Runtime: Python 3
Build Command: pip install -r backend/requirements.txt
Start Command: gunicorn backend.app:app
```

### **Step 4: Deploy**
- Render auto-deploys on push
- Check build logs in dashboard

---

## **☁️ AWS DEPLOYMENT** (PROFESSIONAL)

### **Option A: AWS Elastic Beanstalk (Easiest AWS option)**

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.11 agrosense --region us-east-1

# Create environment
eb create agrosense-env

# Deploy
eb deploy

# Open in browser
eb open
```

### **Option B: EC2 + RDS**

This is more complex - requires:
- Launch EC2 instance (Ubuntu)
- Install Python, Nginx, Gunicorn
- Configure Nginx as reverse proxy
- Set up SSL with Let's Encrypt
- Configure RDS database

**See detailed instructions below in manual setup section.**

---

## **🌊 DIGITALOCEAN VPS DEPLOYMENT**

### **Step 1: Create Droplet**
1. Go to DigitalOcean.com ($5/month droplet)
2. Create Ubuntu 22.04 LTS Droplet
3. Add SSH key
4. Create droplet

### **Step 2: SSH into Server**
```bash
ssh root@your_droplet_ip
```

### **Step 3: Install Dependencies**
```bash
apt update && apt upgrade -y
apt install -y python3 python3-pip python3-venv nginx git
```

### **Step 4: Clone Your Repository**
```bash
cd /var/www
git clone https://github.com/your-username/Agrosense-AI-based-smart-farming-assistant-.git
cd Agrosense-AI-based-smart-farming-assistant-
```

### **Step 5: Setup Python Environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

### **Step 6: Configure Gunicorn**

**Create `/etc/systemd/system/agrosense.service`:**
```ini
[Unit]
Description=AgroSense Flask Application
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/Agrosense-AI-based-smart-farming-assistant-
Environment="PATH=/var/www/Agrosense-AI-based-smart-farming-assistant-/venv/bin"
ExecStart=/var/www/Agrosense-AI-based-smart-farming-assistant-/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 backend.app:app

[Install]
WantedBy=multi-user.target
```

### **Step 7: Configure Nginx**

**Create `/etc/nginx/sites-available/agrosense`:**
```nginx
server {
    listen 80;
    server_name your_domain.com www.your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location ~* ^/(crop|weather|disease|about|index|style)\.* {
        root /var/www/Agrosense-AI-based-smart-farming-assistant-;
        try_files $uri =404;
    }
}
```

**Enable site:**
```bash
ln -s /etc/nginx/sites-available/agrosense /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### **Step 8: Start Services**
```bash
systemctl start agrosense
systemctl enable agrosense
```

### **Step 9: Setup SSL (FREE with Let's Encrypt)**
```bash
apt install certbot python3-certbot-nginx -y
certbot --nginx -d your_domain.com
```

---

## **🔗 LOCAL NGROK DEPLOYMENT** (QUICK TESTING)

Perfect for quick demo without buying servers!

### **Step 1: Install Ngrok**
```bash
# Download from https://ngrok.com/download
# Or: choco install ngrok

# Verify
ngrok version
```

### **Step 2: Start Backend**
```bash
cd backend
python app.py
# Runs on http://localhost:5000
```

### **Step 3: Expose with Ngrok**
```bash
ngrok http 5000
```

**You'll get:** `https://your-random-id.ngrok.io`

### **Step 4: Update Frontend**
Change in all HTML files:
```javascript
const API_URL = 'https://your-random-id.ngrok.io';
```

### **Step 5: Open Frontend**
```bash
Open index.html in browser - it's now accessible from anywhere!
```

**⚠️ Note:** Ngrok URL changes when you restart. Use for testing only.

---

## **✅ PRODUCTION CHECKLIST**

### **Security**
- [ ] Disable Flask debug mode (`debug=False`)
- [ ] Set strong `SECRET_KEY` in environment
- [ ] Use HTTPS/SSL certificate
- [ ] Add rate limiting to API endpoints
- [ ] Validate all user inputs
- [ ] Use environment variables for sensitive data

### **Performance**
- [ ] Use production WSGI server (Gunicorn, uWSGI)
- [ ] Enable compression in Nginx
- [ ] Set up CDN for static files
- [ ] Implement caching headers
- [ ] Use database connection pooling

### **Monitoring**
- [ ] Setup error logging (Sentry)
- [ ] Monitor server health
- [ ] Setup uptime monitoring
- [ ] Monitor database performance
- [ ] Setup alerts for errors

### **Backup & Disaster Recovery**
- [ ] Daily database backups
- [ ] Version control all code
- [ ] Document deployment process
- [ ] Maintain rollback procedure
- [ ] Test recovery process

### **Frontend**
- [ ] Minify CSS/JS
- [ ] Optimize images
- [ ] Enable caching
- [ ] Test on different browsers
- [ ] Test mobile responsiveness

### **Database**
- [ ] Ensure `data/records.json` is writable
- [ ] Or migrate to cloud database (Heroku Postgres, AWS RDS)
- [ ] Setup regular backups
- [ ] Test data persistence

### **DNS & Domain**
- [ ] Register domain name
- [ ] Point DNS to your server
- [ ] Setup SSL certificate
- [ ] Configure email (optional)

---

## **📚 QUICK START: RECOMMENDED PATH**

### **For Quick Demo (5 minutes):**
```bash
# Use Ngrok
pip install pyngrok
python -m pyngrok.pyngrok http 5000
```

### **For Small Scale (Free/Cheap):**
```bash
# Use Heroku or Railway
# Follow respective sections above
```

### **For Medium Scale ($5-50/month):**
```bash
# Use DigitalOcean or Render
# Full control, good performance
```

### **For Enterprise (Scalable):**
```bash
# Use AWS with RDS database
# Auto-scaling, multiple regions
```

---

## **🆘 TROUBLESHOOTING**

### **"ModuleNotFoundError: No module named 'backend'"**
- Make sure `backend` folder has `__init__.py` (empty file)
- Update Procfile to: `web: gunicorn -w 4 -b 0.0.0.0:$PORT backend.app:app`

### **CORS Errors in Production**
- Ensure `Flask-CORS` is installed
- Check that `CORS(app)` is in app.py

### **Static Files Not Loading**
- Ensure frontend HTML/CSS is in correct folder
- Configure web server to serve static files

### **Database/Records Not Saving**
- Check file permissions on `data/` folder
- Ensure `data/records.json` exists and is writable
- Consider migrating to cloud database

### **Slow Performance**
- Enable Gzip compression
- Use CDN for static files
- Optimize database queries
- Scale up server resources

---

## **📖 NEXT STEPS**

1. Choose deployment option based on your needs
2. Follow step-by-step instructions above
3. Test the deployed app thoroughly
4. Setup monitoring and logging
5. Configure backups
6. Go live! 🎉

**Questions?** Check platform-specific documentation:
- Heroku: https://devcenter.heroku.com/
- Railway: https://docs.railway.app/
- Render: https://render.com/docs
- AWS: https://docs.aws.amazon.com/
- DigitalOcean: https://docs.digitalocean.com/

---

**Happy Deploying! 🚀**
