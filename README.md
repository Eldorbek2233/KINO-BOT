# Kino Bot - Telegram Bot

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

## Muhim eslatmalar
- Bot 24/7 ishlashi uchun Free rejada ham Render.com avtomatik ravishda sleeping mode ga o'tkazmasdan ishlaydi
- Botning environment o'zgaruvchilari to'g'ri kiritilganligiga ishonch hosil qiling
- Bot xatoliklari ro'yxatini "Logs" bo'limidan tekshirishingiz mumkin
