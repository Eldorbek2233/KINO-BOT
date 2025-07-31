#!/usr/bin/env python3
"""
🎬 FINAL MOVIE DELETION INTEGRATION TEST
Test the actual bot with movie deletion functionality
"""

import subprocess
import time
import os
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def verify_bot_ready():
    """Verify bot is ready to run"""
    print("🔍 VERIFYING BOT READINESS")
    print("="*40)
    
    # Check required files
    required_files = ['app.py', 'config.py', 'file_ids.json']
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file}: {size:,} bytes")
        else:
            print(f"❌ {file}: MISSING!")
            return False
    
    # Check movie database
    try:
        with open('file_ids.json', 'r', encoding='utf-8') as f:
            movies = json.load(f)
        print(f"✅ Movies database: {len(movies)} movies loaded")
        
        # Show some movies
        if movies:
            print("📋 Available movies for testing:")
            for i, (code, info) in enumerate(list(movies.items())[:3]):
                if isinstance(info, dict):
                    title = info.get('title', f'Movie {code}')
                    print(f"   • {code}: {title}")
                else:
                    print(f"   • {code}: Simple format")
        else:
            print("⚠️ No movies available for testing")
    except Exception as e:
        print(f"❌ Failed to load movies: {e}")
        return False
    
    print("✅ Bot is ready to run!")
    return True

def run_bot_test():
    """Run the bot and test movie deletion"""
    print("\n🚀 STARTING BOT FOR TESTING")
    print("="*40)
    
    print("📝 Instructions for testing:")
    print("1. Bot will start in a few seconds")
    print("2. Open Telegram and find your bot")
    print("3. Send /start to begin")
    print("4. Use admin commands to test movie deletion")
    print("5. Try the sequence: /admin_menu → Delete Movies → Enter movie code")
    print("6. Press Ctrl+C to stop the bot when done testing")
    print()
    
    print("🎬 STARTING KINO BOT...")
    print("⏳ Please wait while bot initializes...")
    print()
    
    try:
        # Run the bot
        result = subprocess.run(['python', 'app.py'], 
                              cwd=os.getcwd(),
                              capture_output=False,
                              text=True)
        
        if result.returncode == 0:
            print("✅ Bot ran successfully!")
        else:
            print(f"❌ Bot exited with code: {result.returncode}")
            
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user (Ctrl+C)")
        print("✅ Test completed")
    except Exception as e:
        print(f"❌ Error running bot: {e}")

def show_testing_guide():
    """Show detailed testing guide"""
    print("\n📚 MOVIE DELETION TESTING GUIDE")
    print("="*50)
    
    print("""
🎯 TESTING STEPS:

1️⃣ START THE BOT:
   • Send /start to your bot
   • Verify welcome message appears
   • Check that buttons work

2️⃣ ACCESS ADMIN PANEL:
   • Send /admin_menu (only works for admin)
   • Look for "🎬 KINO BOSHQARUVI" button
   • Click on it

3️⃣ ACCESS MOVIE DELETION:
   • In movie management menu
   • Click "🗑 KINOLARNI O'CHIRISH" 
   • Bot should ask for movie code

4️⃣ TEST MOVIE DELETION:
   • Enter one of these test codes:
     - 123 (Avengers Endgame)
     - 456 (Spider-Man No Way Home)  
     - 789 (Top Gun Maverick)
   • Bot should show confirmation button
   • Click confirmation to delete

5️⃣ VERIFY DELETION:
   • Check that movie is removed
   • Try accessing the deleted movie
   • Should get "not found" message

🔍 WHAT TO LOOK FOR:
✅ Bot responds to movie codes
✅ Confirmation buttons appear
✅ Deletion completes successfully
✅ File is actually removed
✅ Success message shows correct info

❌ PROBLEMS TO REPORT:
❌ Bot doesn't respond to codes
❌ No confirmation buttons
❌ Deletion fails or hangs
❌ Movies still accessible after deletion
❌ Error messages appear
""")

if __name__ == "__main__":
    print("🤖 KINO BOT - FINAL INTEGRATION TEST")
    print("🎬 Testing complete movie deletion functionality")
    print()
    
    # Verify bot readiness
    if verify_bot_ready():
        show_testing_guide()
        
        # Ask user if ready to start
        input("\n⏳ Press ENTER when ready to start the bot...")
        
        # Run bot test
        run_bot_test()
        
        print("\n" + "="*60)
        print("🎊 TESTING COMPLETED!")
        print("🎬 Movie deletion system has been tested")
        print("💬 If everything worked correctly, your bot is fixed!")
        print("❓ If you found issues, please report them")
        print("="*60)
    else:
        print("\n❌ Bot is not ready. Please fix the issues above.")
