# 🚂 Railway Deployment Guide - Kino Bot

## 🎯 Railway ga deploy qilish uchun qadam-qadam yo'riqnoma

### 1️⃣ GitHub Repository ni tayyorlash
```bash
git add .
git commit -m "🚂 Railway deployment ready"
git push origin main
```

### 2️⃣ Railway.app da loyiha yaratish
1. [Railway.app](https://railway.app) ga kiring
2. "Start a New Project" bosing
3. "Deploy from GitHub repo" ni tanlang
4. `KINO-BOT` repository ni tanlang

### 3️⃣ Environment Variables sozlash
Railway dashboard da quyidagi o'zgaruvchilarni qo'shing:

```env
BOT_TOKEN=8177519032:AAED4FgPoFQiQhqM_lvrK1iV8hL9u4SnkDk
ADMIN_ID=5542016161
MONGODB_URI=mongodb+srv://eldorbekxakimxujayev4:Ali11042004@kinobot-cluster.quzswqg.mongodb.net/kinobot?retryWrites=true&w=majority&appName=kinobot-cluster
DB_NAME=kinobot
PORT=8000
```

### 4️⃣ Custom Domain (ixtiyoriy)
- Railway dashboard da "Settings" > "Networking"
- Custom domain qo'shishingiz mumkin

### 5️⃣ Deployment tekshirish
1. Railway logs ni kuzating
2. Bot ishlayotganligini tekshiring: `/start`
3. Webhook holatini tekshiring

## 🔧 Texnik Ma'lumotlar

### Fayllar tuzilishi:
- `railway.toml` - Railway konfiguratsiyasi
- `nixpacks.toml` - Build konfiguratsiyasi  
- `railway_config.py` - Railway-specific sozlamalar
- `Procfile` - Gunicorn startup command
- `requirements.txt` - Python dependencies

### Port va Webhook:
- Railway avtomatik `$PORT` beradi
- Webhook URL: `https://your-project.up.railway.app/webhook`
- Health check: `https://your-project.up.railway.app/health`

### Monitoring:
- Railway dashboard orqali logs, metrics
- Bot status: `https://your-project.up.railway.app/status`

## 🚀 Deploy tugmasi:
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

## ⚠️ Muhim eslatmalar:
1. MongoDB URI ni to'g'ri kiriting
2. BOT_TOKEN ni himoya qiling
3. ADMIN_ID ni o'zgartirish mumkin
4. Railway free plan: 500 soat/oy

## 🆘 Muammo hal qilish:
- Build xatosi: `nixpacks.toml` tekshiring
- Webhook xatosi: Environment variables ni tekshiring  
- Bot javob bermasa: Logs ni ko'ring
- Memory xatosi: Worker count ni kamaytiring

## 📞 Yordam:
Muammo bo'lsa: [@Eldorbek_Xakimxujayev](https://t.me/Eldorbek_Xakimxujayev)
