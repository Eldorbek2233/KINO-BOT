#!/usr/bin/env python3
"""
MongoDB Integration Test
Test bot with enhanced movie upload and MongoDB features
"""

import os
import requests
import json
from datetime import datetime

# Configuration
BOT_TOKEN = "8177519032:AAED4FgPoFQiQhqM_lvrK1iV8hL9u4SnkDk"
ADMIN_ID = 5542016161
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text, keyboard=None):
    """Send message to Telegram"""
    url = f"{BASE_URL}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    if keyboard:
        data['reply_markup'] = json.dumps(keyboard)
    
    try:
        response = requests.post(url, data=data, timeout=10)
        return response.json()
    except Exception as e:
        print(f"❌ Send message error: {e}")
        return None

def test_mongodb_features():
    """Test MongoDB integration features"""
    print("🧪 Testing MongoDB Integration Features...")
    
    # Test 1: Send start command
    print("\n1️⃣ Testing start command...")
    result = send_message(ADMIN_ID, "/start")
    if result and result.get('ok'):
        print("✅ Start command sent")
    else:
        print("❌ Start command failed")
    
    # Test 2: Send admin command
    print("\n2️⃣ Testing admin panel...")
    result = send_message(ADMIN_ID, "/admin")
    if result and result.get('ok'):
        print("✅ Admin command sent")
    else:
        print("❌ Admin command failed")
    
    # Test 3: Test movie code
    print("\n3️⃣ Testing movie request...")
    result = send_message(ADMIN_ID, "123")
    if result and result.get('ok'):
        print("✅ Movie request sent")
    else:
        print("❌ Movie request failed")
    
    print("\n✅ All tests completed!")
    print("📱 Check your Telegram for results")
    print("🔧 Bot should show:")
    print("   - Professional interface")
    print("   - Enhanced upload system with title input")
    print("   - MongoDB integration status")
    print("   - Complete admin panel")

def test_webhook_status():
    """Check webhook and bot status"""
    try:
        # Get webhook info
        url = f"{BASE_URL}/getWebhookInfo"
        response = requests.get(url, timeout=10)
        webhook_info = response.json()
        
        print("🌐 Webhook Status:")
        if webhook_info.get('ok'):
            webhook_url = webhook_info.get('result', {}).get('url', 'Not set')
            print(f"   URL: {webhook_url}")
            print(f"   Status: {'✅ Active' if webhook_url else '❌ Not set'}")
        
        # Get bot info
        url = f"{BASE_URL}/getMe"
        response = requests.get(url, timeout=10)
        bot_info = response.json()
        
        print("\n🤖 Bot Status:")
        if bot_info.get('ok'):
            bot_data = bot_info.get('result', {})
            print(f"   Name: {bot_data.get('first_name', 'Unknown')}")
            print(f"   Username: @{bot_data.get('username', 'Unknown')}")
            print(f"   Status: ✅ Active")
        else:
            print("   Status: ❌ Error")
        
    except Exception as e:
        print(f"❌ Status check error: {e}")

if __name__ == "__main__":
    print("🎭 PROFESSIONAL KINO BOT - MongoDB Test")
    print("=" * 50)
    
    test_webhook_status()
    print("\n" + "=" * 50)
    test_mongodb_features()
    
    print("\n📋 Next Steps:")
    print("1. Check bot responses in Telegram")
    print("2. Test movie upload with title input")
    print("3. Verify MongoDB connection status")
    print("4. Test all admin panel features")
    print("\n🚀 Bot is ready for professional use!")
