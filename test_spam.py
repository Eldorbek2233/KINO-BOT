#!/usr/bin/env python3
# Test spam protection and normal messages

import sys
sys.path.append('.')

# Import required functions from app.py
exec(open('app.py').read().split('if __name__')[0])

# Test messages
test_messages = [
    {
        'text': 'Claim free Ethereum www.freeether.net - Click, Connect, Collect!',
        'from': {'id': 12345},
        'expected': True,
        'type': 'Crypto Spam'
    },
    {
        'text': 'Salom! Kino kodi 123 kerak',
        'from': {'id': 12346}, 
        'expected': False,
        'type': 'Normal Request'
    },
    {
        'text': 'HURRY UP!!! FREE CRYPTO FOR EVERYONE!!! VISIT bit.ly/free NOW!!!',
        'from': {'id': 12347},
        'expected': True,
        'type': 'Multi-pattern Spam'
    },
    {
        'text': '/start',
        'from': {'id': 12348},
        'expected': False,
        'type': 'Bot Command'
    }
]

print("🧪 TESTING SPAM PROTECTION")
print("=" * 40)

for i, test in enumerate(test_messages, 1):
    result = is_spam_message(test)
    status = "PASS" if result == test['expected'] else "FAIL"
    detection = "SPAM" if result else "CLEAN"
    
    print(f"{i}. {test['type']}: {status}")
    print(f"   Message: {test['text'][:50]}...")
    print(f"   Expected: {'SPAM' if test['expected'] else 'CLEAN'}, Got: {detection}")
    print()

print("🎯 Test complete!")
