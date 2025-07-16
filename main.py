#!/usr/bin/env python3
"""
Main entry point for Render deployment
Alternative to app.py for platform compatibility
"""

import os
import sys
import logging

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def start_server():
    """Start the web server"""
    logger.info("🎭 Initializing Kino Bot for Render...")
    
    try:
        # Import web application
        from web_server import app
        import simple_bot
        
        # Create telegram application
        telegram_app = simple_bot.create_minimal_app()
        
        # Set telegram app in web server
        from web_server import set_telegram_app
        set_telegram_app(telegram_app)
        
        # Setup webhook
        webhook_url = None
        render_url = os.getenv('RENDER_EXTERNAL_URL')
        if render_url:
            webhook_url = f"{render_url}/webhook"
            logger.info(f"🔗 Webhook URL: {webhook_url}")
            
            # Set webhook
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
        
        # Start Flask server
        port = int(os.environ.get('PORT', 8080))
        logger.info(f"🚀 Starting server on port {port}")
        
        app.run(
            host='0.0.0.0',
            port=port,
            debug=False
        )
        
    except Exception as e:
        logger.error(f"❌ Startup error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    start_server()
