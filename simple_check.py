import requests
print("🔍 Railway Bot Status Check")
print("=" * 30)

try:
    # Test Railway health
    r = requests.get('https://web-production-8240a.up.railway.app/health', timeout=5)
    print(f"Railway Health: {r.status_code}")
    if r.status_code == 200:
        print("✅ Railway is running!")
    else:
        print(f"❌ Railway issue: {r.status_code}")
except Exception as e:
    print(f"❌ Railway error: {e}")

try:
    # Check webhook
    webhook_url = 'https://api.telegram.org/bot8177519032:AAED4FgPoFQiQhqM_lvrK1iV8hL9u4SnkDk/getWebhookInfo'
    r = requests.get(webhook_url, timeout=5)
    if r.status_code == 200:
        data = r.json()
        webhook_info = data.get('result', {})
        print(f"Webhook URL: {webhook_info.get('url', 'Not set')}")
        print(f"Pending: {webhook_info.get('pending_update_count', 0)}")
        if webhook_info.get('url'):
            print("✅ Webhook is set!")
        else:
            print("❌ Webhook not set!")
    else:
        print(f"❌ Webhook check failed: {r.status_code}")
except Exception as e:
    print(f"❌ Webhook error: {e}")

print("=" * 30)
