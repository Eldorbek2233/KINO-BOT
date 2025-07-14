#!/usr/bin/env python3
"""
Local test script for Kino Bot
"""

import requests
import json
import time

# Bot ma'lumotlari
BOT_TOKEN = "8177519032:AAED4FgPoFQiQhqM_lvrK1iV8hL9u4SnkDk"
LOCAL_WEBHOOK_URL = "http://localhost:8080/webhook"

def test_webhook():
    """Test webhook endpoint"""
    print("🧪 Testing webhook endpoint...")
    
    # Test /health endpoint
    try:
        response = requests.get("http://localhost:8080/health")
        print(f"✅ Health check: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test basic webhook structure
    test_update = {
        "update_id": 123456789,
        "message": {
            "message_id": 1,
            "from": {
                "id": 5542016161,
                "is_bot": False,
                "first_name": "Test",
                "username": "testuser"
            },
            "chat": {
                "id": 5542016161,
                "first_name": "Test",
                "username": "testuser",
                "type": "private"
            },
            "date": int(time.time()),
            "text": "/start"
        }
    }
    
    try:
        response = requests.post(
            LOCAL_WEBHOOK_URL,
            json=test_update,
            headers={"Content-Type": "application/json"}
        )
        print(f"✅ Webhook test: {response.status_code} - {response.text}")
        return True
    except Exception as e:
        print(f"❌ Webhook test failed: {e}")
        return False

def check_bot_info():
    """Check bot information"""
    print("🤖 Checking bot information...")
    
    try:
        response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getMe")
        result = response.json()
        
        if result.get('ok'):
            bot_info = result['result']
            print(f"✅ Bot name: {bot_info['first_name']}")
            print(f"✅ Bot username: @{bot_info['username']}")
            print(f"✅ Bot ID: {bot_info['id']}")
            return True
        else:
            print(f"❌ Bot check failed: {result}")
            return False
    except Exception as e:
        print(f"❌ Bot check error: {e}")
        return False

def main():
    print("🚀 Starting Kino Bot local test...")
    print("=" * 50)
    
    # Check bot info
    if not check_bot_info():
        return
    
    print("=" * 50)
    
    # Test webhook
    if test_webhook():
        print("=" * 50)
        print("✅ Local test completed successfully!")
        print("🔗 Bot is running at: http://localhost:8080")
        print("📡 Webhook endpoint: http://localhost:8080/webhook")
        print("💡 To test with real Telegram messages, use ngrok or deploy to Railway")
    else:
        print("=" * 50)
        print("❌ Local test failed!")

if __name__ == "__main__":
    main()
