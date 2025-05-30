from flask import Flask, request
import requests

app = Flask(__name__)

# Your actual bot token
BOT_TOKEN = '6649843894:AAFJ7NBRLE3sp_CeIil_BZwztYFvxzPtnWk'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'

# Your deployed webhook URL on Render
WEBHOOK_URL = 'https://dev-rater-bot.onrender.com/'

@app.before_first_request
def set_webhook():
    """Automatically sets the webhook when the app starts."""
    url = f'{TELEGRAM_API_URL}/setWebhook'
    response = requests.post(url, json={'url': WEBHOOK_URL})
    print('Webhook set:', response.json())

@app.route('/', methods=['POST'])
def webhook():
    """Main route Telegram will send POST requests to."""
    data = request.get_json()

    if not data:
        return 'No data received', 400

    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')

        if text == '/start':
            send_message(chat_id, "Hello! Your bot is alive.")
        else:
            send_message(chat_id, "I got your message!")

    return 'ok', 200

def send_message(chat_id, text):
    """Send a message to a Telegram user."""
    url = f'{TELEGRAM_API_URL}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run()
