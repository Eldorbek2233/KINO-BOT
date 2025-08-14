import os
from pymongo import MongoClient
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def test_mongodb():
    try:
        # Get MongoDB URI from environment
        uri = os.getenv('MONGODB_URI')
        if not uri:
            logger.error("❌ MONGODB_URI environment variable not set")
            return False
            
        logger.info(f"🔄 Connecting to MongoDB: {uri[:50]}...")
        
        # Create client with high timeout
        client = MongoClient(uri, 
                           serverSelectionTimeoutMS=30000,
                           connectTimeoutMS=30000,
                           socketTimeoutMS=30000)
        
        # Test connection
        logger.info("🔍 Testing connection...")
        client.admin.command('ping')
        logger.info("✅ Connection successful!")
        
        # Get database
        db = client['kinobot']
        logger.info(f"📊 Using database: {db.name}")
        
        # List collections
        collections = db.list_collection_names()
        logger.info(f"📋 Available collections: {collections}")
        
        # Test write operation
        test_collection = db['connection_test']
        test_doc = {
            'test': True,
            'timestamp': datetime.now(),
            'message': 'Connection test successful'
        }
        
        result = test_collection.insert_one(test_doc)
        logger.info(f"✅ Test document inserted: {result.inserted_id}")
        
        # Clean up
        test_collection.delete_one({'_id': result.inserted_id})
        logger.info("🧹 Test document cleaned up")
        
        client.close()
        logger.info("✅ ALL TESTS PASSED!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Starting MongoDB Connection Test")
    success = test_mongodb()
    if success:
        logger.info("✅ MongoDB is ready to use!")
    else:
        logger.error("❌ MongoDB connection failed!")
