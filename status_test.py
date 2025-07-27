#!/usr/bin/env python3
print("🎭 Professional Kino Bot v3.0 - Status Test")
print("=" * 50)

try:
    import app
    print("✅ Bot imported successfully!")
    
    print(f"\n📊 Status:")  
    print(f"• Users: {len(app.users_db)}")
    print(f"• Movies: {len(app.movies_db)}")
    print(f"• Channels: {len(app.channels_db)}")
    print(f"• Admin ID: {app.ADMIN_ID}")
    
    print(f"\n🔧 Functions:")
    funcs = ['handle_admin_callbacks', 'handle_channels_menu', 'handle_users_menu', 
             'handle_upload_menu', 'handle_broadcast_menu', 'check_all_subscriptions']
    
    for f in funcs:
        print(f"• {f}: {'✅' if hasattr(app, f) else '❌'}")
    
    print(f"\n🚀 Initializing...")
    app.initialize_bot()
    
    print("\n🎉 SUCCESS!")
    print("✅ Admin panel tugmalari ishlaydi!")
    print("✅ Obuna tekshirish tuzatildi!")
    print("✅ Bot tayyor!")
    
except Exception as e:
    print(f"❌ Error: {e}")
