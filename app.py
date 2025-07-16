#!/usr/bin/env python3
"""
Professional Kino Bot for Render - Complete functionality
"""

import os
import sys
import logging
import json
import time
import requests
from flask import Flask, request, jsonify

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Hardcoded config for Render
TOKEN = "8177519032:AAED4FgPoFQiQhqM_lvrK1iV8hL9u4SnkDk"
ADMIN_ID = 5542016161

# Create Flask app
app = Flask(__name__)

# Global data storage
users_data = {}
movie_codes = {}
temp_video_data = {}
temp_ad_data = {}

def load_data():
    """Load movie codes and users data"""
    global movie_codes, users_data
    
    try:
        # Try to read file_ids.json
        if os.path.exists('file_ids.json'):
            with open('file_ids.json', 'r') as f:
                movie_codes = json.load(f)
                logger.info(f"📁 Loaded {len(movie_codes)} movie codes")
        else:
            movie_codes = {}
            logger.info("📁 file_ids.json not found, using empty dict")
    except Exception as e:
        logger.error(f"❌ Error loading movie codes: {e}")
        movie_codes = {}
        
    try:
        # Try to read users.json
        if os.path.exists('users.json'):
            with open('users.json', 'r') as f:
                users_data = json.load(f)
                logger.info(f"👥 Loaded {len(users_data)} users")
        else:
            users_data = {}
            logger.info("👥 users.json not found, using empty dict")
    except Exception as e:
        logger.error(f"❌ Error loading users data: {e}")
        users_data = {}

def save_data():
    """Save movie codes and users data"""
    try:
        with open('file_ids.json', 'w') as f:
            json.dump(movie_codes, f, indent=2)
        logger.info(f"💾 Saved {len(movie_codes)} movie codes")
    except Exception as e:
        logger.error(f"❌ Error saving movie codes: {e}")
        
    try:
        with open('users.json', 'w') as f:
            json.dump(users_data, f, indent=2)
        logger.info(f"💾 Saved {len(users_data)} users")
    except Exception as e:
        logger.error(f"❌ Error saving users data: {e}")

def save_user(user_id, username=None, first_name=None):
    """Save user data"""
    users_data[str(user_id)] = {
        'username': username,
        'first_name': first_name,
        'last_seen': int(time.time())
    }
    logger.info(f"👤 Saved user: {user_id} ({first_name})")
    save_data()

def send_message(chat_id, text):
    """Send message via Telegram API"""
    try:
        if not TOKEN:
            logger.error("❌ No TOKEN available")
            return False
            
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        
        logger.info(f"📤 Sending message to {chat_id}: {text[:50]}...")
        
        response = requests.post(url, data=data, timeout=10)
        result = response.json()
        
        if result.get('ok'):
            logger.info(f"✅ Message sent successfully to {chat_id}")
            return True
        else:
            logger.error(f"❌ Telegram API error: {result}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Send message error: {e}")
        return False

def send_message_with_keyboard(chat_id, text, keyboard=None):
    """Send message with inline keyboard"""
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        
        if keyboard:
            keyboard_json = json.dumps(keyboard)
            data["reply_markup"] = keyboard_json
            logger.info(f"⌨️ Sending keyboard: {keyboard_json[:100]}...")
            
        logger.info(f"📤 Sending message with keyboard to {chat_id}")
        response = requests.post(url, data=data, timeout=10)
        result = response.json()
        
        if result.get('ok'):
            logger.info(f"✅ Message with keyboard sent to {chat_id}")
            return True
        else:
            logger.error(f"❌ Telegram API error: {result}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Send message error: {e}")
        return False

def send_video(chat_id, file_id, caption=""):
    """Send video file"""
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendVideo"
        
        data = {
            "chat_id": chat_id,
            "video": file_id,
            "caption": caption,
            "parse_mode": "HTML"
        }
        
        response = requests.post(url, data=data, timeout=30)
        result = response.json()
        
        if result.get('ok'):
            logger.info(f"✅ Video sent to {chat_id}")
            return True
        else:
            logger.error(f"❌ Send video error: {result}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Send video error: {e}")
        return False

def send_photo(chat_id, photo_id, caption=""):
    """Send photo"""
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
        
        data = {
            "chat_id": chat_id,
            "photo": photo_id,
            "caption": caption,
            "parse_mode": "HTML"
        }
        
        response = requests.post(url, data=data, timeout=10)
        result = response.json()
        
        if result.get('ok'):
            return True
        else:
            logger.error(f"❌ Send photo error: {result}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Send photo error: {e}")
        return False

def send_photo_with_keyboard(chat_id, photo_id, caption, keyboard=None):
    """Send photo with keyboard"""
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
        
        data = {
            "chat_id": chat_id,
            "photo": photo_id,
            "caption": caption,
            "parse_mode": "HTML"
        }
        
        if keyboard:
            data["reply_markup"] = json.dumps(keyboard)
            
        response = requests.post(url, data=data, timeout=10)
        result = response.json()
        
        if result.get('ok'):
            logger.info(f"✅ Photo with keyboard sent to {chat_id}")
            return True
        else:
            logger.error(f"❌ Send photo error: {result}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Send photo error: {e}")
        return False

def answer_callback_query(callback_query_id, text=""):
    """Answer callback query"""
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/answerCallbackQuery"
        
        data = {
            "callback_query_id": callback_query_id,
            "text": text
        }
        
        logger.info(f"📞 Answering callback query: {callback_query_id}")
        response = requests.post(url, data=data, timeout=5)
        result = response.json()
        
        if result.get('ok'):
            logger.info(f"✅ Callback query answered successfully")
            return True
        else:
            logger.error(f"❌ Answer callback error: {result}")
            return False
        
    except Exception as e:
        logger.error(f"❌ Answer callback error: {e}")
        return False

@app.route('/')
def home():
    """Health check"""
    return jsonify({
        "status": "ok", 
        "message": "Professional Kino Bot is running!",
        "platform": "render",
        "webhook_ready": True,
        "version": "2.0",
        "features": ["movie_upload", "broadcast", "admin_panel", "statistics"]
    })

@app.route('/debug')
def debug():
    """Debug endpoint"""
    return jsonify({
        "token_present": bool(TOKEN),
        "admin_id": ADMIN_ID,
        "webhook_url": f"{os.getenv('RENDER_EXTERNAL_URL', 'unknown')}/webhook",
        "users_count": len(users_data),
        "movies_count": len(movie_codes),
        "temp_video_data": list(temp_video_data.keys()),
        "temp_ad_data": list(temp_ad_data.keys()),
        "status": "professional"
    })

@app.route('/test_movie')
def test_movie():
    """Test movie functionality"""
    load_data()
    return jsonify({
        "movies_loaded": len(movie_codes),
        "sample_movies": dict(list(movie_codes.items())[:3]),
        "users_loaded": len(users_data),
        "temp_data": {
            "video_uploads": len(temp_video_data),
            "pending_ads": len(temp_ad_data)
        }
    })

@app.route('/test_admin')
def test_admin():
    """Test admin functionality"""
    return jsonify({
        "admin_id": ADMIN_ID,
        "admin_id_type": type(ADMIN_ID).__name__,
        "test_user_id": 5542016161,
        "match_test": ADMIN_ID == 5542016161,
        "string_match": str(ADMIN_ID) == "5542016161"
    })

@app.route('/webhook_test', methods=['POST'])
def webhook_test():
    """Test webhook manually"""
    data = request.get_json()
    logger.info(f"🧪 Test webhook data: {data}")
    return jsonify({"status": "test_received", "data": data})

@app.route('/stats')
def api_stats():
    """API Stats endpoint"""
    return jsonify({
        "total_users": len(users_data),
        "total_movies": len(movie_codes),
        "active_uploads": len(temp_video_data),
        "pending_ads": len(temp_ad_data)
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Professional webhook handler with all bot functionality"""
    try:
        # Load data on each request
        load_data()
        
        # Log request
        logger.info("📨 Webhook request received")
        
        # Get JSON data
        data = request.get_json(force=True)
        if not data:
            return "NO_DATA", 400
            
        # Process message
        if 'message' in data:
            message = data['message']
            chat_id = message.get('chat', {}).get('id')
            user_id = message.get('from', {}).get('id')
            username = message.get('from', {}).get('username')
            first_name = message.get('from', {}).get('first_name')
            text = message.get('text', '')  # Can be empty string or None
            
            logger.info(f"💬 Message from {user_id} ({username}): '{text}'")
            logger.info(f"💬 Message has: video={'video' in message}, photo={'photo' in message}, text={bool(text)}")
            
            # Save user
            save_user(user_id, username, first_name)
            
            # Process commands - only if text exists
            if text == '/start':
                logger.info(f"🎬 Processing /start for user {user_id}")
                handle_start(chat_id, user_id, first_name)
            elif text == '/admin':
                logger.info(f"🔧 Processing /admin for user {user_id}")
                handle_admin_menu(chat_id, user_id)
            elif text == '/stat':
                logger.info(f"📊 Processing /stat for user {user_id}")
                handle_stats(chat_id, user_id)
            elif text and (text.startswith('#') or text.isdigit()):
                # Auto-add # if user sent just numbers
                if text.isdigit():
                    code = f"#{text}"
                    logger.info(f"🎭 Auto-added # to webhook code: '{code}'")
                else:
                    code = text
                logger.info(f"🎭 Processing movie request '{code}' for user {user_id}")
                handle_movie_request(chat_id, code)
            else:
                logger.info(f"💬 Processing regular message for user {user_id}")
                handle_regular_message(chat_id, user_id, text, message)
                
        # Process callback queries
        elif 'callback_query' in data:
            callback = data['callback_query']
            chat_id = callback.get('message', {}).get('chat', {}).get('id')
            user_id = callback.get('from', {}).get('id')
            callback_data = callback.get('data', '')
            message_id = callback.get('message', {}).get('message_id')
            callback_id = callback.get('id')
            
            logger.info(f"🔘 Callback received: data='{callback_data}', user={user_id}")
            logger.info(f"🔘 Callback details: chat_id={chat_id}, message_id={message_id}")
            
            # Answer callback query first
            try:
                answer_result = answer_callback_query(callback_id)
                logger.info(f"✅ Callback answered: {answer_result}")
            except Exception as e:
                logger.error(f"❌ Failed to answer callback: {e}")
            
            # Process callback
            try:
                handle_callback_query(chat_id, user_id, callback_data, message_id)
                logger.info(f"✅ Callback processed successfully")
            except Exception as e:
                logger.error(f"❌ Callback processing error: {e}")
                import traceback
                logger.error(f"❌ Callback traceback: {traceback.format_exc()}")
        
        return "OK", 200
        
    except Exception as e:
        logger.error(f"❌ Webhook error: {e}")
        return f"ERROR: {str(e)}", 500

def handle_start(chat_id, user_id, first_name):
    """Handle /start command"""
    logger.info(f"🎬 handle_start called: chat_id={chat_id}, user_id={user_id}")
    
    welcome_text = f"""🎬 <b>Professional Kino Bot</b>ga xush kelibsiz, {first_name}!

🔍 <b>Kino qidirish:</b>
Kino kodini yuboring (masalan: <code>#123</code>)

📊 <b>Statistika:</b> /stat
🔧 <b>Admin panel:</b> /admin (faqat admin uchun)

🎭 <b>Bot professional darajada ishlamoqda!</b>
"""
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "📊 Statistika", "callback_data": "stats"}],
            [{"text": "ℹ️ Yordam", "callback_data": "help"}]
        ]
    }
    
    logger.info(f"📤 Sending welcome message to {chat_id}")
    result = send_message_with_keyboard(chat_id, welcome_text, keyboard)
    logger.info(f"📤 Send result: {result}")

def handle_admin_menu(chat_id, user_id):
    """Handle admin menu"""
    logger.info(f"🔧 Admin menu request: user_id={user_id}, admin_id={ADMIN_ID}")
    
    if user_id != ADMIN_ID:
        logger.warning(f"❌ Non-admin access attempt: {user_id}")
        send_message(chat_id, "❌ Siz admin emassiz!")
        return
        
    logger.info(f"✅ Admin access granted for user {user_id}")
    admin_text = """🔧 <b>Professional Admin Panel</b>

📊 Batafsil statistika
🎬 Kino yuklash va boshqarish  
📢 Reklama va xabar yuborish
👥 Foydalanuvchilar boshqaruvi
⚙️ Bot sozlamalari"""

    keyboard = {
        "inline_keyboard": [
            [{"text": "📊 Statistika", "callback_data": "admin_stats"}],
            [{"text": "🎬 Kino yuklash", "callback_data": "upload_movie"}],
            [{"text": "📢 Reklama yuborish", "callback_data": "send_ad"}],
            [{"text": "👥 Foydalanuvchilar", "callback_data": "users_list"}],
            [{"text": "🗂 Kinolar ro'yxati", "callback_data": "movies_list"}]
        ]
    }
    
    result = send_message_with_keyboard(chat_id, admin_text, keyboard)
    logger.info(f"📤 Admin menu sent: {result}")

def handle_stats(chat_id, user_id):
    """Handle stats command"""
    total_users = len(users_data)
    total_movies = len(movie_codes)
    
    # Calculate active users
    current_time = int(time.time())
    day_ago = current_time - 86400
    active_today = sum(1 for user in users_data.values() 
                      if user.get('last_seen', 0) > day_ago)
    
    stats_text = f"""📊 <b>Bot Statistikasi</b>

👥 <b>Jami foydalanuvchilar:</b> {total_users}
📅 <b>Bugun faol:</b> {active_today}
🎬 <b>Jami kinolar:</b> {total_movies}
🤖 <b>Bot holati:</b> Professional ✅

💡 <b>Maslahat:</b> Kino kodlarini # belgisi bilan yuboring!"""

    send_message(chat_id, stats_text)

def handle_movie_request(chat_id, code):
    """Handle movie code request"""
    code = code.strip().lower()
    
    if code in movie_codes:
        movie_info = movie_codes[code]
        file_id = movie_info.get('file_id')
        title = movie_info.get('title', 'Noma\'lum')
        duration = movie_info.get('duration', 0)
        file_size = movie_info.get('file_size', 0)
        
        # Format file size
        if file_size > 0:
            size_mb = file_size / (1024 * 1024)
            size_text = f"\n📦 <b>Hajmi:</b> {size_mb:.1f} MB"
        else:
            size_text = ""
            
        # Format duration
        if duration > 0:
            hours = duration // 3600
            minutes = (duration % 3600) // 60
            if hours > 0:
                duration_text = f"\n⏱ <b>Davomiyligi:</b> {hours}:{minutes:02d}"
            else:
                duration_text = f"\n⏱ <b>Davomiyligi:</b> {minutes} daqiqa"
        else:
            duration_text = ""
        
        if file_id:
            caption = f"🎬 <b>{title}</b>\n\n📁 <b>Kod:</b> <code>{code}</code>{duration_text}{size_text}\n\n🎭 <b>Professional Kino Bot</b>"
            send_video(chat_id, file_id, caption)
            logger.info(f"🎬 Movie {code} sent to user {chat_id}")
        else:
            send_message(chat_id, f"❌ {code} kino fayli topilmadi!")
    else:
        available_codes = list(movie_codes.keys())[:5]  # Show first 5 codes
        codes_text = ", ".join(available_codes) if available_codes else "Hozircha mavjud emas"
        
        send_message(chat_id, f"❌ <b>{code}</b> kod topilmadi!\n\n📋 <b>Mavjud kodlar:</b> {codes_text}\n\n💡 Admin bilan bog'laning.")

def handle_regular_message(chat_id, user_id, text, message):
    """Handle regular messages (file uploads, etc.)"""
    logger.info(f"🔍 handle_regular_message: user_id={user_id}, admin_id={ADMIN_ID}")
    
    # Safely get text - could be None
    if text is None:
        text = ""
    
    # Log message details
    logger.info(f"🔍 Message details:")
    logger.info(f"  - text: '{text}'")
    logger.info(f"  - has_video: {'video' in message if message else False}")
    logger.info(f"  - has_photo: {'photo' in message if message else False}")
    logger.info(f"  - message_keys: {list(message.keys()) if message else 'None'}")
    
    # Check if admin is uploading a movie
    if user_id == ADMIN_ID:
        logger.info(f"🔧 ADMIN MESSAGE DETECTED")
        logger.info(f"🔧 Current temp_video_data: {temp_video_data}")
        logger.info(f"🔧 Chat {chat_id} in temp_video_data: {chat_id in temp_video_data}")
        
        # Check if waiting for movie title
        if chat_id in temp_video_data and temp_video_data[chat_id].get('waiting_for_title'):
            logger.info(f"📝 Processing movie title: '{text}'")
            if text and text.strip():
                finalize_movie_save(chat_id, text.strip())
            else:
                send_message(chat_id, "❌ Kino nomi bo'sh bo'lishi mumkin emas! Qayta yuboring:")
            return
            
        # Check for video upload
        if message and 'video' in message:
            logger.info(f"🎬 VIDEO DETECTED!")
            video = message['video']
            file_id = video['file_id']
            duration = video.get('duration', 0)
            file_size = video.get('file_size', 0)
            
            logger.info(f"🎬 Video details: file_id={file_id}, duration={duration}, size={file_size}")
            
            # Store temporarily
            temp_video_data[chat_id] = {
                'file_id': file_id,
                'duration': duration,
                'file_size': file_size,
                'waiting_for_code': True
            }
            
            logger.info(f"💾 STORED video data for chat {chat_id}: {temp_video_data[chat_id]}")
            
            # Format file info
            size_mb = file_size / (1024 * 1024) if file_size > 0 else 0
            hours = duration // 3600
            minutes = (duration % 3600) // 60
            
            info_text = f"🎬 <b>Video qabul qilindi!</b>\n\n"
            if size_mb > 0:
                info_text += f"📦 <b>Hajmi:</b> {size_mb:.1f} MB\n"
            if duration > 0:
                if hours > 0:
                    info_text += f"⏱ <b>Davomiyligi:</b> {hours}:{minutes:02d}\n"
                else:
                    info_text += f"⏱ <b>Davomiyligi:</b> {minutes} daqiqa\n"
            
            info_text += f"\n📝 Endi kino kodini yuboring (masalan: <code>#123</code>):"
            
            keyboard = {
                "inline_keyboard": [
                    [{"text": "❌ Bekor qilish", "callback_data": "cancel_upload"}]
                ]
            }
            
            send_result = send_message_with_keyboard(chat_id, info_text, keyboard)
            logger.info(f"📤 Video confirmation sent: {send_result}")
            return
            
        # Check for movie code (BOTH # and numbers)
        if text and (text.strip().startswith('#') or text.strip().isdigit()):
            logger.info(f"📁 MOVIE CODE DETECTED: '{text}'")
            logger.info(f"📁 Temp video data state: {temp_video_data.get(chat_id, 'NOT_FOUND')}")
            
            # Auto-add # if user sent just numbers
            if text.strip().isdigit():
                code = f"#{text.strip()}"
                logger.info(f"📁 Auto-added # to code: '{code}'")
            else:
                code = text.strip().lower()
            
            logger.info(f"📁 Final code: '{code}'")
            
            # Check if we have video data
            if chat_id in temp_video_data:
                video_data = temp_video_data[chat_id]
                logger.info(f"📁 Video data found: {video_data}")
                
                # Check if not waiting for title
                if not video_data.get('waiting_for_title', False):
                    logger.info(f"📁 Processing code for new upload")
                    
                    # Check if code already exists
                    if code in movie_codes:
                        logger.info(f"⚠️ Code '{code}' already exists, asking for replacement")
                        keyboard = {
                            "inline_keyboard": [
                                [{"text": "✅ Ha, almashtirish", "callback_data": f"replace_{code}"}],
                                [{"text": "❌ Yo'q, bekor qilish", "callback_data": "cancel_upload"}]
                            ]
                        }
                        send_message_with_keyboard(chat_id, 
                            f"⚠️ <b>{code}</b> kodi allaqachon mavjud!\n\nAlmashtirishni xohlaysizmi?", 
                            keyboard)
                    else:
                        logger.info(f"✅ New code '{code}', asking for title")
                        temp_video_data[chat_id]['code'] = code
                        temp_video_data[chat_id]['waiting_for_title'] = True
                        temp_video_data[chat_id]['waiting_for_code'] = False
                        logger.info(f"💾 Updated temp data: {temp_video_data[chat_id]}")
                        send_message(chat_id, f"📝 <b>{code}</b> kodi uchun kino nomini yuboring:")
                else:
                    logger.warning(f"❌ Already waiting for title, ignoring code")
                    send_message(chat_id, "📝 Kino nomini yuboring (kod allaqachon qabul qilindi)!")
            else:
                logger.warning(f"❌ Code '{text}' sent but no video data found")
                send_message(chat_id, "❌ Avval video yuboring, keyin kino kodini yuboring!")
            return
            
        # Handle other admin messages
        if message and 'photo' in message:
            logger.info(f"📸 Photo from admin")
            if temp_ad_data.get(chat_id, {}).get('waiting_for_ad'):
                logger.info(f"📢 Processing advertisement content")
                handle_advertisement_content(chat_id, message)
            else:
                logger.info(f"❓ Unexpected photo from admin")
                send_message(chat_id, "ℹ️ Admin komandasi tanilmadi. /admin ni bosing.")
        elif text and len(text) > 50:
            logger.info(f"📝 Long text from admin")
            if temp_ad_data.get(chat_id, {}).get('waiting_for_ad'):
                logger.info(f"📢 Processing advertisement content")
                handle_advertisement_content(chat_id, message)
            else:
                logger.info(f"❓ Unexpected long text from admin")
                send_message(chat_id, "ℹ️ Admin komandasi tanilmadi. /admin ni bosing.")
        else:
            logger.info(f"❓ Unknown admin message: '{text}'")
            send_message(chat_id, "ℹ️ Admin komandasi tanilmadi. /admin ni bosing.")
    else:
        # Regular user
        logger.info(f"👤 REGULAR USER message")
        if text and (text.strip().startswith('#') or text.strip().isdigit()):
            # Auto-add # if user sent just numbers
            if text.strip().isdigit():
                code = f"#{text.strip()}"
                logger.info(f"🎭 Auto-added # to user code: '{code}'")
            else:
                code = text.strip()
            
            logger.info(f"🎭 Movie request from user: '{code}'")
            handle_movie_request(chat_id, code)
        else:
            logger.info(f"❓ Unknown user message: '{text}'")
            send_message(chat_id, "🤔 Tushunmadim. Kino kodi yuboring (masalan: #123 yoki 123) yoki /start bosing.")

def handle_advertisement_content(chat_id, message):
    """Handle advertisement content from admin"""
    try:
        photo_id = None
        text_content = ""
        
        if 'photo' in message:
            photo_id = message['photo'][-1]['file_id']
            text_content = message.get('caption', '')
        elif 'text' in message:
            text_content = message['text']
        
        if not photo_id and not text_content:
            send_message(chat_id, "❌ Reklama matni yoki rasmi topilmadi!")
            return
            
        # Store ad content
        temp_ad_data[chat_id] = {
            'photo_id': photo_id,
            'text': text_content,
            'waiting_for_confirmation': True
        }
        
        # Show preview and confirm
        preview_text = f"📢 <b>Reklama ko'rinishi:</b>\n\n{text_content}\n\n👥 <b>{len(users_data)}</b> ta foydalanuvchiga yuborilsinmi?"
        
        keyboard = {
            "inline_keyboard": [
                [{"text": "✅ Ha, yuborish", "callback_data": "confirm_broadcast"}],
                [{"text": "❌ Bekor qilish", "callback_data": "cancel_broadcast"}]
            ]
        }
        
        if photo_id:
            send_photo_with_keyboard(chat_id, photo_id, preview_text, keyboard)
        else:
            send_message_with_keyboard(chat_id, preview_text, keyboard)
            
    except Exception as e:
        logger.error(f"❌ Advertisement content error: {e}")
        send_message(chat_id, "❌ Reklama qabul qilishda xatolik!")

def finalize_movie_save(chat_id, title):
    """Finalize saving movie"""
    try:
        if chat_id not in temp_video_data:
            send_message(chat_id, "❌ Video ma'lumotlari topilmadi!")
            return
            
        video_data = temp_video_data[chat_id]
        code = video_data.get('code')
        
        if not code:
            send_message(chat_id, "❌ Kino kodi topilmadi!")
            return
            
        # Save movie
        movie_codes[code] = {
            'file_id': video_data['file_id'],
            'title': title,
            'duration': video_data.get('duration', 0),
            'file_size': video_data.get('file_size', 0),
            'uploaded_by': ADMIN_ID,
            'upload_time': int(time.time())
        }
        
        save_data()
        
        # Clean up
        del temp_video_data[chat_id]
        
        # Success message with details
        size_mb = video_data.get('file_size', 0) / (1024 * 1024)
        duration = video_data.get('duration', 0)
        
        success_text = f"✅ <b>Kino muvaffaqiyatli saqlandi!</b>\n\n"
        success_text += f"🎬 <b>Nomi:</b> {title}\n"
        success_text += f"📁 <b>Kod:</b> <code>{code}</code>\n"
        if size_mb > 0:
            success_text += f"📦 <b>Hajmi:</b> {size_mb:.1f} MB\n"
        if duration > 0:
            hours = duration // 3600
            minutes = (duration % 3600) // 60
            if hours > 0:
                success_text += f"⏱ <b>Davomiyligi:</b> {hours}:{minutes:02d}\n"
            else:
                success_text += f"⏱ <b>Davomiyligi:</b> {minutes} daqiqa\n"
        
        success_text += f"\n🎭 <b>Professional Kino Bot</b>"
        
        send_message(chat_id, success_text)
        logger.info(f"✅ Movie {code} successfully saved: {title}")
        
    except Exception as e:
        logger.error(f"❌ Movie save error: {e}")
        send_message(chat_id, "❌ Kino saqlashda xatolik yuz berdi!")

def handle_callback_query(chat_id, user_id, callback_data, message_id):
    """Handle callback queries with improved error handling"""
    logger.info(f"🔘 Processing callback: '{callback_data}' from user {user_id}")
    logger.info(f"🔘 Admin check: user={user_id}, admin={ADMIN_ID}, is_admin={user_id == ADMIN_ID}")
    
    try:
        if callback_data == "stats":
            logger.info(f"📊 Stats callback")
            handle_stats(chat_id, user_id)
            
        elif callback_data == "help":
            logger.info(f"ℹ️ Help callback")
            help_text = """ℹ️ <b>Professional Kino Bot Yordami</b>

🔍 <b>Kino qidirish:</b>
• Kino kodini yuboring: <code>#123</code>
• Kino avtomatik yuklab olinadi

📊 <b>Komandalar:</b>
• /start - Botni qayta ishga tushirish
• /stat - Statistika ko'rish  
• /admin - Admin panel (faqat admin uchun)

🎭 <b>Professional darajada xizmat!</b>"""
            send_message(chat_id, help_text)
            
        elif callback_data == "admin_stats":
            logger.info(f"📊 Admin stats callback - checking permissions")
            if user_id == ADMIN_ID:
                logger.info(f"✅ Admin access granted for stats")
                handle_admin_stats(chat_id)
            else:
                logger.warning(f"❌ Non-admin tried to access admin stats: {user_id}")
                send_message(chat_id, "❌ Admin huquqi kerak!")
                
        elif callback_data == "upload_movie":
            logger.info(f"🎬 Upload movie callback - checking permissions")
            if user_id == ADMIN_ID:
                logger.info(f"✅ Admin upload movie request granted")
                send_message(chat_id, "🎬 Video faylni yuboring:")
            else:
                logger.warning(f"❌ Non-admin tried to upload movie: {user_id}")
                send_message(chat_id, "❌ Admin huquqi kerak!")
                
        elif callback_data == "send_ad":
            logger.info(f"📢 Send ad callback - checking permissions")
            if user_id == ADMIN_ID:
                logger.info(f"✅ Admin send ad request granted")
                handle_send_advertisement(chat_id)
            else:
                logger.warning(f"❌ Non-admin tried to send ad: {user_id}")
                send_message(chat_id, "❌ Admin huquqi kerak!")
                
        elif callback_data == "users_list":
            logger.info(f"👥 Users list callback - checking permissions")
            if user_id == ADMIN_ID:
                logger.info(f"✅ Admin users list request granted")
                handle_users_list(chat_id)
            else:
                logger.warning(f"❌ Non-admin tried to view users: {user_id}")
                send_message(chat_id, "❌ Admin huquqi kerak!")
                
        elif callback_data == "movies_list":
            logger.info(f"🗂 Movies list callback - checking permissions")
            if user_id == ADMIN_ID:
                logger.info(f"✅ Admin movies list request granted")
                handle_movies_list(chat_id)
            else:
                logger.warning(f"❌ Non-admin tried to view movies: {user_id}")
                send_message(chat_id, "❌ Admin huquqi kerak!")
                
        elif callback_data == "cancel_upload":
            logger.info(f"❌ Cancel upload callback - checking permissions")
            if user_id == ADMIN_ID:
                if chat_id in temp_video_data:
                    del temp_video_data[chat_id]
                    logger.info(f"🗑 Cleared temp video data for {chat_id}")
                send_message(chat_id, "❌ Kino yuklash bekor qilindi.")
            else:
                logger.warning(f"❌ Non-admin tried to cancel upload: {user_id}")
                send_message(chat_id, "❌ Admin huquqi kerak!")
                
        elif callback_data == "confirm_broadcast":
            logger.info(f"✅ Confirm broadcast callback - checking permissions")
            if user_id == ADMIN_ID:
                logger.info(f"✅ Admin broadcast confirm granted")
                handle_confirm_broadcast(chat_id)
            else:
                logger.warning(f"❌ Non-admin tried to confirm broadcast: {user_id}")
                send_message(chat_id, "❌ Admin huquqi kerak!")
                
        elif callback_data == "cancel_broadcast":
            logger.info(f"❌ Cancel broadcast callback - checking permissions")
            if user_id == ADMIN_ID:
                if chat_id in temp_ad_data:
                    del temp_ad_data[chat_id]
                    logger.info(f"🗑 Cleared temp ad data for {chat_id}")
                send_message(chat_id, "❌ Reklama yuborish bekor qilindi.")
            else:
                logger.warning(f"❌ Non-admin tried to cancel broadcast: {user_id}")
                send_message(chat_id, "❌ Admin huquqi kerak!")
                
        elif callback_data.startswith("replace_"):
            logger.info(f"🔄 Replace callback - checking permissions")
            if user_id == ADMIN_ID:
                code = callback_data.replace("replace_", "")
                logger.info(f"🔄 Replace code: '{code}'")
                if chat_id in temp_video_data:
                    temp_video_data[chat_id]['code'] = code
                    temp_video_data[chat_id]['waiting_for_title'] = True
                    temp_video_data[chat_id]['waiting_for_code'] = False
                    send_message(chat_id, f"📝 <b>{code}</b> kodi uchun yangi kino nomini yuboring:")
                    logger.info(f"🔄 Set replace mode for code '{code}'")
                else:
                    logger.error(f"❌ No video data found for replace operation")
                    send_message(chat_id, "❌ Video ma'lumotlari topilmadi!")
            else:
                logger.warning(f"❌ Non-admin tried to replace: {user_id}")
                send_message(chat_id, "❌ Admin huquqi kerak!")
                
        else:
            logger.warning(f"⚠️ Unknown callback: '{callback_data}'")
            send_message(chat_id, f"❓ Noma'lum buyruq: {callback_data}")
            
    except Exception as e:
        logger.error(f"❌ Callback handling error: {e}")
        import traceback
        logger.error(f"❌ Callback traceback: {traceback.format_exc()}")
        send_message(chat_id, "❌ Xatolik yuz berdi, qayta urinib ko'ring.")

def handle_send_advertisement(chat_id):
    """Handle send advertisement"""
    logger.info(f"📢 Starting advertisement handler for chat {chat_id}")
    temp_ad_data[chat_id] = {'waiting_for_ad': True}
    result = send_message(chat_id, "📢 Reklama matnini yoki rasmini yuboring:")
    logger.info(f"📢 Advertisement prompt sent: {result}")

def handle_confirm_broadcast(chat_id):
    """Handle confirm broadcast"""
    try:
        if chat_id not in temp_ad_data:
            send_message(chat_id, "❌ Reklama ma'lumotlari topilmadi!")
            return
            
        send_message(chat_id, "📡 Reklama barcha foydalanuvchilarga yuborilmoqda...")
        
        sent_count, error_count = broadcast_advertisement()
        
        result_text = f"""📊 <b>Reklama yuborish natijasi:</b>

✅ <b>Muvaffaqiyatli:</b> {sent_count}
❌ <b>Xatolik:</b> {error_count}
👥 <b>Jami:</b> {sent_count + error_count}

🎭 <b>Professional Kino Bot</b>"""

        send_message(chat_id, result_text)
        
        # Clean up
        temp_ad_data.clear()
        
    except Exception as e:
        logger.error(f"❌ Broadcast confirmation error: {e}")
        send_message(chat_id, "❌ Reklama yuborishda xatolik!")

def broadcast_advertisement():
    """Broadcast advertisement to all users"""
    try:
        if not users_data:
            return 0, 0
            
        sent_count = 0
        error_count = 0
        
        for user_id in users_data.keys():
            try:
                chat_id = int(user_id)
                ad_data = list(temp_ad_data.values())[0]  # Get first ad data
                
                if ad_data.get('photo_id'):
                    success = send_photo(chat_id, ad_data['photo_id'], ad_data['text'])
                else:
                    success = send_message(chat_id, ad_data['text'])
                
                if success:
                    sent_count += 1
                else:
                    error_count += 1
                    
                # Small delay to avoid rate limiting
                time.sleep(0.05)
                
            except Exception as e:
                logger.error(f"❌ Broadcast error for user {user_id}: {e}")
                error_count += 1
                
        return sent_count, error_count
        
    except Exception as e:
        logger.error(f"❌ Broadcast error: {e}")
        return 0, 1

def handle_admin_stats(chat_id):
    """Handle admin stats"""
    try:
        total_users = len(users_data)
        total_movies = len(movie_codes)
        
        # Get recent users
        current_time = int(time.time())
        day_ago = current_time - 86400
        week_ago = current_time - 604800
        
        daily_users = sum(1 for user in users_data.values() 
                         if user.get('last_seen', 0) > day_ago)
        weekly_users = sum(1 for user in users_data.values() 
                          if user.get('last_seen', 0) > week_ago)
        
        # Calculate total file size
        total_size = sum(movie.get('file_size', 0) for movie in movie_codes.values())
        total_size_mb = total_size / (1024 * 1024)
        
        stats_text = f"""📊 <b>Professional Admin Statistika</b>

👥 <b>Foydalanuvchilar:</b>
• Jami: {total_users}
• Bugun faol: {daily_users}
• Haftalik faol: {weekly_users}

🎬 <b>Kinolar:</b>
• Jami: {total_movies}
• Umumiy hajmi: {total_size_mb:.1f} MB

💾 <b>Ma'lumotlar:</b>
• Users: {len(users_data)} ta yozuv
• Movies: {len(movie_codes)} ta yozuv
• Temp uploads: {len(temp_video_data)}
• Pending ads: {len(temp_ad_data)}

🎭 <b>Professional Kino Bot</b>"""

        send_message(chat_id, stats_text)
    except Exception as e:
        logger.error(f"❌ Admin stats error: {e}")
        send_message(chat_id, "❌ Statistika olishda xatolik!")

def handle_users_list(chat_id):
    """Handle users list"""
    try:
        if not users_data:
            send_message(chat_id, "📋 Hozircha foydalanuvchilar yo'q.")
            return
            
        users_text = "👥 <b>Professional Foydalanuvchilar ro'yxati:</b>\n\n"
        
        # Sort users by last_seen
        sorted_users = sorted(users_data.items(), 
                            key=lambda x: x[1].get('last_seen', 0), 
                            reverse=True)
        
        count = 0
        for user_id, user_info in sorted_users:
            count += 1
            username = user_info.get('username', 'username yo\'q')
            first_name = user_info.get('first_name', 'Noma\'lum')
            last_seen = user_info.get('last_seen', 0)
            
            # Format last seen
            if last_seen > 0:
                time_diff = int(time.time()) - last_seen
                if time_diff < 300:  # 5 minutes
                    status = "🟢 Faol"
                elif time_diff < 3600:  # 1 hour
                    status = f"🟡 {time_diff//60} daqiqa oldin"
                elif time_diff < 86400:  # 1 day
                    status = f"🟠 {time_diff//3600} soat oldin"
                else:
                    status = f"🔴 {time_diff//86400} kun oldin"
            else:
                status = "⚪️ Noma'lum"
            
            users_text += f"{count}. {first_name} (@{username})\n"
            users_text += f"   ID: <code>{user_id}</code> | {status}\n\n"
            
            if count >= 15:  # Limit to 15 users per message
                break
        
        if len(users_data) > 15:
            users_text += f"... va yana {len(users_data) - 15} ta foydalanuvchi\n\n"
        
        users_text += "🎭 <b>Professional Kino Bot</b>"
        
        send_message(chat_id, users_text)
    except Exception as e:
        logger.error(f"❌ Users list error: {e}")
        send_message(chat_id, "❌ Foydalanuvchilar ro'yxatini olishda xatolik!")

def handle_movies_list(chat_id):
    """Handle movies list for admin"""
    try:
        if not movie_codes:
            send_message(chat_id, "📋 Hozircha kinolar yo'q.")
            return
            
        movies_text = "🎬 <b>Professional Kinolar ro'yxati:</b>\n\n"
        
        # Sort movies by upload time
        sorted_movies = sorted(movie_codes.items(), 
                             key=lambda x: x[1].get('upload_time', 0), 
                             reverse=True)
        
        count = 0
        total_size = 0
        for code, movie_info in sorted_movies:
            count += 1
            title = movie_info.get('title', 'Noma\'lum')
            file_size = movie_info.get('file_size', 0)
            duration = movie_info.get('duration', 0)
            
            total_size += file_size
            size_mb = file_size / (1024 * 1024) if file_size > 0 else 0
            
            movies_text += f"{count}. <b>{title}</b>\n"
            movies_text += f"   📁 <code>{code}</code>"
            if size_mb > 0:
                movies_text += f" | 📦 {size_mb:.1f} MB"
            if duration > 0:
                hours = duration // 3600
                minutes = (duration % 3600) // 60
                if hours > 0:
                    movies_text += f" | ⏱ {hours}:{minutes:02d}"
                else:
                    movies_text += f" | ⏱ {minutes}min"
            movies_text += "\n\n"
            
            if count >= 10:  # Limit to 10 movies per message
                break
        
        if len(movie_codes) > 10:
            movies_text += f"... va yana {len(movie_codes) - 10} ta kino\n\n"
        
        total_size_mb = total_size / (1024 * 1024)
        movies_text += f"💾 <b>Jami hajmi:</b> {total_size_mb:.1f} MB\n"
        movies_text += f"🎭 <b>Professional Kino Bot</b>"
        
        send_message(chat_id, movies_text)
    except Exception as e:
        logger.error(f"❌ Movies list error: {e}")
        send_message(chat_id, "❌ Kinolar ro'yxatini olishda xatolik!")

def setup_webhook():
    """Setup webhook on startup"""
    try:
        webhook_url = os.getenv('RENDER_EXTERNAL_URL')
        if webhook_url:
            webhook_url = f"{webhook_url}/webhook"
            
            response = requests.post(
                f"https://api.telegram.org/bot{TOKEN}/setWebhook",
                data={"url": webhook_url}
            )
            result = response.json()
            
            if result.get('ok'):
                logger.info(f"✅ Professional webhook set: {webhook_url}")
            else:
                logger.error(f"❌ Webhook error: {result}")
        else:
            logger.warning("⚠️ No RENDER_EXTERNAL_URL found")
            
    except Exception as e:
        logger.error(f"❌ Webhook setup error: {e}")

# Load data on startup
load_data()

# Setup webhook on module import (for gunicorn)
setup_webhook()

# For gunicorn compatibility
application = app

if __name__ == "__main__":
    logger.info("🎭 Starting Professional Kino Bot on Render...")
    
    # Start server
    port = int(os.environ.get('PORT', 8080))
    logger.info(f"🚀 Professional server starting on port {port}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )
