from flask import Flask, request, jsonify
import os
import logging
import asyncio
from telegram import Update
from config import TOKEN

# Log konfiguratsiyasi
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

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
        # Import from bot module
        from bot import main, setup_handlers
        from telegram.ext import Application
        
        # Application yaratish - bot.py dan olish
        telegram_app = main()
        
        print("✅ Telegram application yaratildi va webhook uchun tayyor")
        
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
        
        # Get the update from request
        update_dict = request.get_json()
        if not update_dict:
            return jsonify({"status": "error", "message": "No JSON data"}), 400
            
        update = Update.de_json(update_dict, app_instance.bot)
        
        # Process the update
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(app_instance.process_update(update))
        
        return jsonify({"status": "ok"})
    except Exception as e:
        app.logger.error(f"Webhook error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Production port yoki default 8080
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
