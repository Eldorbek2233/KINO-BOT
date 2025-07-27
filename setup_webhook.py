#!/usr/bin/env python3
"""
WEBHOOK SETUP FOR RENDER.COM DEPLOYMENT
Professional Kino Bot - Production Webhook Configuration
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_webhook():
    """Setup webhook for production deployment"""
    
    # Bot configuration
    BOT_TOKEN = "8177519032:AAED4FgPoFQiQhqM_lvrK1iV8hL9u4SnkDk"
    
    # Render.com webhook URL (update this with your actual Render service URL)
    WEBHOOK_URL = "https://kino-bot-latest.onrender.com/webhook"  # Update this!
    
    print("🔗 Setting up webhook for production deployment...")
    print(f"📡 Webhook URL: {WEBHOOK_URL}")
    
    # Set webhook
    set_webhook_url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    
    payload = {
        'url': WEBHOOK_URL,
        'allowed_updates': ['message', 'callback_query', 'channel_post'],
        'drop_pending_updates': True
    }
    
    try:
        response = requests.post(set_webhook_url, json=payload, timeout=10)
        result = response.json()
        
        if result.get('ok'):
            print("✅ Webhook successfully set!")
            print(f"🎯 Webhook URL: {WEBHOOK_URL}")
            print("🚀 Bot is ready for production!")
            
            # Check webhook info
            webhook_info_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo"
            info_response = requests.get(webhook_info_url)
            info_result = info_response.json()
            
            if info_result.get('ok'):
                webhook_info = info_result.get('result', {})
                print("\n📊 WEBHOOK INFO:")
                print(f"• URL: {webhook_info.get('url', 'Not set')}")
                print(f"• Pending updates: {webhook_info.get('pending_update_count', 0)}")
                print(f"• Last error: {webhook_info.get('last_error_message', 'None')}")
                
        else:
            print(f"❌ Failed to set webhook: {result.get('description', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Webhook setup error: {e}")

def remove_webhook():
    """Remove webhook (for development)"""
    BOT_TOKEN = "8177519032:AAED4FgPoFQiQhqM_lvrK1iV8hL9u4SnkDk"
    
    delete_webhook_url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook"
    
    try:
        response = requests.post(delete_webhook_url, timeout=10)
        result = response.json()
        
        if result.get('ok'):
            print("🗑 Webhook removed successfully!")
        else:
            print(f"❌ Failed to remove webhook: {result.get('description')}")
            
    except Exception as e:
        print(f"❌ Webhook removal error: {e}")

if __name__ == "__main__":
    print("""
🎭 PROFESSIONAL KINO BOT - WEBHOOK SETUP

1. Setup webhook for production
2. Remove webhook (for development)
3. Exit

""")
    
    choice = input("Select option (1-3): ").strip()
    
    if choice == "1":
        setup_webhook()
    elif choice == "2":
        remove_webhook()
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice!")
