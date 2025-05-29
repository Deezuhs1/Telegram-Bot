
import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Define a simple start command handler
def start(update, context):
    update.message.reply_text('Bot is online and ready to send alerts!')

# Define a function to send a custom message
def send_alert(update, context):
    update.message.reply_text('🚨 Custom alert triggered!')

def main():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        print("TELEGRAM_BOT_TOKEN environment variable not set")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, send_alert))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
