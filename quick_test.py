#!/usr/bin/env python3
"""Quick test script"""

import requests
from config import TOKEN

def test_webhook():
    """Test webhook status"""
    try:
        # Test server
        print("Testing server...")
        server_response = requests.get("https://kino-bot-o8dw.onrender.com/", timeout=10)
        print(f"Server status: {server_response.status_code}")
        print(f"Server response: {server_response.text[:100]}")
        
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
