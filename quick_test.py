#!/usr/bin/env python3
"""
Simple Railway Test
Quick check for Railway accessibility
"""
import requests
import json

def quick_test():
    try:
        print("🔍 Quick Railway Test...")
        
        # Test Railway health endpoint
        url = "https://web-production-8240a.up.railway.app/health"
        print(f"Testing: {url}")
        
        response = requests.get(url, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
        if response.status_code == 200:
            print("✅ Railway is accessible!")
        else:
            print(f"❌ Railway returned: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout - Railway might be slow")
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error - Railway might be down")
    except Exception as e:
        print(f"❌ Error: {e}")

def check_telegram_webhook():
    try:
        print("\n🔍 Checking Telegram webhook...")
        
        TOKEN = "8177519032:AAED4FgPoFQiQhqM_lvrK1iV8hL9u4SnkDk"
        url = f"https://api.telegram.org/bot{TOKEN}/getWebhookInfo"
        
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            webhook_info = data.get('result', {})
            print(f"Webhook URL: {webhook_info.get('url', 'Not set')}")
            print(f"Pending Updates: {webhook_info.get('pending_update_count', 0)}")
            print(f"Last Error: {webhook_info.get('last_error_message', 'None')}")
        else:
            print(f"❌ Telegram API error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Webhook check error: {e}")

if __name__ == "__main__":
    quick_test()
    check_telegram_webhook()
        # Test webhook info
        print("\nTesting webhook...")
        webhook_response = requests.get(f"https://api.telegram.org/bot{TOKEN}/getWebhookInfo", timeout=10)
        webhook_info = webhook_response.json()['result']
        
        print(f"Webhook URL: {webhook_info.get('url')}")
        print(f"Last error: {webhook_info.get('last_error_message')}")
        print(f"Pending updates: {webhook_info.get('pending_update_count')}")
        
        if webhook_info.get('last_error_message'):
            print("❌ Webhook has errors")
        else:
            print("✅ Webhook OK")
            
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_webhook()
