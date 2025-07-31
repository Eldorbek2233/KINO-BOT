#!/usr/bin/env python3
# Clear channels and reset bot to normal state

import json
import os

# Clear channels.json
with open('channels.json', 'w', encoding='utf-8') as f:
    json.dump({}, f)

print("✅ Channels cleared - bot will work normally now")
print("✅ Users can access bot without subscription requirements")
print("✅ Admin can add channels later if needed via /admin panel")
