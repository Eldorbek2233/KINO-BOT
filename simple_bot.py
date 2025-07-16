#!/usr/bin/env python3
"""
Kino Bot - Minimal working version for Railway deployment
"""

import os
import logging
from telegram.ext import Application

# Platform specific config import
try:
    # Try Render config first
    if os.getenv('RENDER_EXTERNAL_URL'):
        from render_config import get_token, get_admin_id
        TOKEN = get_token()
        ADMIN_ID = get_admin_id()
        logger = logging.getLogger(__name__)
        logger.info("🎭 Using render_config for token management")
    # Then Railway config
    elif os.getenv('RAILWAY_ENVIRONMENT'):
        from railway_config import get_token, get_admin_id
        TOKEN = get_token()
        ADMIN_ID = get_admin_id()
        logger = logging.getLogger(__name__)
        logger.info("🚂 Using railway_config for token management")
    else:
        # Fallback to normal config
        from config import TOKEN, ADMIN_ID
        logger = logging.getLogger(__name__)
        logger.info("💻 Using normal config for local development")
except ImportError:
    # Final fallback to normal config
    from config import TOKEN, ADMIN_ID
    logger = logging.getLogger(__name__)
    logger.info("⚠️ Fallback to normal config")

# Log konfiguratsiyasi
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Debug: Check TOKEN value
TOKEN_FROM_ENV = os.getenv('BOT_TOKEN') or os.getenv('TOKEN')
logger.info(f"🔍 TOKEN from env - Length: {len(TOKEN_FROM_ENV) if TOKEN_FROM_ENV else 0}")
logger.info(f"🔍 TOKEN from env - First 10 chars: {TOKEN_FROM_ENV[:10] if TOKEN_FROM_ENV else 'None'}")
logger.info(f"🔍 Config TOKEN - Length: {len(TOKEN) if TOKEN else 0}")
logger.info(f"🔍 Config TOKEN - First 10 chars: {TOKEN[:10] if TOKEN else 'None'}")
logger.info(f"🔍 All env vars containing 'TOKEN': {[k for k in os.environ.keys() if 'TOKEN' in k.upper()]}")
logger.info(f"🔍 ADMIN_ID env var: {os.getenv('ADMIN_ID', 'NOT SET')}")

def create_minimal_app():
    """Minimal Telegram application yaratish"""
    try:
        logger.info("🔧 Minimal Telegram application yaratilmoqda...")
        
        # Token final validation
        logger.info(f"📋 Final TOKEN length: {len(TOKEN) if TOKEN else 0}")
        logger.info(f"📋 Final TOKEN preview: {TOKEN[:15] if TOKEN else 'None'}...")
        
        if not TOKEN or len(str(TOKEN)) < 30:
            raise ValueError(f"Invalid TOKEN: {TOKEN}")
        
        # Aggressive connection pool optimization for Railway's resource constraints
        app = Application.builder().token(TOKEN)\
            .pool_timeout(180)\
            .connection_pool_size(6)\
            .read_timeout(15)\
            .write_timeout(15)\
            .connect_timeout(10)\
            .get_updates_pool_timeout(180)\
            .get_updates_read_timeout(15)\
            .get_updates_write_timeout(15)\
            .get_updates_connect_timeout(10)\
            .build()
        
        # Faqat mavjud bo'lgan handlerlarni qo'shish
        from handlers import add_handlers
        add_handlers(app)
        
        # Application ni initialize qilish
        import asyncio
        
        async def init_application():
            await app.initialize()
            logger.info("✅ Application initialized")
        
        # Event loop yaratish va initialization
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(init_application())
            loop.close()
        except Exception as init_error:
            logger.error(f"❌ Initialize error: {init_error}")
            raise
        
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
    
    # Check if running on Railway or any cloud platform
    if os.getenv('PORT') or os.getenv('RAILWAY_ENVIRONMENT'):
        logger.info("🌐 Cloud environment detected, starting webhook server...")
        
        # Import and start web server
        import web_server
        
        port = int(os.environ.get('PORT', 8080))
        logger.info(f"🚀 Starting server on port {port}")
        
        # Create application
        telegram_app = create_minimal_app()
        
        # Set global telegram app in web_server
        web_server.set_telegram_app(telegram_app)
        
    # Get webhook URL based on platform
    webhook_url = None
    
    # Render platform
    render_url = os.getenv('RENDER_EXTERNAL_URL')
    if render_url:
        webhook_url = f"{render_url}/webhook"
        logger.info(f"🎭 Render webhook URL: {webhook_url}")
    
    # Railway platform  
    elif os.getenv('RAILWAY_PUBLIC_DOMAIN'):
        railway_url = os.getenv('RAILWAY_PUBLIC_DOMAIN')
        webhook_url = f"https://{railway_url}/webhook"
        logger.info(f"🚂 Railway webhook URL: {webhook_url}")
    
    # Default Railway URL (if domain not detected)
    elif os.getenv('RAILWAY_ENVIRONMENT'):
        webhook_url = "https://web-production-d5427.up.railway.app/webhook"
        logger.info(f"🚂 Default Railway webhook URL: {webhook_url}")
    
    # Default Render URL (if external URL not detected)
    elif os.getenv('PORT'):
        webhook_url = "https://kino-bot-latest.onrender.com/webhook"
        logger.info(f"🎭 Default Render webhook URL: {webhook_url}")
    
    if not webhook_url:
        logger.error("❌ Could not determine webhook URL!")
        return
    
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
