# 🎯 QUICK DEPLOYMENT CHECKLIST

## ✅ COMPLETED

- [x] GitHub repository created and configured
- [x] All 60+ files pushed to GitHub  
- [x] Code cloned to server (`/home/ubuntu/networking_cloud/`)
- [x] `.env` file created with port 8001 configuration
- [x] Systemd service file created
- [x] Nginx reverse proxy configured (port 80)
- [x] All documentation prepared

---

## 🚀 IMMEDIATE NEXT STEPS (Copy & Paste)

### 1️⃣ SSH Into Server
```bash
ssh -i ~/.ssh/id_rsa ubuntu@13.213.12.202
```

### 2️⃣ Install Dependencies (Copy entire block and paste)
```bash
cd /home/ubuntu/networking_cloud
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv postgresql-client redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### 3️⃣ Setup Database & Run Migrations
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### 4️⃣ Create Admin User
```bash
python manage.py createsuperuser
```

### 5️⃣ Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable networking-cloud
sudo systemctl start networking-cloud
sudo systemctl reload nginx
```

### 6️⃣ Verify Everything Works
```bash
curl http://localhost:8001/health/
```

---

## 📍 ACCESS AFTER DEPLOYMENT

### Direct Access (Port 8001)
```
Admin: http://13.213.12.202:8001/admin/
API:   http://13.213.12.202:8001/api/v1/
```

### Via Nginx (Port 80 - Requires Subdomain DNS)
```
Admin: http://api.asilbek.tech/admin/
API:   http://api.asilbek.tech/api/v1/
```

---

## 🔐 SUBDOMAIN & SSL SETUP

### 1. Point DNS to Server
Create DNS A records:
```
api.asilbek.tech       → 13.213.12.202
app.asilbek.tech       → 13.213.12.202  
dashboard.asilbek.tech → 13.213.12.202
```

### 2. Get SSL Certificate (After DNS)
```bash
ssh -i ~/.ssh/id_rsa ubuntu@13.213.12.202
sudo apt install -y certbot python3-certbot-nginx
sudo certbot certonly --nginx -d api.asilbek.tech
```

### 3. Enable HTTPS in Nginx
```bash
# Edit Nginx config (on server)
sudo nano /etc/nginx/sites-available/networking-cloud.conf

# Uncomment HTTPS section and update paths
# Then reload
sudo nginx -t && sudo systemctl reload nginx
```

---

## 🐛 QUICK TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| Port 8001 error | `sudo lsof -i :8001` then `sudo kill -9 <PID>` |
| Service won't start | `sudo journalctl -u networking-cloud -f` |
| Nginx error | `sudo nginx -t` then `sudo systemctl restart nginx` |
| DB connection failed | `psql -h localhost -U postgres -c "SELECT 1"` |
| Can't access admin | Verify `.env` DATABASE settings |

---

## 📊 PORT CONFIGURATION

| Service | Port | Status | Note |
|---------|------|--------|------|
| Django App | 8001 | ✅ Active | Gunicorn |
| Nginx (HTTP) | 80 | ✅ Configured | Proxy to 8001 |
| PostgreSQL | 5432 | ✅ Ready | Local connection |
| Redis | 6379 | ✅ Active | Cache & broker |
| Portfolio | PORT? | ✅ Unchanged | Separate instance |

---

## 🔄 DAILY OPERATIONS

### Check Status
```bash
sudo systemctl status networking-cloud
```

### View Logs
```bash
sudo journalctl -u networking-cloud -f
```

### Stop Service
```bash
sudo systemctl stop networking-cloud
```

### Restart Service
```bash
sudo systemctl restart networking-cloud
```

### Update Code (Pull Latest)
```bash
cd /home/ubuntu/networking_cloud
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
sudo systemctl restart networking-cloud
```

---

## 📋 FILE LOCATIONS

| Item | Location |
|------|----------|
| Project | `/home/ubuntu/networking_cloud/` |
| Config | `/home/ubuntu/networking_cloud/.env` |
| Systemd | `/etc/systemd/system/networking-cloud.service` |
| Nginx | `/etc/nginx/sites-available/networking-cloud.conf` |
| Logs | `/var/log/networking-cloud-*.log` |
| Virtual Env | `/home/ubuntu/networking_cloud/venv/` |

---

## ✅ VERIFICATION COMMANDS

```bash
# All at once:
echo "=== Service Status ===" && sudo systemctl status networking-cloud && \
echo "=== Health Check ===" && curl http://localhost:8001/health/ && \
echo "=== Database ===" && psql -h localhost -U postgres -c "SELECT 1" && \
echo "=== Redis ===" && redis-cli ping && \
echo "=== Nginx ===" && sudo nginx -t && \
echo "✓ All systems operational!"
```

---

## 🎯 IMPORTANT NOTES

⚠️ **CRITICAL**:
- Keep `.env` secure - don't share it
- Change `SECRET_KEY` in production
- Keep `DEBUG = False` for security
- Backup database regularly
- Monitor logs for errors
- Keep software updated

✅ **PORTFOLIO SAFETY**:
- Your portfolio runs on different port/process
- No interference with this application
- Both can run simultaneously

🌐 **DNS/SUBDOMAIN**:
- Wait for DNS propagation (can take 24-48 hours)
- Test with `nslookup api.asilbek.tech`
- Once working, setup SSL certificate

---

## 📞 IF YOU GET STUCK

1. Check logs: `sudo journalctl -u networking-cloud -f`
2. Check connectivity: `curl http://localhost:8001/health/`
3. Check database: `psql -h localhost -U postgres -l`
4. Verify Nginx: `sudo nginx -t`
5. Read: `SERVER_DEPLOYMENT_GUIDE.md` for detailed help

---

## 🎉 SUCCESS CHECKLIST

- [ ] Logged into server via SSH
- [ ] All dependencies installed
- [ ] Migrations completed
- [ ] Superuser created
- [ ] Service started
- [ ] Can access admin panel
- [ ] Health check works
- [ ] Nginx configured
- [ ] Ready for DNS/SSL setup

---

**GitHub Repo**: https://github.com/ASILBEKasilbek/networking_cloud  
**Server**: `13.213.12.202`  
**Status**: 🟢 READY TO DEPLOY

Happy deploying! 🚀
