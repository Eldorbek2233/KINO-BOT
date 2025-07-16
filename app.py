#!/usr/bin/env python3
"""
Ultimate Professional Kino Bot - Completely Fixed Version
"""

import os
import sys
import logging
import json
import time
import requests
from flask import Flask, request, jsonify

# Configure detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('bot.log')
    ]
)

logger = logging.getLogger(__name__)

# Bot configuration
TOKEN = "8177519032:AAED4FgPoFQiQhqM_lvrK1iV8hL9u4SnkDk"
ADMIN_ID = 5542016161

# Flask app
app = Flask(__name__)

# Global storage
users_db = {}
movies_db = {}
upload_sessions = {}
broadcast_data = {}

def load_database():
    """Load all data from JSON files"""
    global users_db, movies_db
    
    # Load users
    try:
        with open('users.json', 'r', encoding='utf-8') as f:
            users_db = json.load(f)
        logger.info(f"✅ Loaded {len(users_db)} users from database")
    except FileNotFoundError:
        users_db = {}
        logger.info("� Creating new users database")
    except Exception as e:
        logger.error(f"❌ Users database error: {e}")
        users_db = {}
    
    # Load movies
    try:
        with open('file_ids.json', 'r', encoding='utf-8') as f:
            movies_db = json.load(f)
        logger.info(f"✅ Loaded {len(movies_db)} movies from database")
        logger.info(f"🎬 Available movie codes: {list(movies_db.keys())}")
    except FileNotFoundError:
        movies_db = {}
        logger.info("� Creating new movies database")
    except Exception as e:
        logger.error(f"❌ Movies database error: {e}")
        movies_db = {}

def save_database():
    """Save all data to JSON files"""
    # Save users
    try:
        with open('users.json', 'w', encoding='utf-8') as f:
            json.dump(users_db, f, indent=2, ensure_ascii=False)
        logger.info(f"💾 Saved {len(users_db)} users to database")
    except Exception as e:
        logger.error(f"❌ Save users error: {e}")
    
    # Save movies
    try:
        with open('file_ids.json', 'w', encoding='utf-8') as f:
            json.dump(movies_db, f, indent=2, ensure_ascii=False)
        logger.info(f"💾 Saved {len(movies_db)} movies to database")
    except Exception as e:
        logger.error(f"❌ Save movies error: {e}")

def save_user(user_id, username=None, first_name=None):
    """Save user information"""
    user_id = str(user_id)
    users_db[user_id] = {
        'username': username or 'Unknown',
        'first_name': first_name or 'Unknown',
        'last_seen': int(time.time()),
        'join_date': users_db.get(user_id, {}).get('join_date', int(time.time()))
    }
    save_database()
    logger.info(f"👤 User saved: {user_id} ({first_name})")

def telegram_request(method, data=None, files=None):
    """Make request to Telegram API"""
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/{method}"
        
        if files:
            response = requests.post(url, data=data, files=files, timeout=30)
        else:
            response = requests.post(url, json=data, timeout=10)
            
        result = response.json()
        
        if result.get('ok'):
            return result.get('result')
        else:
            logger.error(f"❌ Telegram API error in {method}: {result}")
            return None
            
    except Exception as e:
        logger.error(f"❌ Request error in {method}: {e}")
        return None

def send_message(chat_id, text, keyboard=None, parse_mode='HTML'):
    """Send message with optional keyboard"""
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': parse_mode
    }
    
    if keyboard:
        data['reply_markup'] = keyboard
    
    result = telegram_request('sendMessage', data)
    if result:
        logger.info(f"✅ Message sent to {chat_id}")
        return True
    else:
        logger.error(f"❌ Failed to send message to {chat_id}")
        return False

def send_video(chat_id, file_id, caption="", keyboard=None):
    """Send video file"""
    data = {
        'chat_id': chat_id,
        'video': file_id,
        'caption': caption,
        'parse_mode': 'HTML'
    }
    
    if keyboard:
        data['reply_markup'] = keyboard
    
    result = telegram_request('sendVideo', data)
    if result:
        logger.info(f"✅ Video sent to {chat_id}")
        return True
    else:
        logger.error(f"❌ Failed to send video to {chat_id}")
        return False

def send_photo(chat_id, photo_id, caption="", keyboard=None):
    """Send photo"""
    data = {
        'chat_id': chat_id,
        'photo': photo_id,
        'caption': caption,
        'parse_mode': 'HTML'
    }
    
    if keyboard:
        data['reply_markup'] = keyboard
    
    result = telegram_request('sendPhoto', data)
    if result:
        logger.info(f"✅ Photo sent to {chat_id}")
        return True
    else:
        logger.error(f"❌ Failed to send photo to {chat_id}")
        return False

def answer_callback(callback_id, text=""):
    """Answer callback query"""
    data = {
        'callback_query_id': callback_id,
        'text': text
    }
    
    result = telegram_request('answerCallbackQuery', data)
    if result:
        logger.info(f"✅ Callback answered: {callback_id}")
        return True
    else:
        logger.error(f"❌ Failed to answer callback: {callback_id}")
        return False

@app.route('/')
def home():
    """Home page"""
    return jsonify({
        "status": "online",
        "bot": "Ultimate Professional Kino Bot",
        "version": "3.0",
        "features": ["movie_search", "admin_panel", "broadcasting", "statistics"],
        "users": len(users_db),
        "movies": len(movies_db)
    })

@app.route('/status')
def status():
    """Status endpoint"""
    return jsonify({
        "bot_active": bool(TOKEN),
        "admin_id": ADMIN_ID,
        "users_count": len(users_db),
        "movies_count": len(movies_db),
        "upload_sessions": len(upload_sessions),
        "available_codes": list(movies_db.keys())[:10]
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Main webhook handler"""
    try:
        # Load fresh data
        load_database()
        
        # Get update
        update = request.get_json()
        if not update:
            logger.warning("Empty update received")
            return "NO_DATA", 400
        
        logger.info(f"📨 Update received: {update}")
        
        # Handle message
        if 'message' in update:
            handle_message(update['message'])
        
        # Handle callback
        elif 'callback_query' in update:
            handle_callback(update['callback_query'])
        
        return "OK", 200
        
    except Exception as e:
        logger.error(f"❌ Webhook error: {e}")
        import traceback
        logger.error(f"❌ Traceback: {traceback.format_exc()}")
        return f"ERROR: {str(e)}", 500

def handle_message(message):
    """Handle incoming message"""
    try:
        # Extract message data
        chat_id = message.get('chat', {}).get('id')
        user_id = message.get('from', {}).get('id')
        username = message.get('from', {}).get('username')
        first_name = message.get('from', {}).get('first_name', 'Unknown')
        text = message.get('text', '')
        
        logger.info(f"💬 Message from {user_id} ({first_name}): '{text}'")
        
        # Save user
        save_user(user_id, username, first_name)
        
        # Handle commands
        if text == '/start':
            handle_start(chat_id, user_id, first_name)
        elif text == '/admin':
            handle_admin(chat_id, user_id)
        elif text == '/stat' or text == '/stats':
            handle_stats(chat_id, user_id)
        elif text.startswith('#') or text.isdigit():
            handle_movie_code(chat_id, user_id, text)
        elif 'video' in message:
            handle_video_upload(chat_id, user_id, message)
        else:
            handle_text_message(chat_id, user_id, text)
            
    except Exception as e:
        logger.error(f"❌ Message handling error: {e}")
        send_message(chat_id, "❌ Xatolik yuz berdi, qayta urinib ko'ring.")

def handle_start(chat_id, user_id, first_name):
    """Handle /start command"""
    welcome_text = f"""🎬 <b>Ultimate Professional Kino Bot</b>ga xush kelibsiz, {first_name}!

🔍 <b>Kino qidirish:</b>
• Kino kodini yuboring: <code>#123</code> yoki <code>123</code>
• Kino avtomatik yuboriladi

📊 <b>Komandalar:</b>
• /stat - Statistika
• /admin - Admin panel (faqat admin uchun)

🎭 <b>Hozirda {len(movies_db)} ta kino mavjud!</b>

💡 <b>Maslahat:</b> Kino kodini to'g'ri kiriting!"""

    keyboard = {
        'inline_keyboard': [
            [{'text': '📊 Statistika', 'callback_data': 'show_stats'}],
            [{'text': '🎬 Mavjud kinolar', 'callback_data': 'show_movies'}],
            [{'text': 'ℹ️ Yordam', 'callback_data': 'show_help'}]
        ]
    }
    
    send_message(chat_id, welcome_text, keyboard)

def handle_admin(chat_id, user_id):
    """Handle admin panel"""
    if user_id != ADMIN_ID:
        send_message(chat_id, "❌ Siz admin emassiz!")
        return
    
    admin_text = f"""🔧 <b>Ultimate Admin Panel</b>

📊 <b>Statistika:</b>
• Foydalanuvchilar: {len(users_db)}
• Kinolar: {len(movies_db)}
• Upload sessiyalar: {len(upload_sessions)}

⚡️ <b>Tezkor amallar:</b>"""

    keyboard = {
        'inline_keyboard': [
            [{'text': '📊 Batafsil statistika', 'callback_data': 'admin_stats'}],
            [{'text': '🎬 Kino yuklash', 'callback_data': 'upload_movie'}],
            [{'text': '📢 Reklama yuborish', 'callback_data': 'broadcast_ad'}],
            [{'text': '👥 Foydalanuvchilar', 'callback_data': 'list_users'}],
            [{'text': '🗂 Kinolar ro\'yxati', 'callback_data': 'list_movies'}]
        ]
    }
    
    send_message(chat_id, admin_text, keyboard)

def handle_stats(chat_id, user_id):
    """Handle statistics"""
    total_users = len(users_db)
    total_movies = len(movies_db)
    
    # Active users calculation
    current_time = int(time.time())
    day_ago = current_time - 86400
    active_today = sum(1 for user in users_db.values() if user.get('last_seen', 0) > day_ago)
    
    stats_text = f"""📊 <b>Bot Statistikasi</b>

👥 <b>Foydalanuvchilar:</b>
• Jami: {total_users}
• Bugun faol: {active_today}

🎬 <b>Kinolar:</b>
• Jami: {total_movies}
• Mavjud kodlar: {', '.join(list(movies_db.keys())[:5])}{'...' if len(movies_db) > 5 else ''}

🤖 <b>Bot holati:</b> Ultimate Professional ✅

💡 <b>Kod formati:</b> #123 yoki 123"""

    keyboard = {
        'inline_keyboard': [
            [{'text': '🎬 Barcha kinolar', 'callback_data': 'show_all_movies'}]
        ]
    }
    
    send_message(chat_id, stats_text, keyboard)

def handle_movie_code(chat_id, user_id, code):
    """Handle movie code request - FIXED VERSION"""
    # Normalize code
    original_code = code
    code = code.strip().lower()
    
    # Remove # if present
    if code.startswith('#'):
        code = code[1:]
    
    # Try with #
    code_with_hash = f"#{code}"
    
    logger.info(f"🎭 Movie request: original='{original_code}', processed='{code}', with_hash='{code_with_hash}'")
    logger.info(f"🎭 Available codes: {list(movies_db.keys())}")
    
    # Check both formats
    movie_data = None
    found_code = None
    
    if code in movies_db:
        movie_data = movies_db[code]
        found_code = code
    elif code_with_hash in movies_db:
        movie_data = movies_db[code_with_hash]
        found_code = code_with_hash
    
    if movie_data:
        logger.info(f"✅ Movie found with code '{found_code}'")
        
        # Extract movie info
        if isinstance(movie_data, str):
            # Old format - just file_id
            file_id = movie_data
            title = f"Kino #{code}"
            duration = 0
            file_size = 0
        else:
            # New format - dictionary
            file_id = movie_data.get('file_id')
            title = movie_data.get('title', f"Kino #{code}")
            duration = movie_data.get('duration', 0)
            file_size = movie_data.get('file_size', 0)
        
        # Format caption
        caption = f"🎬 <b>{title}</b>\n\n📁 <b>Kod:</b> <code>{found_code}</code>"
        
        if duration > 0:
            hours = duration // 3600
            minutes = (duration % 3600) // 60
            if hours > 0:
                caption += f"\n⏱ <b>Davomiyligi:</b> {hours}:{minutes:02d}"
            else:
                caption += f"\n⏱ <b>Davomiyligi:</b> {minutes} daqiqa"
        
        if file_size > 0:
            size_mb = file_size / (1024 * 1024)
            caption += f"\n� <b>Hajmi:</b> {size_mb:.1f} MB"
        
        caption += f"\n\n🎭 <b>Ultimate Professional Kino Bot</b>"
        
        # Send video
        success = send_video(chat_id, file_id, caption)
        if success:
            logger.info(f"✅ Movie '{found_code}' sent to user {user_id}")
        else:
            logger.error(f"❌ Failed to send movie '{found_code}' to user {user_id}")
            send_message(chat_id, f"❌ {found_code} kino yuborishda xatolik yuz berdi!")
    else:
        logger.warning(f"❌ Movie not found: '{code}' or '{code_with_hash}'")
        
        # Show available codes
        available_codes = list(movies_db.keys())[:5]
        codes_text = ", ".join(available_codes) if available_codes else "Hozircha mavjud emas"
        
        error_text = f"""❌ <b>{original_code}</b> kod topilmadi!

📋 <b>Mavjud kodlar:</b> {codes_text}

💡 <b>To'g'ri format:</b>
• <code>#123</code>
• <code>123</code>

🔍 Barcha kodlar uchun /stat buyrug'ini ishlating."""

        keyboard = {
            'inline_keyboard': [
                [{'text': '📊 Statistika', 'callback_data': 'show_stats'}],
                [{'text': '🎬 Barcha kinolar', 'callback_data': 'show_all_movies'}]
            ]
        }
        
        send_message(chat_id, error_text, keyboard)

def handle_video_upload(chat_id, user_id, message):
    """Handle video upload from admin"""
    if user_id != ADMIN_ID:
        send_message(chat_id, "❌ Faqat admin video yuklashi mumkin!")
        return
    
    video = message['video']
    file_id = video['file_id']
    duration = video.get('duration', 0)
    file_size = video.get('file_size', 0)
    
    # Store upload session
    upload_sessions[chat_id] = {
        'file_id': file_id,
        'duration': duration,
        'file_size': file_size,
        'step': 'waiting_for_code',
        'timestamp': int(time.time())
    }
    
    # Format info
    size_mb = file_size / (1024 * 1024) if file_size > 0 else 0
    hours = duration // 3600
    minutes = (duration % 3600) // 60
    
    info_text = f"""🎬 <b>Video qabul qilindi!</b>

📦 <b>Hajmi:</b> {size_mb:.1f} MB
⏱ <b>Davomiyligi:</b> {f'{hours}:{minutes:02d}' if hours > 0 else f'{minutes} daqiqa'}

📝 <b>Endi kino kodini yuboring:</b>
• Masalan: <code>#123</code> yoki <code>456</code>"""

    keyboard = {
        'inline_keyboard': [
            [{'text': '❌ Bekor qilish', 'callback_data': 'cancel_upload'}]
        ]
    }
    
    send_message(chat_id, info_text, keyboard)

def handle_text_message(chat_id, user_id, text):
    """Handle text message"""
    # Check if admin is in upload session
    if user_id == ADMIN_ID and chat_id in upload_sessions:
        session = upload_sessions[chat_id]
        
        if session['step'] == 'waiting_for_code':
            handle_upload_code(chat_id, text)
        elif session['step'] == 'waiting_for_title':
            handle_upload_title(chat_id, text)
        return
    
    # For regular users, try to process as movie code
    if text.strip() and (text.strip().startswith('#') or text.strip().isdigit()):
        handle_movie_code(chat_id, user_id, text)
    else:
        # Unknown message
        help_text = f"""🤔 <b>Tushunmadim.</b>

🔍 <b>Kino qidirish uchun:</b>
• Kino kodini yuboring: <code>#123</code>
• Yoki raqam: <code>123</code>

📊 <b>Komandalar:</b>
• /start - Bosh sahifa
• /stat - Statistika

💡 <b>Hozirda {len(movies_db)} ta kino mavjud!</b>"""

        keyboard = {
            'inline_keyboard': [
                [{'text': '🎬 Mavjud kinolar', 'callback_data': 'show_all_movies'}],
                [{'text': '📊 Statistika', 'callback_data': 'show_stats'}]
            ]
        }
        
        send_message(chat_id, help_text, keyboard)

def handle_upload_code(chat_id, code):
    """Handle upload code step"""
    code = code.strip()
    
    # Normalize code
    if code.isdigit():
        code = f"#{code}"
    
    if not code.startswith('#'):
        send_message(chat_id, "❌ Kod # bilan boshlanishi kerak! Masalan: #123")
        return
    
    # Check if exists
    if code in movies_db:
        keyboard = {
            'inline_keyboard': [
                [{'text': '✅ Ha, almashtirish', 'callback_data': f'replace_movie_{code}'}],
                [{'text': '❌ Yo\'q, bekor qilish', 'callback_data': 'cancel_upload'}]
            ]
        }
        send_message(chat_id, f"⚠️ <b>{code}</b> kodi allaqachon mavjud!\n\nAlmashtirishni xohlaysizmi?", keyboard)
    else:
        # New code
        upload_sessions[chat_id]['code'] = code
        upload_sessions[chat_id]['step'] = 'waiting_for_title'
        send_message(chat_id, f"📝 <b>{code}</b> kodi uchun kino nomini yuboring:")

def handle_upload_title(chat_id, title):
    """Handle upload title step"""
    title = title.strip()
    
    if not title:
        send_message(chat_id, "❌ Kino nomi bo'sh bo'lishi mumkin emas!")
        return
    
    # Complete upload
    session = upload_sessions[chat_id]
    code = session['code']
    
    # Save movie
    movies_db[code] = {
        'file_id': session['file_id'],
        'title': title,
        'duration': session['duration'],
        'file_size': session['file_size'],
        'uploaded_by': ADMIN_ID,
        'upload_time': int(time.time())
    }
    
    save_database()
    
    # Clean up session
    del upload_sessions[chat_id]
    
    # Success message
    size_mb = session['file_size'] / (1024 * 1024)
    duration = session['duration']
    
    success_text = f"""✅ <b>Kino muvaffaqiyatli saqlandi!</b>

🎬 <b>Nomi:</b> {title}
📁 <b>Kod:</b> <code>{code}</code>
📦 <b>Hajmi:</b> {size_mb:.1f} MB"""

    if duration > 0:
        hours = duration // 3600
        minutes = (duration % 3600) // 60
        if hours > 0:
            success_text += f"\n⏱ <b>Davomiyligi:</b> {hours}:{minutes:02d}"
        else:
            success_text += f"\n⏱ <b>Davomiyligi:</b> {minutes} daqiqa"
    
    success_text += f"\n\n🎭 <b>Ultimate Professional Kino Bot</b>"
    
    send_message(chat_id, success_text)
    logger.info(f"✅ Movie saved: {code} - {title}")

def handle_callback(callback_query):
    """Handle callback query"""
    try:
        chat_id = callback_query.get('message', {}).get('chat', {}).get('id')
        user_id = callback_query.get('from', {}).get('id')
        data = callback_query.get('data', '')
        callback_id = callback_query.get('id')
        
        logger.info(f"🔘 Callback: {data} from user {user_id}")
        
        # Answer callback first
        answer_callback(callback_id)
        
        # Handle different callbacks
        if data == 'show_stats':
            handle_stats(chat_id, user_id)
        elif data == 'show_movies' or data == 'show_all_movies':
            show_movies_list(chat_id, user_id)
        elif data == 'show_help':
            show_help(chat_id)
        elif data == 'admin_stats':
            if user_id == ADMIN_ID:
                show_admin_stats(chat_id)
            else:
                send_message(chat_id, "❌ Admin huquqi kerak!")
        elif data == 'upload_movie':
            if user_id == ADMIN_ID:
                send_message(chat_id, "🎬 Video faylni yuboring:")
            else:
                send_message(chat_id, "❌ Admin huquqi kerak!")
        elif data == 'cancel_upload':
            if user_id == ADMIN_ID and chat_id in upload_sessions:
                del upload_sessions[chat_id]
                send_message(chat_id, "❌ Upload bekor qilindi.")
            else:
                send_message(chat_id, "❌ Hech narsa bekor qilinmadi.")
        elif data.startswith('replace_movie_'):
            if user_id == ADMIN_ID:
                code = data.replace('replace_movie_', '')
                if chat_id in upload_sessions:
                    upload_sessions[chat_id]['code'] = code
                    upload_sessions[chat_id]['step'] = 'waiting_for_title'
                    send_message(chat_id, f"📝 <b>{code}</b> uchun yangi kino nomini yuboring:")
        else:
            send_message(chat_id, f"❓ Noma'lum buyruq: {data}")
            
    except Exception as e:
        logger.error(f"❌ Callback error: {e}")
        send_message(chat_id, "❌ Xatolik yuz berdi.")

def show_movies_list(chat_id, user_id):
    """Show available movies"""
    if not movies_db:
        send_message(chat_id, "📋 Hozircha kinolar mavjud emas.")
        return
    
    movies_text = f"🎬 <b>Mavjud kinolar ({len(movies_db)} ta):</b>\n\n"
    
    count = 0
    for code, movie_data in list(movies_db.items())[:15]:  # Show max 15
        count += 1
        
        if isinstance(movie_data, str):
            title = f"Kino {code}"
        else:
            title = movie_data.get('title', f"Kino {code}")
        
        movies_text += f"{count}. <b>{title}</b>\n"
        movies_text += f"   📁 Kod: <code>{code}</code>\n\n"
    
    if len(movies_db) > 15:
        movies_text += f"... va yana {len(movies_db) - 15} ta kino\n\n"
    
    movies_text += "💡 <b>Kino olish uchun kodni yuboring!</b>"
    
    send_message(chat_id, movies_text)

def show_help(chat_id):
    """Show help information"""
    help_text = f"""ℹ️ <b>Ultimate Professional Kino Bot Yordami</b>

🔍 <b>Kino qidirish:</b>
• Kino kodini yuboring: <code>#123</code>
• Yoki raqam: <code>123</code>
• Kino avtomatik yuboriladi

📊 <b>Komandalar:</b>
• /start - Bosh sahifa
• /stat - Statistika
• /admin - Admin panel

🎬 <b>Hozirda mavjud:</b> {len(movies_db)} ta kino

🎭 <b>Ultimate Professional darajada xizmat!</b>"""

    keyboard = {
        'inline_keyboard': [
            [{'text': '🎬 Mavjud kinolar', 'callback_data': 'show_all_movies'}],
            [{'text': '📊 Statistika', 'callback_data': 'show_stats'}]
        ]
    }
    
    send_message(chat_id, help_text, keyboard)

def show_admin_stats(chat_id):
    """Show detailed admin statistics"""
    current_time = int(time.time())
    day_ago = current_time - 86400
    week_ago = current_time - 604800
    
    daily_users = sum(1 for user in users_db.values() if user.get('last_seen', 0) > day_ago)
    weekly_users = sum(1 for user in users_db.values() if user.get('last_seen', 0) > week_ago)
    
    total_size = sum(
        movie.get('file_size', 0) if isinstance(movie, dict) else 0 
        for movie in movies_db.values()
    )
    total_size_mb = total_size / (1024 * 1024)
    
    stats_text = f"""📊 <b>Ultimate Admin Statistika</b>

👥 <b>Foydalanuvchilar:</b>
• Jami: {len(users_db)}
• Bugun faol: {daily_users}
• Hafta faol: {weekly_users}

🎬 <b>Kinolar:</b>
• Jami: {len(movies_db)}
• Umumiy hajmi: {total_size_mb:.1f} MB

⚙️ <b>Tizim:</b>
• Upload sessiyalar: {len(upload_sessions)}
• Bot versiyasi: 3.0 Ultimate

🎭 <b>Ultimate Professional Bot!</b>"""

    send_message(chat_id, stats_text)

def setup_webhook():
    """Setup webhook"""
    try:
        webhook_url = os.getenv('RENDER_EXTERNAL_URL')
        if webhook_url:
            webhook_url = f"{webhook_url}/webhook"
            
            result = telegram_request('setWebhook', {'url': webhook_url})
            if result:
                logger.info(f"✅ Ultimate webhook set: {webhook_url}")
            else:
                logger.error(f"❌ Webhook setup failed")
        else:
            logger.warning("⚠️ No RENDER_EXTERNAL_URL found")
            
    except Exception as e:
        logger.error(f"❌ Webhook setup error: {e}")

# Initialize on startup
logger.info("🚀 Starting Ultimate Professional Kino Bot...")
load_database()
setup_webhook()

# For gunicorn
application = app

if __name__ == "__main__":
    logger.info("🎭 Ultimate Professional Kino Bot starting...")
    
    port = int(os.environ.get('PORT', 8080))
    logger.info(f"🚀 Server starting on port {port}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )
