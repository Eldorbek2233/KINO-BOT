#!/usr/bin/env python3
"""
Simple Test Bot - Faqat /start va /test command lar
"""

import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import TOKEN, ADMIN_ID

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler"""
    try:
        user_id = update.effective_user.id
        logger.info(f"🔥 Start command from user: {user_id}")
        
        if user_id == ADMIN_ID:
            text = "👑 Salom Admin! Bot ishlayapti.\n\n"
            text += "🔧 /test - Test command"
        else:
            text = "🎬 Salom! Kino Bot ga xush kelibsiz!\n\n"
            text += "🔧 /test - Test command"
        
        await update.message.reply_text(text)
        logger.info(f"✅ Start response sent to user: {user_id}")
        
    except Exception as e:
        logger.error(f"❌ Start command error: {e}")
        await update.message.reply_text("❌ Xatolik yuz berdi!")

async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test command handler"""
    try:
        user_id = update.effective_user.id
        logger.info(f"🔥 Test command from user: {user_id}")
        
        await update.message.reply_text("✅ Bot test muvaffaqiyatli! Hammasi ishlayapti.")
        logger.info(f"✅ Test response sent to user: {user_id}")
        
    except Exception as e:
        logger.error(f"❌ Test command error: {e}")
        await update.message.reply_text("❌ Test xatoligi!")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Error handler"""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Bot ni ishga tushirish"""
    try:
        print("🤖 Simple Test Bot")
        print("=" * 30)
        print(f"TOKEN: {TOKEN[:15]}...")
        print(f"ADMIN: {ADMIN_ID}")
        print("=" * 30)
        
        # Application yaratish
        app = Application.builder().token(TOKEN).build()
        
        # Handlerlar qo'shish
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("test", test_command))
        app.add_error_handler(error_handler)
        
        print("✅ Handlers qo'shildi")
        print("🚀 Bot ishga tushmoqda...")
        print("💬 @uzmovi_film_bot ga /start yuboring")
        print("⏹️  To'xtatish: Ctrl+C")
        print("=" * 30)
        
        # Polling boshqarish
        app.run_polling(
            poll_interval=1.0,
            timeout=20,
            drop_pending_updates=True
        )
        
    except KeyboardInterrupt:
        print("\n👋 Bot to'xtatildi!")
    except Exception as e:
        print(f"❌ Bot error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
