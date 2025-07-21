#!/usr/bin/env python3
"""
Simple Kino Bot for Render.com deployment
Clean and working version
"""

import os
import json
import time
import logging
import requests
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

# Helper functions
def load_data():
    """Load data from JSON files"""
    global users_db, movies_db
    
    try:
        if os.path.exists('users.json'):
            with open('users.json', 'r', encoding='utf-8') as f:
                users_db = json.load(f)
                logger.info(f"✅ Loaded {len(users_db)} users")
        else:
            users_db = {}
            
        if os.path.exists('file_ids.json'):
            with open('file_ids.json', 'r', encoding='utf-8') as f:
                movies_db = json.load(f)
                logger.info(f"✅ Loaded {len(movies_db)} movies")
        else:
            movies_db = {}
            
    except Exception as e:
        logger.error(f"❌ Load error: {e}")
        users_db = {}
        movies_db = {}

def save_data():
    """Save data to JSON files"""
    try:
        with open('users.json', 'w', encoding='utf-8') as f:
            json.dump(users_db, f, ensure_ascii=False, indent=2)
            
        with open('file_ids.json', 'w', encoding='utf-8') as f:
            json.dump(movies_db, f, ensure_ascii=False, indent=2)
            
        logger.info("💾 Data saved successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Save error: {e}")
        return False

def send_message(chat_id, text, keyboard=None):
    """Send message via Telegram Bot API"""
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        
        if keyboard:
            data['reply_markup'] = json.dumps(keyboard)
        
        response = requests.post(url, data=data, timeout=10)
        
        if response.status_code == 200:
            logger.info(f"✅ Message sent to {chat_id}")
            return response.json()
        else:
            logger.error(f"❌ Failed to send message: {response.status_code}")
            return None
            
    except Exception as e:
        logger.error(f"❌ Send message error: {e}")
        return None

def send_video(chat_id, video_file_id, caption=""):
    """Send video via Telegram Bot API"""
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendVideo"
        data = {
            'chat_id': chat_id,
            'video': video_file_id,
            'caption': caption,
            'parse_mode': 'HTML'
        }
        
        response = requests.post(url, data=data, timeout=30)
        
        if response.status_code == 200:
            logger.info(f"✅ Video sent to {chat_id}")
            return response.json()
        else:
            logger.error(f"❌ Failed to send video: {response.status_code}")
            return None
            
    except Exception as e:
        logger.error(f"❌ Send video error: {e}")
        return None

# Flask app
app = Flask(__name__)

@app.route('/')
def home():
    """Health check"""
    return jsonify({
        "status": "🎬 Kino Bot - Working!",
        "users": len(users_db),
        "movies": len(movies_db),
        "timestamp": int(time.time())
    })

@app.route('/ping')
def ping():
    """Ping endpoint for monitoring"""
    return jsonify({
        "status": "alive",
        "timestamp": int(time.time()),
        "message": "Pong! 🏓"
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Main webhook handler"""
    try:
        data = request.get_json()
        logger.info(f"📨 Webhook received")
        
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
        
        # Save user
        users_db[str(user_id)] = {
            'first_name': message.get('from', {}).get('first_name', ''),
            'last_seen': int(time.time())
        }
        save_data()
        
        logger.info(f"💬 Message from {user_id}: {text}")
        
        # Handle commands
        if text == '/start':
            handle_start(chat_id, user_id)
        elif text == '/admin':
            handle_admin(chat_id, user_id)
        elif text == '/stats':
            handle_stats(chat_id, user_id)
        elif 'video' in message:
            handle_video(chat_id, user_id, message)
        else:
            handle_movie_request(chat_id, user_id, text)
            
    except Exception as e:
        logger.error(f"❌ Message handling error: {e}")

def handle_start(chat_id, user_id):
    """Handle /start command"""
    try:
        if user_id == ADMIN_ID:
            text = f"""👑 <b>Admin Panel - Kino Bot</b>

🎬 <b>Statistika:</b>
• Foydalanuvchilar: {len(users_db)} ta
• Kinolar: {len(movies_db)} ta

🔧 <b>Komandalar:</b>
• /admin - Admin panel
• /stats - Statistika
• Kino kodi yuboring: <code>123</code>

🎭 <b>Bot ish holatida!</b>"""
        else:
            text = f"""🎬 <b>Kino Bot ga xush kelibsiz!</b>

📽️ <b>Kino olish uchun:</b>
• Kino kodini yuboring: <code>123</code>
• Yoki # bilan: <code>#123</code>

📊 <b>Mavjud:</b> {len(movies_db)} ta kino

🚀 <b>Hoziroq kod yuboring!</b>"""
        
        send_message(chat_id, text)
        logger.info(f"✅ Start sent to {user_id}")
        
    except Exception as e:
        logger.error(f"❌ Start error: {e}")

def handle_admin(chat_id, user_id):
    """Handle admin command"""
    try:
        if user_id != ADMIN_ID:
            send_message(chat_id, "❌ Siz admin emassiz!")
            return
        
        text = f"""👑 <b>Admin Panel</b>

📊 <b>Statistika:</b>
• Foydalanuvchilar: {len(users_db)} ta
• Kinolar: {len(movies_db)} ta

🎬 <b>Kino yuklash:</b>
• Video fayl yuboring
• Keyin kod bering

💬 <b>Komandalar:</b>
• /stats - Batafsil statistika"""
        
        send_message(chat_id, text)
        
    except Exception as e:
        logger.error(f"❌ Admin error: {e}")

def handle_stats(chat_id, user_id):
    """Handle stats command"""
    try:
        if user_id != ADMIN_ID:
            send_message(chat_id, "❌ Faqat admin statistika ko'ra oladi!")
            return
        
        # Movie codes list
        movie_codes = list(movies_db.keys())[:10]
        codes_text = ", ".join(movie_codes) if movie_codes else "Hech narsa yo'q"
        
        text = f"""📊 <b>Bot Statistikasi</b>

👥 <b>Foydalanuvchilar:</b> {len(users_db)} ta
🎬 <b>Kinolar:</b> {len(movies_db)} ta

📋 <b>Mavjud kodlar:</b>
{codes_text}

⏰ <b>Vaqt:</b> {time.strftime('%Y-%m-%d %H:%M:%S')}
🤖 <b>Status:</b> ✅ Ishlayapti"""
        
        send_message(chat_id, text)
        
    except Exception as e:
        logger.error(f"❌ Stats error: {e}")

def handle_video(chat_id, user_id, message):
    """Handle video upload"""
    try:
        if user_id != ADMIN_ID:
            send_message(chat_id, "❌ Faqat admin video yuklashi mumkin!")
            return
        
        video = message['video']
        file_id = video['file_id']
        
        # Ask for code
        global waiting_for_code
        waiting_for_code[chat_id] = file_id
        
        send_message(chat_id, f"""✅ <b>Video qabul qilindi!</b>

📝 <b>Endi kino kodini yuboring:</b>
• Masalan: <code>123</code> yoki <code>#123</code>

🎬 <b>File ID:</b> <code>{file_id[:20]}...</code>""")
        
    except Exception as e:
        logger.error(f"❌ Video handling error: {e}")
        send_message(chat_id, "❌ Video yuklashda xatolik!")

# Global variable for upload state
waiting_for_code = {}

def handle_movie_request(chat_id, user_id, text):
    """Handle movie code or admin input"""
    try:
        # Check if admin is uploading
        if user_id == ADMIN_ID and chat_id in waiting_for_code:
            # Admin is providing code for uploaded video
            code = text.strip().replace('#', '')
            file_id = waiting_for_code.pop(chat_id)
            
            # Save movie
            movies_db[code] = file_id
            save_data()
            
            send_message(chat_id, f"""✅ <b>Kino saqlandi!</b>

📝 <b>Kod:</b> <code>{code}</code>
🎬 <b>File ID:</b> <code>{file_id[:20]}...</code>

🎉 <b>Endi foydalanuvchilar {code} kodi bilan kino olishlari mumkin!</b>""")
            return
        
        # Regular movie request
        code = text.strip().replace('#', '')
        
        if code in movies_db:
            file_id = movies_db[code]
            caption = f"🎬 <b>Kino #{code}</b>\n\n🤖 @uzmovi_film_bot"
            
            success = send_video(chat_id, file_id, caption)
            if success:
                logger.info(f"✅ Movie {code} sent to {user_id}")
            else:
                send_message(chat_id, f"❌ {code} kino yuborishda xatolik!")
        else:
            # Movie not found
            available_codes = list(movies_db.keys())[:5]
            codes_text = ", ".join(available_codes) if available_codes else "Hozircha yo'q"
            
            send_message(chat_id, f"""❌ <b>{text}</b> kod topilmadi!

📋 <b>Mavjud kodlar:</b> {codes_text}

💡 <b>To'g'ri format:</b>
• <code>123</code>
• <code>#123</code>""")
        
    except Exception as e:
        logger.error(f"❌ Movie request error: {e}")
        send_message(chat_id, "❌ Xatolik yuz berdi!")

def handle_callback(callback_query):
    """Handle callback queries (if needed)"""
    try:
        chat_id = callback_query.get('message', {}).get('chat', {}).get('id')
        user_id = callback_query.get('from', {}).get('id')
        data = callback_query.get('data', '')
        
        # Answer callback
        callback_id = callback_query.get('id')
        answer_callback(callback_id)
        
        # Handle specific callbacks here if needed
        logger.info(f"🔘 Callback: {data} from {user_id}")
        
    except Exception as e:
        logger.error(f"❌ Callback error: {e}")

def answer_callback(callback_id):
    """Answer callback query"""
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/answerCallbackQuery"
        data = {'callback_query_id': callback_id}
        requests.post(url, data=data, timeout=5)
    except:
        pass

def setup_webhook():
    """Setup webhook for Render.com"""
    try:
        webhook_url = os.getenv('RENDER_EXTERNAL_URL')
        if webhook_url:
            webhook_url = f"{webhook_url}/webhook"
            
            response = requests.post(
                f"https://api.telegram.org/bot{TOKEN}/setWebhook",
                data={"url": webhook_url},
                timeout=10
            )
            
            result = response.json()
            if result.get('ok'):
                logger.info(f"✅ Webhook set: {webhook_url}")
            else:
                logger.error(f"❌ Webhook error: {result}")
        else:
            logger.info("💡 Local mode - no webhook setup")
            
    except Exception as e:
        logger.error(f"❌ Webhook setup error: {e}")

# Initialize
logger.info("🚀 Starting Simple Kino Bot...")
load_data()
setup_webhook()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    logger.info(f"🎬 Kino Bot starting on port {port}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )
