# Copilot Instructions for Kino Bot

## Architecture Overview
This is a **Flask-based Telegram webhook bot** with a monolithic `app.py` architecture (9700+ lines). The bot uses **direct HTTP requests** to Telegram API rather than python-telegram-bot library.

### Core Components
- **`app.py`**: Main application - Flask server + all bot logic (webhook handler, message processing, admin commands)
- **`config.py`**: Environment-based configuration with TOKEN/ADMIN_ID fallbacks
- **Data Storage**: Dual-persistence with MongoDB + JSON files (`file_ids.json`, `channels.json`, `users.json`)
- **Session Management**: In-memory dictionaries (`upload_sessions`, `channels_db`, `movies_db`, `subscription_cache`)

### Key Data Flow
1. **Webhook**: `/webhook` route receives Telegram updates → `handle_message()` 
2. **Session Handling**: Admin interactions use `upload_sessions` for multi-step workflows (movie deletion, channel management)
3. **Spam Protection**: `is_spam_message()` with keyword detection + silent blocking
4. **Subscription System**: `check_all_subscriptions()` with cached results (`subscription_cache`)

## Critical Developer Workflows

### Running Locally
```bash
python app.py  # Starts Flask server on port 8080
```

### Deployment (Multiple Platforms)
- **Railway**: Use `railway_config.py` for environment detection
- **Render**: Auto-detects via `RENDER_EXTERNAL_URL` environment variable  
- **Testing**: Multiple test files (`test_*.py`) for different components

### Debugging Patterns
```python
logger.info(f"🔍 Debug info: {variable}")  # Use emoji prefixes consistently
# Check session state: upload_sessions[user_id]
# Monitor cache: subscription_cache[user_id]
```

## Project-Specific Conventions

### Message Handling Pattern
```python
def handle_message(message):
    # 1. Extract data: chat_id, user_id, text
    # 2. Spam check (non-admin only)
    # 3. Subscription check (cached)
    # 4. Session handling (upload/broadcast)
    # 5. Command routing
```

### Admin Command Structure
- All admin commands check `user_id == ADMIN_ID`
- Admin commands start with `/` and have extensive inline keyboard menus
- Session-based workflows for complex operations (movie deletion, channel management)

### Database Pattern (Dual Persistence)
```python
# Always update both MongoDB and JSON
movies_db[code] = movie_data  # Memory
save_movie_to_mongodb(movie_data)  # MongoDB
auto_save_data()  # JSON files
```

### Cache Management
```python
# Subscription cache with expiration
subscription_cache[user_id] = {
    'is_subscribed': True,
    'expires': time.time() + CACHE_DURATION,
    'last_check': time.time()
}
```

## Integration Points

### Telegram API (Direct HTTP)
- `send_message()`, `send_video()`: Custom HTTP request functions
- No external Telegram library - direct API calls with `requests`
- Webhook-based, not polling

### MongoDB Integration
- Fallback architecture: MongoDB preferred, JSON files as backup
- Connection check: `is_mongodb_available()`
- Auto-retry and graceful degradation

### Platform Detection
```python
# Render.com detection
if os.getenv('RENDER_EXTERNAL_URL'):
    # Render-specific configuration
    
# Railway detection  
try:
    from railway_config import get_token
    # Railway-specific configuration
```

## Session Management Patterns

### Upload Sessions (Movie Deletion)
```python
upload_sessions[user_id] = {
    'action': 'delete_movies',
    'stage': 'waiting_for_movie_code',
    'timestamp': datetime.now().isoformat()
}
```

### Cache Invalidation
```python
# Channel changes require cache clear
invalidate_subscription_cache()  # Clears all user subscription cache
```

## Testing & Debugging

### Test Files by Purpose
- `test_complete_bot.py`: Full system test
- `test_movie_deletion.py`: Movie management tests
- `test_subscription.py`: Channel subscription tests  
- `fix_*.py`: Repair/diagnostic scripts

### Admin Debug Commands
- `/spamstats`: Spam protection status
- `/debugchannels`: Channel configuration debug
- `/clearcache`: Clear subscription cache

## Multi-Environment Considerations
- **Development**: Uses JSON files primarily
- **Production**: MongoDB + JSON backup
- **Cloud Deploy**: Auto-detects platform (Railway/Render) via environment variables
- **Keep-Alive**: Anti-sleep system for free hosting tiers
