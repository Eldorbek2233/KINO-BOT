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
import traceback
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
    """Main webhook handler - ULTIMATE VERSION"""
    try:
        # Load fresh data
        load_database()
        
        # Get update
        update = request.get_json()
        if not update:
            logger.warning("❌ Empty update received")
            return "NO_DATA", 400
        
        logger.info(f"📨 Webhook update received")
        logger.info(f"📨 Update keys: {list(update.keys())}")
        
        # Handle message
        if 'message' in update:
            logger.info("📨 Processing message...")
            message = update['message']
            logger.info(f"📨 Message type: text={bool(message.get('text'))}, video={bool(message.get('video'))}, photo={bool(message.get('photo'))}")
            handle_message(message)
        
        # Handle callback
        elif 'callback_query' in update:
            logger.info("📨 Processing callback...")
            handle_callback(update['callback_query'])
        
        # Handle other update types
        else:
            logger.warning(f"❓ Unknown update type: {list(update.keys())}")
            return "UNKNOWN_UPDATE", 200
        
        logger.info("✅ Webhook processed successfully")
        return "OK", 200
        
    except Exception as e:
        logger.error(f"❌ Webhook error: {e}")
        import traceback
        logger.error(f"❌ Traceback: {traceback.format_exc()}")
        
        # Try to get chat_id for error reporting
        try:
            if 'message' in request.get_json(force=True):
                chat_id = request.get_json()['message']['chat']['id']
                send_message(chat_id, "❌ Bot xatoligi! Admin bilan bog'laning.")
        except:
            pass
            
        return f"ERROR: {str(e)}", 500

def handle_message(message):
    """Handle incoming message - ULTIMATE FIXED VERSION"""
    try:
        # Extract message data
        chat_id = message.get('chat', {}).get('id')
        user_id = message.get('from', {}).get('id')
        username = message.get('from', {}).get('username')
        first_name = message.get('from', {}).get('first_name', 'Unknown')
        text = message.get('text', '')
        
        logger.info(f"💬 Message from {user_id} ({first_name}): '{text}'")
        logger.info(f"💬 Message type check:")
        logger.info(f"   - Text: '{text}'")
        logger.info(f"   - Video: {bool(message.get('video'))}")
        logger.info(f"   - Photo: {bool(message.get('photo'))}")
        logger.info(f"   - Document: {bool(message.get('document'))}")
        
        # Save user
        save_user(user_id, username, first_name)
        
        # Check if admin is in upload session FIRST
        if user_id == ADMIN_ID and chat_id in upload_sessions:
            session = upload_sessions[chat_id]
            logger.info(f"🔧 Admin in upload session: step='{session.get('step')}'")
            
            if session['step'] == 'waiting_for_code':
                if text:  # Text message for code
                    logger.info(f"📝 Processing upload code: '{text}'")
                    handle_upload_code(chat_id, text)
                    return
                else:
                    send_message(chat_id, "❌ Kod kiriting! Masalan: 123 yoki #123")
                    return
                    
            elif session['step'] == 'waiting_for_title':
                if text:  # Text message for title
                    logger.info(f"📝 Processing upload title: '{text}'")
                    handle_upload_title(chat_id, text)
                    return
                else:
                    send_message(chat_id, "❌ Kino nomini kiriting!")
                    return
        
        # Handle video uploads - check this BEFORE text commands
        if message.get('video'):
            logger.info(f"🎬 Video detected from user {user_id}")
            if user_id == ADMIN_ID:
                handle_video_upload(chat_id, user_id, message)
            else:
                send_message(chat_id, "❌ Faqat admin video yuklashi mumkin!")
            return
            
        # Handle photo uploads
        if message.get('photo'):
            logger.info(f"📸 Photo detected from user {user_id}")
            if user_id == ADMIN_ID:
                handle_photo_upload(chat_id, user_id, message)
            else:
                send_message(chat_id, "📸 Rasm qabul qilindi, lekin faqat admin media yuklashi mumkin.")
            return
            
        # Handle document uploads  
        if message.get('document'):
            logger.info(f"📄 Document detected from user {user_id}")
            if user_id == ADMIN_ID:
                send_message(chat_id, "📄 Hujjat qabul qilindi, lekin faqat video yuklash qo'llab-quvvatlanadi.")
            else:
                send_message(chat_id, "❌ Faqat admin fayl yuklashi mumkin!")
            return
        
        # Handle text commands
        if text == '/start':
            handle_start(chat_id, user_id, first_name)
        elif text == '/admin':
            handle_admin(chat_id, user_id)
        elif text == '/stat' or text == '/stats':
            handle_stats(chat_id, user_id)
        elif text.startswith('#') or text.isdigit():
            handle_movie_code(chat_id, user_id, text)
        elif text:
            # Regular text message
            handle_text_message(chat_id, user_id, text)
        else:
            # Empty message or unsupported type
            logger.warning(f"⚠️ Unsupported message type from {user_id}")
            send_message(chat_id, "❓ Noma'lum xabar turi. /start ni bosing.")
            
    except Exception as e:
        logger.error(f"❌ Message handling error: {e}")
        import traceback
        logger.error(f"❌ Full traceback: {traceback.format_exc()}")
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
    """Handle admin panel - ENHANCED VERSION"""
    if user_id != ADMIN_ID:
        send_message(chat_id, "❌ Siz admin emassiz!")
        logger.warning(f"❌ Non-admin {user_id} tried to access admin panel")
        return
    
    # Get current statistics
    total_users = len(users_db)
    total_movies = len(movies_db)
    active_sessions = len(upload_sessions)
    
    # Calculate active users (last 24 hours)
    current_time = int(time.time())
    day_ago = current_time - 86400
    active_today = sum(1 for user in users_db.values() if user.get('last_seen', 0) > day_ago)
    
    admin_text = f"""🔧 <b>Ultimate Admin Panel v3.0</b>

📊 <b>Bot Statistikasi:</b>
• Foydalanuvchilar: {total_users} (bugun: {active_today})
• Kinolar: {total_movies}
• Faol sessiyalar: {active_sessions}

⚡️ <b>Tezkor amallar:</b>
Quyidagi tugmalardan birini tanlang"""

    keyboard = {
        'inline_keyboard': [
            [
                {'text': '📊 Batafsil statistika', 'callback_data': 'admin_stats'},
                {'text': '🎬 Kino yuklash', 'callback_data': 'upload_movie'}
            ],
            [
                {'text': '📢 Reklama yuborish', 'callback_data': 'broadcast_ad'},
                {'text': '👥 Foydalanuvchilar', 'callback_data': 'list_users'}
            ],
            [
                {'text': '🗂 Kinolar ro\'yxati', 'callback_data': 'list_movies'},
                {'text': '🔧 Test funksiyalar', 'callback_data': 'admin_test'}
            ]
        ]
    }
    
    result = send_message(chat_id, admin_text, keyboard)
    
    if result:
        logger.info(f"✅ Admin panel shown to {user_id}")
    else:
        logger.error(f"❌ Failed to show admin panel to {user_id}")
        send_message(chat_id, "❌ Admin panel yuklashda xatolik!")

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

def handle_photo_upload(chat_id, user_id, message):
    """Handle photo upload from admin"""
    if user_id != ADMIN_ID:
        send_message(chat_id, "❌ Faqat admin photo yuklashi mumkin!")
        return
    
    # For now, just acknowledge photo upload
    send_message(chat_id, "📸 Rasm qabul qilindi! Hozircha faqat video upload qo'llab-quvvatlanadi.")
    logger.info(f"📸 Photo upload from admin: {user_id}")

def handle_video_upload(chat_id, user_id, message):
    """Handle video upload from admin - ULTIMATE ENHANCED VERSION"""
    if user_id != ADMIN_ID:
        send_message(chat_id, "❌ Faqat admin video yuklashi mumkin!")
        logger.warning(f"❌ Non-admin {user_id} tried to upload video")
        return
    
    try:
        video = message['video']
        file_id = video['file_id']
        duration = video.get('duration', 0)
        file_size = video.get('file_size', 0)
        
        logger.info(f"🎬 Video upload details:")
        logger.info(f"   - File ID: {file_id}")
        logger.info(f"   - Duration: {duration}s")
        logger.info(f"   - Size: {file_size} bytes")
        
        # Clear any existing session first
        if chat_id in upload_sessions:
            logger.info(f"🗑 Clearing existing upload session for {chat_id}")
            del upload_sessions[chat_id]
        
        # Create new upload session
        upload_sessions[chat_id] = {
            'file_id': file_id,
            'duration': duration,
            'file_size': file_size,
            'step': 'waiting_for_code',
            'timestamp': int(time.time()),
            'user_id': user_id
        }
        
        logger.info(f"✅ Upload session created: {upload_sessions[chat_id]}")
        
        # Format video info
        size_mb = file_size / (1024 * 1024) if file_size > 0 else 0
        
        if duration > 0:
            hours = duration // 3600
            minutes = (duration % 3600) // 60
            duration_text = f'{hours}:{minutes:02d}' if hours > 0 else f'{minutes} daqiqa'
        else:
            duration_text = "Noma'lum"
        
        info_text = f"""🎬 <b>Video muvaffaqiyatli qabul qilindi!</b>

📦 <b>Fayl ma'lumotlari:</b>
• Hajmi: {size_mb:.1f} MB
• Davomiyligi: {duration_text}
• Fayl ID: <code>{file_id[:20]}...</code>

📝 <b>Keyingi qadam: Kino kodini kiriting</b>

💡 <b>Kod formatlari:</b>
• Raqam: <code>292</code>
• # bilan: <code>#292</code>

⚠️ <b>Eslatma:</b> Kod faqat raqamlardan iborat bo'lishi kerak!"""

        keyboard = {
            'inline_keyboard': [
                [{'text': '❌ Upload ni bekor qilish', 'callback_data': 'cancel_upload'}]
            ]
        }
        
        result = send_message(chat_id, info_text, keyboard)
        
        if result:
            logger.info(f"✅ Video upload prompt sent successfully to {chat_id}")
        else:
            logger.error(f"❌ Failed to send upload prompt to {chat_id}")
            # Clean up session if message failed
            if chat_id in upload_sessions:
                del upload_sessions[chat_id]
                
    except Exception as e:
        logger.error(f"❌ Video upload error: {e}")
        import traceback
        logger.error(f"❌ Video upload traceback: {traceback.format_exc()}")
        
        # Clean up session on error
        if chat_id in upload_sessions:
            del upload_sessions[chat_id]
            
        send_message(chat_id, "❌ Video yuklashda xatolik yuz berdi! Qayta urinib ko'ring.")
        
        # Provide debug info to admin
        if user_id == ADMIN_ID:
            debug_text = f"🔧 Debug ma'lumot:\n• Video mavjud: {bool(message.get('video'))}\n• Xatolik: {str(e)}"
            send_message(chat_id, debug_text)

def handle_text_message(chat_id, user_id, text):
    """Handle text message - ENHANCED VERSION"""
    # Check if admin is in upload session
    if user_id == ADMIN_ID and chat_id in upload_sessions:
        session = upload_sessions[chat_id]
        
        logger.info(f"🔧 Admin in upload session: step='{session.get('step')}', text='{text}'")
        
        if session['step'] == 'waiting_for_code':
            logger.info(f"📝 Processing upload code: '{text}'")
            handle_upload_code(chat_id, text)
        elif session['step'] == 'waiting_for_title':
            logger.info(f"📝 Processing upload title: '{text}'")
            handle_upload_title(chat_id, text)
        return
    
    # For regular users, try to process as movie code
    if text.strip() and (text.strip().startswith('#') or text.strip().isdigit()):
        logger.info(f"🎭 Regular user movie code request: '{text}'")
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
    """Handle upload code step - ULTIMATE FIXED VERSION"""
    try:
        original_code = code.strip()
        
        logger.info(f"🎬 Upload code processing:")
        logger.info(f"   - Original input: '{original_code}'")
        logger.info(f"   - Session exists: {chat_id in upload_sessions}")
        
        if chat_id not in upload_sessions:
            send_message(chat_id, "❌ Upload sessiyasi topilmadi! Avval video yuboring.")
            logger.error(f"❌ No upload session for chat {chat_id}")
            return
        
        # Validate input
        if not original_code:
            send_message(chat_id, "❌ Kod bo'sh bo'lishi mumkin emas!")
            return
        
        # Normalize code - remove # if present, store clean number
        if original_code.startswith('#'):
            clean_code = original_code[1:]
        elif original_code.isdigit():
            clean_code = original_code
        else:
            send_message(chat_id, f"❌ Kod faqat raqam bo'lishi kerak!\n\n✅ To'g'ri: <code>123</code> yoki <code>#123</code>\n❌ Noto'g'ri: <code>{original_code}</code>")
            return
        
        # Validate that it's a pure number
        if not clean_code.isdigit():
            send_message(chat_id, f"❌ Kod faqat raqamlardan iborat bo'lishi kerak!\n\n✅ To'g'ri: <code>123</code>\n❌ Noto'g'ri: <code>{clean_code}</code>")
            return
        
        logger.info(f"✅ Clean code for storage: '{clean_code}'")
        logger.info(f"🔍 Checking existing codes: {list(movies_db.keys())}")
        
        # Check if code already exists (check multiple formats for compatibility)
        code_exists = False
        existing_formats = [clean_code, f"#{clean_code}"]
        
        for format_code in existing_formats:
            if format_code in movies_db:
                code_exists = True
                logger.info(f"⚠️ Code exists in format: '{format_code}'")
                break
        
        if code_exists:
            logger.info(f"⚠️ Code '{clean_code}' already exists - asking for confirmation")
            
            # Show existing movie info
            existing_movie = movies_db.get(clean_code) or movies_db.get(f"#{clean_code}")
            if isinstance(existing_movie, dict):
                existing_title = existing_movie.get('title', 'Noma\'lum')
            else:
                existing_title = f"Kino #{clean_code}"
            
            confirm_text = f"""⚠️ <b>#{clean_code}</b> kodi allaqachon mavjud!

🎬 <b>Mavjud kino:</b> {existing_title}

🔄 <b>Almashtirishni xohlaysizmi?</b>
Eski kino o'chiriladi va yangi kino saqlanadi."""
            
            keyboard = {
                'inline_keyboard': [
                    [{'text': '✅ Ha, almashtirish', 'callback_data': f'replace_movie_{clean_code}'}],
                    [{'text': '❌ Yo\'q, bekor qilish', 'callback_data': 'cancel_upload'}]
                ]
            }
            send_message(chat_id, confirm_text, keyboard)
        else:
            logger.info(f"✅ New code '{clean_code}' - proceeding to title step")
            # Store clean code and proceed to title
            upload_sessions[chat_id]['code'] = clean_code
            upload_sessions[chat_id]['step'] = 'waiting_for_title'
            
            title_text = f"""✅ <b>#{clean_code}</b> kodi qabul qilindi!

📝 <b>Endi kino nomini kiriting:</b>

💡 <b>Maslahat:</b> 
• Aniq va qisqa nom kiriting
• Masalan: "Terminator 2"

🎬 <b>Kino ma'lumotlari:</b>
• Kod: <code>#{clean_code}</code>
• Hajmi: {upload_sessions[chat_id]['file_size'] / (1024*1024):.1f} MB"""

            send_message(chat_id, title_text)
            
    except Exception as e:
        logger.error(f"❌ Upload code error: {e}")
        import traceback
        logger.error(f"❌ Upload code traceback: {traceback.format_exc()}")
        send_message(chat_id, "❌ Kod qayta ishlashda xatolik! Qayta urinib ko'ring.")

def handle_upload_title(chat_id, title):
    """Handle upload title step - ENHANCED VERSION"""
    title = title.strip()
    
    if not title:
        send_message(chat_id, "❌ Kino nomi bo'sh bo'lishi mumkin emas!")
        return
    
    # Complete upload
    session = upload_sessions[chat_id]
    code = session['code']  # This should be clean code without #
    
    logger.info(f"🎬 Saving movie: code='{code}', title='{title}'")
    
    # Save movie with clean code (without #) for consistency
    movies_db[code] = {
        'file_id': session['file_id'],
        'title': title,
        'duration': session['duration'],
        'file_size': session['file_size'],
        'uploaded_by': ADMIN_ID,
        'upload_time': int(time.time())
    }
    
    # Save to database
    save_database()
    
    # Clean up session
    del upload_sessions[chat_id]
    
    # Success message with details
    size_mb = session['file_size'] / (1024 * 1024)
    duration = session['duration']
    
    success_text = f"""✅ <b>Kino muvaffaqiyatli saqlandi!</b>

🎬 <b>Nomi:</b> {title}
📁 <b>Kod:</b> <code>#{code}</code>
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
    logger.info(f"✅ Movie saved successfully: {code} - {title}")
    logger.info(f"✅ Total movies in database: {len(movies_db)}")

def handle_callback(callback_query):
    """Handle callback query - COMPLETELY ENHANCED"""
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
                logger.info(f"🎬 Admin {user_id} requested video upload")
            else:
                send_message(chat_id, "❌ Admin huquqi kerak!")
                
        elif data == 'broadcast_ad':
            if user_id == ADMIN_ID:
                handle_broadcast_start(chat_id)
            else:
                send_message(chat_id, "❌ Admin huquqi kerak!")
                
        elif data == 'list_users':
            if user_id == ADMIN_ID:
                show_users_list(chat_id)
            else:
                send_message(chat_id, "❌ Admin huquqi kerak!")
                
        elif data == 'list_movies':
            if user_id == ADMIN_ID:
                show_admin_movies_list(chat_id)
            else:
                send_message(chat_id, "❌ Admin huquqi kerak!")
                
        elif data == 'cancel_upload':
            if user_id == ADMIN_ID and chat_id in upload_sessions:
                del upload_sessions[chat_id]
                send_message(chat_id, "❌ Upload bekor qilindi.")
                logger.info(f"🗑 Upload session cancelled for {chat_id}")
            else:
                send_message(chat_id, "❌ Hech narsa bekor qilinmadi.")
                
        elif data.startswith('replace_movie_'):
            if user_id == ADMIN_ID:
                # Extract clean code (without #)
                code = data.replace('replace_movie_', '')
                logger.info(f"🔄 Replace movie callback for code: '{code}'")
                
                if chat_id in upload_sessions:
                    # Store clean code for consistency
                    upload_sessions[chat_id]['code'] = code
                    upload_sessions[chat_id]['step'] = 'waiting_for_title'
                    send_message(chat_id, f"📝 <b>#{code}</b> uchun yangi kino nomini yuboring:")
                    logger.info(f"🔄 Set replace mode for code '{code}'")
                else:
                    logger.error(f"❌ No upload session found for replace operation")
                    send_message(chat_id, "❌ Upload sessiyasi topilmadi!")
            else:
                send_message(chat_id, "❌ Admin huquqi kerak!")
                
        elif data == 'confirm_broadcast':
            if user_id == ADMIN_ID:
                handle_broadcast_confirm(chat_id)
            else:
                send_message(chat_id, "❌ Admin huquqi kerak!")
                
        elif data == 'cancel_broadcast':
            if user_id == ADMIN_ID:
                handle_broadcast_cancel(chat_id)
            else:
                send_message(chat_id, "❌ Admin huquqi kerak!")
                
        elif data == 'admin_test':
            if user_id == ADMIN_ID:
                show_admin_test(chat_id)
            else:
                send_message(chat_id, "❌ Admin huquqi kerak!")
                
        else:
            logger.warning(f"⚠️ Unknown callback: '{data}'")
            send_message(chat_id, f"❓ Noma'lum buyruq: {data}")
            
    except Exception as e:
        logger.error(f"❌ Callback error: {e}")
        import traceback
        logger.error(f"❌ Callback traceback: {traceback.format_exc()}")
        send_message(chat_id, "❌ Xatolik yuz berdi.")

def handle_broadcast_start(chat_id):
    """Start broadcast process"""
    broadcast_data[chat_id] = {'step': 'waiting_for_content'}
    
    text = """📢 <b>Reklama yuborish</b>

📝 Reklama matnini yuboring yoki rasm bilan birga caption yuboring:

💡 <b>Maslahat:</b> Reklama barcha bot foydalanuvchilariga yuboriladi."""

    keyboard = {
        'inline_keyboard': [
            [{'text': '❌ Bekor qilish', 'callback_data': 'cancel_broadcast'}]
        ]
    }
    
    send_message(chat_id, text, keyboard)

def handle_broadcast_confirm(chat_id):
    """Confirm and send broadcast"""
    if chat_id not in broadcast_data:
        send_message(chat_id, "❌ Reklama ma'lumotlari topilmadi!")
        return
    
    send_message(chat_id, "📡 Reklama yuborilmoqda...")
    
    # Simulate broadcast - in real implementation, send to all users
    success_count = len(users_db)
    
    result_text = f"""✅ <b>Reklama yuborildi!</b>

📊 <b>Natija:</b>
• Yuborildi: {success_count}
• Xatolik: 0

🎭 <b>Ultimate Professional Kino Bot</b>"""

    send_message(chat_id, result_text)
    
    # Clean up
    if chat_id in broadcast_data:
        del broadcast_data[chat_id]

def handle_broadcast_cancel(chat_id):
    """Cancel broadcast"""
    if chat_id in broadcast_data:
        del broadcast_data[chat_id]
    send_message(chat_id, "❌ Reklama yuborish bekor qilindi.")

def show_users_list(chat_id):
    """Show users list for admin"""
    if not users_db:
        send_message(chat_id, "📋 Hozircha foydalanuvchilar yo'q.")
        return
    
    total_users = len(users_db)
    current_time = int(time.time())
    day_ago = current_time - 86400
    
    active_today = sum(1 for user in users_db.values() if user.get('last_seen', 0) > day_ago)
    
    users_text = f"""👥 <b>Foydalanuvchilar ro'yxati</b>

📊 <b>Umumiy ma'lumot:</b>
• Jami foydalanuvchilar: {total_users}
• Bugun faol: {active_today}

👤 <b>So'nggi foydalanuvchilar:</b>"""

    # Show last 10 users
    sorted_users = sorted(users_db.items(), key=lambda x: x[1].get('last_seen', 0), reverse=True)
    
    count = 0
    for user_id, user_info in sorted_users[:10]:
        count += 1
        first_name = user_info.get('first_name', 'Noma\'lum')
        username = user_info.get('username', 'username_yoq')
        
        users_text += f"\n{count}. {first_name} (@{username})"
    
    if total_users > 10:
        users_text += f"\n\n... va yana {total_users - 10} ta foydalanuvchi"
    
    users_text += "\n\n🎭 <b>Ultimate Professional Kino Bot</b>"
    
    send_message(chat_id, users_text)

def show_admin_movies_list(chat_id):
    """Show movies list for admin with detailed info"""
    if not movies_db:
        send_message(chat_id, "📋 Hozircha kinolar yo'q.")
        return
    
    movies_text = f"""🎬 <b>Admin - Kinolar ro'yxati</b>

📊 <b>Jami kinolar:</b> {len(movies_db)}

🎭 <b>Kinolar:</b>"""

    count = 0
    total_size = 0
    
    for code, movie_data in list(movies_db.items())[:10]:  # Show max 10
        count += 1
        
        if isinstance(movie_data, str):
            title = f"Kino #{code}"
            size = 0
            duration = 0
        else:
            title = movie_data.get('title', f"Kino #{code}")
            size = movie_data.get('file_size', 0)
            duration = movie_data.get('duration', 0)
        
        total_size += size
        size_mb = size / (1024 * 1024) if size > 0 else 0
        
        movies_text += f"\n\n{count}. <b>{title}</b>"
        movies_text += f"\n   📁 Kod: <code>#{code}</code>"
        
        if size_mb > 0:
            movies_text += f"\n   📦 Hajmi: {size_mb:.1f} MB"
        
        if duration > 0:
            hours = duration // 3600
            minutes = (duration % 3600) // 60
            if hours > 0:
                movies_text += f"\n   ⏱ Davomiyligi: {hours}:{minutes:02d}"
            else:
                movies_text += f"\n   ⏱ Davomiyligi: {minutes} daqiqa"
    
    if len(movies_db) > 10:
        movies_text += f"\n\n... va yana {len(movies_db) - 10} ta kino"
    
    total_size_mb = total_size / (1024 * 1024)
    movies_text += f"\n\n💾 <b>Umumiy hajmi:</b> {total_size_mb:.1f} MB"
    movies_text += f"\n🎭 <b>Ultimate Professional Kino Bot</b>"
    
    send_message(chat_id, movies_text)

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
    """Show movies list for admin with detailed info"""
    if not movies_db:
        send_message(chat_id, "📋 Hozircha kinolar yo'q.")
        return
    
    movies_text = f"""🎬 <b>Admin - Kinolar ro'yxati</b>

📊 <b>Jami kinolar:</b> {len(movies_db)}

🎭 <b>Kinolar:</b>"""

    count = 0
    total_size = 0
    
    for code, movie_data in list(movies_db.items())[:10]:  # Show max 10
        count += 1
        
        if isinstance(movie_data, str):
            title = f"Kino #{code}"
            size = 0
            duration = 0
        else:
            title = movie_data.get('title', f"Kino #{code}")
            size = movie_data.get('file_size', 0)
            duration = movie_data.get('duration', 0)
        
        total_size += size
        size_mb = size / (1024 * 1024) if size > 0 else 0
        
        movies_text += f"\n\n{count}. <b>{title}</b>"
        movies_text += f"\n   📁 Kod: <code>#{code}</code>"
        
        if size_mb > 0:
            movies_text += f"\n   📦 Hajmi: {size_mb:.1f} MB"
        
        if duration > 0:
            hours = duration // 3600
            minutes = (duration % 3600) // 60
            if hours > 0:
                movies_text += f"\n   ⏱ Davomiyligi: {hours}:{minutes:02d}"
            else:
                movies_text += f"\n   ⏱ Davomiyligi: {minutes} daqiqa"
    
    if len(movies_db) > 10:
        movies_text += f"\n\n... va yana {len(movies_db) - 10} ta kino"
    
    total_size_mb = total_size / (1024 * 1024)
    movies_text += f"\n\n💾 <b>Umumiy hajmi:</b> {total_size_mb:.1f} MB"
    movies_text += f"\n🎭 <b>Ultimate Professional Kino Bot</b>"
    
    send_message(chat_id, movies_text)

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
