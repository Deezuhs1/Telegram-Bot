from flask import Flask, request
import requests

app = Flask(__name__)

# ✅ Your actual bot token
BOT_TOKEN = '7643390545:AAG7mNjIP3cEP_7P6F93DJCdNHP75O89TNI'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'

# ✅ Your public Render URL (no token in the path)
WEBHOOK_URL = 'https://dev-rater-bot.onrender.com/'

@app.before_first_request
def set_webhook():
    """Set Telegram webhook to your deployed Render URL."""
    url = f'{TELEGRAM_API_URL}/setWebhook'
    response = requests.post(url, json={'url': WEBHOOK_URL})
    print('Webhook set response:', response.json())

@app.route('/', methods=['POST'])
def webhook():
    """This route handles incoming Telegram updates."""
    data = request.get_json()

    if not data:
        return 'No data received', 400

    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')

        if text == '/start':
            send_message(chat_id, "👋 Hello! Your Dev Rater bot is now live and ready.")
        else:
            send_message(chat_id, f"You said: {text}")

    return 'ok', 200

def send_message(chat_id, text):
    """Send a message to a Telegram user."""
    url = f'{TELEGRAM_API_URL}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
