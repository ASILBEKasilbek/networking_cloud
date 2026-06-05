# 🌐 SUBDOMAIN QUICK REFERENCE

## 🎯 RECOMMENDED SUBDOMAINS FOR YOUR PROJECT

### **Option A: SIMPLE (Recommended for Start)**
```
api.asilbek.tech    → Your application
```

### **Option B: MULTI-PURPOSE**
```
api.asilbek.tech    → REST API
app.asilbek.tech    → Web Application  
admin.asilbek.tech  → Admin Dashboard
```

### **Option C: DEPARTMENT-BASED**
```
erp.asilbek.tech    → ERP Module
crm.asilbek.tech    → CRM Module
wms.asilbek.tech    → WMS Module
api.asilbek.tech    → API Gateway
```

---

## 📋 QUICK SETUP STEPS

### Step 1️⃣: Add DNS A Record
**Where**: Your domain registrar (GoDaddy, Namecheap, etc.)

**What to Add**:
```
Name/Host:     api (or app, admin, etc.)
Type:          A
Value/Points:  13.213.12.202
TTL:           3600 (default)
```

### Step 2️⃣: Wait 24-48 Hours
```bash
# Check if DNS is ready:
nslookup api.asilbek.tech
# Should show: 13.213.12.202
```

### Step 3️⃣: Get SSL Certificate
```bash
ssh -i ~/.ssh/id_rsa ubuntu@13.213.12.202
sudo certbot certonly --nginx -d api.asilbek.tech
```

### Step 4️⃣: Update Nginx & Restart
```bash
sudo systemctl reload nginx
sudo systemctl restart networking-cloud
```

### Step 5️⃣: Access Your App
```
https://api.asilbek.tech/admin/
https://api.asilbek.tech/api/v1/
```

---

## 🔗 EXACT DNS VALUES TO ADD

Copy-paste these into your registrar:

### Single Subdomain (Simple)
```
api                A       13.213.12.202
```

### Multiple Subdomains (Recommended)
```
api                A       13.213.12.202
app                A       13.213.12.202
admin              A       13.213.12.202
```

### All Department Subdomains
```
api                A       13.213.12.202
app                A       13.213.12.202
admin              A       13.213.12.202
erp                A       13.213.12.202
crm                A       13.213.12.202
wms                A       13.213.12.202
```

---

## ✅ TESTING AFTER EACH STEP

```bash
# Test 1: DNS is resolving
nslookup api.asilbek.tech
# Should show: 13.213.12.202

# Test 2: Can access without HTTPS
curl -I http://api.asilbek.tech:8001
# Should show: 200 OK

# Test 3: SSL certificate works
curl -I https://api.asilbek.tech
# Should show: 200 OK

# Test 4: API responds
curl https://api.asilbek.tech/health/
# Should show: JSON response
```

---

## 🎁 BONUS: WILDCARD CERTIFICATE (Optional)

Get ONE certificate for ALL future subdomains:

```bash
sudo certbot certonly --nginx -d asilbek.tech -d *.asilbek.tech
```

Then these will all work automatically:
- anything.asilbek.tech
- another.asilbek.tech
- future.asilbek.tech

---

## 📊 WHAT HAPPENS AT EACH STAGE

```
STAGE 1: DNS A Record Added
├─ You add: api.asilbek.tech A 13.213.12.202
├─ Status: Waiting for propagation
└─ Access: ❌ Not yet (DNS still propagating)

STAGE 2: DNS Propagated (24-48h)
├─ nslookup shows: 13.213.12.202
├─ Status: Ready for SSL
└─ Access: ✅ http://api.asilbek.tech (but HTTP only)

STAGE 3: SSL Certificate Obtained
├─ Certbot gets certificate
├─ Status: Ready for HTTPS
└─ Access: ✅ https://api.asilbek.tech (HTTPS works)

STAGE 4: Nginx Updated & Reloaded
├─ Nginx uses SSL certificate
├─ Status: Production ready
└─ Access: ✅ https://api.asilbek.tech (full setup)
```

---

## 🌍 YOUR DNS RECORDS (CUSTOMIZE)

| Subdomain | Type | Value | Purpose |
|-----------|------|-------|---------|
| api | A | 13.213.12.202 | REST API & Admin |
| app | A | 13.213.12.202 | Web App (optional) |
| admin | A | 13.213.12.202 | Admin Dashboard (optional) |

---

## 🔐 SECURITY CHECKLIST

- [ ] DNS A record added to registrar
- [ ] Waited 24-48 hours for DNS propagation
- [ ] Tested DNS: `nslookup api.asilbek.tech`
- [ ] Got SSL certificate with Certbot
- [ ] Updated Nginx configuration with HTTPS
- [ ] Reloaded Nginx without errors
- [ ] Tested HTTPS: `curl https://api.asilbek.tech`
- [ ] Portfolio still works on separate port
- [ ] Application accessible via subdomain

---

## 📖 FULL GUIDE

For detailed instructions, see: **SUBDOMAIN_SETUP_GUIDE.md**

---

## 🎯 MY RECOMMENDATION

**Start Simple, Add Later:**

1. **Week 1**: Add only `api.asilbek.tech`
2. **Week 2**: Test and verify everything works
3. **Week 3+**: Add more subdomains if needed

This way you:
✅ Get something working quickly  
✅ Test before adding complexity  
✅ Can add more subdomains anytime  

---

## 📞 QUICK COMMANDS

```bash
# Check DNS (on your computer)
nslookup api.asilbek.tech

# Check on server
ssh -i ~/.ssh/id_rsa ubuntu@13.213.12.202
nslookup api.asilbek.tech

# Get SSL cert
sudo certbot certonly --nginx -d api.asilbek.tech

# Check certificate
sudo certbot certificates

# Reload Nginx
sudo systemctl reload nginx

# Restart app
sudo systemctl restart networking-cloud

# Check logs
sudo journalctl -u networking-cloud -f
```

---

## 🎉 FINAL RESULT

After completing all steps:

```
✅ DNS: api.asilbek.tech → 13.213.12.202
✅ SSL: Valid HTTPS certificate
✅ App: Running on port 8001
✅ Proxy: Nginx forwarding traffic
✅ Access: https://api.asilbek.tech

Admin Panel:   https://api.asilbek.tech/admin/
API:           https://api.asilbek.tech/api/v1/
Health:        https://api.asilbek.tech/health/
```

---

**Ready to add subdomains? Start with Step 1! 🚀**
