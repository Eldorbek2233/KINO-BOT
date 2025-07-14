from flask import Flask, request
import threading
import os
import logging
import time
from config import TOKEN

# Flask app yaratish
app = Flask(__name__)

# Bot ishga tushirish uchun funksiya - subprocessda ishga tushiramiz
def run_bot():
    from bot import main
    try:
        main()
    except Exception as e:
        app.logger.error(f"Bot ishga tushishda xatolik: {str(e)}")

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
