#!/usr/bin/env python3
"""MongoDB cleanup script for invalid channels"""

import os
import sys
import json
from datetime import datetime
from pymongo import MongoClient
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get MongoDB URI from environment
MONGODB_URI = os.getenv('MONGODB_URI')

def cleanup_mongodb_channels():
    """Clean up invalid channels from MongoDB"""
    try:
        if not MONGODB_URI:
            print("❌ No MongoDB URI found in environment")
            return False
            
        # Connect to MongoDB
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        db = client.get_default_database()
        
        # Test connection
        client.admin.command('ping')
        print("✅ Connected to MongoDB successfully")
        
        # Find all channels
        channels_collection = db.channels
        all_channels = list(channels_collection.find({}))
        
        print(f"📊 Found {len(all_channels)} channels in MongoDB:")
        
        for channel in all_channels:
            channel_id = channel.get('channel_id')
            name = channel.get('name', 'Unknown')
            active = channel.get('active', True)
            print(f"  - {channel_id}: {name} (active: {active})")
        
        # Mark all channels as inactive or delete them
        if all_channels:
            choice = input("\n🔧 Choose action:\n1) Mark all as inactive\n2) Delete all channels\n3) Cancel\nEnter choice (1/2/3): ")
            
            if choice == '1':
                # Mark all as inactive
                result = channels_collection.update_many({}, {'$set': {'active': False}})
                print(f"✅ Marked {result.modified_count} channels as inactive")
                
            elif choice == '2':
                # Delete all channels
                result = channels_collection.delete_many({})
                print(f"✅ Deleted {result.deleted_count} channels")
                
            elif choice == '3':
                print("❌ Operation cancelled")
                return False
            else:
                print("❌ Invalid choice")
                return False
        else:
            print("ℹ️ No channels found to clean")
            
        # Also clear local channels.json
        channels_json_path = 'channels.json'
        if os.path.exists(channels_json_path):
            with open(channels_json_path, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
            print("✅ Cleared local channels.json file")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ MongoDB cleanup error: {e}")
        return False

if __name__ == "__main__":
    print("🧹 MongoDB Channel Cleanup Tool")
    print("=" * 40)
    
    success = cleanup_mongodb_channels()
    
    if success:
        print("\n✅ Cleanup completed successfully!")
        print("💡 Restart the bot to apply changes")
    else:
        print("\n❌ Cleanup failed!")
    
    input("\nPress Enter to exit...")
