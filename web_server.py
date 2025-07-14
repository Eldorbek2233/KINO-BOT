from flask import Flask, request, jsonify
import os
import logging
import asyncio
import threading
from telegram import Update
from config import TOKEN

# Log konfiguratsiyasi
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Flask app yaratish
app = Flask(__name__)

# Global application object
telegram_app = None
webhook_set = False

def set_webhook_if_needed():
    """Deploy qilingandan keyin webhook ni avtomatik o'rnatish"""
    global webhook_set
    
    if webhook_set:
        return
        
    render_url = os.getenv('RENDER_EXTERNAL_URL')
    if render_url:
        try:
            import requests
            webhook_url = f"{render_url}/webhook"
            
            url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
            data = {"url": webhook_url}
            
            response = requests.post(url, data=data)
            result = response.json()
            
            if result.get('ok'):
                app.logger.info(f"✅ Webhook o'rnatildi: {webhook_url}")
                webhook_set = True
            else:
                app.logger.error(f"❌ Webhook xatoligi: {result}")
        except Exception as e:
            app.logger.error(f"Webhook o'rnatishda xatolik: {e}")

def create_application():
    """Create and configure the Telegram application"""
    global telegram_app
    if telegram_app is None:
        try:
            app.logger.info("🔧 Telegram application yaratilmoqda...")
            
            # Import from bot module
            from bot import main
            
            # Application yaratish - bot.py dan olish
            telegram_app = main()
            
            if telegram_app is None:
                raise Exception("Bot.main() None qaytardi")
            
            # PTB 20.0 uchun application ni initialize qilish
            import asyncio
            try:
                # Synchronized initialization approach
                async def init_app():
                    """Application va Bot ni initialize qilish"""
                    try:
                        # Application ni initialize qilish
                        if hasattr(telegram_app, 'initialize'):
                            await telegram_app.initialize()
                            app.logger.info("🔧 Application initialize qilindi")
                        
                        # Bot ni initialize qilish
                        if hasattr(telegram_app, 'bot') and hasattr(telegram_app.bot, 'initialize'):
                            await telegram_app.bot.initialize()
                            app.logger.info("🤖 Bot initialize qilindi")
                            
                    except Exception as init_error:
                        app.logger.error(f"⚠️ Initialize qilishda muammo: {init_error}")
                        raise
                
                # Event loop yaratish va initialization
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                try:
                    loop.run_until_complete(init_app())
                finally:
                    # Loop ni to'g'ri yopish
                    try:
                        loop.close()
                    except:
                        pass
                    
            except Exception as init_error:
                app.logger.error(f"⚠️ Initialize qilishda muammo: {init_error}")
                # Continue anyway - ba'zi hollarda initialize qilmasdan ham ishlashi mumkin
            
            app.logger.info("✅ Telegram application muvaffaqiyatli yaratildi")
            app.logger.info(f"📋 Application type: {type(telegram_app)}")
            
            # Application attributes ni debug qilish
            if hasattr(telegram_app, 'bot'):
                try:
                    bot_info = f"Bot ID: {telegram_app.bot.id if hasattr(telegram_app.bot, 'id') else 'Unknown'}"
                    app.logger.info(f"🤖 {bot_info}")
                except:
                    app.logger.info("🤖 Bot mavjud")
            
        except Exception as e:
            app.logger.error(f"❌ Application yaratishda xatolik: {e}")
            import traceback
            app.logger.error(traceback.format_exc())
            # Re-raise qilmaslik - application hali ham ishlashiga ruxsat berish
            telegram_app = None
        
    return telegram_app

# Asosiy sahifa
@app.route('/')
def index():
    # Webhook ni tekshirish va o'rnatish
    set_webhook_if_needed()
    return "Kino Bot ishlayapti! Webhook mode."

# Health check endpoint
@app.route('/health')
def health():
    return "OK", 200

# Webhook endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        app_instance = create_application()
        
        if app_instance is None:
            app.logger.error("❌ Telegram application mavjud emas")
            return jsonify({"status": "error", "message": "Application not available"}), 500
        
        # Get the update from request
        update_dict = request.get_json()
        if not update_dict:
            app.logger.warning("Webhook: Bo'sh JSON ma'lumot keldi")
            return jsonify({"status": "error", "message": "No JSON data"}), 400
            
        # Update yaratish
        try:
            update = Update.de_json(update_dict, app_instance.bot)
            app.logger.info(f"📥 Yangi update keldi: {update.update_id}")
        except Exception as e:
            app.logger.error(f"Update parse qilishda xatolik: {e}")
            return jsonify({"status": "error", "message": "Invalid update format"}), 400
        
        # Async task yaratish - blokingni oldini olish
        import asyncio
        import threading
        
        def process_update_sync():
            """Sync context da async update ni process qilish"""
            try:
                app.logger.info("🔄 Update ni process qilish boshlandi...")
                
                # Thread-safe asyncio approach
                import asyncio
                import concurrent.futures
                
                async def async_process():
                    """Async context da update ni process qilish"""
                    try:
                        # Application va Bot ni initialize qilish (agar kerak bo'lsa)
                        try:
                            # Application initialize
                            if hasattr(app_instance, 'initialize'):
                                await app_instance.initialize()
                            
                            # Bot initialize  
                            if hasattr(app_instance, 'bot') and hasattr(app_instance.bot, 'initialize'):
                                await app_instance.bot.initialize()
                                
                        except Exception as init_err:
                            app.logger.warning(f"⚠️ Runtime initialize: {init_err}")
                            # Continue anyway
                        
                        # Update ni process qilish
                        await app_instance.process_update(update)
                        
                        app.logger.info(f"✅ Update {update.update_id} muvaffaqiyatli qayta ishlandi")
                        
                    except Exception as e:
                        app.logger.error(f"❌ Async update process xatolik: {e}")
                        import traceback
                        app.logger.error(traceback.format_exc())
                
                # Yangi event loop yaratish va ishlatish
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(async_process())
                finally:
                    # Loop ni to'g'ri yopish
                    try:
                        loop.close()
                    except:
                        pass
                
            except Exception as e:
                app.logger.error(f"❌ Update process qilishda xatolik: {e}")
                import traceback
                app.logger.error(traceback.format_exc())
        
        # Background thread da ishga tushirish
        thread = threading.Thread(target=process_update_sync)
        thread.daemon = True
        thread.start()
        
        # Tezkor javob - Telegram kutmaydi
        return jsonify({"status": "ok"})
        
    except Exception as e:
        app.logger.error(f"Webhook xatoligi: {str(e)}")
        import traceback
        app.logger.error(traceback.format_exc())
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    try:
        # Environment variables ni tekshirish
        port = int(os.environ.get('PORT', 8080))
        print(f"🚀 Server {port} portda ishga tushirilmoqda...")
        logger.info(f"🚀 Server {port} portda ishga tushirilmoqda...")
        
        # Application yaratish
        print("🔧 Telegram application yaratilmoqda...")
        create_application()
        print("✅ Telegram application tayyor")
        
        print(f"🌐 Server http://localhost:{port} da ishga tushdi")
        print("📡 Webhook endpoint: /webhook")
        print("❤️ Health check: /health")
        print("🏠 Asosiy sahifa: /")
        
        # Flask server ishga tushirish
        app.run(
            host='0.0.0.0', 
            port=port,
            debug=False,  # Production uchun
            threaded=True  # Threading yoqish
        )
        
    except Exception as e:
        print(f"❌ Server ishga tushirishda xatolik: {e}")
        import traceback
        traceback.print_exc()
