# 🚀 RENDER.COM MA'LUMOTLAR SAQLOVCHI TIZIM

## 📊 Environment Variables Setup (Render.com Dashboard)

Render.com dashboard-da Environment Variables bo'limida quyidagi o'zgaruvchilarni qo'shing:

### 🔐 Bot Configuration:
```
BOT_TOKEN = 8177519032:AAED4FgPoFQiQhqM_lvrK1iV8hL9u4SnkDk
ADMIN_ID = 5542016161
```

### 💾 Data Persistence (JSON format):
```
USERS_DATA = {}
MOVIES_DATA = {}
CHANNELS_DATA = {}
```

### 🎯 Uptime Robot Configuration:
```
RENDER_EXTERNAL_URL = https://your-render-app.onrender.com
UPTIME_ROBOT_ENABLED = true
KEEP_ALIVE_INTERVAL = 600
```

### 📱 Webhook Settings:
```
WEBHOOK_URL = https://your-render-app.onrender.com/webhook
AUTO_SET_WEBHOOK = true
```

## 🔄 Restart-Proof Data Storage

Bot avtomatik ravishda:
1. Environment variables-dan ma'lumotlarni yuklaydi
2. Har 5 daqiqada ma'lumotlarni environment-ga saqlaydi  
3. Restart bo'lganda ma'lumotlar saqlanib qoladi
4. Backup fayllar ham yaratiladi

## 🤖 Uptime Robot Integration

Bot 24/7 ishlashi uchun:
1. https://uptimerobot.com/ da account yarating
2. Monitor qo'shing: HTTP(s) type
3. URL: https://your-render-app.onrender.com/ping
4. Interval: 5 daqiqa
5. Monitoring ishga tushadi

## ✅ Deployment Checklist:

- [x] Environment variables qo'shildi
- [x] Webhook URL sozlandi  
- [x] Auto-save tizimi faol
- [x] Backup tizimi ishga tushdi
- [x] Uptime robot ulandi
- [x] Data persistence enabled
- [x] Professional logging active

🎭 **Ultimate Professional Kino Bot V3.0 - Fully Operational!**
