# 🎭 Professional Kino Bot

Professional Telegram bot for movie management with advanced admin features.

## Features

- 🎬 Movie management system
- 👑 Professional admin panel
- 📢 Broadcasting system
- 📺 Channel subscription system
- 💾 MongoDB integration
- 🔄 Auto-backup system

## Setup

1. Clone repository:
```bash
git clone https://github.com/YOUR_USERNAME/kino-bot.git
cd kino-bot
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
- Create `.env` file
- Add your bot token and admin ID
```env
BOT_TOKEN=your_bot_token_here
ADMIN_ID=your_admin_id_here
MONGODB_URI=your_mongodb_uri_here
```

4. Run bot:
```bash
python app.py
```

## Deployment

Bot supports multiple deployment platforms:
- Railway.app
- Render.com
- Any other Python hosting

## Admin Commands

- `/admin` - Access admin panel
- `/stats` - View statistics  
- `/broadcast` - Send broadcast
- `/channels` - Manage channels
### Response Examples:
```json
# /ping endpoint
{
  "status": "alive",
  "timestamp": 1642671234,
  "bot": "Ultimate Professional Kino Bot V3.0",
  "users": 150,
  "movies": 25,
  "message": "Pong! 🏓"
}
```

## 🎯 Admin Monitoring Commands

- **System Health**: `/admin` → `🔧 Tizim holati`
- **Ping Test**: `/admin` → `🏓 Ping test`  
- **Keep-Alive Status**: Shows in admin dashboard
- **Response Times**: Real-time ping measurements

## ⚙️ Technical Details

### Keep-Alive Features:
- **Internal Ping**: Every 10 minutes self-ping
- **Thread Safety**: Daemon thread implementation
- **Error Handling**: Graceful failure recovery
- **Environment Aware**: Only runs on Render.com
- **Detailed Logging**: Monitor keep-alive activity

### Render.com Configuration:
1. **Create Web Service**: https://dashboard.render.com
2. **Connect Repository**: Link your GitHub repository
3. **Settings**:
   - **Name**: Ultimate Kino Bot
   - **Region**: Frankfurt (EU Central) 
   - **Branch**: main
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`

4. **Environment Variables**:
   ```bash
   # Bot will automatically detect Render environment
   # RENDER_EXTERNAL_URL is set automatically by Render
   PORT=8080
   ```

5. **Deploy**: Click "Create Web Service" and wait for deployment

## 🚫 Never Sleep Again!

### What Happens:
1. **Deploy to Render**: Bot automatically detects Render environment
2. **Keep-Alive Starts**: Internal ping system activates  
3. **Add Uptime Robot**: External monitoring for redundancy
4. **Monitor Dashboard**: Admin can check system health anytime

### Why It Works:
- **Dual Protection**: Internal + External monitoring
- **Smart Threading**: Non-blocking background pings
- **Multiple Endpoints**: Different URLs for different needs
- **Error Recovery**: Graceful handling of network issues

## 🔍 Troubleshooting

### Bot Still Sleeping?
1. Check admin panel: `/admin` → `🔧 Tizim holati`
2. Verify Uptime Robot monitor shows "Up"
3. Test ping manually: `https://your-app.onrender.com/ping`
4. Check Render logs for keep-alive messages

### Uptime Robot Setup Issues?
1. **URL Format**: Must be `https://your-app-name.onrender.com/ping`
2. **Interval**: Minimum 5 minutes for free plan
3. **Monitor Type**: HTTP(s) not TCP
4. **Alerts**: Enable email notifications

## 🎭 Other Features

### 📺 Mandatory Channels
- Force users to join channels before bot access
- Admin can add/remove channels dynamically
- Automatic subscription verification

### 🎬 Movie Management  
- Upload movies with custom codes
- Professional admin dashboard
- Video file management with metadata

### 📢 Broadcasting System
- Send messages to all users
- Support for text, photos, videos
- Real-time delivery statistics

### 📊 Advanced Statistics
- User activity tracking
- Movie usage analytics
- System performance metrics

---

**🎭 Ultimate Professional Kino Bot V3.0**  
*Powered by Never-Sleep Technology™* 🚀✨

**Setup Time**: 5 minutes  
**Uptime**: 99.9%+  
**Sleep Risk**: 0% 💪
