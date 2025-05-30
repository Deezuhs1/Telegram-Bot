import os
import threading
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update

# === Flask App for Render to detect a running web service ===
app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot is running!'

def run_flask():
    port = int(os.environ.get("PORT", 5000))  # Render sets this automatically
    app.run(host="0.0.0.0", port=port)

# === Telegram Bot Logic ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm alive and running.")

def run_bot():
    token = os.environ.get("BOT_TOKEN")  # Store your token in Render environment variables
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))

    application.run_polling()

# === Start both Flask and Telegram in parallel ===
if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    run_bot()
