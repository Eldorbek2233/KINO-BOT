#!/usr/bin/env python3
"""
Railway specific configuration
Token va muhit o'zgaruvchilarini to'g'ri boshqarish uchun
"""

import os

# Railway da ishlash uchun hardcoded token
RAILWAY_BOT_TOKEN = "8177519032:AAED4FgPoFQiQhqM_lvrK1iV8hL9u4SnkDk"
RAILWAY_ADMIN_ID = 5542016161

def get_token():
    """Token ni olish - Railway da ishlash uchun"""
    # Birinchi environment variable dan
    token = os.getenv("BOT_TOKEN") or os.getenv("TOKEN")
    
    # Agar topilmasa, hardcoded ishlatamiz
    if not token or token == "None" or len(str(token)) < 30:
        token = RAILWAY_BOT_TOKEN
        print(f"� Using hardcoded token for Railway: {token[:15]}...")
    else:
        print(f"� Using env token on Railway: {token[:15]}...")
    
    return token

def get_admin_id():
    """Admin ID ni olish"""
    try:
        admin_id = int(os.getenv("ADMIN_ID", str(RAILWAY_ADMIN_ID)))
    except (ValueError, TypeError):
        admin_id = RAILWAY_ADMIN_ID
    
    print(f"� Using ADMIN_ID on Railway: {admin_id}")
    return admin_id

def get_webhook_url():
    """Railway webhook URL ni olish"""
    # Railway environment variables
    railway_url = (
        os.getenv("RAILWAY_PUBLIC_DOMAIN") or 
        os.getenv("RAILWAY_STATIC_URL") or
        os.getenv("RAILWAY_PROJECT_DOMAIN")
    )
    
    if railway_url:
        # Railway URL format: https://your-app.up.railway.app  
        if not railway_url.startswith('http'):
            railway_url = f"https://{railway_url}"
        webhook_url = f"{railway_url}/webhook"
    else:
        # Haqiqiy Railway domain'dan foydalanish
        # Railway deployment logidan olingan URL
        webhook_url = "https://kino-bot.up.railway.app/webhook"
    
    print(f"🚂 Railway webhook URL: {webhook_url}")
    return webhook_url

def get_port():
    """Railway port ni olish"""
    port = int(os.getenv("PORT", 8000))
    print(f"🚂 Railway port: {port}")
    return port
