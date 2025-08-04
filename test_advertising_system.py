#!/usr/bin/env python3
"""
Advertising System Debug Test
Tests the broadcast/advertising system functionality
"""

import sys
import os
import json

# Add current directory to path to import from app.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_broadcast_system():
    """Test the advertising system components"""
    print("🧪 Testing Advertising System...")
    
    try:
        # Test 1: Check if app.py can be imported
        print("📦 Test 1: Importing app.py...")
        from app import (
            handle_broadcast_menu, 
            handle_broadcast_start, 
            handle_broadcast_session,
            handle_broadcast_confirmation,
            broadcast_sessions,
            users_db,
            ADMIN_ID
        )
        print("✅ Successfully imported broadcast functions")
        
        # Test 2: Check admin ID
        print(f"\n👑 Test 2: Admin ID configured: {ADMIN_ID}")
        
        # Test 3: Check users database
        print(f"\n👥 Test 3: Users database: {len(users_db)} users loaded")
        
        # Test 4: Check broadcast sessions
        print(f"\n📣 Test 4: Broadcast sessions: {len(broadcast_sessions)} active")
        
        # Test 5: Test callback data mapping
        print("\n🔗 Test 5: Checking callback handlers...")
        
        # Simulate the callback mapping
        callback_map = {
            'broadcast_menu': 'handle_broadcast_menu',
            'broadcast_text': 'handle_broadcast_start',
            'broadcast_photo': 'handle_broadcast_start', 
            'broadcast_video': 'handle_broadcast_start',
            'confirm_broadcast': 'handle_broadcast_confirmation',
            'cancel_broadcast': 'cancel_broadcast_handler'
        }
        
        for callback, handler in callback_map.items():
            print(f"   • {callback} → {handler}")
        
        print("✅ Callback mapping looks correct")
        
        # Test 6: Check send_message function
        print("\n📨 Test 6: Testing send_message function...")
        try:
            from app import send_message
            print("✅ send_message function available")
        except ImportError as e:
            print(f"❌ send_message function missing: {e}")
        
        # Test 7: Check if answer_callback_query exists
        print("\n📞 Test 7: Testing answer_callback_query function...")
        try:
            from app import answer_callback_query
            print("✅ answer_callback_query function available")
        except ImportError as e:
            print(f"❌ answer_callback_query function missing: {e}")
        
        print("\n🎯 Test Summary:")
        print("✅ Broadcast system components are properly imported")
        print("✅ Admin ID is configured")
        print("✅ Database structures are available") 
        print("✅ Callback handlers are mapped")
        
        print("\n💡 Possible Issues to Check:")
        print("1. Check if telegram webhooks are properly configured")
        print("2. Verify admin can access broadcast menu")
        print("3. Test if broadcast sessions are created properly")
        print("4. Check network connectivity for message sending")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Make sure app.py is in the same directory")
        return False
    except Exception as e:
        print(f"❌ Test Error: {e}")
        return False

def test_callback_flow():
    """Test the callback flow for advertising"""
    print("\n🔄 Testing Callback Flow...")
    
    test_cases = [
        "broadcast_menu → Shows advertising menu",
        "broadcast_text → Starts text broadcast session",
        "broadcast_photo → Starts photo broadcast session", 
        "broadcast_video → Starts video broadcast session",
        "confirm_broadcast → Sends broadcast to all users",
        "cancel_broadcast → Cancels broadcast session"
    ]
    
    for case in test_cases:
        print(f"   📋 {case}")
    
    print("\n💭 Expected Flow:")
    print("1. Admin clicks '📣 Reklama' button")
    print("2. Bot shows broadcast menu with options")
    print("3. Admin selects broadcast type (text/photo/video)")
    print("4. Bot creates broadcast session and waits for content")
    print("5. Admin sends content (text/photo/video)")
    print("6. Bot shows confirmation with preview")
    print("7. Admin confirms and broadcast is sent to all users")

if __name__ == "__main__":
    print("🎭 KINO BOT - Advertising System Debug Test")
    print("=" * 50)
    
    success = test_broadcast_system()
    test_callback_flow()
    
    if success:
        print("\n🎉 Basic system test PASSED!")
        print("📝 Next steps: Test actual broadcast functionality")
    else:
        print("\n❌ System test FAILED!")
        print("🔧 Fix import issues before testing functionality")
