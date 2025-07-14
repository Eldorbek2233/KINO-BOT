# No need for telegram_patch with v20.8
# The newer versions of python-telegram-bot don't use imghdr

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ConversationHandler, ContextTypes
import json
import os
import time
import asyncio
import re
import logging
from config import ADMIN_ID, REQUIRED_CHANNELS

logger = logging.getLogger(__name__)

REKLAMA_WAIT = 1
# Kino joylash uchun statuslar
WAITING_FOR_CODE = 2
WAITING_FOR_VIDEO = 3
# Kanal qo'shish uchun statuslar
CHANNEL_MENU = 4
WAITING_FOR_CHANNEL = 5

# Boshlang'ich handler: /reklama bosilganda
async def send_advertisement(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("Siz admin emassiz.")
        return ConversationHandler.END
    await update.message.reply_text("Reklama matnini yoki rasmini yuboring.")
    return REKLAMA_WAIT

# Reklama matni yoki rasmini qabul qilish handleri
async def handle_ad_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("Siz admin emassiz.")
        if 'waiting_for_reklama' in context.user_data:
            context.user_data.pop('waiting_for_reklama')
        return ConversationHandler.END
    
    photo = None
    text = None
    
    if update.message and update.message.photo:
        photo = update.message.photo[-1].file_id
        text = update.message.caption if update.message.caption else ""
    elif update.message and update.message.text:
        text = update.message.text
    else:
        await update.message.reply_text("Xatolik: Reklama matni yoki rasmi topilmadi.")
        if 'waiting_for_reklama' in context.user_data:
            context.user_data.pop('waiting_for_reklama')
        return ConversationHandler.END
        
    users = load_users()
    print(f"DEBUG: Reklama foydalanuvchilar: {users}")  # Debug print
    
    if not users:
        await update.message.reply_text("Xatolik: Foydalanuvchilar ro'yxati bo'sh!")
        if 'waiting_for_reklama' in context.user_data:
            context.user_data.pop('waiting_for_reklama')
        return ConversationHandler.END
    
    await update.message.reply_text("⏳ Reklama yuborilmoqda... Kutib turing.")
    
    count = 0
    for uid in users:
        try:
            if photo:
                await context.bot.send_photo(chat_id=uid, photo=photo, caption=text)
            else:
                await context.bot.send_message(chat_id=uid, text=text)
            count += 1
            # Har 30 xabardan keyin kuting (Telegram cheklovlari uchun)
            if count % 30 == 0:
                await asyncio.sleep(1)
        except Exception as e:
            print(f"DEBUG: Reklama xatolik {uid}: {e}")  # Debug print
            continue
            
    await update.message.reply_text(f"✅ Reklama {count} foydalanuvchiga yuborildi.")
    if 'waiting_for_reklama' in context.user_data:
        context.user_data.pop('waiting_for_reklama')
    return ConversationHandler.END

# Bot ishga tushgan vaqtni global o'zgaruvchida saqlaymiz
if not hasattr(globals(), 'BOT_START_TIME'):
    BOT_START_TIME = time.time()
    
# Aktiv foydalanuvchilar vaqtini saqlash uchun dict
if not hasattr(globals(), 'ACTIVE_USERS'):
    ACTIVE_USERS = {}

# Foydalanuvchining so'nggi aktivligini saqlash
def update_user_activity(user_id):
    global ACTIVE_USERS
    ACTIVE_USERS[user_id] = time.time()

# Aktiv foydalanuvchilar sonini hisoblash (so'nggi 24 soat ichida)
def get_active_users_count():
    global ACTIVE_USERS
    current_time = time.time()
    active_count = 0
    for uid, last_active in ACTIVE_USERS.items():
        # 24 soat = 86400 sekund
        if current_time - last_active < 86400:
            active_count += 1
    return active_count

def format_uptime(seconds):
    mins, sec = divmod(int(seconds), 60)
    hour, mins = divmod(mins, 60)
    day, hour = divmod(hour, 24)
    year, day = divmod(day, 365)
    month, day = divmod(day, 30)
    return f"{year} yil, {month} oy, {day} kun, {hour} soat, {mins} daqiqa, {sec} sekund"

async def bot_stat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("⛔️ Bu funksiyadan faqat adminlar foydalana oladi.")
        return
        
    users = load_users()
    file_ids = load_file_ids()
    video_count = len(file_ids)
    uptime = format_uptime(time.time() - BOT_START_TIME)
    active_users_count = get_active_users_count()
    await update.message.reply_text(
        "\U0001F4CA Bot statistikasi:\n"
        f"\U0001F465 Barcha userlar: {len(users)} ta\n"
        f"👥 Aktiv foydalanuvchilar (24 soat): {active_users_count} ta\n"
        f"\U0001F3A5 Barcha kinolar: {video_count} ta\n"
        f"⏰ Uptime: {uptime}"
    )

FILE_DB = "file_ids.json"
USERS_DB = "users.json"

# Fayl ID'larni yuklab olish
def load_file_ids():
    if os.path.exists(FILE_DB):
        with open(FILE_DB, "r") as f:
            return json.load(f)
    return {}

# Fayl ID'ni saqlash
def save_file_id(code, file_id):
    data = load_file_ids()
    data[code] = file_id
    with open(FILE_DB, "w") as f:
        json.dump(data, f, indent=4)

def load_users():
    if os.path.exists(USERS_DB):
        with open(USERS_DB, "r") as f:
            return list(json.load(f))  # Always return a list
    return []

def save_user(user_id):
    users = load_users()
    if user_id not in users:
        users.append(user_id)
    with open(USERS_DB, "w") as f:
        json.dump(list(users), f, indent=4)

# Kanal boshqarish uchun funksiyalar
def save_channels(channels):
    """Kanallarni config.py faylida yangilash"""
    with open("config.py", "r", encoding="utf-8") as f:
        config_content = f.read()
    
    # REQUIRED_CHANNELS qismini yangilash
    channels_str = "[\n"
    for channel in channels:
        channels_str += f'    "{channel}",\n'
    channels_str += "]"
    
    # REQUIRED_CHANNELS qismini topib, yangilash
    import re
    new_content = re.sub(
        r"REQUIRED_CHANNELS\s*=\s*\[[\s\S]*?\]",
        f"REQUIRED_CHANNELS = {channels_str}",
        config_content
    )
    
    with open("config.py", "w", encoding="utf-8") as f:
        f.write(new_content)
    
    # Global o'zgaruvchini ham yangilash
    global REQUIRED_CHANNELS
    REQUIRED_CHANNELS = channels

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    save_user(user_id)
    update_user_activity(user_id)
    
    # Debug: user_id va admin_id ni ko'rsatish
    print(f"User ID: {user_id}, Admin ID: {ADMIN_ID}, Type user: {type(user_id)}, Type admin: {type(ADMIN_ID)}")
    
    # Sodda javob - membership check o'chirilgan
    try:
        if user_id == ADMIN_ID:
            keyboard = [
                ["📊 Statistika"],
                ["👥 Users", "🔐 Menu", "📣 Reklama"],
                ["🎬 Kino joylash", "📢 Kanallar"]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="🔐 Admin menyusi:",
                reply_markup=reply_markup
            )
        else:
            # Oddiy foydalanuvchilar uchun tugmalar
            keyboard = [
                ["🔍 Kino qidirish"],
                ["ℹ️ Yordam"]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="🎬 Salom! Kino kodini yuboring yoki quyidagi tugmalardan foydalaning:",
                reply_markup=reply_markup
            )
        
        logger.info(f"✅ Start command processed for user {user_id}")
        
    except Exception as e:
        logger.error(f"❌ Start command error: {e}")
        try:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="❌ Xatolik yuz berdi. Qaytadan urinib ko'ring."
            )
        except Exception as send_error:
            logger.error(f"❌ Error sending error message: {send_error}")

# Statistika knopkasi uchun handler
async def stat_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    users = load_users()
    file_ids = load_file_ids()
    video_count = len(file_ids)
    active_users_count = get_active_users_count()
    await query.edit_message_text(
        f"📊 Bot statistikasi:\n"
        f"👥 Foydalanuvchilar: {len(users)}\n"
        f"👤 Aktiv foydalanuvchilar (24 soat): {active_users_count} ta\n"
        f"🎬 Kino kodlari: {video_count}"
    )


# Kod kelganda – file_id bo'yicha yuboradi
async def handle_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    save_user(user_id)
    update_user_activity(user_id)
    
    # Agar admin reklama kontentini yuborayotgan bo'lsa
    if user_id == ADMIN_ID and 'waiting_for_reklama' in context.user_data and context.user_data['waiting_for_reklama']:
        # Reklama kontenti kiritilganda uni qayta ishlash
        return await handle_ad_content(update, context)
    
    if not await check_membership(user_id, context):
        await send_subscription_message(update, context)
        return
    
    # Text yoki photo kelishi mumkin
    if update.message.text:
        code = update.message.text.strip().lower()
    else:
        # Agar rasm kelsa va kod bo'lmasa
        return
    # Admin uchun reply keyboard tugmasi
    if user_id == ADMIN_ID and (code.lower() == "reklama" or code.lower() == "📣 reklama"):
        # Admin menyudan "Reklama" tugmasi bosilganda
        # Keyboard orqali "Reklama" bosilganda to'g'ridan-to'g'ri reklama jo'natish
        await update.message.reply_text("Reklama matnini yoki rasmini yuboring.")
        context.user_data['waiting_for_reklama'] = True
        return
    
    # Admin knopkalari uchun qo'shimcha tekshiruvlar
    if user_id == ADMIN_ID:
        if code.lower() == "users" or code.lower() == "👥 users":
            await users_count(update, context)
            return
        elif code == "📊 statistika":
            await bot_stat(update, context)
            return
        elif code.lower() == "menu" or code.lower() == "🔐 menu":
            await admin_menu(update, context)
            return
        elif code.lower() == "kino joylash" or code.lower() == "🎬 kino joylash":
            await add_movie_handler(update, context)
            return
        elif code.lower() == "kanallar" or code.lower() == "📢 kanallar":
            await manage_channels(update, context)
            return
    
    # Oddiy foydalanuvchilar knopkalari
    if code.lower() == "kino qidirish" or code.lower() == "🔍 kino qidirish":
        await search_movie(update, context)
        return
    elif code.lower() == "yordam" or code.lower() == "ℹ️ yordam":
        await help_command(update, context)
        return
    
    # Statistika faqat admin uchun
    if code == "📊 statistika" and user_id == ADMIN_ID:
        users = load_users()
        file_ids = load_file_ids()
        video_count = len(file_ids)
        uptime = format_uptime(time.time() - BOT_START_TIME)
        await update.message.reply_text(
            "\U0001F4CA Bot statistikasi:\n"
            f"\U0001F465 Barcha userlar: {len(users)} ta\n"
            f"\U0001F3A5 Barcha kinolar: {video_count} ta\n"
            f"⏰ Uptime: {uptime}"
        )
        return
    elif code == "📊 statistika" and user_id != ADMIN_ID:
        await update.message.reply_text("⛔️ Bu funksiyadan faqat adminlar foydalana oladi.")
        return
    file_ids = load_file_ids()
    if code not in file_ids:
        await update.message.reply_text("❌ Bunday kod mavjud emas.")
        return
    try:
        await update.message.reply_video(video=file_ids[code], caption=f"🎬 Kod: {code}")
    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik: {str(e)}")
        
# /users komandasi – foydalanuvchilar sonini ko'rsatadi
async def users_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = load_users()
    await update.message.reply_text(f"👥 Bot foydalanuvchilari soni: {len(users)}")

# Admin kanalga video tashlaganda – file_id ni avtomatik saqlaydi
async def check_membership(user_id, context):
    """Temporarily disable membership check for testing"""
    # Vaqtincha barcha foydalanuvchilarni ruxsat berish
    return True

async def send_subscription_message(update: Update, context: ContextTypes.DEFAULT_TYPE = None):
    text = "👋 Botdan foydalanish uchun quyidagi kanallarga aʼzo bo'ling:"
    keyboard = []
    for channel in REQUIRED_CHANNELS:
        # Kanal username yoki ID dan link yasash
        if channel.startswith("@"):
            url = f"https://t.me/{channel[1:]}"
        elif channel.startswith("https://t.me/"):
            url = channel
        else:
            url = channel
        keyboard.append([InlineKeyboardButton(f"Aʼzo bo'lish ➡️", url=url)])
    # Tasdiqlash knopkasi
    keyboard.append([InlineKeyboardButton("✅ Tasdiqlash", callback_data="check_membership")])
    keyboard_markup = InlineKeyboardMarkup(keyboard)
    text += "\nAʼzo bo'lgach, pastdagi 'Tasdiqlash' tugmasini bosing."
    await update.message.reply_text(text, reply_markup=keyboard_markup)

# Tasdiqlash knopkasi uchun handler
async def confirm_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    if await check_membership(user_id, context):
        await query.edit_message_text(
            "✅ Tabriklaymiz! Endi botdan foydalanishingiz mumkin.\n\n" 
            "🎬 Kino kodini yuboring."
        )
    else:
        # Kanal links and confirmation button again
        from config import REQUIRED_CHANNELS
        text = "❌ Hali hamma kanallarga aʼzo bo'lmagansiz. Iltimos, quyidagi kanallarga aʼzo bo'ling va yana tasdiqlang."
        keyboard = []
        for channel in REQUIRED_CHANNELS:
            if channel.startswith("@"):
                url = f"https://t.me/{channel[1:]}"
            elif channel.startswith("https://t.me/"):
                url = channel
            else:
                url = channel
            keyboard.append([InlineKeyboardButton(f"Aʼzo bo'lish ➡️", url=url)])
        keyboard.append([InlineKeyboardButton("✅ Tasdiqlash", callback_data="check_membership")])
        keyboard_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text + "\nAʼzo bo'lgach, pastdagi 'Tasdiqlash' tugmasini bosing.", reply_markup=keyboard_markup)
        
async def handle_channel_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.channel_post
    if not message:
        return
    caption = message.caption
    if not caption:
        return
    code = caption.strip().lower()
    if not hasattr(message, "video") or not message.video:
        return
    file_id = message.video.file_id
    save_file_id(code, file_id)
    print(f"✅ Saqlandi: {code} → {file_id}")

async def admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from config import ADMIN_ID
    user_id = update.effective_user.id
    if user_id == ADMIN_ID:
        # Slashsiz va emoji bilan chiroyli tugmalar
        keyboard = [
            [InlineKeyboardButton("📊 Statistika", callback_data="show_stat")],
            [InlineKeyboardButton("📣 Reklama", callback_data="reklama_inline")],
            [InlineKeyboardButton("🎬 Kino joylash", callback_data="add_movie")],
            [InlineKeyboardButton("📢 Majburiy kanallar", callback_data="manage_channels")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("🔐 Admin menyusi:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("❌ Siz admin emassiz.")
        
# Inline reklama tugmasi uchun handler
async def reklama_inline_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    if user_id != ADMIN_ID:
        await query.edit_message_text("Siz admin emassiz.")
        return ConversationHandler.END
    await query.edit_message_text("Reklama matnini yoki rasmini yuboring.")
    # Reklama kutish holati sozlaymiz
    context.user_data['waiting_for_reklama'] = True
    return REKLAMA_WAIT

async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the conversation and return to the main menu."""
    await update.message.reply_text("Amal bekor qilindi.")
    return ConversationHandler.END

# Kino joylash uchun funksiyalar
async def add_movie_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kino joylash knopkasi bosilganda ishlaydi"""
    query = update.callback_query
    if query:  # Agar inline button orqali kelgan bo'lsa
        user_id = query.from_user.id
        await query.answer()
        if user_id != ADMIN_ID:
            await query.edit_message_text("Siz admin emassiz.")
            return ConversationHandler.END
        await query.edit_message_text("Kino kodini kiriting (masalan: 123):")
        return WAITING_FOR_CODE
    else:  # Agar oddiy keyboard button orqali kelgan bo'lsa
        user_id = update.effective_user.id
        if user_id != ADMIN_ID:
            await update.message.reply_text("Siz admin emassiz.")
            return ConversationHandler.END
        await update.message.reply_text("Kino kodini kiriting (masalan: 123):", reply_markup=ReplyKeyboardRemove())
        return WAITING_FOR_CODE

async def get_movie_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kino kodi kiritilganda ishga tushadi"""
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("Siz admin emassiz.")
        return ConversationHandler.END
        
    code = update.message.text.strip().lower()
    context.user_data['movie_code'] = code
    
    # Kod mavjudligini tekshirish
    file_ids = load_file_ids()
    if code in file_ids:
        await update.message.reply_text(f"❗️ Bu kod ({code}) allaqachon mavjud.\n\nBoshqa kod kiriting yoki bekor qilish uchun /cancel bosing.")
        return WAITING_FOR_CODE
        
    await update.message.reply_text(f"Endi {code} kodi uchun video yuboring:")
    return WAITING_FOR_VIDEO
    
async def get_movie_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Video yuborilganda ishga tushadi"""
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("Siz admin emassiz.")
        return ConversationHandler.END
        
    if not update.message.video:
        await update.message.reply_text("❌ Video yuborilmadi. Iltimos, video yuboring yoki bekor qilish uchun /cancel bosing.")
        return WAITING_FOR_VIDEO
        
    code = context.user_data.get('movie_code')
    if not code:
        await update.message.reply_text("❌ Xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")
        return ConversationHandler.END
        
    file_id = update.message.video.file_id
    save_file_id(code, file_id)
    
    # Admin klaviaturasini qayta ko'rsatish
    keyboard = [
        ["📊 Statistika"],
        ["👥 Users", "🔐 Menu", "📣 Reklama"],
        ["🎬 Kino joylash"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(f"✅ Kino muvaffaqiyatli saqlandi!\n\nKod: {code}", reply_markup=reply_markup)
    return ConversationHandler.END

# Kanal boshqarish funksiyalari
async def manage_channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kanal boshqarish menyusi"""
    query = update.callback_query
    user_id = None
    
    if query:  # Inline button orqali kelgan
        user_id = query.from_user.id
        await query.answer()
        if user_id != ADMIN_ID:
            await query.edit_message_text("Siz admin emassiz.")
            return ConversationHandler.END
    else:  # Oddiy keyboard button orqali kelgan
        user_id = update.effective_user.id
        if user_id != ADMIN_ID:
            await update.message.reply_text("Siz admin emassiz.")
            return ConversationHandler.END
    
    # Mavjud kanallar ro'yxatini chiqarish
    channels_text = "📢 Majburiy a'zolik kanallari:\n\n"
    
    if not REQUIRED_CHANNELS:
        channels_text += "🔴 Kanallar yo'q. Yangi kanal qo'shing."
    else:
        for i, channel in enumerate(REQUIRED_CHANNELS, 1):
            channels_text += f"{i}. {channel}\n"
    
    # Kanal qo'shish/o'chirish tugmalari
    keyboard = [
        [InlineKeyboardButton("➕ Kanal qo'shish", callback_data="add_channel")],
        [InlineKeyboardButton("➖ Kanal o'chirish", callback_data="remove_channel")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if query:
        await query.edit_message_text(channels_text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(channels_text, reply_markup=reply_markup)
    
    return CHANNEL_MENU

async def add_channel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kanal qo'shish"""
    query = update.callback_query
    await query.answer()
    
    if query.from_user.id != ADMIN_ID:
        await query.edit_message_text("Siz admin emassiz.")
        return ConversationHandler.END
    
    await query.edit_message_text("Qo'shiladigan kanal usernameni yoki ID ni kiriting:\n\n"
                                 "Masalan: @example_channel yoki -1001234567890\n\n"
                                 "Bekor qilish uchun /cancel bosing.")
    return WAITING_FOR_CHANNEL

async def remove_channel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kanal o'chirish"""
    query = update.callback_query
    await query.answer()
    
    if query.from_user.id != ADMIN_ID:
        await query.edit_message_text("Siz admin emassiz.")
        return ConversationHandler.END
    
    if not REQUIRED_CHANNELS:
        await query.edit_message_text("O'chirish uchun kanallar yo'q. Avval kanallarni qo'shing.")
        keyboard = [[InlineKeyboardButton("🔙 Orqaga", callback_data="manage_channels")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_reply_markup(reply_markup=reply_markup)
        return CHANNEL_MENU
    
    # Kanallar ro'yxati
    keyboard = []
    for i, channel in enumerate(REQUIRED_CHANNELS):
        keyboard.append([InlineKeyboardButton(f"{i+1}. {channel}", callback_data=f"delete_channel_{i}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="manage_channels")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("O'chiriladigan kanalni tanlang:", reply_markup=reply_markup)
    return CHANNEL_MENU

async def process_new_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yangi kanal qo'shish"""
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("Siz admin emassiz.")
        return ConversationHandler.END
    
    new_channel = update.message.text.strip()
    
    if new_channel.startswith("/"):
        await update.message.reply_text("Kanal qo'shish bekor qilindi.")
        return ConversationHandler.END
    
    # @ belgisi qo'yilganligini tekshirish
    if not new_channel.startswith("@") and not new_channel.startswith("-100"):
        new_channel = "@" + new_channel
    
    # Kanalni ro'yxatga qo'shish
    global REQUIRED_CHANNELS
    if new_channel in REQUIRED_CHANNELS:
        # Admin klaviaturasini qayta ko'rsatish
        keyboard = [
            ["📊 Statistika"],
            ["👥 Users", "🔐 Menu", "📣 Reklama"],
            ["🎬 Kino joylash", "📢 Kanallar"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(f"❗️ {new_channel} allaqachon ro'yxatda mavjud!", reply_markup=reply_markup)
    else:
        channels = list(REQUIRED_CHANNELS)
        channels.append(new_channel)
        save_channels(channels)
        
        # Admin klaviaturasini qayta ko'rsatish
        keyboard = [
            ["📊 Statistika"],
            ["👥 Users", "🔐 Menu", "📣 Reklama"],
            ["🎬 Kino joylash", "📢 Kanallar"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(f"✅ Kanal {new_channel} muvaffaqiyatli qo'shildi!", reply_markup=reply_markup)
    
    # Inline knopkalarni ko'rsatish
    inline_keyboard = [
        [InlineKeyboardButton("📢 Kanallarni boshqarish", callback_data="manage_channels")]
    ]
    inline_markup = InlineKeyboardMarkup(inline_keyboard)
    await update.message.reply_text("🔐 Boshqa amal tanlash uchun tugmalardan foydalaning:", reply_markup=inline_markup)
    return ConversationHandler.END

async def delete_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kanalni o'chirish"""
    query = update.callback_query
    await query.answer()
    
    if query.from_user.id != ADMIN_ID:
        await query.edit_message_text("Siz admin emassiz.")
        return ConversationHandler.END
    
    # Callback data formatidan indeksni olish (delete_channel_X)
    data = query.data
    index = int(data.split("_")[-1])
    
    if 0 <= index < len(REQUIRED_CHANNELS):
        channel = REQUIRED_CHANNELS[index]
        channels = list(REQUIRED_CHANNELS)
        channels.pop(index)
        save_channels(channels)
        
        await query.edit_message_text(f"✅ Kanal {channel} muvaffaqiyatli o'chirildi!")
    else:
        await query.edit_message_text("❌ Xatolik: kanal topilmadi.")
    
    # Kanal boshqarish menyusini qayta ko'rsatish
    keyboard = [[InlineKeyboardButton("🔙 Orqaga", callback_data="manage_channels")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_reply_markup(reply_markup=reply_markup)
    return CHANNEL_MENU

async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Asosiy menyuga qaytish"""
    query = update.callback_query
    await query.answer()
    
    # Admin menyusiga qaytish
    keyboard = [
        [InlineKeyboardButton("📊 Statistika", callback_data="show_stat")],
        [InlineKeyboardButton("📣 Reklama", callback_data="reklama_inline")],
        [InlineKeyboardButton("🎬 Kino joylash", callback_data="add_movie")],
        [InlineKeyboardButton("📢 Majburiy kanallar", callback_data="manage_channels")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("🔐 Admin menyusi:", reply_markup=reply_markup)
    return ConversationHandler.END

# Foydalanuvchilar uchun kino qidirish funksiyasi
async def search_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kino qidirish funksiyasi"""
    user_id = update.effective_user.id
    save_user(user_id)
    update_user_activity(user_id)
    
    # A'zolikni tekshirish
    if not await check_membership(user_id, context):
        await send_subscription_message(update, context)
        return
    
    await update.message.reply_text("🔍 Qidirmoqchi bo'lgan kino kodini yozing:")
    return

# Yordam funksiyasi
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yordam ko'rsatish funksiyasi"""
    user_id = update.effective_user.id
    save_user(user_id)
    update_user_activity(user_id)
    
    # A'zolikni tekshirish
    if not await check_membership(user_id, context):
        await send_subscription_message(update, context)
        return
    
    help_text = (
        "🎬 *Kino bot qo'llanmasi*\n\n"
        "• Kino kodini yozib, kinoni tomosha qiling\n"
        "• '🔍 Kino qidirish' tugmasini bosib, kerakli kinoni qidiring\n\n"
        "Botdan foydalanish uchun majburiy kanallarga a'zo bo'ling!"
    )
    
    await update.message.reply_text(help_text, parse_mode="Markdown")
    return

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Global error handler - barcha xatoliklarni log qilish"""
    import logging
    import traceback
    
    logger = logging.getLogger(__name__)
    
    # Error ma'lumotlarini log qilish
    logger.error(f"Update {update.update_id if update else 'None'} caused error: {context.error}")
    
    # Traceback ni log qilish
    if context.error:
        logger.error("".join(traceback.format_exception(type(context.error), context.error, context.error.__traceback__)))
    
    # Foydalanuvchiga xabar berish (agar update mavjud bo'lsa)
    if update and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "⚠️ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring."
            )
        except Exception as e:
            logger.error(f"Error handler o'zida xatolik: {e}")

def add_handlers(app):
    """Barcha handlerlarni application ga qo'shish"""
    from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, filters
    
    # Test handler - darhol javob beradi
    async def test_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="✅ Bot ishlayapti! Test muvaffaqiyatli."
            )
            logger.info(f"✅ Test command processed for user {update.effective_user.id}")
        except Exception as e:
            logger.error(f"❌ Test command error: {e}")
    
    # Asosiy handlerlar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test_handler))
    app.add_handler(CommandHandler("help", help_command))
    
    # Matn xabarlar uchun handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_code))
    
    # Error handler
    app.add_error_handler(error_handler)
    
    return app
