import requests

def test_token(token):
    url = f"https://api.telegram.org/bot{token}/getMe"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("✅ Token is valid!")
            print(response.json())
            return True
        else:
            print("❌ Token is invalid!")
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing token: {e}")
        return False

# Test the token
TOKEN = "8177519032:AAGnJN0ngSSEnqrVKLb24QHhRfRnQlBuKDA"
test_token(TOKEN)
