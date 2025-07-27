#!/usr/bin/env python3
# Test channels generator for multi-channel testing

import json
from datetime import datetime

# Test channels data
test_channels = {
    '-1001234567890': {
        'channel_id': '-1001234567890',
        'name': 'Test Channel 1',
        'username': '@test_channel1',
        'url': 'https://t.me/test_channel1',
        'add_date': datetime.now().isoformat(),
        'active': True,
        'added_by': 5542016161
    },
    '-1001234567891': {
        'channel_id': '-1001234567891',
        'name': 'Test Channel 2', 
        'username': '@test_channel2',
        'url': 'https://t.me/test_channel2',
        'add_date': datetime.now().isoformat(),
        'active': True,
        'added_by': 5542016161
    }
}

# Save to channels.json for testing
with open('channels.json', 'w', encoding='utf-8') as f:
    json.dump(test_channels, f, ensure_ascii=False, indent=2)

print(f'✅ {len(test_channels)} ta test kanal yaratildi!')
print('📋 Test kanallar:')
for cid, cdata in test_channels.items():
    print(f'  • {cdata["name"]} (ID: {cid})')
