#!/usr/bin/env python3
"""Test /delete command directly"""

import os
import sys
import json
import logging
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

print("🔧 TESTING /delete COMMAND")
print("=" * 50)

# Import from app
try:
    from app import (
        handle_message, 
        handle_delete_movies_menu_impl,
        movies_db,
        ADMIN_ID,
        upload_sessions
    )
    print("✅ Successfully imported app components")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def test_delete_command():
    """Test the /delete command processing"""
    print("\n🧪 Testing /delete command processing...")
    
    # Test message structure
    test_message = {
        'chat': {'id': ADMIN_ID},
        'from': {'id': ADMIN_ID, 'username': 'admin'},
        'text': '/delete'
    }
    
    print(f"📝 Test message: {test_message}")
    print(f"👑 Admin ID: {ADMIN_ID}")
    print(f"🎬 Movies in database: {len(movies_db)}")
    
    # Clear any existing sessions
    if ADMIN_ID in upload_sessions:
        del upload_sessions[ADMIN_ID]
        print("🧹 Cleared existing admin session")
    
    # Test the message handler
    try:
        print("\n🚀 Processing /delete message...")
        handle_message(test_message)
        
        # Check if session was created
        if ADMIN_ID in upload_sessions:
            session = upload_sessions[ADMIN_ID]
            print(f"✅ Session created: {session}")
            
            if session.get('type') == 'delete_movie':
                print("🎯 PERFECT! Delete session was created correctly!")
                return True
            else:
                print(f"❌ Wrong session type: {session.get('type')}")
                return False
        else:
            print("❌ No session was created")
            return False
            
    except Exception as e:
        print(f"❌ Error processing message: {e}")
        return False

def test_direct_delete_menu():
    """Test the delete menu function directly"""
    print("\n🧪 Testing delete menu function directly...")
    
    try:
        # Mock send_message to capture output
        sent_messages = []
        
        def mock_send_message(chat_id, text, keyboard=None):
            sent_messages.append({
                'chat_id': chat_id,
                'text': text,
                'keyboard': keyboard
            })
            print(f"📤 Would send message to {chat_id}:")
            print(f"   Text: {text[:100]}...")
            if keyboard:
                print(f"   Keyboard: {keyboard}")
        
        # Temporarily replace send_message
        import app
        original_send_message = app.send_message
        app.send_message = mock_send_message
        
        # Test the function
        handle_delete_movies_menu_impl(ADMIN_ID)
        
        # Restore original function
        app.send_message = original_send_message
        
        if sent_messages:
            print(f"✅ Delete menu function sent {len(sent_messages)} messages")
            return True
        else:
            print("❌ No messages were sent")
            return False
            
    except Exception as e:
        print(f"❌ Error testing delete menu: {e}")
        return False

if __name__ == "__main__":
    print("🎬 Current movies in database:")
    for code, movie in movies_db.items():
        print(f"  • {code}: {movie.get('title', 'Unknown')}")
    
    print(f"\n👑 Admin ID: {ADMIN_ID}")
    print(f"📋 Current sessions: {upload_sessions}")
    
    # Run tests
    test1_result = test_delete_command()
    test2_result = test_direct_delete_menu()
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS:")
    print(f"• /delete command test: {'✅ PASS' if test1_result else '❌ FAIL'}")
    print(f"• Delete menu direct test: {'✅ PASS' if test2_result else '❌ FAIL'}")
    
    if test1_result and test2_result:
        print("\n🎉 ALL TESTS PASSED! /delete command should work!")
    else:
        print("\n❌ Some tests failed. Check the logs above.")
