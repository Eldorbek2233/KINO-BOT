#!/usr/bin/env python3
"""
Kino Bot - Minimal working version for Render deployment
"""

import os
import logging
from telegram.ext import Application
from config import TOKEN

# Log konfiguratsiyasi
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def create_minimal_app():
    """Minimal Telegram application yaratish"""
    try:
        logger.info("🔧 Minimal Telegram application yaratilmoqda...")
        
        # Connection pool optimizations for Render - minimal but efficient
        app = Application.builder().token(TOKEN)\
            .pool_timeout(60)\
            .connection_pool_size(8)\
            .read_timeout(30)\
            .write_timeout(30)\
            .connect_timeout(30)\
            .get_updates_pool_timeout(60)\
            .get_updates_read_timeout(30)\
            .get_updates_write_timeout(30)\
            .get_updates_connect_timeout(30)\
            .build()
        
        # Faqat mavjud bo'lgan handlerlarni qo'shish
        from handlers import add_handlers
        add_handlers(app)
        
        logger.info("✅ Minimal application tayyor")
        return app
        
    except Exception as e:
        logger.error(f"❌ Application yaratishda xatolik: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise

def main():
    """Main function"""
    logger.info("🚀 Kino Bot minimal version starting...")
    
    # Check if running on Render
    if os.getenv('PORT'):
        logger.info("🌐 Render environment detected, starting webhook server...")
        
        # Import and start web server
        import web_server
        
        port = int(os.environ.get('PORT', 8080))
        logger.info(f"🚀 Starting server on port {port}")
        
        # Create application
        telegram_app = create_minimal_app()
        
        # Set global telegram app in web_server
        web_server.set_telegram_app(telegram_app)
        
        # Set webhook
        render_url = "https://kino-bot-o8dw.onrender.com"
        webhook_url = f"{render_url}/webhook"
        
        try:
            import requests
            response = requests.post(
                f"https://api.telegram.org/bot{TOKEN}/setWebhook",
                data={"url": webhook_url}
            )
            result = response.json()
            
            if result.get('ok'):
                logger.info(f"✅ Webhook set: {webhook_url}")
            else:
                logger.error(f"❌ Webhook error: {result}")
                
        except Exception as e:
            logger.error(f"Webhook setup error: {e}")
        
        # Start Flask server
        logger.info(f"🌐 Starting Flask server on 0.0.0.0:{port}")
        web_server.app.run(
            host='0.0.0.0',
            port=port,
            debug=False,
            threaded=True
        )
    else:
        logger.info("💻 Local development mode")
        logger.info("Use: python web_server.py")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
