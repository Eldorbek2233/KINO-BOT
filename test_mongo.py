from pymongo import MongoClient
import os
from datetime import datetime

def test_mongo_connection():
    try:
        # MongoDB connection string
        uri = "mongodb+srv://kinobot_user:KinoBotPass123@kinobot-cluster.quzswqg.mongodb.net/kinobot?retryWrites=true&w=majority"
        
        # Create client
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        
        # Test connection
        client.admin.command('ping')
        print("✅ MongoDB ulanish muvaffaqiyatli!")
        
        # Test database operations
        db = client['kinobot']
        test_collection = db['test']
        
        # Insert test document
        test_doc = {
            'test': True,
            'timestamp': datetime.now(),
            'message': 'Test successful'
        }
        result = test_collection.insert_one(test_doc)
        print(f"✅ Test hujjat qo'shildi: {result.inserted_id}")
        
        # Clean up
        test_collection.delete_one({'_id': result.inserted_id})
        print("✅ Test hujjat o'chirildi")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ MongoDB xato: {e}")
        return False

if __name__ == "__main__":
    print("🔄 MongoDB ulanishini tekshirish...")
    test_mongo_connection()
