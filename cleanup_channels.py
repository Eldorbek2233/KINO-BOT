#!/usr/bin/env python3
# Clean up invalid channels

import json
import requests
import os
from datetime import datetime

# Bot configuration
TOKEN = os.getenv('BOT_TOKEN', "8177519032:AAED4FgPoFQiQhqM_lvrK1iV8hL9u4SnkDk")
ADMIN_ID = 5542016161

def check_channel_validity(channel_id, channel_name):
    """Check if channel is valid and bot has access"""
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getChat"
        data = {'chat_id': channel_id}
        response = requests.post(url, data=data, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                print(f"✅ {channel_name}: Valid channel")
                return True
            else:
                error_desc = result.get('description', 'Unknown error')
                print(f"❌ {channel_name}: API Error - {error_desc}")
                return False
        else:
            print(f"❌ {channel_name}: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ {channel_name}: Exception - {e}")
        return False

def clean_channels():
    """Clean invalid channels from channels.json"""
    try:
        # Load current channels
        with open('channels.json', 'r', encoding='utf-8') as f:
            channels = json.load(f)
        
        print(f"🔍 Found {len(channels)} channels to check:")
        
        valid_channels = {}
        invalid_count = 0
        
        for channel_id, channel_data in channels.items():
            channel_name = channel_data.get('name', 'Unknown')
            username = channel_data.get('username', 'No username')
            
            print(f"\n🔍 Checking: {channel_name} ({username})")
            
            if check_channel_validity(channel_id, channel_name):
                valid_channels[channel_id] = channel_data
            else:
                invalid_count += 1
                print(f"🗑 Removing invalid channel: {channel_name}")
        
        # Save cleaned channels
        with open('channels.json', 'w', encoding='utf-8') as f:
            json.dump(valid_channels, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Cleanup completed!")
        print(f"📊 Results:")
        print(f"  • Valid channels: {len(valid_channels)}")
        print(f"  • Invalid channels removed: {invalid_count}")
        print(f"  • Total processed: {len(channels)}")
        
        if len(valid_channels) == 0:
            print(f"\n⚠️ No valid channels remain - subscription system will be disabled")
        else:
            print(f"\n🎯 Subscription system will work with {len(valid_channels)} valid channels")
            
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")

if __name__ == "__main__":
    print("🧹 Starting channel cleanup...")
    clean_channels()
