from flask import Flask, request
import os
import logging
import threading
import time
from config import TOKEN

# Log konfiguratsiyasi
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Flask app yaratish
app = Flask(__name__)

# Bot ishga tushirish uchun funksiya
def run_bot():
    try:
        # Simple retry mechanism
        max_retries = 3
        for attempt in range(max_retries):
            try:
                from bot import main
                main()
                break  # If successful, break out of retry loop
            except Exception as e:
                app.logger.error(f"Bot start attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(5)  # Wait 5 seconds before retry
                else:
                    app.logger.error("All retry attempts failed")
                    raise
    except Exception as e:
        app.logger.error(f"Bot ishga tushishda xatolik: {str(e)}")
        import traceback
        app.logger.error(traceback.format_exc())

# Bot threadini boshlash
def start_bot_thread():
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    return bot_thread

# Bot threadini ishga tushirish
bot_thread = start_bot_thread()

# Asosiy sahifa
@app.route('/')
def index():
    return "Kino Bot ishlayapti!"

# Health check endpoint
@app.route('/health')
def health():
    return "OK", 200

# Webhook endpoint (kerak bo'lganda)
@app.route('/webhook', methods=['POST'])
def webhook():
    return "Webhook received", 200

if __name__ == '__main__':
    # Production port yoki default 8080
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
