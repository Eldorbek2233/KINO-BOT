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
    application.add_handler(CommandHandler("stat", stat))
    application.add_handler(CommandHandler("admin_menu", admin_menu))
    application.add_handler(CommandHandler("help", help_command))
    # Reklama conversation handler
    application.add_handler(ConversationHandler(
        entry_points=[CommandHandler("reklama", send_advertisement)],
        states={
            REKLAMA_WAIT: [MessageHandler(filters.TEXT | filters.PHOTO, handle_ad_content)]
        },
        fallbacks=[CommandHandler("cancel", cancel_command)],
        per_message=False
    ))
    
    # Matn xabarlar uchun handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Error handler qo'shish
    from handlers import error_handler
    application.add_error_handler(error_handler)
    
    # Komandalarni o'rnatish
    application.post_init = set_commands

def main():
    # Application yaratish - webhook mode uchun
    builder = Application.builder()
    builder.token(TOKEN)
    
    # Connection pool sozlamalari - webhook uchun maksimal optimallashtirilgan
    builder.pool_timeout(120)       # Pool timeout 2 daqiqaga ko'tarish
    builder.connection_pool_size(16) # Pool size sezilarli ko'tarish
    builder.read_timeout(60)        # Read timeout ko'tarish
    builder.write_timeout(60)       # Write timeout ko'tarish
    builder.connect_timeout(60)     # Connect timeout ko'tarish
    
    # Get updates sozlamalari
    builder.get_updates_pool_timeout(120)
    builder.get_updates_read_timeout(60)
    builder.get_updates_write_timeout(60)
    builder.get_updates_connect_timeout(60)
    
    application = builder.build()
    
    # Setup handlers using the function
    setup_handlers(application)
    
    print("🤖 Kino bot webhook mode da tayyor...")  # Uzbek tilida
    
    # Webhook mode da polling ishlatmaymiz
    # application.run_polling() ni olib tashlaymiz
    
    return application  # Web server uchun qaytaramiz

if __name__ == "__main__":
    try:
        # Webhook mode uchun web_server.py ishlatish kerak
        print("⚠️  Bot webhook mode uchun sozlangan!")
        print("🚀 Web server ni ishga tushirish...")
        
        # web_server.py ni import qilib ishga tushirish
        import web_server
        
        # Agar PORT environment variable bo'lsa, web server ishga tushirish
        import os
        if os.getenv('PORT') or os.getenv('RENDER_EXTERNAL_URL'):
            print("🌐 Render environment aniqlandi, web server ishga tushirilmoqda...")
            
            # Environment variables ni tekshirish
            port = int(os.environ.get('PORT', 8080))
            print(f"🚀 Server {port} portda ishga tushirilmoqda...")
            
            # Application yaratish
            print("🔧 Telegram application yaratilmoqda...")
            web_server.create_application()
            print("✅ Telegram application tayyor")
            
            # Webhook URL ni o'rnatish
            render_url = os.getenv('RENDER_EXTERNAL_URL')
            if not render_url:
                render_url = f"https://kino-bot-o8dw.onrender.com"
                print(f"🔗 RENDER_EXTERNAL_URL o'rnatildi: {render_url}")
            
            # Webhook o'rnatish
            webhook_url = f"{render_url}/webhook"
            print(f"📡 Webhook URL: {webhook_url}")
            
            import requests
            url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
            data = {"url": webhook_url}
            
            response = requests.post(url, data=data)
            result = response.json()
            
            if result.get('ok'):
                print(f"✅ Webhook o'rnatildi: {webhook_url}")
            else:
                print(f"❌ Webhook xatoligi: {result}")
            
            print(f"🌐 Server 0.0.0.0:{port} da ishga tushdi")
            print("📡 Webhook endpoint: /webhook")
            print("❤️ Health check: /health")
            print("🏠 Asosiy sahifa: /")
            
            # Flask server ishga tushirish
            web_server.app.run(
                host='0.0.0.0', 
                port=port,
                debug=False,  # Production uchun
                threaded=True  # Threading yoqish
            )
        else:
            print("💻 Local development uchun web_server.py ni alohida ishga tushiring:")
            print("   python web_server.py")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
