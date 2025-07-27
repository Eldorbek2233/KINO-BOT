#!/bin/bash

# Professional Kino Bot deployment script
echo "🎭 Starting Professional Kino Bot deployment..."

# Set environment variables
export PYTHONUNBUFFERED=1
export PYTHONPATH="."

# Install dependencies
echo "📦 Installing dependencies..."
pip install --no-cache-dir -r requirements.txt

# Run with Gunicorn
echo "🚀 Starting Professional Kino Bot with Gunicorn..."
exec gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --keep-alive 30 --workers 1
