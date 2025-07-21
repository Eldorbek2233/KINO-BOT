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
            # Reklama yuborish rejimini boshlash
            waiting_for_ad_content[user_id] = True
            await update.message.reply_text(
                "📣 Reklama yuborish\n\n"
                "Barcha foydalanuvchilarga yubormoqchi bo'lgan xabaringizni yuboring.\n"
                "Matn yoki rasm yuborishingiz mumkin.\n\n"
                "❌ Bekor qilish uchun /cancel yuboring."
            )
            
        elif text == "🎬 Kino joylash":
            # Kino joylash rejimini boshlash
            waiting_for_movie_code[user_id] = True
            await update.message.reply_text(
                "🎬 Kino joylash\n\n"
                "Birinchi kino kodini yuboring (masalan: 123, abc, film1):\n\n"
                "❌ Bekor qilish uchun /cancel yuboring."
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

async def handle_combined_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all text messages (admin buttons, movie codes, admin inputs)"""
    try:
        text = update.message.text
        user_id = update.effective_user.id
        logger.info(f"📝 Message from {user_id}: {text}")
        
        # Check if this is an admin button
        if user_id == ADMIN_ID:
            admin_buttons = ["📊 Statistika", "👥 Foydalanuvchilar", "📣 Reklama", "🎬 Kino joylash", "🔙 Orqaga"]
            
            if text in admin_buttons:
                await handle_admin_buttons(update, context)
                return
        
        # Handle regular messages and admin inputs
        await handle_message(update, context)
        
    except Exception as e:
        logger.error(f"❌ Message handling error: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages (movie codes, admin inputs)"""
    try:
        text = update.message.text
        user_id = update.effective_user.id
        logger.info(f"📝 Message from {user_id}: {text}")
        
        # Admin functions
        if user_id == ADMIN_ID:
            # Reklama yuborish rejimi
            if user_id in waiting_for_ad_content:
                waiting_for_ad_content.pop(user_id)
                
                await update.message.reply_text("⏳ Reklama yuborilmoqda...")
                
                # Reklama yuborish
                success_count, result_msg = await send_broadcast(context, text)
                
                await update.message.reply_text(
                    f"✅ Reklama yuborish tugadi!\n\n{result_msg}",
                    reply_markup=ReplyKeyboardRemove()
                )
                
                # Admin panel qaytarish
                await admin_command(update, context)
                return
            
            # Kino kodi kutish rejimi
            elif user_id in waiting_for_movie_code:
                waiting_for_movie_code.pop(user_id)
                waiting_for_movie_file[user_id] = text  # Kino kodini saqlash
                
                await update.message.reply_text(
                    f"� Kino kodi: {text}\n\n"
                    "Endi kino faylini yuboring (video fayl):"
                )
                return
        
        # Oddiy foydalanuvchilar uchun kino qidirish
        movie_file_id = get_movie(text)
        
        if movie_file_id:
            try:
                await context.bot.send_video(
                    chat_id=user_id,
                    video=movie_file_id,
                    caption=f"🎬 Kino: {text}\n\n@uzmovi_film_bot"
                )
                logger.info(f"✅ Movie sent to {user_id}: {text}")
            except Exception as send_error:
                logger.error(f"❌ Movie send error: {send_error}")
                await update.message.reply_text(
                    f"❌ Kino yuborishda xatolik: {text}\n"
                    "Iltimos admin bilan bog'laning."
                )
        else:
            await update.message.reply_text(
                f"🔍 Kino qidirilmoqda: {text}\n\n"
                "❌ Bunday kodli kino topilmadi.\n"
                "Iltimos to'g'ri kino kodini yuboring."
            )
        
    except Exception as e:
        logger.error(f"❌ Message handler error: {e}")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle video files (admin kino joylash)"""
    try:
        user_id = update.effective_user.id
        
        if user_id != ADMIN_ID:
            await update.message.reply_text("❌ Faqat admin kino joylay oladi!")
            return
        
        if user_id not in waiting_for_movie_file:
            await update.message.reply_text("❌ Avval kino kodini yuboring!")
            return
        
        # Kino kodini olish
        movie_code = waiting_for_movie_file.pop(user_id)
        
        # Video file ID olish
        if update.message.video:
            file_id = update.message.video.file_id
            file_name = update.message.video.file_name or f"movie_{movie_code}"
        elif update.message.document and update.message.document.mime_type.startswith('video'):
            file_id = update.message.document.file_id
            file_name = update.message.document.file_name or f"movie_{movie_code}"
        else:
            await update.message.reply_text("❌ Iltimos video fayl yuboring!")
            return
        
        # Kino saqlash
        if save_movie(movie_code, file_id):
            await update.message.reply_text(
                f"✅ Kino muvaffaqiyatli joylandi!\n\n"
                f"📝 Kod: {movie_code}\n"
                f"📁 Fayl: {file_name}\n"
                f"🆔 File ID: {file_id[:20]}...",
                reply_markup=ReplyKeyboardRemove()
            )
            
            # Admin panel qaytarish
            await admin_command(update, context)
        else:
            await update.message.reply_text("❌ Kino saqlashda xatolik!")
        
        logger.info(f"✅ Movie uploaded: {movie_code} -> {file_id}")
        
    except Exception as e:
        logger.error(f"❌ Video handler error: {e}")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle photo messages (reklama uchun)"""
    try:
        user_id = update.effective_user.id
        
        if user_id != ADMIN_ID:
            return
        
        if user_id in waiting_for_ad_content:
            waiting_for_ad_content.pop(user_id)
            
            photo_file_id = update.message.photo[-1].file_id
            caption = update.message.caption or ""
            
            await update.message.reply_text("⏳ Reklama rasmi yuborilmoqda...")
            
            # Reklama yuborish
            success_count, result_msg = await send_broadcast(context, caption, photo_file_id)
            
            await update.message.reply_text(
                f"✅ Reklama rasmi yuborish tugadi!\n\n{result_msg}",
                reply_markup=ReplyKeyboardRemove()
            )
            
            # Admin panel qaytarish
            await admin_command(update, context)
        
    except Exception as e:
        logger.error(f"❌ Photo handler error: {e}")

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel any ongoing operation"""
    try:
        user_id = update.effective_user.id
        
        # Clear all waiting states
        waiting_for_ad_content.pop(user_id, None)
        waiting_for_movie_code.pop(user_id, None)
        waiting_for_movie_file.pop(user_id, None)
        
        await update.message.reply_text(
            "❌ Amal bekor qilindi.",
            reply_markup=ReplyKeyboardRemove()
        )
        
        # Return to start
        await start_command(update, context)
        
    except Exception as e:
        logger.error(f"❌ Cancel command error: {e}")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Error handler"""
    logger.error(f"Update {update} caused error {context.error}")

# Global variables for conversation states
waiting_for_movie_code = {}
waiting_for_movie_file = {}
waiting_for_ad_content = {}

def save_movie(code, file_id):
    """Kino file ID sini saqlash"""
    try:
        import json
        import os
        
        file_path = "file_ids.json"
        
        # Fayl mavjud bo'lsa, ma'lumotlarni o'qish
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
        else:
            data = {}
        
        # Kino kodini saqlash
        data[code] = file_id
        
        # Faylga yozish
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
        
        logger.info(f"🎬 Movie saved: {code} -> {file_id}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Save movie error: {e}")
        return False

def get_movie(code):
    """Kino file ID sini olish"""
    try:
        import json
        import os
        
        file_path = "file_ids.json"
        
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
                return data.get(code)
        
        return None
        
    except Exception as e:
        logger.error(f"❌ Get movie error: {e}")
        return None

async def send_broadcast(context, message_text, photo_file_id=None):
    """Barcha foydalanuvchilarga reklama yuborish"""
    try:
        import json
        import os
        
        if not os.path.exists("users.json"):
            return 0, "Foydalanuvchilar fayli topilmadi"
        
        with open("users.json", "r") as f:
            users_data = json.load(f)
            users = users_data.get("users", [])
        
        if not users:
            return 0, "Foydalanuvchilar ro'yxati bo'sh"
        
        success_count = 0
        failed_count = 0
        
        for user_id in users:
            try:
                if photo_file_id:
                    await context.bot.send_photo(
                        chat_id=user_id,
                        photo=photo_file_id,
                        caption=message_text
                    )
                else:
                    await context.bot.send_message(
                        chat_id=user_id,
                        text=message_text
                    )
                success_count += 1
                
                # Rate limiting
                if success_count % 30 == 0:
                    await asyncio.sleep(1)
                    
            except Exception as send_error:
                failed_count += 1
                logger.error(f"❌ Failed to send to {user_id}: {send_error}")
        
        return success_count, f"Yuborildi: {success_count}, Xatolik: {failed_count}"
        
    except Exception as e:
        logger.error(f"❌ Broadcast error: {e}")
        return 0, f"Xatolik: {e}"

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
        app.add_handler(CommandHandler("cancel", cancel_command))
        
        # Media handlers (admin uchun)
        app.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, handle_video))
        app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
        
        # Combined message handler (handles both admin and regular messages)
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_combined_message))
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
