# 🚨 BOT TOKEN MUAMMOSI ANIQLANDI!

## Problem: Environment Variable O'rnatilmagan

Bot ishlamayotganning sababi: **BOT_TOKEN environment variable o'rnatilmagan**

## ✅ Yechim:

### 1. Windows PowerShell orqali (Vaqtinchalik):
```powershell
$env:BOT_TOKEN="YANGI_BOT_TOKENINGIZNI_SHU_JOYGA_QOYING"
$env:ADMIN_ID="5542016161"
```

### 2. Doimiy o'rnatish uchun:
```powershell
[Environment]::SetEnvironmentVariable("BOT_TOKEN", "YANGI_BOT_TOKENINGIZNI_SHU_JOYGA_QOYING", "User")
[Environment]::SetEnvironmentVariable("ADMIN_ID", "5542016161", "User")
```

### 3. .env fayli yaratish:
.env faylini yaratib quyidagilarni yozing:
```
BOT_TOKEN=YANGI_BOT_TOKENINGIZNI_SHU_JOYGA_QOYING
ADMIN_ID=5542016161
```

## 🔧 Bot tokenni qayerdan olish:

1. @BotFather ga boring
2. `/newtoken` yuboring
3. Botingizni tanlang
4. Yangi tokenni oling
5. Tokenni yuqoridagi usullardan biri bilan o'rnating

## ⚠️ MUHIM:
- Token 45-50 ta belgidan iborat bo'lishi kerak
- Format: `123456789:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- Tokenni hech kimga bermang!

## 🧪 Token o'rnatilganligini tekshirish:
```powershell
echo $env:BOT_TOKEN
```

Agar token ko'rinsa, bot ishlaydi!
