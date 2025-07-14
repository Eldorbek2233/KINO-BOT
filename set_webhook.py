#!/usr/bin/env python3
"""
Bu script bot deploy qilingandan keyin webhook URL ni o'rnatadi
Render-da Environment Variables orqali RENDER_EXTERNAL_URL ni oladi
"""

import requests
import os
from config import TOKEN

def set_webhook():
    # Render avtomatik ravishda RENDER_EXTERNAL_URL beradi
    render_url = os.getenv('RENDER_EXTERNAL_URL')
    
    if not render_url:
        print("❌ RENDER_EXTERNAL_URL topilmadi. Render-da deploy qilgandan keyin ishga tushiring.")
        return
    
    # Webhook URL yaratish
    webhook_url = f"{render_url}/webhook"
    
    print(f"📡 Webhook URL o'rnatilmoqda: {webhook_url}")
    
    # Webhook o'rnatish
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
    data = {"url": webhook_url}
    
    response = requests.post(url, data=data)
    result = response.json()
    
    if result.get('ok'):
        print(f"✅ Webhook muvaffaqiyatli o'rnatildi!")
        print(f"📄 Response: {result}")
    else:
        print(f"❌ Webhook o'rnatishda xatolik: {result}")

def delete_webhook():
    """Webhook ni o'chirish - test uchun"""
    url = f"https://api.telegram.org/bot{TOKEN}/deleteWebhook"
    response = requests.post(url)
    result = response.json()
    print(f"🗑️ Webhook o'chirildi: {result}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "delete":
        delete_webhook()
    else:
        set_webhook()
