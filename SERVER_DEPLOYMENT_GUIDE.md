# 🚀 SERVER DEPLOYMENT GUIDE

## ✅ Completed

✅ GitHub repository created and pushed  
✅ Code cloned to server at `/home/ubuntu/networking_cloud/`  
✅ `.env` file configured for port 8001  
✅ Systemd service file created  
✅ Nginx configuration created (port 80)  

---

## 📋 SERVER INFORMATION

**Server Address**: `13.213.12.202`  
**SSH Command**: `ssh -i ~/.ssh/id_rsa ubuntu@13.213.12.202`  
**GitHub Repo**: https://github.com/ASILBEKasilbek/networking_cloud  

---

## 🔧 NEXT STEPS TO DEPLOY

### Step 1: SSH into Server
```bash
ssh -i ~/.ssh/id_rsa ubuntu@13.213.12.202
```

### Step 2: Navigate to Project
```bash
cd /home/ubuntu/networking_cloud
```

### Step 3: Install System Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python, PostgreSQL client
sudo apt install -y python3 python3-pip python3-venv postgresql-client redis-server

# Start Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

### Step 4: Create Python Virtual Environment & Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### Step 5: Setup Database Connection
```bash
# Test PostgreSQL connection
psql -h localhost -U postgres -d networking_cloud -c "SELECT 1"

# If database doesn't exist, create it:
# psql -h localhost -U postgres -c "CREATE DATABASE networking_cloud"
```

### Step 6: Run Migrations
```bash
python manage.py migrate
```

### Step 7: Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Step 8: Test Application Locally
```bash
python manage.py runserver 0.0.0.0:8001
```

### Step 9: Setup Systemd Service
```bash
# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable networking-cloud
sudo systemctl start networking-cloud

# Check status
sudo systemctl status networking-cloud

# View logs
sudo journalctl -u networking-cloud -f
```

### Step 10: Reload Nginx
```bash
sudo systemctl reload nginx
```

---

## 📍 ACCESS POINTS

### Port 8001 (Direct - Local Test)
```
http://localhost:8001/admin/
http://localhost:8001/api/v1/
http://localhost:8001/health/
```

### Port 80 (Via Nginx - Using Subdomain)
```
http://api.asilbek.tech/
http://app.asilbek.tech/
http://dashboard.asilbek.tech/
```
*(Requires DNS configuration and subdomain pointing to 13.213.12.202)*

---

## 🔐 SSL/TLS SETUP (After DNS Configuration)

Once you have DNS configured:

### Option 1: Let's Encrypt (Free & Automatic)
```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Generate certificate
sudo certbot certonly --nginx -d api.asilbek.tech -d app.asilbek.tech

# Certificate will be at:
# /etc/letsencrypt/live/api.asilbek.tech/
```

### Option 2: Update Nginx for HTTPS
```bash
# After certificate is obtained, uncomment HTTPS section in /etc/nginx/sites-available/networking-cloud.conf
sudo nano /etc/nginx/sites-available/networking-cloud.conf

# Update paths:
# ssl_certificate /etc/letsencrypt/live/api.asilbek.tech/fullchain.pem;
# ssl_certificate_key /etc/letsencrypt/live/api.asilbek.tech/privkey.pem;

# Test & reload Nginx
sudo nginx -t
sudo systemctl reload nginx
```

---

## 📊 MONITORING & LOGS

### Application Logs
```bash
# Systemd logs
sudo journalctl -u networking-cloud -f

# Error logs
tail -f /var/log/networking-cloud-error.log

# Access logs
tail -f /var/log/networking-cloud-access.log
```

### System Logs
```bash
# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Check Service Status
```bash
sudo systemctl status networking-cloud
sudo systemctl is-active networking-cloud
```

---

## 📝 IMPORTANT CONFIGURATION NOTES

### .env File Location
```
/home/ubuntu/networking_cloud/.env
```

### Change These Values:
1. **SECRET_KEY** - Generate a new one for production
2. **DB_PASSWORD** - Change from default `postgres123secure`
3. **ALLOWED_HOSTS** - Add your actual domain
4. **DEBUG** - Keep as `False` for production

### Database Setup (If Needed)
```bash
# Connect to PostgreSQL
sudo -i -u postgres
createdb networking_cloud
createuser -P networking  # Enter password when prompted
psql -d networking_cloud -c "GRANT ALL PRIVILEGES ON DATABASE networking_cloud TO networking;"
exit
```

---

## 🐛 TROUBLESHOOTING

### Port 8001 in Use
```bash
# Find process using port 8001
sudo lsof -i :8001

# Kill process
sudo kill -9 <PID>
```

### Nginx Error: Address Already in Use
```bash
# Check Nginx is running
sudo systemctl status nginx

# Restart Nginx
sudo systemctl restart nginx
```

### Database Connection Error
```bash
# Verify PostgreSQL is running
sudo systemctl status postgresql

# Test connection
psql -h localhost -U postgres -c "SELECT 1"
```

### Permission Issues
```bash
# Change directory ownership
sudo chown -R ubuntu:ubuntu /home/ubuntu/networking_cloud

# Make scripts executable
chmod +x /home/ubuntu/networking_cloud/start_app.sh
```

---

## 🔄 GIT WORKFLOW

### Pull Latest Changes
```bash
cd /home/ubuntu/networking_cloud
git pull origin main
```

### After Pulling Changes
```bash
# Stop service
sudo systemctl stop networking-cloud

# Install new dependencies
source venv/bin/activate
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start service
sudo systemctl start networking-cloud
```

### Create a Deployment Script
```bash
#!/bin/bash
# Save as deploy.sh
set -e

cd /home/ubuntu/networking_cloud
source venv/bin/activate

echo "Pulling latest code..."
git pull origin main

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Restarting service..."
sudo systemctl restart networking-cloud

echo "✓ Deployment complete!"
```

---

## ✅ VERIFICATION CHECKLIST

- [ ] SSH into server successfully
- [ ] Project directory exists at `/home/ubuntu/networking_cloud`
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] `.env` file configured
- [ ] Database connection works
- [ ] Migrations completed
- [ ] Static files collected
- [ ] Systemd service created and enabled
- [ ] Nginx configuration valid
- [ ] Application starts without errors
- [ ] Can access http://localhost:8001
- [ ] Can access via subdomain (after DNS setup)

---

## 📞 SUPPORT COMMANDS

### Quick Status Check
```bash
# One-liner to check everything
sudo systemctl status networking-cloud && \
  echo "---" && \
  curl -s http://localhost:8001/health/ && \
  echo "---" && \
  redis-cli ping
```

### Create Superuser
```bash
cd /home/ubuntu/networking_cloud
source venv/bin/activate
python manage.py createsuperuser
```

### Run Django Shell
```bash
cd /home/ubuntu/networking_cloud
source venv/bin/activate
python manage.py shell
```

### Test API Endpoint
```bash
curl -X GET http://localhost:8001/health/
curl -X POST http://localhost:8001/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your-password"}'
```

---

## 🎯 FINAL STEPS

### 1. Configure DNS
Add DNS A record pointing to `13.213.12.202`:
```
api.asilbek.tech      A  13.213.12.202
app.asilbek.tech      A  13.213.12.202
dashboard.asilbek.tech A  13.213.12.202
```

### 2. Setup SSL Certificate
Once DNS is configured, run:
```bash
sudo certbot certonly --nginx -d api.asilbek.tech -d app.asilbek.tech
```

### 3. Update Nginx Configuration
Uncomment HTTPS section in Nginx config and update certificate paths

### 4. Test Application
```bash
# Via IP
curl http://13.213.12.202/admin/

# Via domain (after DNS)
curl http://api.asilbek.tech/admin/

# Via HTTPS (after SSL)
curl https://api.asilbek.tech/admin/
```

---

## 🚀 SUCCESS INDICATORS

✅ Service is running: `sudo systemctl status networking-cloud`  
✅ Port 8001 is listening: `sudo lsof -i :8001`  
✅ Nginx is proxying: `curl http://localhost/health/`  
✅ Database connected: `python manage.py dbshell`  
✅ Static files served: `curl http://localhost:8001/admin/`  

---

**Status**: 🟢 READY FOR DEPLOYMENT  
**Portfolio**: ✅ Not affected (running on different port)  
**Next**: Follow steps above and run the application!

