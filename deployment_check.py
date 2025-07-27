#!/usr/bin/env python3
"""
RENDER.COM DEPLOYMENT CHECKER
Professional Kino Bot Deployment Status
"""

import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_deployment_status():
    """Check deployment requirements"""
    logger.info("🔍 CHECKING DEPLOYMENT STATUS...")
    
    # Check required environment variables
    required_env_vars = [
        'BOT_TOKEN',
        'ADMIN_ID', 
        'MONGODB_URI'
    ]
    
    missing_vars = []
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"❌ Missing environment variables: {missing_vars}")
        return False
    
    logger.info("✅ All environment variables present")
    
    # Check critical files
    critical_files = [
        'app.py',
        'requirements.txt',
        'render.yaml',
        'Procfile'
    ]
    
    missing_files = []
    for file in critical_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        logger.error(f"❌ Missing critical files: {missing_files}")
        return False
    
    logger.info("✅ All critical files present")
    
    # Test app import
    try:
        import app
        logger.info("✅ App import successful")
    except Exception as e:
        logger.error(f"❌ App import failed: {e}")
        return False
    
    logger.info("🎉 DEPLOYMENT STATUS: READY!")
    return True

if __name__ == "__main__":
    check_deployment_status()
