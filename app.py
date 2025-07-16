#!/usr/bin/env python3
"""
Render deployment entry point
Simple Flask server for Render platform
"""

import os
import sys
import logging

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """Main entry point for Render"""
    logger.info("🎭 Starting Kino Bot on Render...")
    
    try:
        # Import after path setup
        from wsgi import application
        
        # Get port from environment
        port = int(os.environ.get('PORT', 8080))
        
        logger.info(f"🌐 Starting server on port {port}")
        
        # Run the Flask app
        application.run(
            host='0.0.0.0',
            port=port,
            debug=False
        )
        
    except Exception as e:
        logger.error(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
