#!/usr/bin/env python3
"""
Bu script bot deploy qilingandan keyin webhook URL ni o'rnatadi
"""

import requests
import os
from config import TOKEN

def set_webhook():
    # Render URL ni o'zgartiring - sizning deploy URL ingiz
    webhook_url = "https://your-app-name.onrender.com/webhook"
    
    # Webhook o'rnatish
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
    data = {"url": webhook_url}
    
    response = requests.post(url, data=data)
    print(f"Webhook response: {response.json()}")

if __name__ == "__main__":
    set_webhook()
