#!/usr/bin/env python3
"""
Bot for Railway production deployment
Railway da webhook mode uchun - wsgi.py ishlatiladi
"""

from telegram.ext import Application
from railway_config import get_token, get_admin_id
from handlers import add_handlers
import logging

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def create_production_app():
    """Railway production uchun bot yaratish"""
    try:
        TOKEN = get_token()
        ADMIN_ID = get_admin_id()
        
        logger.info("🚀 Production Bot ishga tushirilmoqda...")
        logger.info(f"✅ TOKEN: {TOKEN[:15]}...")
        logger.info(f"👤 ADMIN_ID: {ADMIN_ID}")
        
        # Application yaratish
        app = Application.builder().token(TOKEN)\
            .pool_timeout(180)\
            .connection_pool_size(6)\
            .read_timeout(15)\
            .write_timeout(15)\
            .connect_timeout(10)\
            .build()
        
        # Handlerlarni qo'shish
        add_handlers(app)
        logger.info("✅ Production handlers qo'shildi")
        
        return app
        
    except Exception as e:
        logger.error(f"❌ Production bot yaratishda xatolik: {e}")
        raise

if __name__ == "__main__":
    print("⚠️  Bu fayl Railway production uchun!")
    print("💻 Local development uchun: python bot.py")
    print("🚀 Railway production: gunicorn wsgi:application")
