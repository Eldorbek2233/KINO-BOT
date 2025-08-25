import requests
import logging
import os
from time import sleep

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_bot_token():
    """Test if bot token is valid"""
    try:
        # Get token from environment or use fallback
        token = os.getenv('BOT_TOKEN', '8177519032:AAED4FgPoFQiQhqM_lvrK1iV8hL9u4SnkDk')
        
        # Test getMe method
        url = f"https://api.telegram.org/bot{token}/getMe"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if data['ok']:
                bot_info = data['result']
                logger.info(f"✅ Bot token is valid!")
                logger.info(f"Bot info: {bot_info['first_name']} (@{bot_info['username']})")
                return True
            else:
                logger.error(f"❌ Bot API error: {data.get('description')}")
                return False
        else:
            logger.error(f"❌ HTTP error {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Test error: {e}")
        return False

def delete_webhook():
    """Delete any existing webhook"""
    try:
        token = os.getenv('BOT_TOKEN', '8177519032:AAED4FgPoFQiQhqM_lvrK1iV8hL9u4SnkDk')
        url = f"https://api.telegram.org/bot{token}/deleteWebhook"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if data['ok']:
                logger.info("✅ Webhook deleted successfully")
                return True
            else:
                logger.error(f"❌ Delete webhook error: {data.get('description')}")
                return False
        else:
            logger.error(f"❌ HTTP error {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Delete webhook error: {e}")
        return False

if __name__ == "__main__":
    logger.info("🤖 Testing bot token...")
    
    if test_bot_token():
        logger.info("🎯 Now deleting webhook...")
        if delete_webhook():
            logger.info("✅ Bot is ready for polling mode!")
        else:
            logger.error("❌ Failed to delete webhook")
    else:
        logger.error("❌ Invalid bot token")
