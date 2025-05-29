from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# === Replace this with your real token ===
BOT_TOKEN = "7643390545:AAG7mNjIP3cEP_7P6F93DJCdNHP75O89TNI"

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your bot. Use /help for commands.")

# Command: /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Available commands:\n/start - Welcome message\n/help - Show this help")

def main():
    # Initialize the application
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # Start the bot
    app.run_polling()

if __name__ == "__main__":
    main()
