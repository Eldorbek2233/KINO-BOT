from flask import Flask, request, jsonify
import os
import logging
import asyncio
import threading
import time
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram import Update
from config import TOKEN

# Log konfiguratsiyasi
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Flask app yaratish
app = Flask(__name__)

# Environment detection (Railway, Render, yoki local)
RAILWAY_ENV = os.getenv('RAILWAY_ENVIRONMENT')
RENDER_ENV = os.getenv('RENDER_EXTERNAL_URL')

if RAILWAY_ENV:
    logger.info(f"🚂 Railway environment detected: {RAILWAY_ENV}")
elif RENDER_ENV:
    logger.info(f"🎭 Render environment detected: {RENDER_ENV}")
else:
    logger.info("💻 Local environment detected")

# Global error handler
@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 Internal Server Error: {error}")
    return jsonify({"status": "error", "message": "Internal server error"}), 200

@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404 Not Found: {error}")
    return jsonify({"status": "error", "message": "Not found"}), 404

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled exception: {e}")
    import traceback
    logger.error(traceback.format_exc())
    return jsonify({"status": "error", "message": "Internal server error"}), 500

# Global variables
telegram_app = None
app_initialized = False
active_updates = 0
max_concurrent_updates = 5
update_timeout = 30  # Timeout ni 30 soniyaga kamaytirish

def set_telegram_app(app_instance):
    """Set global telegram app from external source"""
    global telegram_app, app_initialized
    telegram_app = app_instance
    app_initialized = True
    logger.info(f"✅ Global telegram_app set: {telegram_app}")
    logger.info(f"✅ App initialized: {app_initialized}")

# Asosiy sahifa
@app.route('/')
def index():
    return "Kino Bot ishlayapti! Webhook mode."

# Health check endpoint
@app.route('/health')
def health():
    return "OK", 200

# Webhook endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    global active_updates, telegram_app
    
    try:
        logger.info("🌐 Webhook so'rovi keldi")
        logger.info(f"📋 Global telegram_app: {telegram_app}")
        logger.info(f"📋 App initialized: {app_initialized}")
        
        # Rate limiting
        if active_updates >= max_concurrent_updates:
            logger.warning(f"⚠️ Juda ko'p active update'lar ({active_updates})")
            return jsonify({"status": "busy"}), 429
        
        if telegram_app is None:
            logger.error("❌ telegram_app is None")
            return jsonify({"status": "error", "message": "Bot not initialized"}), 500
        
        logger.info("✅ Using global telegram_app")
        
        # Webhook data olish
        webhook_data = request.json
        if not webhook_data:
            logger.warning("⚠️ Bo'sh webhook data")
            return jsonify({"status": "error", "message": "No data"}), 400
        
        # Update obyektini yaratish
        update = Update.de_json(webhook_data, telegram_app.bot)
        if not update:
            logger.warning("⚠️ Noto'g'ri update ma'lumotlari")
            return jsonify({"status": "error", "message": "Invalid update"}), 400
        
        update_id = update.update_id
        logger.info(f"📥 Yangi update keldi: {update_id}")
        
        # Process update in background
        def process_update_sync():
            global active_updates
            active_updates += 1
            start_time = time.time()
            
            try:
                logger.info(f"🔄 Update ni process qilish boshlandi... (Active: {active_updates})")
                
                if update.message:
                    message_text = update.message.text or "No text"
                    logger.info(f"🔍 Processing message: {message_text} (ID: {update_id})")
                
                # Use existing event loop instead of creating new one
                try:
                    # Try to get existing loop
                    loop = asyncio.get_event_loop()
                    if loop.is_closed():
                        # If closed, create new one
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                except RuntimeError:
                    # No loop exists, create new one
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                
                try:
                    # Process update with timeout
                    loop.run_until_complete(
                        asyncio.wait_for(
                            telegram_app.process_update(update), 
                            timeout=update_timeout
                        )
                    )
                    
                    process_time = time.time() - start_time
                    logger.info(f"✅ Update {update_id} muvaffaqiyatli qayta ishlandi ({process_time:.2f}s)")
                    
                except asyncio.TimeoutError:
                    logger.error(f"⏰ Update {update_id} timeout ({update_timeout}s)")
                except Exception as process_error:
                    logger.error(f"❌ Update {update_id} processing error: {process_error}")
                    import traceback
                    logger.error(traceback.format_exc())
                finally:
                    # Only close loop if we created it
                    try:
                        if not loop.is_running():
                            loop.close()
                    except:
                        pass
                    
            except Exception as thread_error:
                logger.error(f"❌ Thread error processing update {update_id}: {thread_error}")
                import traceback
                logger.error(traceback.format_exc())
            finally:
                active_updates -= 1
                logger.info(f"🏁 Update qayta ishlash tugadi (Active: {active_updates})")
        
        # Background thread yaratish
        update_thread = threading.Thread(
            target=process_update_sync,
            name=f"update-{update_id}",
            daemon=True
        )
        update_thread.start()
        
        logger.info("✅ Webhook javobi yuborildi")
        return jsonify({"status": "ok"}), 200
        
    except Exception as e:
        logger.error(f"❌ Webhook xatolik: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    logger.info("🚀 Server 8080 portda ishga tushirilmoqda...")
    logger.info("🌐 Server http://localhost:8080 da ishga tushdi")
    logger.info("📡 Webhook endpoint: /webhook")
    logger.info("❤️ Health check: /health")
    app.run(host="0.0.0.0", port=8080, debug=False, threaded=True)
