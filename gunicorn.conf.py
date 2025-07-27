# Gunicorn configuration file for Professional Kino Bot
import os

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', 8080)}"
backlog = 2048

# Worker processes
workers = 1
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 30

# Restart workers after this many requests, to help control memory usage
max_requests = 1000
max_requests_jitter = 100

# Logging
loglevel = "info"
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "kino-bot"

# Server mechanics
preload_app = True
daemon = False

# Platform detection for logging
platform = "unknown"
if os.getenv('RAILWAY_ENVIRONMENT'):
    platform = "railway"
elif os.getenv('RENDER_EXTERNAL_URL'):
    platform = "render"

print(f"🚀 Gunicorn starting on {platform} platform")
print(f"📡 Binding to: {bind}")
print(f"👥 Workers: {workers}")
print(f"⏰ Timeout: {timeout}s")
pidfile = None
user = None
group = None
tmp_upload_dir = None

# SSL
keyfile = None
certfile = None
