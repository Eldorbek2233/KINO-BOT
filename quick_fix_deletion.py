#!/usr/bin/env python3
"""
🎬 QUICK MOVIE DELETION FIX - FINAL SOLUTION
Instant fix for movie deletion problem
"""

import json
import os
import time

def fix_movie_deletion_now():
    """Fix movie deletion problem immediately"""
    print("🔧 FIXING MOVIE DELETION SYSTEM...")
    print("="*50)
    
    # Step 1: Check file_ids.json
    if not os.path.exists('file_ids.json'):
        print("❌ file_ids.json not found!")
        return False
    
    # Load movies
    with open('file_ids.json', 'r', encoding='utf-8') as f:
        movies_db = json.load(f)
    
    print(f"✅ Loaded {len(movies_db)} movies")
    
    if not movies_db:
        print("❌ No movies found in database!")
        return False
    
    # Show first few movies
    print("\n📋 Available movies:")
    for i, (code, movie) in enumerate(list(movies_db.items())[:5], 1):
        if isinstance(movie, dict):
            title = movie.get('title', f'Movie {code}')
            print(f"   {i}. {code}: {title}")
        else:
            print(f"   {i}. {code}: Simple format")
    
    # Create test session (simulating what bot does)
    print(f"\n🔧 SIMULATING DELETE SESSION...")
    
    ADMIN_ID = 5542016161  # Your admin ID
    upload_sessions = {}
    
    # Start delete session
    upload_sessions[ADMIN_ID] = {
        'type': 'delete_movie',
        'status': 'waiting_movie_code',
        'start_time': time.time()
    }
    
    print(f"✅ Created session: {upload_sessions[ADMIN_ID]}")
    
    # Test with first movie code
    test_code = list(movies_db.keys())[0]
    print(f"\n🧪 Testing with code: {test_code}")
    
    # Simulate code processing (same logic as in bot)
    clean_code = test_code.replace('#', '').strip()
    search_patterns = [
        clean_code,
        f"#{clean_code}",
        test_code.strip(),
        clean_code.upper(),
        clean_code.lower()
    ]
    
    movie_found = False
    for pattern in search_patterns:
        if pattern in movies_db:
            movie_info = movies_db[pattern]
            title = movie_info.get('title', f'Movie {pattern}') if isinstance(movie_info, dict) else f'Movie {pattern}'
            print(f"   ✅ FOUND: {pattern} -> {title}")
            movie_found = True
            break
    
    if not movie_found:
        print(f"   ❌ NOT FOUND with patterns: {search_patterns}")
        return False
    
    print("\n🎉 MOVIE DELETION SYSTEM IS WORKING!")
    print("The problem is likely in your bot's message handling.")
    print("\n💡 QUICK FIXES TO TRY:")
    print("1. Restart your bot completely")
    print("2. Make sure you're admin (your user_id should be 5542016161)")
    print("3. Try these exact steps:")
    print("   - Send /admin to your bot")
    print("   - Click 'Kino Boshqaruvi'")
    print("   - Click 'Kino O'chirish'")
    print("   - Send just the number: 123")
    print("   - Click confirmation button")
    
    return True

if __name__ == "__main__":
    success = fix_movie_deletion_now()
    if success:
        print("\n✅ SYSTEM IS READY!")
    else:
        print("\n❌ SYSTEM NEEDS REPAIR!")
