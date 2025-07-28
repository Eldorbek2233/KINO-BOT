#!/usr/bin/env python3
"""
Test Railway Bot Functionality
Quick test to verify bot is working correctly
"""
import requests
import json
import os

# Bot configuration
TOKEN = "8177519032:AAED4FgPoFQiQhqM_lvrK1iV8hL9u4SnkDk"
RAILWAY_URL = "https://web-production-8240a.up.railway.app"

def test_webhook_endpoint():
    """Test webhook endpoint"""
    try:
        print("🔍 Testing Railway webhook endpoint...")
        
        # Test health endpoint
        health_url = f"{RAILWAY_URL}/health"
        response = requests.get(health_url, timeout=10)
        
        print(f"Health Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check: {data}")
        else:
            print(f"❌ Health check failed: {response.text}")
            
        # Test webhook endpoint with sample data
        webhook_url = f"{RAILWAY_URL}/webhook"
        sample_data = {
            "update_id": 12345,
            "message": {
                "message_id": 1,
                "date": 1234567890,
                "chat": {"id": 123, "type": "private"},
                "from": {"id": 123, "first_name": "Test", "username": "testuser"},
                "text": "/start"
            }
        }
        
        print(f"\n🔍 Testing webhook with sample data...")
        webhook_response = requests.post(
            webhook_url, 
            json=sample_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"Webhook Status: {webhook_response.status_code}")
        print(f"Webhook Response: {webhook_response.text}")
        
        if webhook_response.status_code == 200:
            print("✅ Webhook is working!")
        else:
            print("❌ Webhook has issues")
            
    except Exception as e:
        print(f"❌ Test error: {e}")

def test_telegram_webhook():
    """Test Telegram webhook configuration"""
    try:
        print("\n🔍 Testing Telegram webhook configuration...")
        
        # Get webhook info
        url = f"https://api.telegram.org/bot{TOKEN}/getWebhookInfo"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                webhook_info = data.get('result', {})
                print(f"✅ Webhook Info:")
                print(f"   URL: {webhook_info.get('url', 'Not set')}")
                print(f"   Has Custom Certificate: {webhook_info.get('has_custom_certificate', False)}")
                print(f"   Pending Update Count: {webhook_info.get('pending_update_count', 0)}")
                print(f"   Last Error Date: {webhook_info.get('last_error_date', 'None')}")
                print(f"   Last Error Message: {webhook_info.get('last_error_message', 'None')}")
                print(f"   Max Connections: {webhook_info.get('max_connections', 40)}")
                
                return webhook_info
            else:
                print(f"❌ Telegram API error: {data}")
        else:
            print(f"❌ HTTP error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Telegram webhook test error: {e}")

def send_test_message():
    """Send test message to admin"""
    try:
        print("\n🔍 Sending test message to admin...")
        
        admin_id = 5542016161
        test_message = "🧪 Railway Bot Test - Bot is working correctly!"
        
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {
            'chat_id': admin_id,
            'text': test_message,
            'parse_mode': 'HTML'
        }
        
        response = requests.post(url, data=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                print("✅ Test message sent successfully!")
                return True
            else:
                print(f"❌ Message send failed: {result}")
        else:
            print(f"❌ HTTP error: {response.status_code}")
            
        return False
        
    except Exception as e:
        print(f"❌ Test message error: {e}")
        return False

def main():
    """Run all tests"""
    print("🎭 Railway Bot Testing Started")
    print("=" * 50)
    
    # Test 1: Railway endpoints
    test_webhook_endpoint()
    
    # Test 2: Telegram webhook
    test_telegram_webhook()
    
    # Test 3: Send test message
    send_test_message()
    
    print("\n" + "=" * 50)
    print("🏁 Testing completed!")
    print("\n💡 If all tests pass, your bot should be working correctly.")
    print("💡 If there are errors, we'll fix them step by step.")

if __name__ == "__main__":
    main()
