#!/usr/bin/env python3
"""
Bot holatini tekshirish uchun test script
"""

import requests
from config import TOKEN
import os

def test_bot_api():
    """Bot API ni tekshirish"""
    print("🔍 Bot API ni tekshirish...")
    
    # getMe API chaqiruvi
    url = f"https://api.telegram.org/bot{TOKEN}/getMe"
    
    try:
        response = requests.get(url, timeout=10)
        result = response.json()
        
        if result.get('ok'):
            bot_info = result.get('result', {})
            print(f"✅ Bot API ishlayapti!")
            print(f"   Bot username: @{bot_info.get('username', 'Unknown')}")
            print(f"   Bot ID: {bot_info.get('id', 'Unknown')}")
            print(f"   Bot name: {bot_info.get('first_name', 'Unknown')}")
            return True
        else:
            print(f"❌ Bot API xatoligi: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Bot API so'rovida xatolik: {e}")
        return False

def test_webhook_status():
    """Webhook holatini tekshirish"""
    print("\n🔍 Webhook holatini tekshirish...")
    
    url = f"https://api.telegram.org/bot{TOKEN}/getWebhookInfo"
    
    try:
        response = requests.get(url, timeout=10)
        result = response.json()
        
        if result.get('ok'):
            webhook_info = result.get('result', {})
            webhook_url = webhook_info.get('url', '')
            
            print(f"📡 Webhook URL: {webhook_url}")
            print(f"📊 Pending updates: {webhook_info.get('pending_update_count', 0)}")
            
            last_error_date = webhook_info.get('last_error_date', 'Yoq')
            last_error_msg = webhook_info.get('last_error_message', 'Yoq')
            print(f"📅 Last error date: {last_error_date}")
            print(f"❌ Last error: {last_error_msg}")
            
            if webhook_url:
                print("✅ Webhook o'rnatilgan")
                return True
            else:
                print("⚠️ Webhook o'rnatilmagan")
                return False
        else:
            print(f"❌ Webhook info xatoligi: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Webhook info so'rovida xatolik: {e}")
        return False

def test_render_url():
    """Render URL ni tekshirish"""
    print("\n🔍 Render URL ni tekshirish...")
    
    render_url = os.getenv('RENDER_EXTERNAL_URL')
    if not render_url:
        print("⚠️ RENDER_EXTERNAL_URL environment variable topilmadi")
        print("💡 Local test ekan, manual webhook o'rnatish kerak")
        return False
    
    print(f"🌐 Render URL: {render_url}")
    
    # Health check
    try:
        health_url = f"{render_url}/health"
        response = requests.get(health_url, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ Health check OK: {response.text}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Health check xatolik: {e}")
        return False

def set_webhook_manually():
    """Manual webhook o'rnatish"""
    print("\n🔧 Manual webhook o'rnatish...")
    
    render_url = os.getenv('RENDER_EXTERNAL_URL')
    if not render_url:
        print("❌ RENDER_EXTERNAL_URL topilmadi, webhook o'rnatib bo'lmaydi")
        return False
    
    webhook_url = f"{render_url}/webhook"
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
    data = {"url": webhook_url}
    
    try:
        response = requests.post(url, data=data, timeout=10)
        result = response.json()
        
        if result.get('ok'):
            print(f"✅ Webhook muvaffaqiyatli o'rnatildi: {webhook_url}")
            return True
        else:
            print(f"❌ Webhook o'rnatishda xatolik: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Webhook o'rnatish so'rovida xatolik: {e}")
        return False

if __name__ == "__main__":
    print("🤖 Kino Bot holat tekshiruvi\n")
    print("=" * 50)
    
    # Bot API tekshirish
    bot_ok = test_bot_api()
    
    # Webhook holati tekshirish
    webhook_ok = test_webhook_status()
    
    # Render URL tekshirish
    render_ok = test_render_url()
    
    print("\n" + "=" * 50)
    print("📋 XULOSA:")
    print(f"   Bot API: {'✅ OK' if bot_ok else '❌ XATOLIK'}")
    print(f"   Webhook: {'✅ OK' if webhook_ok else '❌ XATOLIK'}")
    print(f"   Render:  {'✅ OK' if render_ok else '❌ XATOLIK'}")
    
    if not webhook_ok and render_ok:
        print("\n🔧 Webhook o'rnatishga harakat qilmoqda...")
        if set_webhook_manually():
            print("✅ Webhook qayta o'rnatildi!")
        else:
            print("❌ Webhook o'rnatishda muammo")
    
    if bot_ok and webhook_ok and render_ok:
        print("\n🎉 Hammasi yaxshi! Bot ishlashi kerak.")
        print("💬 Telegram da botga /start yuboring")
    else:
        print("\n⚠️ Muammolar mavjud. Loglarni tekshiring.")
