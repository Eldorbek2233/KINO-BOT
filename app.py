#!/usr/bin/env python3
"""
Full Kino Bot for Render - Complete functionality
"""

import os
import sys
import logging
import json
from flask import Flask, request, jsonify

#        # Process callback queries
        elif 'callback_query' in data:
            callback = data['callback_query']
            chat_id = callback.get('message', {}).get('chat', {}).get('id')
            user_id = callback.get('from', {}).get('id')
            callback_data = callback.get('data', '')
            message_id = callback.get('message', {}).get('message_id')
            callback_id = callback.get('id')
            
            logger.info(f"🔘 Callback received: data='{callback_data}', user={user_id}, chat={chat_id}")
            logger.info(f"🔘 Full callback object: {callback}")
            
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
                logger.error(f"❌ Callback traceback: {traceback.format_exc()}")ing
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
    import time
    users_data[str(user_id)] = {
        'username': username,
        'first_name': first_name,
        'last_seen': int(time.time())
    }
    logger.info(f"👤 Saved user: {user_id} ({first_name})")
    save_data()

def send_message_with_keyboard(chat_id, text, keyboard=None):
    """Send message with inline keyboard"""
    try:
        import requests
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        
        if keyboard:
            keyboard_json = json.dumps(keyboard)
            data["reply_markup"] = keyboard_json
            logger.info(f"⌨️ Sending keyboard: {keyboard_json}")
            
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
        import traceback
        logger.error(f"❌ Traceback: {traceback.format_exc()}")
        return False

@app.route('/')
def home():
    """Health check"""
    return jsonify({
        "status": "ok", 
        "message": "Kino Bot is running on Render!",
        "platform": "render",
        "webhook_ready": True,
        "token_length": len(TOKEN) if TOKEN else 0,
        "entry_point": "app.py via gunicorn"
    })

@app.route('/debug')
def debug():
    """Debug endpoint"""
    return jsonify({
        "token_present": bool(TOKEN),
        "token_length": len(TOKEN) if TOKEN else 0,
        "admin_id": ADMIN_ID,
        "webhook_url": f"{os.getenv('RENDER_EXTERNAL_URL', 'unknown')}/webhook",
        "users_count": len(users_data),
        "movies_count": len(movie_codes),
        "temp_video_data": list(temp_video_data.keys()),
        "temp_ad_data": list(temp_ad_data.keys())
    })

@app.route('/test_keyboard')
def test_keyboard():
    """Test keyboard endpoint"""
    test_keyboard = {
        "inline_keyboard": [
            [{"text": "✅ Test Button", "callback_data": "test_callback"}]
        ]
    }
    return jsonify({
        "keyboard": test_keyboard,
        "keyboard_json": json.dumps(test_keyboard)
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Full webhook handler with all bot functionality"""
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
            text = message.get('text', '')
            
            logger.info(f"� Message from {user_id} ({username}): {text}")
            
            # Save user
            save_user(user_id, username, first_name)
            
            # Process commands
            if text == '/start':
                logger.info(f"🎬 Processing /start for user {user_id}")
                handle_start(chat_id, user_id, first_name)
            elif text == '/admin':
                logger.info(f"🔧 Processing /admin for user {user_id}")
                handle_admin_menu(chat_id, user_id)
            elif text == '/stat':
                logger.info(f"📊 Processing /stat for user {user_id}")
                handle_stats(chat_id, user_id)
            elif text.startswith('#'):
                logger.info(f"🎭 Processing movie request {text} for user {user_id}")
                handle_movie_request(chat_id, text)
            else:
                logger.info(f"💬 Processing regular message for user {user_id}")
                # Check if waiting for input
                handle_regular_message(chat_id, user_id, text, message)
                
        # Process callback queries
        elif 'callback_query' in data:
            callback = data['callback_query']
            chat_id = callback.get('message', {}).get('chat', {}).get('id')
            user_id = callback.get('from', {}).get('id')
            callback_data = callback.get('data', '')
            message_id = callback.get('message', {}).get('message_id')
            
            logger.info(f"� Callback from {user_id}: {callback_data}")
            
            # Answer callback query
            answer_callback_query(callback.get('id'))
            
            # Process callback
            handle_callback_query(chat_id, user_id, callback_data, message_id)
        
        return "OK", 200
        
    except Exception as e:
        logger.error(f"❌ Webhook error: {e}")
        import traceback
        logger.error(f"❌ Traceback: {traceback.format_exc()}")
        return f"ERROR: {str(e)}", 500

def handle_start(chat_id, user_id, first_name):
    """Handle /start command"""
    logger.info(f"🎬 handle_start called: chat_id={chat_id}, user_id={user_id}, first_name={first_name}")
    
    welcome_text = f"""🎬 <b>Kino Bot</b>ga xush kelibsiz, {first_name}!

🔍 <b>Kino qidirish:</b>
Kino kodini yuboring (masalan: <code>#123</code>)

📊 <b>Statistika:</b> /stat

🎭 <b>Bot ishlamoqda va tayyor!</b>
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
    if user_id != ADMIN_ID:
        send_message(chat_id, "❌ Siz admin emassiz!")
        return
        
    admin_text = """🔧 <b>Admin Panel</b>

📊 Statistika
🎬 Kino joylash  
📢 Reklama yuborish
👥 Foydalanuvchilar"""

    keyboard = {
        "inline_keyboard": [
            [{"text": "📊 Statistika", "callback_data": "admin_stats"}],
            [{"text": "🎬 Kino joylash", "callback_data": "upload_movie"}],
            [{"text": "📢 Reklama yuborish", "callback_data": "send_ad"}],
            [{"text": "👥 Foydalanuvchilar", "callback_data": "users_list"}]
        ]
    }
    
    send_message_with_keyboard(chat_id, admin_text, keyboard)

def handle_stats(chat_id, user_id):
    """Handle stats command"""
    total_users = len(users_data)
    total_movies = len(movie_codes)
    
    stats_text = f"""📊 <b>Bot Statistikasi</b>

👥 <b>Foydalanuvchilar:</b> {total_users}
🎬 <b>Kinolar:</b> {total_movies}
🤖 <b>Bot holati:</b> Ishlamoqda ✅"""

    send_message(chat_id, stats_text)

def handle_movie_request(chat_id, code):
    """Handle movie code request"""
    code = code.strip().lower()
    
    if code in movie_codes:
        movie_info = movie_codes[code]
        file_id = movie_info.get('file_id')
        title = movie_info.get('title', 'Noma\'lum')
        
        if file_id:
            send_video(chat_id, file_id, f"🎬 <b>{title}</b>\n\n📁 Kod: <code>{code}</code>")
        else:
            send_message(chat_id, f"❌ {code} kino fayli topilmadi!")
    else:
        send_message(chat_id, f"❌ {code} kod topilmadi!\n\nMavjud kodlar uchun admin bilan bog'laning.")

def handle_regular_message(chat_id, user_id, text, message):
    """Handle regular messages (file uploads, etc.)"""
    logger.info(f"🔍 handle_regular_message: user_id={user_id}, admin_id={ADMIN_ID}, text='{text[:20]}...'")
    
    # Check if admin is uploading a movie
    if user_id == ADMIN_ID:
        logger.info(f"🔧 Admin message detected")
        
        # Check if waiting for movie title
        if chat_id in temp_video_data and temp_video_data[chat_id].get('waiting_for_title'):
            logger.info(f"📝 Processing movie title: {text}")
            finalize_movie_save(chat_id, text)
            return
            
        if 'video' in message:
            logger.info(f"🎬 Video detected: {message['video']['file_id']}")
            # Admin sent a video - ask for movie code
            video = message['video']
            file_id = video['file_id']
            duration = video.get('duration', 0)
            file_size = video.get('file_size', 0)
            
            # Store temporarily
            temp_video_data[chat_id] = {
                'file_id': file_id,
                'duration': duration,
                'file_size': file_size
            }
            
            logger.info(f"💾 Stored video data for chat {chat_id}")
            
            keyboard = {
                "inline_keyboard": [
                    [{"text": "❌ Bekor qilish", "callback_data": "cancel_upload"}]
                ]
            }
            
            send_message_with_keyboard(chat_id, 
                "🎬 Video qabul qilindi!\n\n📝 Endi kino kodini yuboring (masalan: #123):", 
                keyboard)
        elif text.startswith('#') and chat_id in temp_video_data and not temp_video_data[chat_id].get('waiting_for_title'):
            logger.info(f"📁 Processing movie code: {text}")
            # Admin sent movie code after video
            code = text.strip().lower()
            temp_video_data[chat_id]['code'] = code
            temp_video_data[chat_id]['waiting_for_title'] = True
            send_message(chat_id, f"📝 {code} kodi uchun kino nomini yuboring:")
        elif 'photo' in message or (message.get('text') and len(message.get('text', '')) > 10):
            # Admin might be sending advertisement
            if temp_ad_data.get(chat_id, {}).get('waiting_for_ad'):
                logger.info(f"📢 Processing advertisement content")
                handle_advertisement_content(chat_id, message)
            else:
                send_message(chat_id, "ℹ️ Admin komandasi tanilmadi. /admin ni bosing.")
        else:
            logger.info(f"❓ Unknown admin message")
            send_message(chat_id, "ℹ️ Admin komandasi tanilmadi. /admin ni bosing.")
    else:
        send_message(chat_id, "🤔 Tushunmadim. Kino kodi yuboring (masalan: #123) yoki /start bosing.")

# Temporary storage for advertisements
temp_ad_data = {}

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
        preview_text = f"📢 <b>Reklama ko'rinishi:</b>\n\n{text_content}\n\n✅ Barcha foydalanuvchilarga yuborilsinmi?"
        
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

def send_photo_with_keyboard(chat_id, photo_id, caption, keyboard=None):
    """Send photo with keyboard"""
    try:
        import requests
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
                import time
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"❌ Broadcast error for user {user_id}: {e}")
                error_count += 1
                
        return sent_count, error_count
        
    except Exception as e:
        logger.error(f"❌ Broadcast error: {e}")
        return 0, 1

def send_photo(chat_id, photo_id, caption=""):
    """Send photo"""
    try:
        import requests
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

def handle_callback_query(chat_id, user_id, callback_data, message_id):
    """Handle callback queries"""
    logger.info(f"🔘 Processing callback: {callback_data} from user {user_id}")
    
    try:
        if callback_data == "stats":
            handle_stats(chat_id, user_id)
        elif callback_data == "help":
            help_text = """ℹ️ <b>Yordam</b>

🔍 <b>Kino qidirish:</b>
• Kino kodini yuboring: <code>#123</code>
• Kino yuklab olinadi

📊 <b>Komandalar:</b>
• /start - Botni qayta ishga tushirish
• /stat - Statistika ko'rish
• /admin - Admin panel (faqat admin uchun)"""
            send_message(chat_id, help_text)
        elif callback_data == "admin_stats" and user_id == ADMIN_ID:
            handle_admin_stats(chat_id)
        elif callback_data == "upload_movie" and user_id == ADMIN_ID:
            logger.info(f"🎬 Admin clicked upload_movie")
            send_message(chat_id, "🎬 Video faylni yuboring:")
        elif callback_data == "send_ad" and user_id == ADMIN_ID:
            handle_send_advertisement(chat_id)
        elif callback_data == "users_list" and user_id == ADMIN_ID:
            handle_users_list(chat_id)
        elif callback_data == "cancel_upload" and user_id == ADMIN_ID:
            if chat_id in temp_video_data:
                del temp_video_data[chat_id]
            send_message(chat_id, "❌ Kino yuklash bekor qilindi.")
        elif callback_data == "confirm_broadcast" and user_id == ADMIN_ID:
            handle_confirm_broadcast(chat_id)
        elif callback_data == "cancel_broadcast" and user_id == ADMIN_ID:
            if chat_id in temp_ad_data:
                del temp_ad_data[chat_id]
            send_message(chat_id, "❌ Reklama yuborish bekor qilindi.")
        elif callback_data == "test_callback":
            send_message(chat_id, "✅ Test callback ishlayapti!")
        else:
            logger.warning(f"⚠️ Unknown callback: {callback_data}")
            # Send a response even for unknown callbacks
            send_message(chat_id, f"❓ Noma'lum buyruq: {callback_data}")
    except Exception as e:
        logger.error(f"❌ Callback handling error: {e}")
        import traceback
        logger.error(f"❌ Callback traceback: {traceback.format_exc()}")
        send_message(chat_id, "❌ Xatolik yuz berdi, qayta urinib ko'ring.")

def handle_send_advertisement(chat_id):
    """Handle send advertisement"""
    temp_ad_data[chat_id] = {'waiting_for_ad': True}
    send_message(chat_id, "📢 Reklama matnini yoki rasmini yuboring:")

def handle_confirm_broadcast(chat_id):
    """Handle confirm broadcast"""
    try:
        if chat_id not in temp_ad_data:
            send_message(chat_id, "❌ Reklama ma'lumotlari topilmadi!")
            return
            
        send_message(chat_id, "📡 Reklama yuborilmoqda...")
        
        sent_count, error_count = broadcast_advertisement()
        
        result_text = f"""📊 <b>Reklama yuborish natijasi:</b>

✅ <b>Muvaffaqiyatli:</b> {sent_count}
❌ <b>Xatolik:</b> {error_count}
👥 <b>Umumiy:</b> {sent_count + error_count}"""

        send_message(chat_id, result_text)
        
        # Clean up
        temp_ad_data.clear()
        
    except Exception as e:
        logger.error(f"❌ Broadcast confirmation error: {e}")
        send_message(chat_id, "❌ Reklama yuborishda xatolik!")

def handle_admin_stats(chat_id):
    """Handle admin stats"""
    total_users = len(users_data)
    total_movies = len(movie_codes)
    
    # Get recent users
    import time
    current_time = int(time.time())
    day_ago = current_time - 86400
    week_ago = current_time - 604800
    
    daily_users = sum(1 for user in users_data.values() 
                     if user.get('last_seen', 0) > day_ago)
    weekly_users = sum(1 for user in users_data.values() 
                      if user.get('last_seen', 0) > week_ago)
    
    stats_text = f"""📊 <b>Admin Statistika</b>

👥 <b>Umumiy foydalanuvchilar:</b> {total_users}
📅 <b>Bugun faol:</b> {daily_users}
📆 <b>Haftalik faol:</b> {weekly_users}
🎬 <b>Umumiy kinolar:</b> {total_movies}

💾 <b>Ma'lumotlar:</b>
• Users: {len(users_data)} ta yozuv
• Movies: {len(movie_codes)} ta yozuv"""

    send_message(chat_id, stats_text)

def handle_users_list(chat_id):
    """Handle users list"""
    if not users_data:
        send_message(chat_id, "📋 Hozircha foydalanuvchilar yo'q.")
        return
        
    users_text = "👥 <b>Foydalanuvchilar ro'yxati:</b>\n\n"
    
    count = 0
    for user_id, user_info in users_data.items():
        count += 1
        username = user_info.get('username', 'username yo\'q')
        first_name = user_info.get('first_name', 'Noma\'lum')
        
        users_text += f"{count}. {first_name} (@{username})\n"
        users_text += f"   ID: <code>{user_id}</code>\n\n"
        
        if count >= 20:  # Limit to 20 users per message
            break
    
    if len(users_data) > 20:
        users_text += f"... va yana {len(users_data) - 20} ta foydalanuvchi"
    
    send_message(chat_id, users_text)

# Temporary storage for video uploads
temp_video_data = {}

def save_movie_with_code(chat_id, code):
    """Save movie with code"""
    if chat_id not in temp_video_data:
        send_message(chat_id, "❌ Avval video yuboring!")
        return
        
    code = code.strip().lower()
    video_data = temp_video_data[chat_id]
    
    # Ask for movie title
    send_message(chat_id, f"📝 {code} kodi uchun kino nomini yuboring:")
    
    # Store for title input
    temp_video_data[chat_id]['code'] = code
    temp_video_data[chat_id]['waiting_for_title'] = True

def finalize_movie_save(chat_id, title):
    """Finalize saving movie"""
    if chat_id not in temp_video_data:
        return
        
    video_data = temp_video_data[chat_id]
    code = video_data.get('code')
    
    if not code:
        return
        
    # Save movie
    import time
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
    
    send_message(chat_id, f"✅ Kino muvaffaqiyatli saqlandi!\n\n🎬 <b>{title}</b>\n📁 Kod: <code>{code}</code>")

def send_video(chat_id, file_id, caption=""):
    """Send video file"""
    try:
        import requests
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

def answer_callback_query(callback_query_id, text=""):
    """Answer callback query"""
    try:
        import requests
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

# Load data on startup
load_data()
import time

def send_message(chat_id, text):
    """Send message via Telegram API"""
    try:
        if not TOKEN:
            logger.error("❌ No TOKEN available")
            return False
            
        import requests
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
        import traceback
        logger.error(f"❌ Traceback: {traceback.format_exc()}")
        return False

def setup_webhook():
    """Setup webhook on startup"""
    try:
        webhook_url = os.getenv('RENDER_EXTERNAL_URL')
        if webhook_url:
            webhook_url = f"{webhook_url}/webhook"
            
            import requests
            response = requests.post(
                f"https://api.telegram.org/bot{TOKEN}/setWebhook",
                data={"url": webhook_url}
            )
            result = response.json()
            
            if result.get('ok'):
                logger.info(f"✅ Webhook set: {webhook_url}")
            else:
                logger.error(f"❌ Webhook error: {result}")
        else:
            logger.warning("⚠️ No RENDER_EXTERNAL_URL found")
            
    except Exception as e:
        logger.error(f"❌ Webhook setup error: {e}")

# Setup webhook on module import (for gunicorn)
setup_webhook()

# For gunicorn compatibility
application = app

if __name__ == "__main__":
    logger.info("🎭 Starting Kino Bot on Render via app.py...")
    
    # Start server
    port = int(os.environ.get('PORT', 8080))
    logger.info(f"🚀 Server starting on port {port}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )
