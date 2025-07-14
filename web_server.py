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
app_initialized = False  # Application initialize bo'lganligini kuzatish
active_updates = 0      # Hozirda qaytarilayotgan update'lar soni
max_concurrent_updates = 5  # Maksimal bir vaqtda qayta ishlanadigan update'lar
update_timeout = 60  # Update processing timeout (60 soniya)

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
    global telegram_app, app_initialized
    if telegram_app is None:
        try:
            app.logger.info("🔧 Telegram application yaratilmoqda...")
            
            # Import from bot module
            from bot import main
            
            # Application yaratish - bot.py dan olish
            telegram_app = main()
            
            if telegram_app is None:
                raise Exception("Bot.main() None qaytardi")
            
            # PTB 20.0 uchun application ni faqat bir marta initialize qilish
            if not app_initialized:
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
                        app_initialized = True  # Initialize muvaffaqiyatli bo'ldi
                    finally:
                        # Loop ni to'g'ri yopish
                        try:
                            loop.close()
                        except:
                            pass
                        
                except Exception as init_error:
                    app.logger.error(f"⚠️ Initialize qilishda muammo: {init_error}")
                    # Continue anyway - ba'zi hollarda initialize qilmasdan ham ishlashi mumkin
            else:
                app.logger.info("ℹ️ Application allaqachon initialize qilingan")
            
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
    global active_updates
    
    try:
        # Rate limiting - juda ko'p concurrent update'larni oldini olish
        if active_updates >= max_concurrent_updates:
            app.logger.warning(f"⚠️ Juda ko'p active update'lar ({active_updates}), keyinroq qayta urining")
            return jsonify({"status": "busy", "message": "Too many concurrent updates"}), 429
        
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
            global active_updates
            
            try:
                active_updates += 1  # Active update counter ko'tarish
                app.logger.info(f"🔄 Update ni process qilish boshlandi... (Active: {active_updates})")
                
                # Thread-safe asyncio approach
                import asyncio
                import concurrent.futures
                
                async def async_process():
                    """Async context da update ni process qilish"""
                    try:
                        # Update type ni aniqlash
                        update_type = "unknown"
                        if update.message:
                            update_type = f"message: {update.message.text[:20] if update.message.text else 'no_text'}"
                        elif update.callback_query:
                            update_type = f"callback: {update.callback_query.data[:20] if update.callback_query.data else 'no_data'}"
                        
                        app.logger.info(f"🔍 Processing {update_type} (ID: {update.update_id})")
                        
                        # Update ni timeout bilan process qilish
                        import asyncio
                        import time
                        
                        start_time = time.time()
                        
                        # Update processing timeout (60 soniya)
                        await asyncio.wait_for(
                            app_instance.process_update(update), 
                            timeout=update_timeout
                        )
                        
                        processing_time = time.time() - start_time
                        app.logger.info(f"✅ Update {update.update_id} muvaffaqiyatli qayta ishlandi ({processing_time:.2f}s)")
                        
                    except asyncio.TimeoutError:
                        processing_time = time.time() - start_time
                        app.logger.error(f"⏰ Update {update.update_id} timeout - {update_timeout} soniyadan ko'p vaqt oldi ({processing_time:.2f}s)")
                        app.logger.error(f"⏰ Timeout update type: {update_type}")
                    except Exception as e:
                        processing_time = time.time() - start_time if 'start_time' in locals() else 0
                        app.logger.error(f"❌ Async update process xatolik: {e} ({processing_time:.2f}s)")
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
            finally:
                active_updates -= 1  # Active update counter pasaytirish
                app.logger.info(f"🏁 Update qayta ishlash tugadi (Active: {active_updates})")
        
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
