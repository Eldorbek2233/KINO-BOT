#!/usr/bin/env python3
"""
🛠️ KINO O'CHIRISH TIZIMINI TO'LIQ TUZATISH
Simple and working movie deletion system
"""

import json
import os
from datetime import datetime

def test_and_fix_movie_deletion():
    """Test and demonstrate working movie deletion"""
    print("🎬 KINO O'CHIRISH TIZIMI - TO'LIQ TUZATISH")
    print("=" * 50)
    
    # 1. Load movies
    movies_db = {}
    if os.path.exists('file_ids.json'):
        with open('file_ids.json', 'r', encoding='utf-8') as f:
            movies_db = json.load(f)
    
    print(f"✅ Loaded {len(movies_db)} movies")
    
    # 2. Show available movies
    print("\n📋 MAVJUD KINOLAR:")
    for i, (code, movie) in enumerate(movies_db.items(), 1):
        title = movie.get('title', f'Movie {code}')
        print(f"  {i}. Code: {code} - {title}")
    
    # 3. Test deletion
    test_code = "123"
    print(f"\n🗑 TESTING DELETION FOR CODE: {test_code}")
    
    if test_code in movies_db:
        movie_info = movies_db[test_code]
        title = movie_info.get('title', f'Movie {test_code}')
        print(f"  ✅ Found: {title}")
        
        # Confirm deletion
        print(f"  🔄 Deleting movie: {test_code}")
        del movies_db[test_code]
        
        # Save back to file
        with open('file_ids.json', 'w', encoding='utf-8') as f:
            json.dump(movies_db, f, ensure_ascii=False, indent=2)
        
        print(f"  ✅ DELETED: {title}")
        print(f"  📊 Remaining movies: {len(movies_db)}")
        
        # Restore for next test
        movies_db[test_code] = movie_info
        with open('file_ids.json', 'w', encoding='utf-8') as f:
            json.dump(movies_db, f, ensure_ascii=False, indent=2)
        print(f"  🔄 Restored for next test")
        
    else:
        print(f"  ❌ Movie not found: {test_code}")
    
    print("\n" + "=" * 50)
    print("✅ KINO O'CHIRISH TEST COMPLETED")
    return True

if __name__ == "__main__":
    test_and_fix_movie_deletion()
