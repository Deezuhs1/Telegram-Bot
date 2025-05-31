from flask import Flask, request
import requests

app = Flask(__name__)

# Your bot token
BOT_TOKEN = '7643390545:AAG7mNjIP3cEP_7P6F93DJCdNHP75O89TNI'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'

# Your unique webhook path
WEBHOOK_PATH = f'/{BOT_TOKEN}'
FULL_WEBHOOK_URL = f'https://dev-rater-bot.onrender.com{WEBHOOK_PATH}'

@app.route(WEBHOOK_PATH, methods=['POST'])
def webhook():
    data = request.get_json()

    if not data:
        return 'No data received', 400

    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')

        if text == '/start':
            send_message(chat_id, "✅ Bot is active and responding!")
        else:
            send_message(chat_id, f"You said: {text}")

    return 'ok', 200

def send_message(chat_id, text):
    url = f'{TELEGRAM_API_URL}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, json=payload)

# Move webhook setup here
def set_webhook():
    url = f'{TELEGRAM_API_URL}/setWebhook'
    response = requests.post(url, json={'url': FULL_WEBHOOK_URL})
    print('Webhook set response:', response.json())

if __name__ == '__main__':
    set_webhook()  # Call this BEFORE running the server
    app.run(host='0.0.0.0', port=10000)
