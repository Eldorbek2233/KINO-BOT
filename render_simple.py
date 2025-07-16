#!/usr/bin/env python3
"""
Ultra simple Render deployment - No complex imports
"""

import os
import logging
from flask import Flask, request, jsonify

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Hardcoded config for Render
TOKEN = "8177519032:AAED4FgPoFQiQhqM_lvrK1iV8hL9u4SnkDk"
ADMIN_ID = 5542016161

@app.route('/')
def home():
    """Health check"""
    return jsonify({
        "status": "ok", 
        "message": "Kino Bot is alive on Render!",
        "platform": "render",
        "webhook_ready": True,
        "token_length": len(TOKEN) if TOKEN else 0
    })

@app.route('/debug')
def debug():
    """Debug endpoint"""
    return jsonify({
        "token_present": bool(TOKEN),
        "token_length": len(TOKEN) if TOKEN else 0,
        "admin_id": ADMIN_ID,
        "webhook_url": f"{os.getenv('RENDER_EXTERNAL_URL', 'unknown')}/webhook"
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Simple webhook handler"""
    try:
        # Log raw request data
        logger.info(f"📨 Webhook request received")
        logger.info(f"📨 Content-Type: {request.content_type}")
        logger.info(f"📨 Headers: {dict(request.headers)}")
        
        # Try to get JSON data
        data = None
        try:
            data = request.get_json(force=True)
            logger.info(f"📨 Webhook data: {data}")
        except Exception as json_error:
            logger.error(f"❌ JSON parse error: {json_error}")
            logger.error(f"❌ Raw data: {request.get_data()}")
            return "JSON_ERROR", 400
        
        # Process message if exists
        if data and 'message' in data:
            message = data['message']
            chat_id = message.get('chat', {}).get('id')
            text = message.get('text', '')
            
            logger.info(f"💬 Message from {chat_id}: {text}")
            
            # Response to commands
            if text == '/start':
                send_message(chat_id, "🎬 Kino Bot ishlamoqda! Render da deploy qilindi.")
            elif text == '/test':
                send_message(chat_id, "✅ Test muvaffaqiyatli! Bot ishlamoqda.")
            elif text:
                send_message(chat_id, f"Echo: {text}")
        
        # Log successful processing
        logger.info("✅ Webhook processed successfully")
        return "OK", 200
        
    except Exception as e:
        logger.error(f"❌ Webhook error: {e}")
        import traceback
        logger.error(f"❌ Traceback: {traceback.format_exc()}")
        return f"ERROR: {str(e)}", 500

def send_message(chat_id, text):
    """Send message via Telegram API"""
    try:
        if not TOKEN:
            logger.error("❌ No TOKEN available")
            return False
            
        import requests
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text
        }
        
        logger.info(f"📤 Sending message to {chat_id}: {text[:50]}...")
        
        response = requests.post(url, data=data, timeout=10)
        result = response.json()
        
        if result.get('ok'):
            logger.info(f"✅ Message sent successfully to {chat_id}")
            return True
        else:
            logger.error(f"❌ Telegram API error: {result}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Send message error: {e}")
        import traceback
        logger.error(f"❌ Traceback: {traceback.format_exc()}")
        return False

def setup_webhook():
    """Setup webhook on startup"""
    try:
        webhook_url = os.getenv('RENDER_EXTERNAL_URL')
        if webhook_url:
            webhook_url = f"{webhook_url}/webhook"
            
            import requests
            response = requests.post(
                f"https://api.telegram.org/bot{TOKEN}/setWebhook",
                data={"url": webhook_url}
            )
            result = response.json()
            
            if result.get('ok'):
                logger.info(f"✅ Webhook set: {webhook_url}")
            else:
                logger.error(f"❌ Webhook error: {result}")
        else:
            logger.warning("⚠️ No RENDER_EXTERNAL_URL found")
            
    except Exception as e:
        logger.error(f"❌ Webhook setup error: {e}")

if __name__ == "__main__":
    logger.info("🎭 Starting Ultra Simple Kino Bot on Render...")
    
    # Setup webhook
    setup_webhook()
    
    # Start server
    port = int(os.environ.get('PORT', 8080))
    logger.info(f"🚀 Server starting on port {port}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )
