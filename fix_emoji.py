#!/usr/bin/env python3
# Fix broken emojis in app.py

# Read the file
with open('app.py', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Fix broken emojis
fixes = [
    ("'text': '�️ Spam Himoya'", "'text': '🛡️ Spam Himoya'"),
    ("'text': '� Tizim Sozlamalari'", "'text': '⚙️ Tizim Sozlamalari'"), 
    ("'text': '� Ma\\'lumotlar'", "'text': '💾 Ma\\'lumotlar'")
]

count = 0
for old, new in fixes:
    if old in content:
        content = content.replace(old, new)
        count += 1
        print(f"Fixed: {old} -> {new}")

# Write back the file
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Total fixes applied: {count}")
print("Admin panel buttons fixed!")
