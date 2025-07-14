# Kino Bot - Telegram Bot

## Muhim eslatma
Bu bot Python-Telegram-Bot kutubxonasining 13.15 versiyasi bilan ishlaydi (20.x versiyasi emas).
Version 13.15 da ayrim funksiyalar va API lardan foydalanish usuli boshqacha.

## Render.com ga o'rnatish

### 1. Render.com da yangi Web Service yaratish:
1. https://dashboard.render.com saytiga kiring
2. "New +" tugmasini bosib, "Web Service" ni tanlang
3. GitHub repozitoriyangizni ulang yoki "Deploy from Git Repository" bo'limidan to'g'ridan-to'g'ri deploy qiling

### 2. Konfiguratsiya:
- **Name**: Kino Bot (yoki xohlagan nomingiz)
- **Region**: Frankfurt (EU Central) yoki eng yaqin server
- **Branch**: main (yoki sizning asosiy branch)
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn web_server:app`

### 3. Environment Variables:
Quyidagi muhit o'zgaruvchilarini qo'shing:
- `BOT_TOKEN`: Telegram bot tokeningiz
- `ADMIN_ID`: Admin foydalanuvchi ID raqami

### 4. Plan:
- Free yoki Web Service uchun mos keladigan tarif rejasini tanlang

### 5. Deploy:
"Create Web Service" tugmasini bosing va botingiz deploy bo'lishini kuting.

## Xatoliklarni bartaraf etish

1. `ModuleNotFoundError: No module named 'imghdr'` - bu xatolik yangi Python versiyalarida bo'ladi. Bunday holda `requirements.txt` ga Pillow kutubxonasini qo'shing.

2. `AttributeError: 'Updater' object has no attribute '...'` - bu versiya nomuvofiqligidan kelib chiqadi. Kod python-telegram-bot'ning 13.15 versiyasi uchun moslab yozilgan.

3. Render.com da bot ishlamaganda, web serverni qaytadan ishga tushiring va log larni tekshiring.
