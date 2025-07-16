#!/usr/bin/env python3
"""
Kino Bot - Local Development Version
VS Code da local ishlatish uchun - python bot.py
"""

import logging
import asyncio
import signal
import sys
import platform
from telegram.ext import Application
from config import TOKEN, ADMIN_ID
from handlers import add_handlers

# Logging sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Windows event loop muammosini hal qilish
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

def signal_handler(signum, frame):
    """Signal handler for graceful shutdown"""
    logger.info("🛑 Signal qabul qilindi, bot to'xtatilmoqda...")
    sys.exit(0)

async def main():
    """Bot ni local development uchun ishga tushirish"""
    app = None
    try:
        logger.info("🚀 Kino Bot ishga tushirilmoqda (Local Development)...")
        
        # Token tekshirish
        if not TOKEN or len(TOKEN) < 30:
            logger.error("❌ TOKEN noto'g'ri yoki mavjud emas!")
            return
            
        logger.info(f"✅ TOKEN: {TOKEN[:15]}...")
        logger.info(f"👤 ADMIN_ID: {ADMIN_ID}")
        
        # Application yaratish
        app = Application.builder().token(TOKEN)\
            .read_timeout(30)\
            .write_timeout(30)\
            .connect_timeout(30)\
            .pool_timeout(30)\
            .connection_pool_size(8)\
            .build()
        
        # Handlerlarni qo'shish
        add_handlers(app)
        logger.info("✅ Handlers qo'shildi")
        
        # Application ni initialize qilish
        await app.initialize()
        logger.info("✅ Application initialized")
        
        # Bot ma'lumotlarini olish
        bot_info = await app.bot.get_me()
        logger.info(f"🤖 Bot: @{bot_info.username} ({bot_info.first_name})")
        
        # Polling boshqaruvchi
        updater = app.updater
        
        logger.info("🔄 Polling rejimida ishga tushirilmoqda...")
        logger.info("💻 Bot tayyor! Telegram da @uzmovi_film_bot ga /start yuboring")
        logger.info("⏹️  Bot to'xtatish uchun Ctrl+C bosing")
        
        # Start polling
        await updater.start_polling(
            poll_interval=1.0,
            timeout=20,
            bootstrap_retries=5,
            drop_pending_updates=True
        )
        
        # Keep running until interrupted
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("🛑 Bot foydalanuvchi tomonidan to'xtatildi")
    except Exception as e:
        logger.error(f"❌ Bot xatoligi: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        if app:
            try:
                logger.info("🧹 Bot resources tozalanmoqda...")
                if app.updater and app.updater.running:
                    await app.updater.stop()
                await app.shutdown()
                logger.info("✅ Bot to'xtatildi")
            except Exception as cleanup_error:
                logger.error(f"❌ Cleanup error: {cleanup_error}")

def run_bot():
    """Event loop ni to'g'ri boshqarish"""
    try:
        # Signal handlers o'rnatish
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Event loop yaratish va ishga tushirish
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(main())
        finally:
            # Pending tasks ni tozalash
            pending = asyncio.all_tasks(loop)
            if pending:
                logger.info(f"🧹 {len(pending)} pending task tozalanmoqda...")
                for task in pending:
                    task.cancel()
                loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
            
            loop.close()
            logger.info("✅ Event loop yopildi")
            
    except KeyboardInterrupt:
        logger.info("👋 Xayr! Bot to'xtatildi.")
    except Exception as e:
        logger.error(f"❌ Event loop error: {e}")

if __name__ == "__main__":
    print("🤖 Kino Bot - Local Development")
    print("=" * 40)
    print("🔧 Ishlatish: python bot.py")
    print("📝 Bot @uzmovi_film_bot")
    print("⏹️  To'xtatish: Ctrl+C")
    print("=" * 40)
    
    run_bot()
