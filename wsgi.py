#!/usr/bin/env python3
"""
Gunicorn WSGI entry point for Railway and Render deployment
"""

import os
import sys
import logging

# Add current directory to path for module imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import after path setup
from web_server import app
import simple_bot

# Log konfiguratsiyasi
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def create_app():
    """Application factory for Gunicorn"""
    logger.info("🚀 Creating application for Gunicorn...")
    
    # Telegram application yaratish
    telegram_app = simple_bot.create_minimal_app()
    
    # Web server ga telegram app o'rnatish
    import web_server
    web_server.set_telegram_app(telegram_app)
    
    # Platform-specific webhook URL
    webhook_url = None
    
    # Render platform
    render_url = os.getenv('RENDER_EXTERNAL_URL')
    if render_url:
        webhook_url = f"{render_url}/webhook"
    
    # Railway platform
    elif os.getenv('RAILWAY_PUBLIC_DOMAIN'):
        railway_url = os.getenv('RAILWAY_PUBLIC_DOMAIN')
        webhook_url = f"https://{railway_url}/webhook"
    
    # Default URLs
    elif os.getenv('RAILWAY_ENVIRONMENT'):
        webhook_url = "https://web-production-d5427.up.railway.app/webhook"
    elif os.getenv('PORT'):
        webhook_url = "https://kino-bot-latest.onrender.com/webhook"
    
    if not webhook_url:
        logger.error("❌ Could not determine webhook URL!")
        return app
    
    try:
        import requests
        response = requests.post(
            f"https://api.telegram.org/bot{simple_bot.TOKEN}/setWebhook",
            data={"url": webhook_url}
        )
        result = response.json()
        
        if result.get('ok'):
            logger.info(f"✅ Webhook set: {webhook_url}")
        else:
            logger.error(f"❌ Webhook error: {result}")
            
    except Exception as e:
        logger.error(f"Webhook setup error: {e}")
    
    logger.info("✅ Application ready for Gunicorn")
    return app

# Gunicorn uchun application obyekti
application = create_app()

if __name__ == "__main__":
    # Development mode uchun
    port = int(os.environ.get('PORT', 8080))
    application.run(host='0.0.0.0', port=port)
