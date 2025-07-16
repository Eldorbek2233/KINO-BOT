#!/usr/bin/env python3
"""
Kino Bot - Local Development Version
VS Code da local ishlatish uchun - python bot.py
"""

import logging
import asyncio
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from config import TOKEN, ADMIN_ID

# Logging sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def save_user(user_id):
    """Foydalanuvchini users.json ga saqlash"""
    try:
        import json
        import os
        from datetime import datetime
        
        file_path = "users.json"
        
        # Fayl mavjud bo'lsa, ma'lumotlarni o'qish
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
        else:
            data = {"users": [], "total_users": 0, "last_updated": ""}
        
        # Foydalanuvchi ro'yxatda yo'qligini tekshirish
        if user_id not in data["users"]:
            data["users"].append(user_id)
            data["total_users"] = len(data["users"])
            data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Faylga yozish
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)
            
            logger.info(f"👤 New user saved: {user_id}")
        
    except Exception as e:
        logger.error(f"❌ Save user error: {e}")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler"""
    try:
        user_id = update.effective_user.id
        logger.info(f"🔥 Start command from user: {user_id}")
        
        # Foydalanuvchini saqlash
        save_user(user_id)
        
        if user_id == ADMIN_ID:
            text = "👑 Salom Admin! Kino Bot ishlayapti.\n\n"
            text += "🎬 Kino kodi yuboring\n"
            text += "🔧 /test - Test command\n"
            text += "👑 /admin - Admin panel\n"
            text += "📊 /stats - Statistika"
        else:
            text = "🎬 Salom! Kino Bot ga xush kelibsiz!\n\n"
            text += "📽️ Kino kodi yuboring\n"
            text += "🔧 /test - Test command"
        
        await update.message.reply_text(text)
        logger.info(f"✅ Start response sent to user: {user_id}")
        
    except Exception as e:
        logger.error(f"❌ Start command error: {e}")
        try:
            await update.message.reply_text("❌ Xatolik yuz berdi!")
        except:
            pass

async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test command handler"""
    try:
        user_id = update.effective_user.id
        logger.info(f"🔥 Test command from user: {user_id}")
        
        await update.message.reply_text("✅ Bot test muvaffaqiyatli! Hammasi ishlayapti. 🚀")
        logger.info(f"✅ Test response sent to user: {user_id}")
        
    except Exception as e:
        logger.error(f"❌ Test command error: {e}")

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin panel command"""
    try:
        user_id = update.effective_user.id
        logger.info(f"🔥 Admin command from user: {user_id}")
        
        if user_id != ADMIN_ID:
            await update.message.reply_text("❌ Siz admin emassiz!")
            return
        
        keyboard = [
            ["📊 Statistika", "👥 Foydalanuvchilar"],
            ["📣 Reklama", "🎬 Kino joylash"],
            ["🔙 Orqaga"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(
            "👑 Admin Panel\n\nKerakli bo'limni tanlang:",
            reply_markup=reply_markup
        )
        logger.info(f"✅ Admin panel sent to user: {user_id}")
        
    except Exception as e:
        logger.error(f"❌ Admin command error: {e}")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Statistics command"""
    try:
        user_id = update.effective_user.id
        logger.info(f"🔥 Stats command from user: {user_id}")
        
        if user_id != ADMIN_ID:
            await update.message.reply_text("❌ Siz admin emassiz!")
            return
        
        # Simple stats
        import os
        
        # File stats
        movies_dir = "movies"
        movie_count = 0
        if os.path.exists(movies_dir):
            movie_count = len([f for f in os.listdir(movies_dir) if f.endswith(('.mp4', '.mkv', '.avi'))])
        
        # Users stats (from users.json)
        users_count = 0
        try:
            import json
            if os.path.exists("users.json"):
                with open("users.json", "r") as f:
                    users_data = json.load(f)
                    users_count = len(users_data.get("users", []))
        except:
            pass
        
        stats_text = f"""📊 Bot Statistikasi
        
👥 Foydalanuvchilar: {users_count}
🎬 Kinolar: {movie_count}
⏰ Status: ✅ Ishlayapti
💻 Version: Local Development"""
        
        await update.message.reply_text(stats_text)
        logger.info(f"✅ Stats sent to user: {user_id}")
        
    except Exception as e:
        logger.error(f"❌ Stats command error: {e}")

async def handle_admin_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle admin keyboard buttons"""
    try:
        text = update.message.text
        user_id = update.effective_user.id
        
        if user_id != ADMIN_ID:
            return
        
        logger.info(f"🔥 Admin button: {text} from user: {user_id}")
        
        if text == "📊 Statistika":
            await stats_command(update, context)
            
        elif text == "👥 Foydalanuvchilar":
            # Simple user list
            try:
                import json
                import os
                
                users_text = "👥 Foydalanuvchilar ro'yxati:\n\n"
                
                if os.path.exists("users.json"):
                    with open("users.json", "r") as f:
                        users_data = json.load(f)
                        users = users_data.get("users", [])
                        
                    if users:
                        for i, uid in enumerate(users[:10], 1):  # First 10 users
                            users_text += f"{i}. User ID: {uid}\n"
                        
                        if len(users) > 10:
                            users_text += f"... va yana {len(users) - 10} foydalanuvchi"
                    else:
                        users_text += "Hech qanday foydalanuvchi topilmadi."
                else:
                    users_text += "Foydalanuvchilar fayli topilmadi."
                
                await update.message.reply_text(users_text)
                
            except Exception as e:
                await update.message.reply_text(f"❌ Foydalanuvchilar ro'yxatini olishda xatolik: {e}")
                
        elif text == "📣 Reklama":
            await update.message.reply_text(
                "📣 Reklama funksiyasi\n\n"
                "Bu yerda barcha foydalanuvchilarga reklama yuborish mumkin.\n"
                "Hozircha development rejimida."
            )
            
        elif text == "🎬 Kino joylash":
            await update.message.reply_text(
                "🎬 Kino joylash funksiyasi\n\n"
                "Bu yerda yangi kinolar qo'shish mumkin.\n"
                "Hozircha development rejimida."
            )
            
        elif text == "🔙 Orqaga":
            await update.message.reply_text(
                "🔙 Asosiy menyuga qaytdingiz.",
                reply_markup=ReplyKeyboardRemove()
            )
            # Send start message again
            await start_command(update, context)
        
    except Exception as e:
        logger.error(f"❌ Admin button handler error: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages (movie codes)"""
    try:
        text = update.message.text
        user_id = update.effective_user.id
        logger.info(f"📝 Message from {user_id}: {text}")
        
        # Simple echo for now
        await update.message.reply_text(f"📨 Sizning xabaringiz: {text}\n\n🔍 Kino qidirilmoqda...")
        
    except Exception as e:
        logger.error(f"❌ Message handler error: {e}")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Error handler"""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Bot ni ishga tushirish"""
    try:
        print("🤖 Kino Bot - Local Development")
        print("=" * 40)
        print(f"🔑 TOKEN: {TOKEN[:15]}...")
        print(f"👤 ADMIN: {ADMIN_ID}")
        print("📝 Bot: @uzmovi_film_bot")
        print("=" * 40)
        
        # Application yaratish
        app = Application.builder().token(TOKEN).build()
        
        # Handlerlar qo'shish
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("test", test_command))
        app.add_handler(CommandHandler("admin", admin_command))
        app.add_handler(CommandHandler("stats", stats_command))
        
        # Admin keyboard buttons handler (admin faqat)
        app.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND & filters.User(user_id=ADMIN_ID), 
            handle_admin_buttons
        ))
        
        # Regular message handler (non-admin users)
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        app.add_error_handler(error_handler)
        
        print("✅ Handlers qo'shildi")
        print("🚀 Bot ishga tushmoqda...")
        print("💬 Telegram da @uzmovi_film_bot ga /start yuboring")
        print("⏹️  To'xtatish: Ctrl+C")
        print("=" * 40)
        
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
