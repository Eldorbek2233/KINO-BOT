@echo off
echo 🎬 KINO BOT - QUICK START
echo ========================
echo.

echo 📋 Checking bot files...
if not exist "app.py" (
    echo ❌ app.py not found!
    pause
    exit /b 1
)

if not exist "config.py" (
    echo ❌ config.py not found!
    pause
    exit /b 1
)

if not exist "file_ids.json" (
    echo ❌ file_ids.json not found!
    pause
    exit /b 1
)

echo ✅ All required files found
echo.

echo 🚀 Starting Kino Bot...
echo ⏳ Please wait...
echo.
echo 📝 Testing instructions:
echo 1. Open Telegram and find your bot
echo 2. Send /start to test basic functionality  
echo 3. Send /admin_menu to test admin features
echo 4. Test movie deletion: Admin Panel → Movie Management → Delete Movies
echo 5. Press Ctrl+C here to stop the bot
echo.

python app.py

echo.
echo 🛑 Bot stopped
pause
