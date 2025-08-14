#!/usr/bin/env python3
"""
MongoDB Connection Test Script
Sizning MongoDB connection stringini test qilish uchun
"""

import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from datetime import datetime

def test_mongodb_connection():
    """Test MongoDB connection"""
    print("🧪 MONGODB CONNECTION TEST")
    print("=" * 50)
    
    # Production MongoDB URI
    test_uri = "mongodb+srv://eldorbekxakimxujayev4:7cszqUNVfQ6TPGz2@kinobot-cluster.quzswqg.mongodb.net/?retryWrites=true&w=majority&appName=kinobot-cluster"
    
    print(f"📝 Connection String: {test_uri[:50]}...")
    
    try:
        print("\n🔄 Connecting to MongoDB...")
        
        # Create client with basic settings
        client = MongoClient(
            test_uri,
            serverSelectionTimeoutMS=5000,
            connect=True
        )
        
        # Test connection
        client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        
        # Get database
        db = client['kinobot']
        print(f"📊 Database: {db.name}")
        
        # Test collections
        collections = db.list_collection_names()
        print(f"📋 Collections: {collections}")
        
        # Test write operation
        test_collection = db['test_connection']
        test_doc = {
            'test': True,
            'timestamp': datetime.now(),
            'message': 'MongoDB connection test successful!'
        }
        
        result = test_collection.insert_one(test_doc)
        print(f"✅ Test document inserted: {result.inserted_id}")
        
        # Clean up test document
        test_collection.delete_one({'_id': result.inserted_id})
        print("🧹 Test document cleaned up")
        
        print("\n🎉 MONGODB CONNECTION TEST PASSED!")
        print("✅ MongoDB Atlas ready for use!")
        
        client.close()
        return True
        
    except ConnectionFailure as e:
        print(f"❌ Connection failed: {e}")
        print("💡 Check your connection string and network")
        return False
        
    except ServerSelectionTimeoutError as e:
        print(f"❌ Server timeout: {e}")
        print("💡 Check if IP is whitelisted in MongoDB Atlas")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Check your credentials and permissions")
        return False

def check_environment_setup():
    """Check if environment is properly configured"""
    print("\n🔧 ENVIRONMENT CHECK")
    print("=" * 30)
    
    required_vars = ['BOT_TOKEN', 'ADMIN_ID', 'MONGODB_URI', 'DB_NAME']
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            display_value = value[:20] + "..." if len(value) > 20 else value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: Not set")
    
    print("\n💡 Agar environment variables bo'sh bo'lsa:")
    print("   1. Render.com dashboard ga kiring")
    print("   2. Environment tab ni oching") 
    print("   3. Variables qo'shing")
    print("   4. Manual deploy qiling")

if __name__ == "__main__":
    print("🎭 KINO BOT - MONGODB SETUP TEST")
    print("🔧 Version: Professional with Enhanced Features")
    print("")
    
    # Check environment
    check_environment_setup()
    
    # Test MongoDB connection
    success = test_mongodb_connection()
    
    print("\n" + "=" * 50)
    if success:
        print("🚀 READY FOR DEPLOYMENT!")
        print("📋 Next steps:")
        print("   1. Set environment variables in Render.com")
        print("   2. Replace YOUR_PASSWORD with real password")
        print("   3. Deploy to Render.com")
        print("   4. Test bot with /admin command")
    else:
        print("⚠️ FIX REQUIRED!")
        print("📋 Fix these issues:")
        print("   1. Check MongoDB password")
        print("   2. Verify IP whitelist (0.0.0.0/0)")
        print("   3. Confirm user permissions")
        print("   4. Test connection again")
    
    print("\n🎯 Enhanced Features Available:")
    print("   ✅ Movie upload with title input")
    print("   ✅ MongoDB professional storage")
    print("   ✅ JSON backup system")
    print("   ✅ Complete admin panel")
    print("   ✅ Channel management")
    print("   ✅ Broadcasting system")
