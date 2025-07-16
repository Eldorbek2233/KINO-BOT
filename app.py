#!/usr/bin/env python3
"""
Render deployment entry point - Simple Flask server
"""

import os
import sys
import logging
from flask import Flask, request, jsonify

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Global telegram app
telegram_app = None

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "message": "Kino Bot is running on Render!",
        "platform": "render"
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Telegram webhook endpoint"""
    try:
        if telegram_app is None:
            return jsonify({"error": "Telegram app not initialized"}), 500
            
        # Process telegram update
        update_data = request.get_json()
        if update_data:
            from telegram import Update
            update = Update.de_json(update_data, telegram_app.bot)
            
            # Process update in background
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(telegram_app.process_update(update))
            loop.close()
            
        return "OK"
        
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return jsonify({"error": str(e)}), 500

def setup_telegram():
    """Setup telegram bot"""
    global telegram_app
    
    try:
        logger.info("� Setting up Telegram bot...")
        
        # Import telegram setup
        import simple_bot
        telegram_app = simple_bot.create_minimal_app()
        
        # Setup webhook
        webhook_url = None
        render_url = os.getenv('RENDER_EXTERNAL_URL')
        
        if render_url:
            webhook_url = f"{render_url}/webhook"
            logger.info(f"🔗 Setting webhook: {webhook_url}")
            
            # Set webhook using requests
            import requests
            response = requests.post(
                f"https://api.telegram.org/bot{simple_bot.TOKEN}/setWebhook",
                data={"url": webhook_url}
            )
            result = response.json()
            
            if result.get('ok'):
                logger.info("✅ Webhook configured successfully")
            else:
                logger.error(f"❌ Webhook error: {result}")
        else:
            logger.warning("⚠️ No RENDER_EXTERNAL_URL found")
            
    except Exception as e:
        logger.error(f"❌ Telegram setup error: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main entry point"""
    logger.info("🎭 Starting Kino Bot on Render...")
    
    # Setup telegram bot
    setup_telegram()
    
    # Get port
    port = int(os.environ.get('PORT', 8080))
    logger.info(f"🚀 Starting Flask server on port {port}")
    
    # Run Flask app
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        threaded=True
    )

if __name__ == "__main__":
    main()
