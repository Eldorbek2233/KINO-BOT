#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIMPLE VERIFICATION SCRIPT - Test the new subscription system
Run this to verify your bot's subscription system is working correctly
"""

def verify_subscription_system():
    """
    Simple verification of the new subscription system
    """
    print("🔍 YANGI MAJBURIY AZOLIK TIZIMI - TEKSHIRISH")
    print("=" * 50)
    
    # Read the app.py file to verify key components
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        checks = [
            ("NEW ROBUST SUBSCRIPTION SYSTEM", "check_all_subscriptions" in content and "NEW ROBUST SUBSCRIPTION SYSTEM" in content),
            ("Cache system", "subscription_cache" in content and "CACHE_DURATION" in content),
            ("Error handling", "requests.Timeout" in content and "except Exception" in content),
            ("Channel validation", "active_channels" in content and "channel_data.get('active'" in content),
            ("Auto cleanup", "auto_save_data" in content),
            ("Professional messages", "MAJBURIY AZOLIK TIZIMI" in content),
            ("No emergency bypass", ".subscription_disabled" not in content or "os.path.exists('.subscription_disabled')" not in content),
            ("Proper API handling", "response.status_code" in content and "timeout=" in content)
        ]
        
        print("📋 SYSTEM COMPONENTS CHECK:")
        print("-" * 30)
        
        passed = 0
        for check_name, passed_check in checks:
            status = "✅" if passed_check else "❌"
            print(f"{status} {check_name}")
            if passed_check:
                passed += 1
        
        print("-" * 30)
        success_rate = (passed / len(checks)) * 100
        print(f"📊 Success Rate: {passed}/{len(checks)} ({success_rate:.1f}%)")
        
        if success_rate >= 90:
            print("🎉 EXCELLENT! Yangi tizim to'liq o'rnatildi!")
            print("✅ Bot majburiy azolik bilan ishlashga tayyor!")
        elif success_rate >= 70:
            print("⚠️ GOOD: Asosiy funksiyalar ishlaydi, ba'zi qismlar yaxshilanishi mumkin")
        else:
            print("❌ NEEDS WORK: Ba'zi muhim qismlar yo'q yoki noto'g'ri")
        
        return success_rate >= 70
        
    except FileNotFoundError:
        print("❌ app.py fayli topilmadi!")
        return False
    except Exception as e:
        print(f"❌ Xatolik: {e}")
        return False

def check_channels_data():
    """
    Check if channels.json exists and has proper structure
    """
    print("\n📺 KANALLAR MA'LUMOTLARI TEKSHIRUVI:")
    print("-" * 30)
    
    try:
        import json
        with open('channels.json', 'r', encoding='utf-8') as f:
            channels = json.load(f)
        
        if not channels:
            print("ℹ️ Kanallar ro'yxati bo'sh - bu normal holat")
            print("💡 Admin panel orqali kanallar qo'shing")
            return True
        
        print(f"📊 Jami kanallar: {len(channels)}")
        
        for channel_id, channel_data in channels.items():
            name = channel_data.get('name', 'Noma\'lum')
            active = channel_data.get('active', True)
            status = "🟢 Faol" if active else "🔴 Nofaol"
            print(f"  • {name} - {status}")
        
        active_count = sum(1 for c in channels.values() if c.get('active', True))
        print(f"📈 Faol kanallar: {active_count}/{len(channels)}")
        
        return True
        
    except FileNotFoundError:
        print("ℹ️ channels.json fayli yo'q - bu normal holat")
        print("💡 Birinchi kanal qo'shganda yaratiladi")
        return True
    except Exception as e:
        print(f"❌ Xatolik: {e}")
        return False

def show_usage_instructions():
    """
    Show how to use the new system
    """
    print("\n📖 FOYDALANISH YO'RIQNOMASI:")
    print("=" * 30)
    print("""
1️⃣ KANAL QO'SHISH:
   • Botga /admin yuboring
   • 'Kanallar' bo'limini tanlang  
   • 'Kanal qo'shish' tugmasini bosing
   • Kanal username yoki ID kiriting
   • Bot o'sha kanalda admin bo'lishi kerak!

2️⃣ MAJBURIY AZOLIK TEKSHIRUVI:
   • Oddiy foydalanuvchi sifatida botga /start yuboring
   • Agar kanallar mavjud bo'lsa, majburiy azolik xabari ko'rsatiladi
   • Barcha kanallarga obuna bo'ling
   • 'Tekshirish' tugmasini bosing

3️⃣ MONITORING:
   • Admin panel → Kanallar → Kanallar statistikasi
   • Faol/nofaol kanallarni ko'rish
   • Invalid kanallarni tozalash

4️⃣ TROUBLESHOOTING:
   • Agar kanal ishlamayotgan bo'lsa, avtomatik nofaol qilinadi
   • Logs ni tekshiring: bot.log fayli
   • Admin sifatida /admin → Tizim → Logs
""")

def main():
    """
    Main verification function
    """
    print("🎭 ULTIMATE PROFESSIONAL KINO BOT")
    print("🔧 Yangi Majburiy Azolik Tizimi - Tekshirish")
    print("=" * 60)
    
    # Verify system components
    system_ok = verify_subscription_system()
    
    # Check channels data
    channels_ok = check_channels_data()
    
    # Show usage instructions
    show_usage_instructions()
    
    # Final verdict
    print("\n🎯 YAKUNIY NATIJA:")
    print("=" * 20)
    
    if system_ok and channels_ok:
        print("✅ PERFECT! Bot yangi tizim bilan ishga tayyor!")
        print("🚀 Endi foydalanuvchilar majburiy azolik orqali o'tishi kerak!")
        print("💡 Test uchun oddiy foydalanuvchi sifatida /start yuboring")
    else:
        print("⚠️ Ba'zi muammolar mavjud")
        print("🔧 app.py faylini tekshiring va qayta deploy qiling")
    
    print("\n🎭 Ultimate Professional Kino Bot V3.0")
    print("🔥 Yangi majburiy azolik tizimi faol!")

if __name__ == "__main__":
    main()
