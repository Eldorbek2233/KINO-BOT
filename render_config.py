#!/usr/bin/env python3
"""
Render specific configuration
Token va muhit o'zgaruvchilarini to'g'ri boshqarish uchun
"""

import os

# Render da ishlash uchun hardcoded token
RENDER_BOT_TOKEN = "8177519032:AAED4FgPoFQiQhqM_lvrK1iV8hL9u4SnkDk"
RENDER_ADMIN_ID = 5542016161

def get_token():
    """Token ni olish - Render da ishlash uchun"""
    # Birinchi environment variable dan
    token = os.getenv("BOT_TOKEN") or os.getenv("TOKEN")
    
    # Agar topilmasa, hardcoded ishlatamiz
    if not token or token == "None" or len(str(token)) < 30:
        token = RENDER_BOT_TOKEN
        print(f"🎭 Using hardcoded token for Render: {token[:15]}...")
    else:
        print(f"🎭 Using env token on Render: {token[:15]}...")
    
    return token

def get_admin_id():
    """Admin ID ni olish"""
    try:
        admin_id = int(os.getenv("ADMIN_ID", str(RENDER_ADMIN_ID)))
    except (ValueError, TypeError):
        admin_id = RENDER_ADMIN_ID
    
    print(f"🎭 Using ADMIN_ID on Render: {admin_id}")
    return admin_id

def get_webhook_url():
    """Render webhook URL ni olish"""
    render_url = os.getenv("RENDER_EXTERNAL_URL")
    
    if render_url:
        # RENDER_EXTERNAL_URL format: https://your-app.onrender.com
        webhook_url = f"{render_url}/webhook"
    else:
        # Default Render URL pattern (siz o'zgartirishingiz kerak)
        webhook_url = "https://kino-bot-latest.onrender.com/webhook"
    
    print(f"🎭 Render webhook URL: {webhook_url}")
    return webhook_url
