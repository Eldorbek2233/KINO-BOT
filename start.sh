#!/bin/bash

# Railway deployment script
echo "🚂 Starting Railway deployment..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install --no-cache-dir -r requirements.txt

# Run the bot
echo "🤖 Starting Kino Bot..."
exec python simple_bot.py
