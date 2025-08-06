import os
from dotenv import load_dotenv

# .env faylidan o'zgaruvchilarni yuklab olish
load_dotenv()

# Bot token - faqat environment variable dan
TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TOKEN")

# Token mavjudligini tekshirish
if not TOKEN or TOKEN == "None" or len(TOKEN) < 30:
    raise ValueError("BOT_TOKEN environment variable not found or invalid. Please set BOT_TOKEN in your environment.")

# O'zgaruvchilarni olish
ADMIN_ID = int(os.getenv("ADMIN_ID", "5542016161"))  # Fallback admin ID

# Majburiy aʼzo bo'lish uchun kanal IDlari
REQUIRED_CHANNELS = [
    "@tarjima_kino_movie"  # Kanal username yoki ID
]

# Debug logging (local development uchun)
if __name__ == "__main__":
    print(f"DEBUG - BOT_TOKEN env: {os.getenv('BOT_TOKEN', 'NOT SET')}")
    print(f"DEBUG - TOKEN env: {os.getenv('TOKEN', 'NOT SET')}")
    print(f"DEBUG - Final TOKEN length: {len(TOKEN) if TOKEN else 0}")
    print(f"DEBUG - Final TOKEN: {TOKEN[:15]}..." if TOKEN else "None")
    print(f"DEBUG - ADMIN_ID: {ADMIN_ID}")
