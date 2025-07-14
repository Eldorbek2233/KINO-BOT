#!/usr/bin/env python3
"""Final webhook test"""

import requests
import json
from config import TOKEN

# Test 1: Server status
print("🔍 Testing server...")
try:
    response = requests.get("https://kino-bot-o8dw.onrender.com/", timeout=15)
    print(f"✅ Server status: {response.status_code}")
    print(f"📝 Response: {response.text[:50]}")
except Exception as e:
    print(f"❌ Server error: {e}")

# Test 2: Webhook info
print("\n🔍 Testing webhook...")
try:
    response = requests.get(f"https://api.telegram.org/bot{TOKEN}/getWebhookInfo", timeout=15)
    info = response.json()['result']
    
    print(f"📡 Webhook URL: {info.get('url')}")
    print(f"⚠️ Last error: {info.get('last_error_message')}")
    print(f"📊 Pending updates: {info.get('pending_update_count')}")
    
    if info.get('last_error_message'):
        print("❌ Webhook has errors")
    else:
        print("✅ Webhook OK")
        
except Exception as e:
    print(f"❌ Webhook test error: {e}")

# Test 3: Direct webhook test
print("\n🔍 Testing webhook endpoint...")
test_data = {
    "update_id": 999,
    "message": {
        "message_id": 1,
        "date": 1234567890,
        "chat": {"id": 12345, "type": "private"},
        "from": {"id": 12345, "first_name": "Test"},
        "text": "/start"
    }
}

try:
    response = requests.post(
        "https://kino-bot-o8dw.onrender.com/webhook", 
        json=test_data,
        headers={'Content-Type': 'application/json'},
        timeout=15
    )
    print(f"📊 Webhook status: {response.status_code}")
    print(f"📝 Webhook response: {response.text[:100]}")
    
    if response.status_code == 200:
        print("✅ Webhook responding correctly!")
    else:
        print("❌ Webhook still has issues")
        
except Exception as e:
    print(f"❌ Direct webhook test error: {e}")

print("\n📋 XULOSA:")
print("Bot Telegram'da test qilish uchun @uzmovi_film_bot ga /start yuboring")
