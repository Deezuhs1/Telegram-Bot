import requests
from flask import Flask, request

app = Flask(__name__)

# === CONFIGURATION ===
BOT_TOKEN = '6484374680:AAHuhyya0iKnKpbdHgBz4CxeXhYQrd0dGKY'  # Your bot token
CHAT_IDS = [
    524164659,     # You (Swagglesworth)
    8056255833,    # Donald Day (@dond54mon)
    6889398762     # Cool (@Coolbeans12345)
]

# === ALERT FUNCTION (Loop Through Recipients) ===
def send_alert(message):
    for chat_id in CHAT_IDS:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message
        }
        try:
            response = requests.post(url, json=payload)
            print(f"Message sent to {chat_id}, status: {response.status_code}")
        except Exception as e:
            print(f"Error sending message to {chat_id}: {e}")

# === SAMPLE LOGIC TO TRIGGER ALERT ===
@app.route('/trigger-alert', methods=['POST'])
def trigger_alert():
    data = request.json
    token = data.get('token', 'Unknown Token')
    reason = data.get('reason', 'Golden Cluster Alert')

    message = f"🚨 Alert: {token} triggered!\nReason: {reason}"
    send_alert(message)
    return {'status': 'alert sent'}

# === SAMPLE ENDPOINT TO VERIFY SERVER IS LIVE ===
@app.route('/')
def home():
    return "Bot is running and listening."

# === LAUNCH SERVER ===
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
