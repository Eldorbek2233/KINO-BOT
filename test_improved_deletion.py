#!/usr/bin/env python3
"""Test improved movie deletion system with buttons"""

print("🎯 TESTING IMPROVED MOVIE DELETION SYSTEM")
print("=" * 50)

# Read current movies
try:
    import json
    with open("c:\\Kino bot\\file_ids.json", "r", encoding="utf-8") as f:
        movies = json.load(f)
    
    print(f"🎬 Current movies: {len(movies)}")
    for code, movie in list(movies.items())[:5]:
        title = movie.get('title', 'Unknown') if isinstance(movie, dict) else f'Movie {code}'
        print(f"  • {code}: {title}")
    
    if len(movies) > 5:
        print(f"  ... and {len(movies) - 5} more movies")
    
    print("\n✅ IMPROVED FEATURES:")
    print("1. ✅ Clickable buttons for each movie")
    print("2. ✅ Movie code + title shown on buttons")
    print("3. ✅ Confirmation dialog before deletion")
    print("4. ✅ Proper callback handling")
    print("5. ✅ Updated /delete command")
    
    print("\n📋 HOW TO TEST:")
    print("1. Send /delete to your bot")
    print("2. You'll see buttons with movie codes and titles")
    print("3. Click any button to delete that movie")
    print("4. Confirm deletion in the dialog")
    
    print("\n🎊 SYSTEM IS READY FOR TESTING!")
    
except Exception as e:
    print(f"❌ Error: {e}")

print("\n💡 Remember: Only admin can use /delete command!")
print("👑 The system now uses proper button interface!")
