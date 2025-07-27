#!/usr/bin/env python3
"""
Local deployment test script for Professional Kino Bot
"""

import os
import sys
import logging

# Set environment variables for testing
os.environ['BOT_TOKEN'] = "8177519032:AAED4FgPoFQiQhqM_lvrK1iV8hL9u4SnkDk"
os.environ['ADMIN_ID'] = "5542016161"
os.environ['PORT'] = "8080"
os.environ['MONGODB_URI'] = "mongodb+srv://eldorbekxakimxujayev4:Ali11042004@kinobot-cluster.quzswqg.mongodb.net/kinobot?retryWrites=true&w=majority&appName=kinobot-cluster"

print("🎭 PROFESSIONAL KINO BOT - LOCAL DEPLOYMENT TEST")
print("=" * 60)

try:
    from app import app, initialize_bot
    
    print("✅ Import successful")
    
    # Initialize bot
    print("🔄 Initializing bot...")
    initialize_bot()
    print("✅ Bot initialized")
    
    # Test basic routes
    with app.test_client() as client:
        # Test home route
        response = client.get('/')
        if response.status_code == 200:
            print("✅ Home route working")
        else:
            print(f"❌ Home route failed: {response.status_code}")
        
        # Test health route
        response = client.get('/health')
        if response.status_code == 200:
            print("✅ Health route working")
        else:
            print(f"❌ Health route failed: {response.status_code}")
    
    print("=" * 60)
    print("🎉 ALL TESTS PASSED - READY FOR DEPLOYMENT!")
    print("📋 Deployment commands:")
    print("   • Railway: git push origin main")
    print("   • Render: Connect GitHub repo")
    print("   • Heroku: git push heroku main")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    sys.exit(1)
