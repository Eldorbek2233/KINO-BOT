# No need for telegram_patch with v20.0

from telegram import BotCommand, KeyboardButton, Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler, 
    ConversationHandler, ContextTypes, filters
)
from config import TOKEN, ADMIN_ID
import logging
import asyncio
from handlers import *

# Log konfiguratsiyasi
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def set_commands(application):
    # Oddiy foydalanuvchilar uchun komandalar
    user_commands = [
        BotCommand("start", "Botni boshlash"),
        BotCommand("help", "Yordam")
    ]
    
    # Admin uchun komandalar
    admin_commands = [
        BotCommand("start", "Botni boshlash"),
        BotCommand("users", "Foydalanuvchilar soni"),
        BotCommand("stat", "Bot statistikasi"),
        BotCommand("admin_menu", "Admin menyusi"),
        BotCommand("help", "Yordam")
    ]
    
    # Barcha foydalanuvchilar uchun komandalarni o'rnatish
    await application.bot.set_my_commands(user_commands)
    
    # Admin uchun alohida komandalar o'rnatish
    try:
        from telegram import BotCommandScopeChat
        await application.bot.set_my_commands(
            admin_commands, 
            scope=BotCommandScopeChat(chat_id=ADMIN_ID)
        )
    except Exception as e:
        print(f"Admin komandalarini o'rnatishda xatolik: {e}")

def setup_handlers(application):
    """Setup all bot handlers"""
    # Set up handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("users", users_count))
    application.add_handler(CommandHandler("stat", bot_stat))
    application.add_handler(CommandHandler("admin_menu", admin_menu))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("reklama", send_advertisement), 
            CallbackQueryHandler(reklama_inline_handler, pattern="^reklama_inline$")
        ],
        states={
            REKLAMA_WAIT: [MessageHandler(filters.ALL & ~filters.COMMAND, handle_ad_content)]
        },
        fallbacks=[CommandHandler("cancel", cancel_handler)],
        per_message=False
    ))
    
    # Kino joylash uchun conversation handler
    application.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("add_movie", add_movie_handler),
            CallbackQueryHandler(add_movie_handler, pattern="^add_movie$"),
            MessageHandler(filters.Regex(r"(?i)^🎬?\s*kino\s*joylash$"), add_movie_handler)
        ],
        states={
            WAITING_FOR_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_movie_code)],
            WAITING_FOR_VIDEO: [MessageHandler(filters.VIDEO | filters.ANIMATION, get_movie_video)]
        },
        fallbacks=[CommandHandler("cancel", cancel_handler)],
        per_message=False
    ))
    
    # Kanal boshqarish uchun conversation handler
    application.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("manage_channels", manage_channels),
            CallbackQueryHandler(manage_channels, pattern="^manage_channels$"),
            MessageHandler(filters.Regex(r"(?i)^📢?\s*kanallar$"), manage_channels)
        ],
        states={
            CHANNEL_MENU: [
                CallbackQueryHandler(add_channel_command, pattern="^add_channel$"),
                CallbackQueryHandler(remove_channel_command, pattern="^remove_channel$"),
                CallbackQueryHandler(back_to_menu, pattern="^back_to_menu$"),
                CallbackQueryHandler(delete_channel, pattern="^delete_channel_[0-9]+$")
            ],
            WAITING_FOR_CHANNEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_new_channel)]
        },
        fallbacks=[CommandHandler("cancel", cancel_handler)],
        per_message=False
    ))
    
    application.add_handler(MessageHandler((filters.TEXT | filters.PHOTO) & ~filters.COMMAND, handle_code))
    application.add_handler(MessageHandler(filters.ALL, handle_channel_video))
    application.add_handler(CallbackQueryHandler(confirm_membership, pattern="^check_membership$"))
    application.add_handler(CallbackQueryHandler(stat_button_handler, pattern="^show_stat$"))
    
    # Komandalarni o'rnatish
    application.post_init = set_commands

def main():
    # Application yaratish - webhook mode uchun
    builder = Application.builder()
    builder.token(TOKEN)
    
    # Connection pool sozlamalari
    builder.pool_timeout(30)
    builder.read_timeout(30)
    builder.write_timeout(30)
    builder.connect_timeout(30)
    
    application = builder.build()
    
    # Setup handlers using the function
    setup_handlers(application)
    
    print("🤖 Kino bot webhook mode da tayyor...")  # Uzbek tilida
    
    # Webhook mode da polling ishlatmaymiz
    # application.run_polling() ni olib tashlaymiz
    
    return application  # Web server uchun qaytaramiz

if __name__ == "__main__":
    try:
        # Agar to'g'ridan-to'g'ri ishga tushirilsa, xabar ko'rsatamiz
        print("Bot webhook mode uchun sozlangan. web_server.py orqali ishga tushiring.")
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
