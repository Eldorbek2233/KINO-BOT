#!/usr/bin/env python3
"""
Bot token test - Tokenni tekshirish
"""

import os
import sys

print("🔍 Bot Token Tekshiruvi...")
print("=" * 40)

# Check environment variables
bot_token_env = os.getenv("BOT_TOKEN")
token_env = os.getenv("TOKEN")
admin_id_env = os.getenv("ADMIN_ID")

success_msg = "✅ O'rnatilgan"
fail_msg = "❌ Yo'q"

print(f"BOT_TOKEN env: {success_msg if bot_token_env else fail_msg}")
print(f"TOKEN env: {success_msg if token_env else fail_msg}")
print(f"ADMIN_ID env: {success_msg if admin_id_env else fail_msg}")

if bot_token_env:
    print(f"BOT_TOKEN uzunligi: {len(bot_token_env)} ta belgi")
    print(f"BOT_TOKEN boshi: {bot_token_env[:15]}...")
    
    # Check token format
    if ':' in bot_token_env and len(bot_token_env) > 40:
        print("✅ Token formati to'g'ri ko'rinadi")
    else:
        print("❌ Token formati noto'g'ri!")

if token_env:
    print(f"TOKEN uzunligi: {len(token_env)} ta belgi")
    print(f"TOKEN boshi: {token_env[:15]}...")

# Try to load railway config
print("\n🚂 Railway Config Tekshiruvi...")
try:
    from railway_config import get_token, get_admin_id
    token = get_token()
    admin_id = get_admin_id()
    
    print("✅ Railway config yuklandi")
    print(f"Token uzunligi: {len(token)} ta belgi")
    print(f"Admin ID: {admin_id}")
    
except Exception as e:
    print(f"❌ Railway config xatosi: {e}")

print("\n" + "=" * 40)
print("Token tekshiruvi tugadi!")
