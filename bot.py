import requests
from flask import Flask, request

app = Flask(__name__)

# === CONFIGURATION ===
BOT_TOKEN = 'YOUR_BOT_TOKEN'  # Replace with your actual Telegram bot token
CHAT_IDS = [524164659, 123456789, 987654321]  # Replace with real Telegram user IDs

# === ALERT FUNCTION (Loop Through Recipients) ===
def send_alert(message):
    for chat_id in CHAT_IDS:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message
        }
        try:
            requests.post(url, json=payload)
        except Exception as e:
            print(f"Error sending message to {chat_id}: {e}")

# === SAMPLE LOGIC FOR TRIGGERING AN ALERT ===
@app.route('/trigger-alert', methods=['POST'])
def trigger_alert():
    data = request.json
    token = data.get('token', 'Unknown Token')
    reason = data.get('reason', 'Golden Cluster Alert')
    
    message = f"🚨 Alert: {token} triggered!\nReason: {reason}"
    send_alert(message)
    return {'status': 'alert sent'}

# === SAMPLE ENDPOINT TO VERIFY
