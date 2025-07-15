#!/usr/bin/env python3
"""
Kino Bot - Local Development Version
VS Code da local ishlatish uchun - python bot.py
"""

import logging
import asyncio
from telegram.ext import Application
from config import TOKEN, ADMIN_ID
from handlers import add_handlers

# Logging sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

async def main():
    """Bot ni local development uchun ishga tushirish"""
    try:
        logger.info("🚀 Kino Bot ishga tushirilmoqda (Local Development)...")
        
        # Token tekshirish
        if not TOKEN or len(TOKEN) < 30:
            logger.error("❌ TOKEN noto'g'ri yoki mavjud emas!")
            return
            
        logger.info(f"✅ TOKEN: {TOKEN[:15]}...")
        logger.info(f"👤 ADMIN_ID: {ADMIN_ID}")
        
        # Application yaratish
        app = Application.builder().token(TOKEN).build()
        
        # Handlerlarni qo'shish
        add_handlers(app)
        logger.info("✅ Handlers qo'shildi")
        
        # Polling rejimida ishga tushirish
        logger.info("🔄 Polling rejimida ishga tushirilmoqda...")
        logger.info("💻 Bot tayyor! Telegram da @uzmovi_film_bot ga /start yuboring")
        logger.info("⏹️  Bot to'xtatish uchun Ctrl+C bosing")
        
        await app.run_polling(
            poll_interval=1.0,  # 1 soniyada bir marta tekshirish
            timeout=20,         # 20 soniya timeout
            bootstrap_retries=5,
            drop_pending_updates=True  # Eski updatelarni o'chirish
        )
        
    except KeyboardInterrupt:
        logger.info("🛑 Bot foydalanuvchi tomonidan to'xtatildi")
    except Exception as e:
        logger.error(f"❌ Bot xatoligi: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🤖 Kino Bot - Local Development")
    print("=" * 40)
    print("� Ishlatish: python bot.py")
    print("📝 Bot @uzmovi_film_bot")
    print("⏹️  To'xtatish: Ctrl+C")
    print("=" * 40)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Xayr! Bot to'xtatildi.")
