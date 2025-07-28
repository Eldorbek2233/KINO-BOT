#!/usr/bin/env python3
"""
Railway deployment test
Botni Railway da test qilish uchun
"""

import os
import sys
import requests
import time

def test_railway_config():
    """Railway konfiguratsiyasini test qilish"""
    print("🚂 RAILWAY DEPLOYMENT TEST")
    print("=" * 50)
    
    try:
        from railway_config import get_token, get_admin_id, get_webhook_url, get_port
        
        # Token tekshirish
        token = get_token()
        print(f"✅ Bot Token: {token[:15]}..." if len(token) > 30 else f"❌ Invalid token: {token}")
        
        # Admin ID
        admin_id = get_admin_id()
        print(f"✅ Admin ID: {admin_id}")
        
        # Webhook URL
        webhook_url = get_webhook_url()
        print(f"✅ Webhook URL: {webhook_url}")
        
        # Port
        port = get_port()
        print(f"✅ Port: {port}")
        
        return True
        
    except Exception as e:
        print(f"❌ Railway config error: {e}")
        return False

def test_bot_connection():
    """Bot API bilan aloqani tekshirish"""
    try:
        from railway_config import get_token
        token = get_token()
        
        response = requests.get(f"https://api.telegram.org/bot{token}/getMe", timeout=10)
        data = response.json()
        
        if data.get('ok'):
            bot_info = data['result']
            print(f"✅ Bot connected: @{bot_info['username']}")
            print(f"   Bot name: {bot_info['first_name']}")
            return True
        else:
            print(f"❌ Bot connection failed: {data.get('description', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Bot connection error: {e}")
        return False

def test_mongodb():
    """MongoDB ulanishini tekshirish"""
    try:
        from pymongo import MongoClient
        from pymongo.errors import ConnectionFailure
        
        mongodb_uri = os.getenv('MONGODB_URI', 'mongodb+srv://eldorbekxakimxujayev4:Ali11042004@kinobot-cluster.quzswqg.mongodb.net/kinobot?retryWrites=true&w=majority&appName=kinobot-cluster')
        
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print("✅ MongoDB connected successfully")
        client.close()
        return True
        
    except Exception as e:
        print(f"⚠️ MongoDB connection failed (using file storage): {e}")
        return False

def test_app_import():
    """App import qilishni tekshirish"""
    try:
        import app
        print("✅ App imported successfully")
        return True
    except Exception as e:
        print(f"❌ App import failed: {e}")
        return False

def main():
    """Barcha testlarni ishga tushirish"""
    print("\n🚂 RAILWAY KINO BOT DEPLOYMENT TEST")
    print("=" * 60)
    
    tests = [
        ("Railway Config", test_railway_config),
        ("Bot Connection", test_bot_connection), 
        ("MongoDB", test_mongodb),
        ("App Import", test_app_import)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        if test_func():
            passed += 1
        time.sleep(1)
    
    print("\n" + "=" * 60)
    print(f"🎯 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Railway deployment ready! 🚂")
        print("\n📋 Next steps:")
        print("1. Push to GitHub: git add . && git commit -m 'Railway ready' && git push")
        print("2. Deploy to Railway: Connect GitHub repo")
        print("3. Set environment variables")
        print("4. Check deployment logs")
    else:
        print("⚠️ Some tests failed. Fix issues before deploying.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
