import logging
import os
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load bot token
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TOKEN_HERE")  # Replace if not using environment variable

# Define command handlers
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! Bot is live on Render and responding!")

# Error handler
def error(update: object, context: CallbackContext):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# Main application logic
def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add command handlers
    dp.add_handler(CommandHandler("start", start))

    # Log all errors
    dp.add_error_handler(error)

    # Set webhook info
    PORT = int(os.environ.get("PORT", "8443"))
    WEBHOOK_URL = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'your-app-name.onrender.com')}/{BOT_TOKEN}"

    # Start the webhook
    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=WEBHOOK_URL,
    )

    updater.idle()

if __name__ == "__main__":
    main()
