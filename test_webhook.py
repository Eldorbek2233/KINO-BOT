#!/usr/bin/env python3
"""Webhook endpointini test qilish uchun script"""

import requests
import json

def test_webhook():
    """Webhook'ga test update yuborish"""
    webhook_url = "https://kino-bot-o8dw.onrender.com/webhook"
    
    # Test update data
    test_data = {
        "update_id": 123456789,
        "message": {
            "message_id": 1,
            "date": 1234567890,
            "chat": {
                "id": 123456789,
                "type": "private",
                "first_name": "Test"
            },
            "from": {
                "id": 123456789,
                "first_name": "Test",
                "username": "testuser"
            },
            "text": "/start"
        }
    }
    
    try:
        print("🔍 Webhook'ga test so'rovi yuborilmoqda...")
        print(f"🌐 URL: {webhook_url}")
        
        # POST so'rovi yuborish
        response = requests.post(
            webhook_url,
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"📊 Status kod: {response.status_code}")
        print(f"📝 Response body: {response.text}")
        print(f"📋 Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Webhook muvaffaqiyatli javob berdi!")
        else:
            print(f"❌ Webhook xatolik berdi: {response.status_code}")
            
    except Exception as e:
        print(f"💥 Test yuborishda xatolik: {e}")

if __name__ == "__main__":
    test_webhook()
