#!/usr/bin/env python3
"""
Send Test Message to Admin
Direct bot test without external requests
"""
import requests
import json
from datetime import datetime

# Configuration
TOKEN = "8177519032:AAED4FgPoFQiQhqM_lvrK1iV8hL9u4SnkDk"
ADMIN_ID = 5542016161

def send_test_message():
    """Send test message to admin"""
    try:
        print("📱 Sending test message to admin...")
        
        # Message content
        message = f"""🧪 <b>Railway Bot Test</b>

✅ Bot is running on Railway
⏰ Test time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🔗 URL: https://web-production-8240a.up.railway.app

📊 <b>Database Status:</b>
• 👥 Users: 71
• 🎬 Movies: 12  
• 📺 Channels: 2

🎯 <b>Test /start command to verify bot response!</b>"""
        
        # Send message
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {
            'chat_id': ADMIN_ID,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        response = requests.post(url, data=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                print("✅ Test message sent to admin successfully!")
                print("💬 Check your Telegram for the message")
                print("🧪 Now test /start command in bot to verify it responds")
                return True
            else:
                print(f"❌ Telegram API error: {result}")
        else:
            print(f"❌ HTTP error: {response.status_code}")
            print(f"Response: {response.text}")
        
        return False
        
    except Exception as e:
        print(f"❌ Error sending test message: {e}")
        return False

def check_bot_me():
    """Check bot info"""
    try:
        print("🤖 Checking bot info...")
        
        url = f"https://api.telegram.org/bot{TOKEN}/getMe"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                bot = result['result']
                print(f"✅ Bot: @{bot.get('username')} - {bot.get('first_name')}")
                return True
        
        print("❌ Bot info check failed")
        return False
        
    except Exception as e:
        print(f"❌ Bot info error: {e}")
        return False

if __name__ == "__main__":
    print("🎭 Railway Bot Direct Test")
    print("=" * 40)
    
    # Check bot
    bot_ok = check_bot_me()
    
    if bot_ok:
        # Send test message
        message_sent = send_test_message()
        
        if message_sent:
            print("\n" + "=" * 40)
            print("🎉 SUCCESS! Test message sent.")
            print("\n📋 NEXT STEPS:")
            print("1. Check your Telegram for the test message")
            print("2. Send /start to your bot to test response")
            print("3. Try sending movie codes (like '123' or '#123')")
            print("4. If bot responds, everything is working!")
        else:
            print("\n❌ Failed to send test message")
    else:
        print("\n❌ Bot connection failed")
        
    print("\n🔗 Your bot URL: https://web-production-8240a.up.railway.app")
    print("💡 Bot should be accessible to users now!")
