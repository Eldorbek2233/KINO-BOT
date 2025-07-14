#!/usr/bin/env python3
"""
Gunicorn WSGI entry point for Railway production deployment
"""

import os
import logging
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
    
    # Webhook o'rnatish
    railway_url = os.getenv('RAILWAY_PUBLIC_DOMAIN')
    if railway_url:
        webhook_url = f"https://{railway_url}/webhook"
    else:
        webhook_url = "https://web-production-d5427.up.railway.app/webhook"
    
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
