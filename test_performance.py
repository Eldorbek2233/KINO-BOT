#!/usr/bin/env python3
# Test subscription performance

import json
import time
import sys
import os

# Set up logging
import logging
logging.basicConfig(level=logging.INFO)

# Import app functions
sys.path.append('.')
try:
    from app import channels_db, check_all_subscriptions, subscription_cache, ADMIN_ID
    
    print('🔍 Testing multi-channel subscription system...')
    print(f'📊 Loaded {len(channels_db)} channels from database')
    
    if len(channels_db) == 0:
        print('⚠️ No channels loaded, loading from file...')
        try:
            with open('channels.json', 'r', encoding='utf-8') as f:
                channels_data = json.load(f)
                channels_db.update(channels_data)
                print(f'✅ Loaded {len(channels_db)} channels from channels.json')
        except Exception as e:
            print(f'❌ Failed to load channels: {e}')
    
    # Test with multiple channels
    if len(channels_db) > 0:
        print('\n🚀 Starting performance test...')
        
        # Test subscription check for admin (should pass)
        start_time = time.time()
        result = check_all_subscriptions(ADMIN_ID)
        end_time = time.time()
        
        print(f'⚡ Subscription check completed in {end_time - start_time:.2f} seconds')
        print(f'✅ Admin subscription result: {result}')
        
        # Test cache
        print(f'💾 Cache contains: {len(subscription_cache)} entries')
        if ADMIN_ID in subscription_cache:
            cache_entry = subscription_cache[ADMIN_ID]
            expires_in = cache_entry["expires"] - time.time()
            print(f'🗃 Cache entry: subscribed={cache_entry["is_subscribed"]}, expires in {expires_in:.1f}s')
        
        # Test second call (should use cache)
        print('\n🔄 Testing cached call...')
        start_time = time.time()
        result2 = check_all_subscriptions(ADMIN_ID)
        end_time = time.time()
        
        print(f'⚡ Cached check completed in {end_time - start_time:.3f} seconds')
        print(f'✅ Cached result: {result2}')
        
        print('\n🎯 Multi-channel test completed successfully!')
        print(f'📈 Performance improvement: Cache is {"WORKING" if end_time - start_time < 0.1 else "NOT WORKING"}')
    else:
        print('❌ No channels to test with')
        
except ImportError as e:
    print(f'❌ Import error: {e}')
except Exception as e:
    print(f'❌ Test error: {e}')
