import os
from dotenv import load_dotenv

# .env faylidan o'zgaruvchilarni yuklab olish
load_dotenv()

# Bot token - environment variable yoki hardcoded fallback
TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TOKEN") or "8177519032:AAED4FgPoFQiQhqM_lvrK1iV8hL9u4SnkDk"

# Agar TOKEN hali ham None bo'lsa, to'g'ridan-to'g'ri o'rnataylik
if not TOKEN or TOKEN == "None" or len(TOKEN) < 30:
    TOKEN = "8177519032:AAED4FgPoFQiQhqM_lvrK1iV8hL9u4SnkDk"

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
