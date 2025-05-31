from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# ✅ Your new token
TOKEN = "7643390545:AAEnR7LpJ3AEw-APqWvSz5_0tlgAdK9Y0mA"

# Start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! I'm alive and working!")

# Main function
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Register the /start command
    dp.add_handler(CommandHandler("start", start))

    # Start polling for updates
    updater.start_polling()

    print("Bot is running... Press Ctrl+C to stop.")
    updater.idle()

if __name__ == "__main__":
    main()
