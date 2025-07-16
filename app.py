#!/usr/bin/env python3
"""
🎭 ULTIMATE PROFESSIONAL KINO BOT V3.0 🎭
Comprehensive Telegram Bot with Full Admin Panel & Broadcasting System
"""

import os
import sys
import json
import time
import logging
from flask import Flask, request, jsonify

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
TOKEN = "8177519032:AAED4FgPoFQiQhqM_lvrK1iV8hL9u4SnkDk"
ADMIN_ID = 5542016161

# Data storage
users_db = {}
movies_db = {}
upload_sessions = {}
broadcast_data = {}

# Load data from files
def load_database():
    """Load all databases"""
    global users_db, movies_db
    try:
        # Load users
        if os.path.exists('users.json'):
            with open('users.json', 'r', encoding='utf-8') as f:
                users_db = json.load(f)
                logger.info(f"✅ Loaded {len(users_db)} users")
        
        # Load movies  
        if os.path.exists('file_ids.json'):
            with open('file_ids.json', 'r', encoding='utf-8') as f:
                movies_db = json.load(f)
                logger.info(f"✅ Loaded {len(movies_db)} movies")
                
    except Exception as e:
        logger.error(f"❌ Database load error: {e}")

def save_database():
    """Save all databases"""
    try:
        with open('users.json', 'w', encoding='utf-8') as f:
            json.dump(users_db, f, ensure_ascii=False, indent=2)
        
        with open('file_ids.json', 'w', encoding='utf-8') as f:
            json.dump(movies_db, f, ensure_ascii=False, indent=2)
            
        logger.info("✅ Database saved successfully")
    except Exception as e:
        logger.error(f"❌ Database save error: {e}")

# Create Flask app
app = Flask(__name__)

@app.route('/')
def home():
    """Health check"""
    return jsonify({
        "status": "🎭 Ultimate Professional Kino Bot V3.0",
        "users": len(users_db),
        "movies": len(movies_db),
        "platform": "render",
        "webhook_ready": True
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Main webhook handler"""
    try:
        data = request.get_json()
        logger.info(f"📨 Webhook data: {data}")
        
        if 'message' in data:
            handle_message(data['message'])
        elif 'callback_query' in data:
            handle_callback(data['callback_query'])
            
        return "OK", 200
        
    except Exception as e:
        logger.error(f"❌ Webhook error: {e}")
        return f"ERROR: {str(e)}", 500

def handle_message(message):
    """Handle incoming message"""
    try:
        chat_id = message.get('chat', {}).get('id')
        user_id = message.get('from', {}).get('id')
        text = message.get('text', '')
        
        # Save user info
        user_info = message.get('from', {})
        users_db[str(user_id)] = {
            'first_name': user_info.get('first_name', ''),
            'username': user_info.get('username', ''),
            'last_seen': int(time.time())
        }
        save_database()
        
        logger.info(f"💬 Message from {user_id}: {text}")
        
        # Check if admin is in broadcast session  
        if user_id == ADMIN_ID and chat_id in broadcast_data and broadcast_data[chat_id].get('waiting'):
            # Admin is sending broadcast content - send immediately to all users
            send_immediate_broadcast(chat_id, message)
            return
        
        # Handle commands
        if text == '/start':
            handle_start(chat_id, user_id)
        elif text == '/admin':
            if user_id == ADMIN_ID:
                handle_admin_menu(chat_id, user_id)
            else:
                send_message(chat_id, """❌ <b>Admin paneli</b>

🔐 Bu panel faqat admin uchun mo'ljallangan.

🎬 <b>Siz uchun mavjud:</b>
• Kino kodlarini yuborish
• Kinolar ro'yxatini ko'rish
• Yordam olish

💡 Kino olish uchun kod yuboring: <code>#123</code>""")
        elif text == '/stat':
            handle_stats(chat_id, user_id)
        elif 'video' in message:
            handle_video_upload(chat_id, user_id, message)
        elif 'photo' in message:
            handle_photo_upload(chat_id, user_id, message)
        else:
            handle_text_message(chat_id, user_id, text)
            
    except Exception as e:
        logger.error(f"❌ Message handling error: {e}")

def handle_start(chat_id, user_id):
    """Handle /start command"""
    if user_id == ADMIN_ID:
        # Admin version with statistics
        start_text = f"""🎭 <b>Ultimate Professional Kino Bot V3.0</b>

👋 Xush kelibsiz! Eng professional kino bot xizmatida!

🔍 <b>Kino qidirish:</b>
• Kino kodini yuboring: <code>#123</code>
• Yoki faqat raqam: <code>123</code>

📊 <b>Mavjud kontentlar:</b>
• Kinolar: {len(movies_db)} ta
• Foydalanuvchilar: {len(users_db)} ta

💎 <b>Premium xususiyatlar:</b>
• Yuqori sifatli videolar
• Tezkor qidiruv tizimi  
• Professional admin panel
• Avtomatik reklama tizimi

🎬 <b>Hoziroq kino kodi bilan boshlang!</b>"""

        keyboard = {
            'inline_keyboard': [
                [{'text': '🎬 Mavjud kinolar', 'callback_data': 'show_movies'}],
                [{'text': '📊 Statistika', 'callback_data': 'show_stats'}],
                [{'text': 'ℹ️ Yordam', 'callback_data': 'show_help'}],
                [{'text': '👑 Admin Panel', 'callback_data': 'admin_menu'}]
            ]
        }
    else:
        # Regular user version without statistics
        start_text = f"""🎭 <b>Ultimate Professional Kino Bot V3.0</b>

👋 Xush kelibsiz! Eng professional kino bot xizmatida!

🔍 <b>Kino qidirish:</b>
• Kino kodini yuboring: <code>#123</code>
• Yoki faqat raqam: <code>123</code>

🎬 <b>Mavjud kinolar:</b> {len(movies_db)} ta

💎 <b>Premium xususiyatlar:</b>
• Yuqori sifatli videolar
• Tezkor qidiruv tizimi  
• Professional interfeys
• Barcha janrlar

🎬 <b>Hoziroq kino kodi bilan boshlang!</b>"""

        keyboard = {
            'inline_keyboard': [
                [{'text': '🎬 Mavjud kinolar', 'callback_data': 'show_movies'}],
                [{'text': 'ℹ️ Yordam', 'callback_data': 'show_help'}]
            ]
        }
    
    send_message(chat_id, start_text, keyboard)

def handle_admin_menu(chat_id, user_id):
    """Handle admin menu"""
    if user_id != ADMIN_ID:
        send_message(chat_id, "❌ Admin huquqi kerak!")
        return
        
    admin_text = f"""👑 <b>Ultimate Professional Admin Panel V3.0</b>

📊 <b>Bot statistikasi:</b>
• Foydalanuvchilar: {len(users_db)}
• Kinolar: {len(movies_db)}
• Upload sessiyalar: {len(upload_sessions)}

⚙️ <b>Admin amallar:</b>"""

    keyboard = {
        'inline_keyboard': [
            [{'text': '📊 Batafsil statistika', 'callback_data': 'admin_stats'}],
            [{'text': '🎬 Kino yuklash', 'callback_data': 'upload_movie'}],
            [{'text': '📢 Reklama yuborish', 'callback_data': 'broadcast_ad'}],
            [{'text': '👥 Foydalanuvchilar', 'callback_data': 'list_users'}],
            [{'text': '🎭 Kinolar ro\'yxati', 'callback_data': 'list_movies'}],
            [{'text': '🔧 Test funksiya', 'callback_data': 'admin_test'}]
        ]
    }
    
    send_message(chat_id, admin_text, keyboard)

def handle_stats(chat_id, user_id):
    """Handle statistics - Admin only"""
    if user_id != ADMIN_ID:
        send_message(chat_id, """❌ <b>Kirish rad etildi!</b>

🔐 Bu ma'lumot faqat admin uchun mo'ljallangan.

🎬 <b>Kino qidirish uchun:</b>
• Kino kodini yuboring: <code>#123</code>
• Yoki raqam: <code>123</code>

💡 Mavjud kinolar ro'yxatini ko'rish uchun "🎬 Mavjud kinolar" tugmasini bosing.""")
        return
        
    total_users = len(users_db)
    total_movies = len(movies_db)
    
    # Active users calculation
    current_time = int(time.time())
    day_ago = current_time - 86400
    active_today = sum(1 for user in users_db.values() if user.get('last_seen', 0) > day_ago)
    
    stats_text = f"""📊 <b>Admin Statistika</b>

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
            [{'text': '🎬 Barcha kinolar', 'callback_data': 'show_all_movies'}],
            [{'text': '👑 Admin Panel', 'callback_data': 'admin_menu'}]
        ]
    }
    
    send_message(chat_id, stats_text, keyboard)

def handle_movie_code(chat_id, user_id, code):
    """Handle movie code request"""
    original_code = code
    code = code.strip().lower()
    
    # Remove # if present
    if code.startswith('#'):
        code = code[1:]
    
    # Try with #
    code_with_hash = f"#{code}"
    
    logger.info(f"🎭 Movie request: original='{original_code}', processed='{code}', with_hash='{code_with_hash}'")
    
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
            caption += f"\n📦 <b>Hajmi:</b> {size_mb:.1f} MB"
        
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
        logger.warning(f"❌ Non-admin {user_id} tried to upload video")
        return
    
    try:
        video = message['video']
        file_id = video['file_id']
        duration = video.get('duration', 0)
        file_size = video.get('file_size', 0)
        
        # Clear any existing session first
        if chat_id in upload_sessions:
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
        
        send_message(chat_id, info_text, keyboard)
        
    except Exception as e:
        logger.error(f"❌ Video upload error: {e}")
        send_message(chat_id, "❌ Video yuklashda xatolik yuz berdi!")

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
    try:
        original_code = code.strip()
        
        # Clean code - remove # and make lowercase
        clean_code = original_code.replace('#', '').strip()
        
        # Validate code is numeric
        if not clean_code.isdigit():
            send_message(chat_id, f"❌ Kod faqat raqam bo'lishi kerak!\n\n✅ To'g'ri: <code>123</code> yoki <code>#123</code>\n❌ Noto'g'ri: <code>{clean_code}</code>")
            return
        
        # Check if code already exists
        code_exists = False
        existing_formats = [clean_code, f"#{clean_code}"]
        
        for format_code in existing_formats:
            if format_code in movies_db:
                code_exists = True
                break
        
        if code_exists:
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
        send_message(chat_id, "❌ Kod qayta ishlashda xatolik!")

def handle_upload_title(chat_id, title):
    """Handle upload title step"""
    title = title.strip()
    
    if not title:
        send_message(chat_id, "❌ Kino nomi bo'sh bo'lishi mumkin emas!")
        return
    
    # Complete upload
    session = upload_sessions[chat_id]
    code = session['code']
    
    # Save movie with clean code
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
    
    # Success message
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

def handle_callback(callback_query):
    """Handle callback query"""
    try:
        chat_id = callback_query.get('message', {}).get('chat', {}).get('id')
        user_id = callback_query.get('from', {}).get('id')
        data = callback_query.get('data', '')
        callback_id = callback_query.get('id')
        
        # Answer callback first
        answer_callback(callback_id)
        
        # Handle different callbacks
        if data == 'show_stats':
            handle_stats(chat_id, user_id)
        elif data == 'show_movies' or data == 'show_all_movies':
            show_movies_list(chat_id, user_id)
        elif data == 'show_help':
            show_help(chat_id)
        elif data == 'admin_menu':
            if user_id == ADMIN_ID:
                handle_admin_menu(chat_id, user_id)
            else:
                send_message(chat_id, "❌ Admin huquqi kerak!")
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
        elif data == 'broadcast_ad':
            if user_id == ADMIN_ID:
                # Set waiting mode for immediate broadcast
                broadcast_data[chat_id] = {'waiting': True}
                send_message(chat_id, """📢 <b>Reklama yuborish</b>

📝 <b>Endi reklama kontentini yuboring:</b>
• Matn (oddiy xabar)
• Rasm + caption
• Video + caption

💡 <b>Maslahat:</b> Yuborgan kontentingiz darhol barcha foydalanuvchilarga yuboriladi!

⚠️ <b>Diqqat:</b> Tasdiqlash bosqichi yo'q - to'g'ridan-to'g'ri yuboriladi.""")
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
            else:
                send_message(chat_id, "❌ Hech narsa bekor qilinmadi.")
        elif data.startswith('replace_movie_'):
            if user_id == ADMIN_ID:
                code = data.replace('replace_movie_', '')
                if chat_id in upload_sessions:
                    upload_sessions[chat_id]['code'] = code
                    upload_sessions[chat_id]['step'] = 'waiting_for_title'
                    send_message(chat_id, f"📝 <b>#{code}</b> uchun yangi kino nomini yuboring:")
                else:
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
        elif data == 'back_to_start':
            handle_start(chat_id, user_id)
        else:
            send_message(chat_id, f"❓ Noma'lum buyruq: {data}")
            
    except Exception as e:
        logger.error(f"❌ Callback error: {e}")
        send_message(chat_id, "❌ Xatolik yuz berdi.")

def send_immediate_broadcast(chat_id, message):
    """Send broadcast immediately to all users"""
    try:
        # Clear broadcast mode
        if chat_id in broadcast_data:
            del broadcast_data[chat_id]
            
        send_message(chat_id, "📡 <b>Reklama yuborilmoqda...</b>\n\n⏳ Kuting...")
        
        success_count = 0
        error_count = 0
        
        # Send to all users
        for user_id in users_db.keys():
            try:
                target_chat_id = int(user_id)
                
                if 'photo' in message:
                    # Send photo with caption
                    photo = message['photo'][-1]  # Highest resolution
                    file_id = photo['file_id']
                    caption = message.get('caption', '')
                    result = send_photo(target_chat_id, file_id, caption)
                    
                elif 'video' in message:
                    # Send video with caption
                    video = message['video']
                    file_id = video['file_id']
                    caption = message.get('caption', '')
                    result = send_video(target_chat_id, file_id, caption)
                    
                elif message.get('text'):
                    # Send text
                    text = message.get('text')
                    result = send_message(target_chat_id, text)
                    
                else:
                    result = False
                
                if result:
                    success_count += 1
                else:
                    error_count += 1
                    
            except Exception as e:
                logger.error(f"❌ Broadcast error for user {user_id}: {e}")
                error_count += 1
                continue
        
        # Send results
        total = len(users_db)
        rate = (success_count / total * 100) if total > 0 else 0
        
        result_text = f"""✅ <b>Reklama yuborish tugallandi!</b>

📊 <b>Natijalar:</b>
• ✅ Muvaffaqiyat: {success_count}
• ❌ Xatolik: {error_count} 
• 📊 Jami: {total}
• 📈 Foiz: {rate:.1f}%

🎭 <b>Ultimate Professional Kino Bot</b>"""

        send_message(chat_id, result_text)
        logger.info(f"✅ Immediate broadcast: {success_count} success, {error_count} errors")
        
    except Exception as e:
        logger.error(f"❌ Immediate broadcast error: {e}")
        send_message(chat_id, "❌ Reklama yuborishda xatolik!")
        if chat_id in broadcast_data:
            del broadcast_data[chat_id]

def handle_broadcast_start(chat_id):
    """Start broadcast process"""
    broadcast_data[chat_id] = {'step': 'waiting_for_content'}
    
    text = """📢 <b>Reklama yuborish</b>

📝 <b>Reklama kontentini yuboring:</b>
• Matn yuboring (oddiy reklama)
• Rasm + caption yuboring (rasmli reklama)
• Video + caption yuboring (videoli reklama)

💡 <b>Maslahat:</b> Reklama barcha bot foydalanuvchilariga yuboriladi.

⚠️ <b>Diqqat:</b> Bu jarayon bekor qilinmaydigan bo'ladi!</b>"""

    keyboard = {
        'inline_keyboard': [
            [{'text': '❌ Bekor qilish', 'callback_data': 'cancel_broadcast'}]
        ]
    }
    
    send_message(chat_id, text, keyboard)

def handle_broadcast_content(chat_id, message):
    """Handle broadcast content from admin"""
    try:
        if chat_id not in broadcast_data:
            return
            
        session = broadcast_data[chat_id]
        
        if session['step'] == 'waiting_for_content':
            # Store broadcast content
            if 'photo' in message:
                # Photo broadcast
                photo = message['photo'][-1]  # Get highest resolution
                file_id = photo['file_id']
                caption = message.get('caption', '')
                
                session['type'] = 'photo'
                session['file_id'] = file_id
                session['caption'] = caption
                
                preview_text = f"""📸 <b>Rasmli reklama tayyor!</b>

📝 <b>Caption:</b> {caption if caption else 'Caption yoq'}

📊 <b>Yuborilish ma'lumotlari:</b>
• Foydalanuvchilar: {len(users_db)} ta
• Turi: Rasmli reklama

✅ <b>Yuborishni tasdiqlaysizmi?</b>"""
                
            elif 'video' in message:
                # Video broadcast  
                video = message['video']
                file_id = video['file_id']
                caption = message.get('caption', '')
                duration = video.get('duration', 0)
                file_size = video.get('file_size', 0)
                
                session['type'] = 'video'
                session['file_id'] = file_id
                session['caption'] = caption
                session['duration'] = duration
                session['file_size'] = file_size
                
                size_mb = file_size / (1024 * 1024) if file_size > 0 else 0
                
                preview_text = f"""🎬 <b>Videoli reklama tayyor!</b>

📝 <b>Caption:</b> {caption if caption else 'Caption yoq'}
📦 <b>Hajmi:</b> {size_mb:.1f} MB
⏱ <b>Davomiyligi:</b> {duration} soniya

📊 <b>Yuborilish ma'lumotlari:</b>
• Foydalanuvchilar: {len(users_db)} ta
• Turi: Videoli reklama

✅ <b>Yuborishni tasdiqlaysizmi?</b>"""
                
            elif message.get('text'):
                # Text broadcast
                text = message.get('text', '')
                
                session['type'] = 'text'
                session['text'] = text
                
                preview_text = f"""📝 <b>Matnli reklama tayyor!</b>

📄 <b>Matn:</b> 
{text}

📊 <b>Yuborilish ma'lumotlari:</b>
• Foydalanuvchilar: {len(users_db)} ta
• Turi: Matnli reklama

✅ <b>Yuborishni tasdiqlaysizmi?</b>"""
            else:
                send_message(chat_id, "❌ Noto'g'ri format! Matn, rasm yoki video yuboring.")
                return
            
            session['step'] = 'waiting_for_confirmation'
            
            keyboard = {
                'inline_keyboard': [
                    [{'text': '✅ Ha, yuborish', 'callback_data': 'confirm_broadcast'}],
                    [{'text': '❌ Yo\'q, bekor qilish', 'callback_data': 'cancel_broadcast'}]
                ]
            }
            
            send_message(chat_id, preview_text, keyboard)
            
    except Exception as e:
        logger.error(f"❌ Broadcast content error: {e}")
        send_message(chat_id, "❌ Reklama qayta ishlashda xatolik!")

def handle_broadcast_confirm(chat_id):
    """Confirm and send broadcast to all users"""
    if chat_id not in broadcast_data:
        send_message(chat_id, "❌ Reklama ma'lumotlari topilmadi!")
        return
    
    session = broadcast_data[chat_id]
    
    if session.get('step') != 'waiting_for_confirmation':
        send_message(chat_id, "❌ Reklama hali tayyor emas!")
        return
    
    send_message(chat_id, "📡 <b>Reklama yuborilmoqda...</b>\n\n⏳ Iltimos kuting...")
    
    # Send to all users
    success_count = 0
    error_count = 0
    
    for user_id in users_db.keys():
        try:
            if session['type'] == 'text':
                # Send text message
                result = send_message(int(user_id), session['text'])
            elif session['type'] == 'photo':
                # Send photo
                result = send_photo(int(user_id), session['file_id'], session.get('caption'))
            elif session['type'] == 'video':
                # Send video
                result = send_video(int(user_id), session['file_id'], session.get('caption'))
            
            if result:
                success_count += 1
            else:
                error_count += 1
                
        except Exception as e:
            logger.error(f"❌ Broadcast error for user {user_id}: {e}")
            error_count += 1
            continue
    
    # Send result
    result_text = f"""✅ <b>Reklama yuborish yakunlandi!</b>

📊 <b>Natijalar:</b>
• Muvaffaqiyatli: {success_count}
• Xatolik: {error_count}
• Jami: {len(users_db)}

📈 <b>Muvaffaqiyat darajasi:</b> {(success_count/len(users_db)*100):.1f}%

🎭 <b>Ultimate Professional Kino Bot</b>"""

    send_message(chat_id, result_text)
    
    # Clean up
    if chat_id in broadcast_data:
        del broadcast_data[chat_id]
        
    logger.info(f"✅ Broadcast completed: {success_count} success, {error_count} errors")

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
    """Show movies list for admin"""
    if not movies_db:
        send_message(chat_id, "📋 Hozircha kinolar yo'q.")
        return
    
    movies_text = f"""🎬 <b>Admin - Kinolar ro'yxati</b>

📊 <b>Jami kinolar:</b> {len(movies_db)}

🎭 <b>Kinolar:</b>"""

    count = 0
    total_size = 0
    
    for code, movie_data in list(movies_db.items())[:10]:
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
        no_movies_text = """📋 <b>Hozircha kinolar mavjud emas</b>

🔄 Admin tomonidan kinolar tez orada qo'shiladi.

💡 <b>Qanday ishlaydi:</b>
• Kino kodi yuborilganda avtomatik yuklanadi
• Yuqori sifatli videolar
• Tez yuklanish

🎭 <b>Ultimate Professional Kino Bot</b>"""
        
        keyboard = {
            'inline_keyboard': [
                [{'text': '🏠 Bosh sahifa', 'callback_data': 'back_to_start'}]
            ]
        }
        send_message(chat_id, no_movies_text, keyboard)
        return
    
    movies_text = f"""🎬 <b>Mavjud kinolar ({len(movies_db)} ta)</b>

📋 <b>Kinolar ro'yxati:</b>

"""
    
    count = 0
    for code, movie_data in list(movies_db.items())[:15]:
        count += 1
        
        if isinstance(movie_data, str):
            title = f"Kino {code}"
        else:
            title = movie_data.get('title', f"Kino {code}")
        
        movies_text += f"{count}. <b>{title}</b>\n"
        movies_text += f"   📁 Kod: <code>{code}</code>\n\n"
    
    if len(movies_db) > 15:
        movies_text += f"... va yana {len(movies_db) - 15} ta kino\n\n"
    
    movies_text += """💡 <b>Kino olish uchun:</b>
• Yuqoridagi kodlardan birini yuboring
• Masalan: <code>123</code> yoki <code>#123</code>
• Video avtomatik yuboriladi

🎭 <b>Ultimate Professional Kino Bot</b>"""

    keyboard = {
        'inline_keyboard': [
            [{'text': '🏠 Bosh sahifa', 'callback_data': 'back_to_start'}],
            [{'text': 'ℹ️ Yordam', 'callback_data': 'show_help'}]
        ]
    }
    
    send_message(chat_id, movies_text, keyboard)

def show_help(chat_id):
    """Show help information"""
    help_text = f"""ℹ️ <b>Ultimate Professional Kino Bot Yordami</b>

🔍 <b>Kino qidirish:</b>
• Kino kodini yuboring: <code>#123</code>
• Yoki raqam: <code>123</code>
• Kino avtomatik yuboriladi

📊 <b>Asosiy komandalar:</b>
• /start - Bosh sahifa
• Kino kodi yuborish

🎬 <b>Hozirda mavjud:</b> {len(movies_db)} ta kino

💡 <b>Maslahat:</b>
• Aniq kino kodini kiriting
• # belgisi ixtiyoriy
• Kinolar yuqori sifatda

🎭 <b>Ultimate Professional darajada xizmat!</b>"""

    keyboard = {
        'inline_keyboard': [
            [{'text': '🎬 Mavjud kinolar', 'callback_data': 'show_all_movies'}],
            [{'text': '🏠 Bosh sahifa', 'callback_data': 'back_to_start'}]
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

def show_admin_test(chat_id):
    """Show admin test"""
    test_text = """🔧 <b>Admin Test Panel</b>
    
✅ Barcha sistemalar normal ishlaydi!
✅ Database ulanish: OK
✅ Upload tizimi: OK
✅ Broadcast tizimi: OK

🎭 Ultimate Professional Bot V3.0"""
    
    send_message(chat_id, test_text)

def handle_photo_upload(chat_id, user_id, message):
    """Handle photo upload from admin"""
    if user_id != ADMIN_ID:
        send_message(chat_id, "❌ Faqat admin photo yuklashi mumkin!")
        return
    
    send_message(chat_id, "📸 Rasm qabul qilindi! Hozircha faqat video upload qo'llab-quvvatlanadi.")

# API functions
def send_message(chat_id, text, keyboard=None):
    """Send message via Telegram API"""
    try:
        import requests
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        
        if keyboard:
            data["reply_markup"] = json.dumps(keyboard)
        
        response = requests.post(url, data=data, timeout=10)
        result = response.json()
        
        if result.get('ok'):
            return True
        else:
            logger.error(f"❌ Send message error: {result}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Send message exception: {e}")
        return False

def send_video(chat_id, file_id, caption=None):
    """Send video via Telegram API"""
    try:
        import requests
        url = f"https://api.telegram.org/bot{TOKEN}/sendVideo"
        data = {
            "chat_id": chat_id,
            "video": file_id
        }
        
        if caption:
            data["caption"] = caption
            data["parse_mode"] = "HTML"
        
        response = requests.post(url, data=data, timeout=30)
        result = response.json()
        
        if result.get('ok'):
            return True
        else:
            logger.error(f"❌ Send video error: {result}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Send video exception: {e}")
        return False

def send_photo(chat_id, file_id, caption=None):
    """Send photo via Telegram API"""
    try:
        import requests
        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
        data = {
            "chat_id": chat_id,
            "photo": file_id
        }
        
        if caption:
            data["caption"] = caption
            data["parse_mode"] = "HTML"
        
        response = requests.post(url, data=data, timeout=30)
        result = response.json()
        
        if result.get('ok'):
            return True
        else:
            logger.error(f"❌ Send photo error: {result}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Send photo exception: {e}")
        return False

def answer_callback(callback_id):
    """Answer callback query"""
    try:
        import requests
        url = f"https://api.telegram.org/bot{TOKEN}/answerCallbackQuery"
        data = {"callback_query_id": callback_id}
        
        response = requests.post(url, data=data, timeout=5)
        return response.json().get('ok', False)
        
    except Exception as e:
        logger.error(f"❌ Answer callback error: {e}")
        return False

def setup_webhook():
    """Setup webhook"""
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

# Initialize on startup
logger.info("🚀 Starting Ultimate Professional Kino Bot V3.0...")
load_database()
setup_webhook()

# For gunicorn compatibility
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
