#!/usr/bin/env python3
"""
WSGI Configuration for Professional Kino Bot
"""

import os
import sys
import logging

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

try:
    from app import app, initialize_bot
    
    # Initialize bot on startup
    logger.info("🎭 Initializing Professional Kino Bot...")
    initialize_bot()
    logger.info("✅ Bot initialization completed!")
    
    # WSGI application
    application = app
    
    if __name__ == "__main__":
        port = int(os.environ.get('PORT', 8080))
        logger.info(f"🚀 Starting development server on port {port}")
        app.run(host='0.0.0.0', port=port, debug=False)
        
except Exception as e:
    logger.error(f"❌ WSGI startup error: {e}")
    raise
