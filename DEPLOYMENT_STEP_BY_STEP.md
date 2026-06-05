# 🎯 DEPLOYMENT ACTION PLAN - DO THIS NOW

## 📍 Current Status

```
✅ GitHub Setup       COMPLETE
✅ Server Cloned      COMPLETE  
✅ Nginx Config       COMPLETE
✅ Systemd Service    COMPLETE
✅ Documentation      COMPLETE
⏳ Application Start   PENDING
⏳ DNS Setup          PENDING
⏳ SSL Certificate    PENDING
```

---

## 🚀 STEP-BY-STEP DEPLOYMENT

### STEP 1: SSH INTO SERVER
```bash
ssh -i ~/.ssh/id_rsa ubuntu@13.213.12.202
```
**Expected Result**: Connected to Ubuntu server

---

### STEP 2: NAVIGATE TO PROJECT
```bash
cd /home/ubuntu/networking_cloud
pwd
ls -la
```
**Expected Result**: See all project files

---

### STEP 3: INSTALL SYSTEM PACKAGES
```bash
# This will take 2-3 minutes
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv postgresql-client redis-server
```
**Expected Result**: All packages installed

---

### STEP 4: START REDIS SERVICE
```bash
sudo systemctl start redis-server
sudo systemctl enable redis-server
redis-cli ping
```
**Expected Result**: Output should say "PONG"

---

### STEP 5: CREATE PYTHON VIRTUAL ENVIRONMENT
```bash
python3 -m venv venv
source venv/bin/activate
```
**Expected Result**: Prompt changes to include `(venv)`

---

### STEP 6: INSTALL PYTHON DEPENDENCIES
```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
```
**Expected Result**: All packages installed (takes 2-3 minutes)

---

### STEP 7: RUN DATABASE MIGRATIONS
```bash
python manage.py migrate
```
**Expected Result**: See "Operations to perform" and "Applied migrations"

---

### STEP 8: COLLECT STATIC FILES
```bash
python manage.py collectstatic --noinput
```
**Expected Result**: "X static files copied to '/home/ubuntu/networking_cloud/staticfiles'"

---

### STEP 9: CREATE ADMIN USER
```bash
python manage.py createsuperuser
```
**Expected Result**: Follow prompts, create admin user (e.g., admin/admin123)

---

### STEP 10: TEST APPLICATION LOCALLY
```bash
python manage.py runserver 0.0.0.0:8001
```
**Expected Result**: "Starting development server at http://0.0.0.0:8001/"

**Then in another terminal**:
```bash
curl http://localhost:8001/health/
```
**Expected Result**: JSON response with health status

**Stop the server**: Press `Ctrl+C`

---

### STEP 11: START GUNICORN SERVICE
```bash
# First exit virtualenv
deactivate

# Then start the service
sudo systemctl daemon-reload
sudo systemctl enable networking-cloud
sudo systemctl start networking-cloud
```
**Expected Result**: Service starts without errors

---

### STEP 12: CHECK SERVICE STATUS
```bash
sudo systemctl status networking-cloud
```
**Expected Result**: "active (running)"

---

### STEP 13: VERIFY APPLICATION WORKS
```bash
curl http://localhost:8001/health/
```
**Expected Result**: JSON with status

---

### STEP 14: RELOAD NGINX
```bash
sudo systemctl reload nginx
```
**Expected Result**: No errors

---

## 🎉 IF EVERYTHING WORKS

You can now access the application at:

```
Admin Panel:  http://13.213.12.202:8001/admin/
API:          http://13.213.12.202:8001/api/v1/
Health:       http://13.213.12.202:8001/health/
```

Username: `admin` (or whatever you created)  
Password: (whatever you set)

---

## 🔐 NEXT: CONFIGURE DNS & SSL (OPTIONAL - FOR SUBDOMAINS)

### 1. Add DNS Records
In your domain registrar (GoDaddy, Namecheap, etc.), add:
```
A record: api.asilbek.tech       → 13.213.12.202
A record: app.asilbek.tech       → 13.213.12.202
A record: dashboard.asilbek.tech → 13.213.12.202
```

### 2. Wait for DNS Propagation (24-48 hours)
Test with:
```bash
nslookup api.asilbek.tech
# Should show 13.213.12.202
```

### 3. Setup SSL Certificate
Once DNS works:
```bash
sudo certbot certonly --nginx -d api.asilbek.tech -d app.asilbek.tech
```

### 4. Update Nginx Configuration
```bash
sudo nano /etc/nginx/sites-available/networking-cloud.conf
# Uncomment HTTPS section
# Update certificate paths
sudo nginx -t
sudo systemctl reload nginx
```

---

## 🆘 IF SOMETHING GOES WRONG

### Check Application Logs
```bash
sudo journalctl -u networking-cloud -f
tail -f /var/log/networking-cloud-error.log
```

### Check if Port is in Use
```bash
sudo lsof -i :8001
```

### Restart Service
```bash
sudo systemctl restart networking-cloud
```

### Check Database
```bash
psql -h localhost -U postgres -c "SELECT 1"
```

### Check Redis
```bash
redis-cli ping
```

### Check Nginx
```bash
sudo nginx -t
sudo systemctl status nginx
```

---

## 📊 COMPLETE COMMAND SCRIPT

You can copy-paste this entire block:

```bash
#!/bin/bash
set -e

# SSH not needed if already connected
# ssh -i ~/.ssh/id_rsa ubuntu@13.213.12.202

cd /home/ubuntu/networking_cloud

# Install and setup
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv postgresql-client redis-server

# Start Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Python setup
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# Database setup
python manage.py migrate
python manage.py collectstatic --noinput

# Create superuser (skip if already exists)
# python manage.py createsuperuser

# Deactivate venv
deactivate

# Start service
sudo systemctl daemon-reload
sudo systemctl enable networking-cloud
sudo systemctl start networking-cloud
sudo systemctl reload nginx

# Verify
echo "✓ Deployment complete!"
echo "✓ Check status: sudo systemctl status networking-cloud"
echo "✓ Test health: curl http://localhost:8001/health/"
```

---

## ✅ VERIFICATION CHECKLIST

After deployment, verify these are all working:

```bash
# 1. Service is running
sudo systemctl status networking-cloud
# Should show: active (running)

# 2. Port 8001 is listening
sudo lsof -i :8001
# Should show gunicorn

# 3. Health check works
curl http://localhost:8001/health/
# Should return JSON

# 4. Database is working
psql -h localhost -U postgres -c "SELECT 1"
# Should return: 1

# 5. Redis is working
redis-cli ping
# Should return: PONG

# 6. Nginx is working
sudo nginx -t
# Should say: successful

# 7. Django loads
python manage.py shell -c "import django; print('OK')"
# Should print: OK
```

---

## 📋 TROUBLESHOOTING TABLE

| Issue | Command | Solution |
|-------|---------|----------|
| Service won't start | `sudo journalctl -u networking-cloud -f` | Check error log |
| Port 8001 in use | `sudo lsof -i :8001` | Kill process or change port |
| DB connection error | `psql -h localhost -U postgres -l` | Verify PostgreSQL running |
| Redis error | `redis-cli ping` | Start Redis service |
| Nginx error | `sudo nginx -t` | Fix config syntax |
| Import error | `cd /home/ubuntu/networking_cloud && source venv/bin/activate && python manage.py shell` | Check Python path |

---

## 🎯 SUCCESS INDICATORS

You're done when you see:

✅ `sudo systemctl status networking-cloud` → **active (running)**  
✅ `curl http://localhost:8001/health/` → **JSON response**  
✅ `curl http://localhost:8001/admin/` → **HTML page** (not connection error)  
✅ Admin login works with your credentials  
✅ API returns data: `curl http://localhost:8001/api/v1/customers/` → **JSON list**  
✅ No errors in logs: `sudo journalctl -u networking-cloud -f`  

---

## 📞 HELPFUL RESOURCES

- Full guide: `SERVER_DEPLOYMENT_GUIDE.md`
- Quick reference: `DEPLOYMENT_QUICK_REFERENCE.md`  
- Complete summary: `DEPLOYMENT_COMPLETE_SUMMARY.md`
- Django docs: https://docs.djangoproject.com/
- Gunicorn docs: https://gunicorn.org/

---

## 🎉 FINAL CHECKLIST

- [ ] SSH into server ✓
- [ ] Navigate to project folder ✓
- [ ] Install system packages ✓
- [ ] Create virtual environment ✓
- [ ] Install Python packages ✓
- [ ] Run migrations ✓
- [ ] Collect static files ✓
- [ ] Create superuser ✓
- [ ] Start service ✓
- [ ] Verify health check ✓
- [ ] Access admin panel ✓
- [ ] Test API ✓

**READY TO DEPLOY!**

---

**Everything is set up. You're just one SSH command away from running the application! 🚀**

```bash
ssh -i ~/.ssh/id_rsa ubuntu@13.213.12.202
cd /home/ubuntu/networking_cloud
# Follow the steps above!
```
