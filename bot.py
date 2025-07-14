from telegram import BotCommand, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ConversationHandler
from config import TOKEN, ADMIN_ID
from handlers import *
                    

async def set_commands(app):
    # Admin uchun komandalar
    admin_commands = [
        BotCommand("start", "Botni boshlash"),
        BotCommand("users", "Foydalanuvchilar soni"),
        BotCommand("stat", "Bot statistikasi"),
        BotCommand("admin_menu", "Admin menyusi")
    ]
    await app.bot.set_my_commands(admin_commands, scope={"type": "chat", "chat_id": ADMIN_ID})
    
    # Oddiy foydalanuvchilar uchun komandalar
    user_commands = [
        BotCommand("start", "Botni boshlash"),
        BotCommand("help", "Yordam")
    ]
    # Barcha foydalanuvchilar uchun komandalarni o'rnatish
    await app.bot.set_my_commands(user_commands)

def main():
    app = Application.builder().token(TOKEN).post_init(set_commands).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("users", users_count))
    app.add_handler(CommandHandler("stat", bot_stat))
    app.add_handler(CommandHandler("admin_menu", admin_menu))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("reklama", send_advertisement), 
            CallbackQueryHandler(reklama_inline_handler, pattern="^reklama_inline$")
        ],
        states={
            REKLAMA_WAIT: [MessageHandler(filters.ALL, handle_ad_content)]
        },
        fallbacks=[CommandHandler("cancel", cancel_handler)],
        per_chat=True
    ))
    
    # Kino joylash uchun conversation handler
    app.add_handler(ConversationHandler(
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
        per_chat=True
    ))
    
    # Kanal boshqarish uchun conversation handler
    app.add_handler(ConversationHandler(
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
        per_chat=True
    ))
    
    app.add_handler(MessageHandler((filters.TEXT | filters.PHOTO) & ~filters.COMMAND, handle_code))
    app.add_handler(MessageHandler(filters.ALL, handle_channel_video))
    app.add_handler(CallbackQueryHandler(confirm_membership, pattern="^check_membership$"))
    app.add_handler(CallbackQueryHandler(stat_button_handler, pattern="^show_stat$"))

    print("🤖 Kino bot ishga tushdi...")  # Uzbek tilida
    # Polling rejimida ishlash
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
