import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define your command handlers
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! I'm your bot. How can I help?")

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Send /start to get started.")

# Main function to start the bot
def main():
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        logger.error("TELEGRAM_TOKEN environment variable not set.")
        return

    updater = Updater(token=token, use_context=True)

    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    # Start the bot using polling
    updater.start_polling()
    logger.info("Bot started with polling.")
    updater.idle()

# Ensure this only runs when script is called directly
if __name__ == '__main__':
    main()
