from telegram import BotCommand, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters, ConversationHandler
from config import TOKEN, ADMIN_ID
import logging
from handlers import *

# Log konfiguratsiyasi
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
                    

def set_commands(updater):
    # Admin uchun komandalar
    admin_commands = [
        BotCommand("start", "Botni boshlash"),
        BotCommand("users", "Foydalanuvchilar soni"),
        BotCommand("stat", "Bot statistikasi"),
        BotCommand("admin_menu", "Admin menyusi")
    ]
    
    # Oddiy foydalanuvchilar uchun komandalar
    user_commands = [
        BotCommand("start", "Botni boshlash"),
        BotCommand("help", "Yordam")
    ]
    
    # Barcha foydalanuvchilar uchun komandalarni o'rnatish
    updater.bot.set_my_commands(user_commands)

def main():
    # Updater yaratish
    updater = Updater(TOKEN, use_context=True)
    
    # Dispatcher olish
    dp = updater.dispatcher
    
    # Komandalarni o'rnatish
    set_commands(updater)
    
    # Asosiy komandalar uchun handler
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("users", users_count))
    dp.add_handler(CommandHandler("stat", bot_stat))
    dp.add_handler(CommandHandler("admin_menu", admin_menu))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("reklama", send_advertisement), 
            CallbackQueryHandler(reklama_inline_handler, pattern="^reklama_inline$")
        ],
        states={
            REKLAMA_WAIT: [MessageHandler(Filters.all, handle_ad_content)]
        },
        fallbacks=[CommandHandler("cancel", cancel_handler)]
    ))
    
    # Kino joylash uchun conversation handler
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("add_movie", add_movie_handler),
            CallbackQueryHandler(add_movie_handler, pattern="^add_movie$"),
            MessageHandler(Filters.regex(r"(?i)^🎬?\s*kino\s*joylash$"), add_movie_handler)
        ],
        states={
            WAITING_FOR_CODE: [MessageHandler(Filters.text & ~Filters.command, get_movie_code)],
            WAITING_FOR_VIDEO: [MessageHandler(Filters.video | Filters.animation, get_movie_video)]
        },
        fallbacks=[CommandHandler("cancel", cancel_handler)]
    ))
    
    # Kanal boshqarish uchun conversation handler
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("manage_channels", manage_channels),
            CallbackQueryHandler(manage_channels, pattern="^manage_channels$"),
            MessageHandler(Filters.regex(r"(?i)^📢?\s*kanallar$"), manage_channels)
        ],
        states={
            CHANNEL_MENU: [
                CallbackQueryHandler(add_channel_command, pattern="^add_channel$"),
                CallbackQueryHandler(remove_channel_command, pattern="^remove_channel$"),
                CallbackQueryHandler(back_to_menu, pattern="^back_to_menu$"),
                CallbackQueryHandler(delete_channel, pattern="^delete_channel_[0-9]+$")
            ],
            WAITING_FOR_CHANNEL: [MessageHandler(Filters.text & ~Filters.command, process_new_channel)]
        },
        fallbacks=[CommandHandler("cancel", cancel_handler)]
    ))
    
    dp.add_handler(MessageHandler((Filters.text | Filters.photo) & ~Filters.command, handle_code))
    dp.add_handler(MessageHandler(Filters.all, handle_channel_video))
    dp.add_handler(CallbackQueryHandler(confirm_membership, pattern="^check_membership$"))
    dp.add_handler(CallbackQueryHandler(stat_button_handler, pattern="^show_stat$"))
    
    print("🤖 Kino bot ishga tushdi...")  # Uzbek tilida
    
    # Botni ishga tushirish
    updater.start_polling()
    
    # Ctrl+C bosilmaguncha kutish
    updater.idle()

if __name__ == "__main__":
    main()
