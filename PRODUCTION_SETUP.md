# 🏗️ PRODUCTION SETUP GUIDE

Complete guide to prepare AgroSense for production deployment.

---

## **📋 PRODUCTION CHECKLIST**

### **Phase 1: Code Preparation** ✅
- [x] Add `.gitignore` - prevents uploading unnecessary files
- [x] Create `Procfile` - tells Heroku/Railway how to run app
- [x] Create `runtime.txt` - specifies Python version
- [x] Update `requirements.txt` - add gunicorn
- [x] Update `app.py` - handle PORT environment variable
- [x] Create `__init__.py` in backend - make it a Python package
- [x] Create `.env.example` - example environment variables

### **Phase 2: Security** 🔒

#### A. Environment Variables
```python
# Update backend/app.py to use environment variables
import os

SECRET_KEY = os.environ.get('SECRET_KEY', 'default-dev-key')
FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
DEBUG = FLASK_ENV != 'production'
```

#### B. Disable Debug Mode in Production
```python
# Your app.py already does this:
debug = os.environ.get('FLASK_ENV') != 'production'
app.run(debug=debug, ...)
```

#### C. Set Strong SECRET_KEY
```bash
# Generate a secure key
python -c "import secrets; print(secrets.token_hex(32))"

# Set on Heroku
heroku config:set SECRET_KEY=your-generated-key
```

#### D. CORS Configuration
```python
# Currently allows all origins - for production, restrict to your domain:
from flask_cors import CORS

CORS(app, origins=['https://yourdomain.com', 'https://www.yourdomain.com'])
```

### **Phase 3: Database Security** 🗄️

#### Current: JSON File Storage
**Pros:** Simple, no setup needed
**Cons:** Not scalable, lost on redeploy (Heroku ephemeral storage)

#### Recommended: PostgreSQL

**Heroku Setup:**
```bash
heroku addons:create heroku-postgresql:hobby-dev
heroku config  # Get DATABASE_URL
```

**Update app.py:**
```python
import os
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///agrosense.db')
db = SQLAlchemy(app)

# Replace JSON file operations with database queries
```

### **Phase 4: Static Files & CDN** 📦

#### For Frontend Files
```nginx
# In production Nginx config:
location ~* \.(html|css|js|jpg|png)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

#### CDN Setup (Optional)
- Use CloudFlare for free CDN
- Serves static files from edge servers
- Better performance globally

### **Phase 5: HTTPS/SSL** 🔐

#### Heroku (Automatic)
- Heroku automatically provides SSL
- Your app runs on HTTPS

#### DigitalOcean/AWS
```bash
# Use Let's Encrypt (free)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

#### Enforce HTTPS
```python
# In app.py
from flask_talisman import Talisman

Talisman(app, force_https=True)
```

### **Phase 6: Logging & Monitoring** 📊

#### Setup Error Tracking
```bash
# Heroku
heroku addons:create sentry:free

# Or use Rollbar
pip install rollbar
```

#### Application Logging
```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler('logs/agrosense.log', maxBytes=10240000, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('AgroSense startup')
```

### **Phase 7: Performance Optimization** ⚡

#### A. Enable Compression
```python
from flask_compress import Compress

Compress(app)
```

#### B. Caching
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/weather/<location>')
@cache.cached(timeout=3600)  # Cache for 1 hour
def get_weather(location):
    ...
```

#### C. Database Connection Pooling
```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
}
```

### **Phase 8: Rate Limiting** 🛡️

Prevent abuse:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/crop/recommend', methods=['POST'])
@limiter.limit("10 per minute")
def recommend_crop():
    ...
```

### **Phase 9: Input Validation** ✓

Prevent injection attacks:
```python
from flask_inputs import Inputs
from inputs import validators

class CropForm(Inputs):
    temperature = validators.float(required=True)
    humidity = validators.float(required=True)
    ph = validators.float(required=True)
```

### **Phase 10: Backups** 💾

#### For PostgreSQL on Heroku
```bash
# Automatic daily backups enabled
heroku pg:backups

# Manual backup
heroku pg:backups:capture

# Restore from backup
heroku pg:backups:restore [BACKUP_ID] DATABASE_URL
```

#### For File-Based Storage
```bash
# Daily backup cron job
0 2 * * * tar -czf /backup/agrosense-$(date +%Y%m%d).tar.gz /var/www/agrosense/data/
```

---

## **🚀 DEPLOYMENT WORKFLOW**

```
Local Development
    ↓
    ├─ Test thoroughly
    ├─ Update requirements.txt
    └─ Commit to git
        ↓
Version Control (GitHub/GitLab)
    ↓
    ├─ Push to main branch
    └─ CI/CD pipeline (optional)
        ↓
Production Server (Heroku/AWS/etc)
    ↓
    ├─ Install dependencies
    ├─ Run migrations
    └─ Start app
        ↓
Monitoring & Logging
    ↓
    ├─ Monitor performance
    ├─ Track errors
    └─ Daily backups
```

---

## **📝 DEPLOYMENT COMMANDS SUMMARY**

### **Heroku**
```bash
# Initial setup
git init
git add .
git commit -m "Initial commit"
heroku login
heroku create app-name

# Deploy
git push heroku main

# Configure
heroku config:set KEY=VALUE
heroku config:set SECRET_KEY=your-key
heroku config:set FLASK_ENV=production

# Monitor
heroku logs --tail
heroku ps
```

### **Railway**
```bash
# Just push to GitHub
git push origin main
# Railway auto-deploys!
```

### **DigitalOcean**
```bash
# SSH into server
ssh root@your-ip

# Clone code
git clone your-repo
cd repo

# Setup Python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 backend.app:app
```

---

## **✅ PRE-DEPLOYMENT CHECKLIST**

Before going live, verify:

- [ ] All dependencies in `requirements.txt`
- [ ] `Procfile` configured correctly
- [ ] `runtime.txt` specifies Python version
- [ ] `debug=False` in production
- [ ] SECRET_KEY set in environment
- [ ] CORS configured for your domain
- [ ] Database backups setup
- [ ] Error logging configured
- [ ] SSL/HTTPS enabled
- [ ] Frontend API URLs point to production server
- [ ] Tested all API endpoints
- [ ] Tested all HTML pages
- [ ] Performance acceptable (< 2s load time)
- [ ] Mobile responsive tested
- [ ] Different browsers tested

---

## **🆘 TROUBLESHOOTING PRODUCTION ISSUES**

### **App Crashes After Deploy**
```bash
# Check logs
heroku logs --tail

# Common issues:
# - Missing dependency in requirements.txt
# - Wrong Python version in runtime.txt
# - Procfile configuration error
```

### **High Memory Usage**
```bash
# Reduce worker count
heroku ps:scale web=1
# Or upgrade dyno type
heroku dyno:type standard-2x
```

### **Slow Response Times**
- Enable caching
- Add CDN
- Optimize database queries
- Reduce payload size

### **Static Files Return 404**
- Ensure files in correct directory
- Configure web server properly
- Check file permissions

---

## **📚 USEFUL LINKS**

- Heroku Docs: https://devcenter.heroku.com/
- Flask Production: https://flask.palletsprojects.com/deployment/
- Gunicorn: https://gunicorn.org/
- PostgreSQL: https://www.postgresql.org/docs/
- Let's Encrypt: https://letsencrypt.org/

---

**Your app is ready for production! 🎉**
