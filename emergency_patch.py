
# EMERGENCY CHANNEL DISABLE PATCH - Add to app.py
def emergency_disable_channels():
    """Emergency function to disable all channels"""
    global channels_db
    channels_db = {}
    print("🚨 EMERGENCY: All channels disabled")
    return True

# Override check_all_subscriptions
def emergency_check_all_subscriptions(user_id):
    """Emergency bypass for all users"""
    print(f"🚨 EMERGENCY BYPASS: User {user_id} granted access")
    return True
