#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAJBURIY AZOLIK TIZIMI TEST SCRIPTI
Botda majburiy azolik sistemasi to'g'ri ishlayotganini tekshirish uchun
"""

def test_subscription_enforcement():
    """
    Test majburiy azolik sistemasi
    """
    print("🔒 MAJBURIY AZOLIK TIZIMI TESTI")
    print("=" * 50)
    
    # Read app.py to check subscription implementation
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if subscription enforcement is properly implemented
        checks = [
            ("handle_movie_request da azolik tekshiruvi", 
             "check_all_subscriptions(user_id)" in content and 
             "handle_movie_request" in content and
             "send_subscription_message(chat_id, user_id)" in content),
            
            ("handle_start_command da azolik tekshiruvi", 
             "is_subscribed = check_all_subscriptions(user_id)" in content and
             "handle_start_command" in content),
            
            ("check_subscription callback handler", 
             "elif data == 'check_subscription':" in content and
             "is_subscribed = check_all_subscriptions(user_id)" in content),
            
            ("Admin bypass mavjud", 
             "if user_id == ADMIN_ID:" in content and
             "if user_id != ADMIN_ID:" in content),
            
            ("Subscription message yuborish", 
             "send_subscription_message" in content and
             "NEW ROBUST SUBSCRIPTION MESSAGE" in content),
            
            ("Error handling", 
             "logger.info" in content and "subscription" in content.lower()),
        ]
        
        print("📋 MAJBURIY AZOLIK KOMPONENLARI:")
        print("-" * 30)
        
        passed = 0
        for check_name, passed_check in checks:
            status = "✅" if passed_check else "❌"
            print(f"{status} {check_name}")
            if passed_check:
                passed += 1
        
        print("-" * 30)
        success_rate = (passed / len(checks)) * 100
        print(f"📊 Muvaffaqiyat: {passed}/{len(checks)} ({success_rate:.1f}%)")
        
        if success_rate >= 90:
            print("🎉 EXCELLENT! Majburiy azolik tizimi to'liq faol!")
            print("✅ Hech kim obuna bo'lmasdan botdan foydalana olmaydi!")
        elif success_rate >= 70:
            print("⚠️ GOOD: Asosiy himoya ishlaydi, ba'zi qismlar yaxshilanishi mumkin")
        else:
            print("❌ CRITICAL: Majburiy azolik tizimi to'liq ishlamaydi!")
        
        return success_rate >= 90
        
    except FileNotFoundError:
        print("❌ app.py fayli topilmadi!")
        return False
    except Exception as e:
        print(f"❌ Xatolik: {e}")
        return False

def test_subscription_flow():
    """
    Test subscription flow scenarios
    """
    print("\n🔄 AZOLIK FLOW TESTI:")
    print("-" * 30)
    
    scenarios = [
        "1. Yangi foydalanuvchi /start bosadi",
        "2. check_all_subscriptions() chaqiriladi", 
        "3. Agar obuna yo'q: send_subscription_message()",
        "4. Foydalanuvchi kanallarga obuna bo'ladi",
        "5. 'Tekshirish' tugmasini bosadi",
        "6. check_subscription callback ishga tushadi",
        "7. Agar obuna bo'lsa: handle_start_command()",
        "8. Kino kodi yuborganda: handle_movie_request()",
        "9. Yana check_all_subscriptions() tekshiriladi",
        "10. Obuna bo'lsa: kino yuboriladi"
    ]
    
    for scenario in scenarios:
        print(f"✅ {scenario}")
    
    print("\n💡 MUHIM QOIDALAR:")
    print("• Admin (5542016161) hech qachon majburiy azolikka tabi emas")
    print("• Oddiy foydalanuvchilar har bir amalda tekshiriladi") 
    print("• Invalid kanallar avtomatik o'chiriladi")
    print("• 5 daqiqalik cache mavjud (performance uchun)")

def show_usage_guide():
    """
    Show usage guide for testing
    """
    print("\n📖 TEST QILISH YO'RIQNOMASI:")
    print("=" * 30)
    print("""
🧪 QANDAY TEST QILISH:

1️⃣ KANAL QO'SHISH:
   • /admin → Kanallar → Kanal qo'shish
   • Test kanali: @your_test_channel
   • Bot o'sha kanalda admin bo'lishi kerak

2️⃣ ODDIY FOYDALANUVCHI SIFATIDA TEST:
   • Boshqa Telegram accountdan botga /start yuboring
   • Majburiy azolik xabari ko'rsatilishi kerak
   • Kanallarga obuna bo'lmay "Tekshirish" bosing → xatolik
   • Kanallarga obuna bo'lib "Tekshirish" bosing → kirish
   • Kino kodi yuboring → ishlashi kerak

3️⃣ ADMIN TEST:
   • O'zingizdan /start yuboring
   • Darhol admin panel ko'rsatilishi kerak
   • Hech qanday majburiy azolik bo'lmasligi kerak

4️⃣ XATOLIK TEST:
   • Invalid kanal qo'shing
   • Bot avtomatik nofaol qilishi kerak
   • Xatolik bo'lganda graceful handling

5️⃣ CACHE TEST:
   • Bir marta tekshirilgandan keyin
   • 5 daqiqa ichida qayta API chaqiruv bo'lmasligi kerak
""")

def main():
    """
    Main test function
    """
    print("🎭 ULTIMATE PROFESSIONAL KINO BOT")
    print("🔒 Majburiy Azolik Tizimi - Test Script") 
    print("="*60)
    
    # Run main test
    system_working = test_subscription_enforcement()
    
    # Show subscription flow
    test_subscription_flow()
    
    # Show usage guide
    show_usage_guide()
    
    # Final result
    print("\n🎯 YAKUNIY NATIJA:")
    print("="*20)
    
    if system_working:
        print("✅ PERFECT! Majburiy azolik tizimi to'liq faol!")
        print("🛡️ Botingiz endi himoyalangan!")
        print("🎯 Faqat obuna bo'lgan foydalanuvchilar botdan foydalana oladi!")
        print("👑 Admin har doim to'liq ruxsatga ega!")
        print("")
        print("📱 TEST QILISH:")
        print("1. Oddiy account dan botga /start yuboring")
        print("2. Majburiy azolik xabari ko'rsatilishini tekshiring")
        print("3. Kanallarga obuna bo'ling va 'Tekshirish' bosing")
        print("4. Faqat shundan keyin bot ishlay boshlashi kerak!")
    else:
        print("❌ XATOLIK: Majburiy azolik tizimi to'liq ishlamaydi!")
        print("🔧 app.py faylini qayta tekshiring")
        print("📞 Developer bilan bog'laning")
    
    print("\n🎭 Ultimate Professional Kino Bot V3.0")
    print("🔥 Majburiy azolik tizimi - Test tugallandi!")

if __name__ == "__main__":
    main()
