import os
from dotenv import load_dotenv

# .env faylidan o'zgaruvchilarni yuklab olish
load_dotenv()

# O'zgaruvchilarni olish
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
# Majburiy aʼzo bo‘lish uchun kanal IDlari
REQUIRED_CHANNELS = [
    "@tarjima_kino_movie"  # Kanal username yoki ID
]