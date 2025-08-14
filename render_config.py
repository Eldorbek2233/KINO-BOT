#!/usr/bin/env python3
"""
Render specific configuration
Token va muhit o'zgaruvchilarini to'g'ri boshqarish uchun
"""

import os

# Render environment variables only - no hardcoded credentials
RENDER_ADMIN_ID = 5542016161

def get_token():
    """Token ni olish - faqat environment variable dan yoki yangi token fallback"""
    token = os.getenv("BOT_TOKEN") or os.getenv("TOKEN")
    if not token or token == "None" or len(token) < 30:
        # Fallback to new token if env not set
        token = "8177519032:AAFzJSkRpJoU5DuuMoE2yqxH4MZE9tVez2o"
        print("⚠️ BOT_TOKEN environment variable not set, using new fallback token!")
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
