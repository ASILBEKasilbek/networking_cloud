# 🌐 SUBDOMAIN SETUP GUIDE FOR asilbek.tech

## 📍 WHAT SUBDOMAINS TO ADD

### ✅ RECOMMENDED SUBDOMAINS FOR YOUR PROJECT

Choose one or more based on your needs:

```
Option 1: Single Subdomain (SIMPLE)
├─ api.asilbek.tech    → Main application

Option 2: Multi-Purpose (RECOMMENDED)
├─ api.asilbek.tech    → REST API
├─ app.asilbek.tech    → Web Application
└─ admin.asilbek.tech  → Admin Dashboard

Option 3: Department-Based (ENTERPRISE)
├─ erp.asilbek.tech    → ERP Module
├─ crm.asilbek.tech    → CRM Module
├─ wms.asilbek.tech    → WMS Module
└─ api.asilbek.tech    → API Gateway
```

**My recommendation**: Start with `api.asilbek.tech` for simplicity

---

## 🔧 STEP 1: ADD DNS A RECORDS

### Where to Add DNS Records?

You need to go to your domain registrar:
- **GoDaddy**
- **Namecheap**
- **Google Domains**
- **CloudFlare**
- **Or wherever you registered asilbek.tech**

### How to Add A Records?

#### For GoDaddy:
```
1. Login to GoDaddy
2. Go to My Products → Domains
3. Click on asilbek.tech
4. DNS Management
5. Add Record → Type: A
6. Name: api (or app, admin, etc.)
7. Value: 13.213.12.202
8. Save
```

#### For Namecheap:
```
1. Login to Namecheap
2. Domain List → asilbek.tech
3. Advanced DNS
4. Add New Record
5. Type: A Record
6. Host: api (or app, admin, etc.)
7. Value: 13.213.12.202
8. Save
```

#### For CloudFlare:
```
1. Login to CloudFlare
2. Select asilbek.tech domain
3. DNS → Add Record
4. Type: A
5. Name: api (or app, admin, etc.)
6. IPv4 address: 13.213.12.202
7. Proxy status: DNS only (or Proxied)
8. Save
```

---

## 📝 COMPLETE DNS CONFIGURATION

Add these A records to your DNS provider:

### All Subdomains (Choose which ones you need)

```
SUBDOMAIN          TYPE    VALUE            TTL
───────────────────────────────────────────────
api.asilbek.tech    A      13.213.12.202    3600
app.asilbek.tech    A      13.213.12.202    3600
admin.asilbek.tech  A      13.213.12.202    3600
erp.asilbek.tech    A      13.213.12.202    3600
crm.asilbek.tech    A      13.213.12.202    3600
wms.asilbek.tech    A      13.213.12.202    3600
```

---

## ⏳ WAIT FOR DNS PROPAGATION

After adding DNS records, wait **24-48 hours** for propagation.

### Test DNS Resolution (After 24 hours)

```bash
# Method 1: nslookup
nslookup api.asilbek.tech
# Should show: 13.213.12.202

# Method 2: dig
dig api.asilbek.tech
# Should show: 13.213.12.202

# Method 3: curl (on your computer)
curl -I http://api.asilbek.tech
# Should work (may show 502 if app not running yet)
```

---

## 🔐 STEP 2: UPDATE NGINX CONFIGURATION

Once DNS is working, update Nginx on your server:

### SSH into Server
```bash
ssh -i ~/.ssh/id_rsa ubuntu@13.213.12.202
```

### Edit Nginx Config
```bash
sudo nano /etc/nginx/sites-available/networking-cloud.conf
```

### Current Config (Before)
```nginx
server {
    listen 80;
    listen [::]:80;
    server_name api.asilbek.tech app.asilbek.tech dashboard.asilbek.tech;
    
    location / {
        proxy_pass http://networking_cloud_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

### Update Subdomains (After)
```nginx
server {
    listen 80;
    listen [::]:80;
    server_name api.asilbek.tech;  # Add your subdomain(s)
    
    location / {
        proxy_pass http://networking_cloud_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

### If You Want Multiple Subdomains
```nginx
server {
    listen 80;
    listen [::]:80;
    server_name api.asilbek.tech app.asilbek.tech admin.asilbek.tech;
    
    location / {
        proxy_pass http://networking_cloud_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

### Save and Exit
```
Press: Ctrl+X
Then: Y (yes)
Then: Enter
```

### Test Nginx Config
```bash
sudo nginx -t
# Should show: "successful"
```

### Reload Nginx
```bash
sudo systemctl reload nginx
```

---

## 🟢 STEP 3: UPDATE .env FILE

Edit your .env file with the correct subdomain:

### SSH into Server
```bash
ssh -i ~/.ssh/id_rsa ubuntu@13.213.12.202
```

### Edit .env
```bash
cd /home/ubuntu/networking_cloud
nano .env
```

### Update This Line
```
# BEFORE:
ALLOWED_HOSTS=localhost,127.0.0.1,13.213.12.202,asilbek.tech,*.asilbek.tech

# AFTER (same, but confirm):
ALLOWED_HOSTS=localhost,127.0.0.1,13.213.12.202,asilbek.tech,api.asilbek.tech,app.asilbek.tech
```

### Also Update CORS
```
# CORS settings
CORS_ALLOWED_ORIGINS=http://localhost,http://127.0.0.1,https://asilbek.tech,https://api.asilbek.tech,https://app.asilbek.tech
```

### Save and Exit
```
Press: Ctrl+X
Then: Y
Then: Enter
```

---

## 🔐 STEP 4: SETUP SSL/TLS CERTIFICATE

Once DNS is working, get an SSL certificate:

### Install Certbot
```bash
sudo apt install -y certbot python3-certbot-nginx
```

### Get Certificate for Your Subdomain(s)
```bash
# For single subdomain:
sudo certbot certonly --nginx -d api.asilbek.tech

# For multiple subdomains:
sudo certbot certonly --nginx -d api.asilbek.tech -d app.asilbek.tech -d admin.asilbek.tech
```

### What You'll Get
```
Certificate saved at:
/etc/letsencrypt/live/api.asilbek.tech/fullchain.pem

Private key saved at:
/etc/letsencrypt/live/api.asilbek.tech/privkey.pem
```

---

## 🔐 STEP 5: UPDATE NGINX FOR HTTPS

Now update Nginx to use SSL:

### Edit Nginx Config Again
```bash
sudo nano /etc/nginx/sites-available/networking-cloud.conf
```

### Replace with HTTPS Configuration
```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name api.asilbek.tech;
    return 301 https://$server_name$request_uri;
}

# HTTPS Server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name api.asilbek.tech;
    
    # SSL Certificates
    ssl_certificate /etc/letsencrypt/live/api.asilbek.tech/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.asilbek.tech/privkey.pem;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    
    location / {
        proxy_pass http://networking_cloud_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_redirect off;
    }
    
    location /static/ {
        alias /home/ubuntu/networking_cloud/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias /home/ubuntu/networking_cloud/media/;
        expires 7d;
        add_header Cache-Control "public";
    }
}
```

### Test Configuration
```bash
sudo nginx -t
```

### Reload Nginx
```bash
sudo systemctl reload nginx
```

---

## ✅ VERIFY EVERYTHING WORKS

### Test Subdomain Access

```bash
# Test HTTP (should redirect to HTTPS)
curl -I http://api.asilbek.tech
# Should show: 301 (redirect)

# Test HTTPS
curl -I https://api.asilbek.tech
# Should show: 200 (success)

# Test API
curl https://api.asilbek.tech/health/
# Should return JSON
```

### Or Use Browser
```
https://api.asilbek.tech/admin/
https://api.asilbek.tech/api/v1/
```

---

## 🎯 QUICK SUMMARY

### What You Need to Do:

1. **Add DNS A Record** (at your registrar)
   ```
   api.asilbek.tech  A  13.213.12.202
   ```

2. **Wait 24-48 hours** for DNS propagation

3. **Get SSL Certificate**
   ```bash
   sudo certbot certonly --nginx -d api.asilbek.tech
   ```

4. **Update Nginx** with HTTPS configuration

5. **Restart Services**
   ```bash
   sudo systemctl restart networking-cloud
   sudo systemctl reload nginx
   ```

6. **Access Your App**
   ```
   https://api.asilbek.tech/admin/
   https://api.asilbek.tech/api/v1/
   ```

---

## 🚀 AFTER SETUP

Your application will be accessible at:

```
✅ Admin Panel:  https://api.asilbek.tech/admin/
✅ API:          https://api.asilbek.tech/api/v1/
✅ Health:       https://api.asilbek.tech/health/
```

### Portfolio Remains Safe
```
Your portfolio will still be on its own port/domain
No interference, no conflicts
Both run simultaneously
```

---

## ⏳ TIMELINE

```
Today:        Add DNS A record
Tomorrow:     (Wait for DNS propagation)
In 24-48h:    Test DNS resolution
In 24-48h:    Get SSL certificate
In 24-48h:    Update Nginx
In 24-48h:    Access via https://api.asilbek.tech
```

---

## 🔧 FREQUENTLY ASKED QUESTIONS

### Q: How many subdomains can I add?
A: Unlimited! Add as many as you need.

### Q: Will this affect my portfolio?
A: No! Your portfolio is on a different port/domain. No interference.

### Q: How long does DNS take to propagate?
A: Usually 24 hours, sometimes up to 48 hours.

### Q: Can I test before DNS is ready?
A: Yes! Modify your local hosts file to test locally.

### Q: Do I need SSL for each subdomain?
A: No! One certificate covers all subdomains with `*.asilbek.tech`.

### Q: Can I get a wildcard certificate?
A: Yes! Add `-w *.asilbek.tech` to certbot command.

---

## 🎁 BONUS: WILDCARD CERTIFICATE

Get ONE certificate for ALL future subdomains:

```bash
sudo certbot certonly --nginx -d asilbek.tech -d *.asilbek.tech
```

Then all these will work without new certificates:
```
api.asilbek.tech
app.asilbek.tech
admin.asilbek.tech
erp.asilbek.tech
crm.asilbek.tech
wms.asilbek.tech
anything.asilbek.tech
```

---

## 📞 TROUBLESHOOTING

### DNS Not Resolving?
```bash
# Clear DNS cache (on Mac)
sudo dscacheutil -flushcache

# Test DNS
nslookup api.asilbek.tech
# or
dig api.asilbek.tech
```

### Certbot Error "No A Record Found"?
```
1. Verify DNS A record was added
2. Wait longer for DNS propagation
3. Try: nslookup api.asilbek.tech
```

### Nginx Won't Reload?
```bash
# Check for syntax errors
sudo nginx -t

# View error log
sudo tail -f /var/log/nginx/error.log
```

### Certificate Validation Error?
```bash
# Check certificate
sudo certbot certificates

# Renew manually
sudo certbot renew --force-renewal
```

---

## ✨ YOU'RE READY!

Once you've:
1. ✅ Added DNS A record
2. ✅ Waited for propagation
3. ✅ Got SSL certificate
4. ✅ Updated Nginx

Your application will be live on `https://api.asilbek.tech`! 🎉

---

**Next Steps:**
1. Add DNS A record at your registrar
2. Wait 24-48 hours for propagation
3. Come back to this guide and follow Step 3-5
4. Your app will be LIVE! 🚀
