import certifi
from pymongo import MongoClient
import time
import logging
import sys

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def test_connection():
    try:
        logger.info("🔄 MongoDB ulanish testi boshlandi...")
        
        # Connection string
        uri = "mongodb+srv://eldorbekxakimxujayev4:Ali11042004@kinobot-cluster.quzswqg.mongodb.net/?retryWrites=true&w=majority&appName=kinobot-cluster"
        
        logger.info(f"URI: {uri}")
        
        # Create client with SSL certificate
        client = MongoClient(
            uri, 
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=20000,
            socketTimeoutMS=20000
        )
        
        # Force connection test
        logger.info("Serverga ulanish...")
        
        # First test connection with ping
        client.admin.command('ping')
        logger.info("✅ Ping muvaffaqiyatli!")
        
        # Get server info
        db = client.kinobot
        server_info = client.server_info()
        logger.info(f"✅ Server ulanishi muvaffaqiyatli! Server versiyasi: {server_info.get('version')}")
        
        # Test write operation
        logger.info("\nTest yozuv yaratish...")
        test_doc = {
            "test": True,
            "timestamp": time.time(),
            "message": "Test connection"
        }
        result = db.test_collection.insert_one(test_doc)
        logger.info(f"✅ Test yozuv yaratildi: {result.inserted_id}")
        
        # Test read operation
        logger.info("\nTest yozuvni o'qish...")
        found = db.test_collection.find_one({"_id": result.inserted_id})
        if found:
            logger.info("✅ Test yozuv o'qildi")
            
        # Clean up
        logger.info("\nTest yozuvni o'chirish...")
        db.test_collection.delete_one({"_id": result.inserted_id})
        logger.info("✅ Test yozuv o'chirildi")
        
        # List collections
        logger.info("\nMavjud kolleksiyalar:")
        collections = db.list_collection_names()
        for collection in collections:
            logger.info(f"📁 {collection}")
        
        client.close()
        logger.info("\n✅ BARCHA TESTLAR MUVAFFAQIYATLI!")
        return True
    
    except Exception as e:
        logger.error(f"\n❌ XATOLIK: {str(e)}")
        logger.error("Stack trace:", exc_info=True)
        return False

if __name__ == "__main__":
    test_connection()
