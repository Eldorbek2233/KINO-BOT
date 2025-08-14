import certifi
from pymongo import MongoClient
from datetime import datetime

def test_mongo():
    try:
        # Connection string
        uri = "mongodb+srv://kinobot_user:KinoBotPass123@kinobot-cluster.quzswqg.mongodb.net/kinobot?retryWrites=true&w=majority"
        
        # Create client with SSL certificate
        client = MongoClient(uri, tlsCAFile=certifi.where())
        
        # Test connection
        print("MongoDB ga ulanish...")
        client.admin.command('ping')
        print("✅ Ulanish muvaffaqiyatli!")
        
        # Test database
        db = client['kinobot']
        print(f"Database: {db.name}")
        
        # Test write
        result = db.test.insert_one({"test": True, "date": datetime.now()})
        print(f"Test yozuv yaratildi: {result.inserted_id}")
        
        # Clean up
        db.test.delete_one({"_id": result.inserted_id})
        print("Test yozuv o'chirildi")
        
        return True
    except Exception as e:
        print(f"Xatolik: {str(e)}")
        return False

if __name__ == "__main__":
    print("MongoDB Test boshlandi...")
    success = test_mongo()
    if success:
        print("✅ Hammasi ishladi!")
    else:
        print("❌ Xatolik yuz berdi!")
