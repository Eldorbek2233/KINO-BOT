# Render.com Deployment Instructions

## 🎭 Render da Deploy Qilish

### 1. **Render Account**
- [render.com](https://render.com) ga kiring
- GitHub account bilan login qiling

### 2. **New Web Service**
- Dashboard da "New +" → "Web Service"
- GitHub repository ni ulang: `KINO-BOT`
- Branch: `main`

### 3. **Configuration**
```
Name: kino-bot (yoki boshqa nom)
Region: Frankfurt (yoki yaqin region)
Branch: main
Runtime: Python 3
```

### 4. **Build & Start Commands**
```bash
Build Command: pip install -r requirements.txt
Start Command: gunicorn -c gunicorn.conf.py wsgi:application
```

### 5. **Environment Variables**
Render Dashboard → Settings → Environment:
```
BOT_TOKEN = 8177519032:AAED4FgPoFQiQhqM_lvrK1iV8hL9u4SnkDk
ADMIN_ID = 5542016161
RENDER_ENVIRONMENT = production
```

### 6. **Auto-Deploy**
- GitHub ga push qilganda avtomatik deploy bo'ladi
- Webhook avtomatik o'rnatiladi

### 7. **URL Format**
Render URL: `https://your-service-name.onrender.com`

### 8. **Status Check**
- `/health` - Health check
- `/webhook` - Telegram webhook endpoint

## 🔧 **Files for Render:**
- ✅ `render.yaml` - Render configuration
- ✅ `render_config.py` - Render-specific settings
- ✅ `wsgi.py` - WSGI entry point
- ✅ `gunicorn.conf.py` - Gunicorn config
- ✅ `requirements.txt` - Dependencies

## 🚀 **Ready to Deploy!**
1. Commit va push qiling
2. Render da connect qiling
3. Environment variables o'rnating
4. Deploy qiling!
