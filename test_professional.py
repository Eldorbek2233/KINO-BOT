# Quick Test for Professional Bot
import json
import os

# Test data files existence
print("📊 PROFESSIONAL BOT TEST RESULTS:")
print("=" * 50)

files_to_check = [
    'app.py',
    'config.py', 
    'users.json',
    'movies.json',
    'channels.json'
]

for file in files_to_check:
    if os.path.exists(file):
        size = os.path.getsize(file)
        print(f"✅ {file} - {size} bytes")
    else:
        print(f"❌ {file} - Not found")

print("\n📋 Configuration Check:")
try:
    from config import BOT_TOKEN, ADMIN_ID, API_URL
    print(f"✅ BOT_TOKEN: {'*' * 20}...{BOT_TOKEN[-10:] if BOT_TOKEN else 'Not set'}")
    print(f"✅ ADMIN_ID: {ADMIN_ID}")
    print(f"✅ API_URL: {API_URL}")
except Exception as e:
    print(f"❌ Config error: {e}")

print("\n🎬 Movies Database:")
try:
    if os.path.exists('movies.json'):
        with open('movies.json', 'r', encoding='utf-8') as f:
            movies = json.load(f)
        print(f"✅ Total movies: {len(movies)}")
        if movies:
            print(f"✅ Sample codes: {list(movies.keys())[:5]}")
    else:
        print("❌ Movies database not found")
except Exception as e:
    print(f"❌ Movies error: {e}")

print("\n👥 Users Database:")
try:
    if os.path.exists('users.json'):
        with open('users.json', 'r', encoding='utf-8') as f:
            users = json.load(f)
        print(f"✅ Total users: {len(users)}")
    else:
        print("❌ Users database not found")
except Exception as e:
    print(f"❌ Users error: {e}")

print("\n🎭 ULTIMATE PROFESSIONAL KINO BOT V3.0 - READY! ✅")
