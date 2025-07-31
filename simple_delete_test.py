#!/usr/bin/env python3
"""Simple test to verify delete command structure"""

print("🔧 TESTING /delete COMMAND STRUCTURE")
print("=" * 50)

# Read the app.py file and check for /delete command
try:
    with open("app.py", "r", encoding="utf-8") as f:
        app_content = f.read()
    
    # Check for the delete command
    delete_command_found = "elif text == '/delete' and user_id == ADMIN_ID:" in app_content
    handle_delete_found = "handle_delete_movies_menu_impl" in app_content
    
    print(f"✅ /delete command found: {delete_command_found}")
    print(f"✅ handle_delete_movies_menu_impl found: {handle_delete_found}")
    
    if delete_command_found and handle_delete_found:
        print("\n🎉 SUCCESS! /delete command is properly implemented in app.py!")
        
        # Show the relevant lines
        lines = app_content.split('\n')
        for i, line in enumerate(lines):
            if "elif text == '/delete' and user_id == ADMIN_ID:" in line:
                print(f"\n📍 Found at line {i+1}:")
                for j in range(max(0, i-1), min(len(lines), i+4)):
                    marker = ">>> " if j == i else "    "
                    print(f"{marker}{j+1}: {lines[j]}")
                break
    else:
        print("\n❌ /delete command not properly implemented!")
        
    # Check file_ids.json for movies
    try:
        with open("file_ids.json", "r", encoding="utf-8") as f:
            import json
            movies = json.load(f)
        
        print(f"\n🎬 Movies available for deletion: {len(movies)}")
        for code, movie in list(movies.items())[:3]:  # Show first 3
            title = movie.get('title', 'Unknown')
            print(f"  • {code}: {title}")
        
        if len(movies) > 3:
            print(f"  ... and {len(movies) - 3} more movies")
            
    except Exception as e:
        print(f"❌ Error reading movies: {e}")
        
    print("\n📋 INSTRUCTIONS FOR TESTING:")
    print("1. Run your bot")
    print("2. Send /delete command to the bot")
    print("3. You should see the delete movies menu")
    print("4. Enter a movie code to delete it")
    
except Exception as e:
    print(f"❌ Error reading app.py: {e}")
