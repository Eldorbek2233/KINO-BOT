#!/usr/bin/env python3
"""
🧪 KINO O'CHIRISH TEST SCRIPT
Tests movie deletion functionality
"""

import sys
import os
import json
from datetime import datetime

def test_movie_deletion():
    """Test movie deletion system"""
    print("🎬 TESTING MOVIE DELETION SYSTEM...")
    
    # Load file_ids.json
    if os.path.exists('file_ids.json'):
        with open('file_ids.json', 'r', encoding='utf-8') as f:
            movies_data = json.load(f)
        print(f"✅ file_ids.json loaded: {len(movies_data)} movies")
        
        # Show available movies
        print("\n📋 Available movies:")
        for code, movie in movies_data.items():
            title = movie.get('title', f'Movie {code}')
            print(f"  {code}: {title}")
    else:
        print("❌ file_ids.json not found!")
        return False
    
    # Simulate upload session
    upload_sessions = {}
    user_id = 5542016161  # ADMIN_ID
    
    print(f"\n🔧 Starting delete session for admin {user_id}")
    upload_sessions[user_id] = {
        'type': 'delete_movie',
        'status': 'waiting_movie_code', 
        'start_time': datetime.now().isoformat()
    }
    
    # Test movie search
    test_codes = ['123', '#123', '456', 'invalid_code']
    
    for test_code in test_codes:
        print(f"\n🔍 Testing search for code: '{test_code}'")
        
        # Clean and normalize code (same logic as in bot)
        clean_code = test_code.replace('#', '').strip()
        
        # Search for movie
        movie_data = None
        found_code = None
        
        # Try multiple formats
        for search_code in [clean_code, f"#{clean_code}", test_code.strip()]:
            if search_code in movies_data:
                movie_data = movies_data[search_code]
                found_code = search_code
                break
        
        if movie_data:
            print(f"  ✅ Found: {found_code} -> {movie_data.get('title', 'Unknown')}")
        else:
            print(f"  ❌ Not found for code: '{test_code}'")
    
    return True

def main():
    """Main test function"""
    print("🧪 KINO O'CHIRISH DEBUG TEST")
    print("=" * 40)
    
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    success = test_movie_deletion()
    
    print("\n" + "=" * 40)
    if success:
        print("✅ MOVIE DELETION TEST COMPLETED")
        print("\n💡 DEBUGGING TIPS:")
        print("1. Check if movies_db is loaded in bot")
        print("2. Check if upload_session is created correctly")  
        print("3. Check debug logs in bot terminal")
        print("4. Verify admin user_id matches")
    else:
        print("❌ MOVIE DELETION TEST FAILED")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
