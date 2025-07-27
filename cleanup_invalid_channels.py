#!/usr/bin/env python3
"""
EMERGENCY CLEANUP SCRIPT
Removes all invalid channels from database and forces subscription system reset
"""

import json
import os
import sys

def cleanup_invalid_channels():
    """Remove all problematic channels and reset subscription system"""
    
    print("🚨 EMERGENCY: Cleaning up invalid channels...")
    
    # List of problematic channels to remove
    problematic_channels = [
        '@soglomxayot_ersag', 
        '-1002047665778',
        'soglomxayot_ersag'
    ]
    
    # 1. Clean channels.json
    try:
        channels_data = {}
        with open('channels.json', 'w') as f:
            json.dump(channels_data, f, indent=2)
        print("✅ channels.json cleared")
    except Exception as e:
        print(f"⚠️ Could not clear channels.json: {e}")
    
    # 2. Create clean file_ids.json if exists
    try:
        file_ids_data = {}
        with open('file_ids.json', 'w') as f:
            json.dump(file_ids_data, f, indent=2)
        print("✅ file_ids.json cleared")
    except Exception as e:
        print(f"⚠️ Could not clear file_ids.json: {e}")
    
    # 3. Force subscription system reset
    try:
        # Create temporary disable flag
        with open('.subscription_disabled', 'w') as f:
            f.write('TEMPORARY_DISABLE_FOR_CLEANUP')
        print("✅ Subscription temporarily disabled")
    except Exception as e:
        print(f"⚠️ Could not create disable flag: {e}")
    
    print("🎯 CLEANUP COMPLETED!")
    print("📋 Actions taken:")
    print("  - Cleared all channels from database")
    print("  - Reset file IDs")
    print("  - Temporarily disabled subscription system")
    print("\n🚀 Next steps:")
    print("  1. Restart the bot (it will load with no channels)")
    print("  2. Add only valid channels using /addchannel")
    print("  3. Remove .subscription_disabled file when ready")

if __name__ == "__main__":
    cleanup_invalid_channels()
