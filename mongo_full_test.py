from pymongo import MongoClient
import certifi
import time

def test_connection():
    # Connection string
    uri = "mongodb+srv://kino_bot_user:KinoBot2025Pass@kinobot-cluster.quzswqg.mongodb.net/kinobot?retryWrites=true&w=majority"
    
    try:
        print("MongoDB ulanish testi boshlandi...")
        
        # Create client
        client = MongoClient(uri, tlsCAFile=certifi.where())
        
        # Test connection
        print("Serverga ulanish...")
        client.admin.command('ping')
        print("✅ Server ulanishi muvaffaqiyatli!")
        
        # Get database
        db = client.kinobot
        print(f"✅ Bazaga ulandi: {db.name}")
        
        # Test write
        test_doc = {"test": True, "timestamp": time.time()}
        result = db.test_collection.insert_one(test_doc)
        print(f"✅ Test yozuv yaratildi: {result.inserted_id}")
        
        # Test read
        found = db.test_collection.find_one({"_id": result.inserted_id})
        if found:
            print("✅ Test yozuv o'qildi")
            
        # Clean up
        db.test_collection.delete_one({"_id": result.inserted_id})
        print("✅ Test yozuv o'chirildi")
        
        print("\n✅ BARCHA TESTLAR MUVAFFAQIYATLI!")
        client.close()
        return True
        
    except Exception as e:
        print(f"\n❌ XATOLIK: {str(e)}")
        return False

if __name__ == "__main__":
    test_connection()
