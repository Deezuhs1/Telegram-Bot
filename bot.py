import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)
import os

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Simulate user-tracked dev wallets
user_watchlists = {}

# Simulated dev clusters
GOLDEN_CLUSTER = {'CemfzAqaUGDof18CEdB1jv2CeECGQqMjWEMh8772pump'}
BIG_GAINER_CLUSTER = {'9j6twpYWrV1ueJok76D9YK8wJTVoG9Zy8spC7wnTpump'}

# Simulated token data (you’ll plug real logic here)
TOKEN_DEPLOYER_MAP = {
    'So1ToKenExAmpLe1111111111111111111111111': 'CemfzAqaUGDof18CEdB1jv2CeECGQqMjWEMh8772pump',
    'BadTokenExample22222222222222222222222': 'UnknownDeployer'
}

TOKEN_INFO = {
    'So1ToKenExAmpLe1111111111111111111111111': {
        'market_cap': '$4.4M',
        'status': 'Steady Growth',
        'launch_age': '16 days ago'
    },
    'BadTokenExample22222222222222222222222': {
        'market_cap': '$18K',
        'status': 'Dead',
        'launch_age': '4 days ago'
    }
}

# COMMAND HANDLERS
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! I’m your token tracker bot.\n\n"
        "Commands:\n"
        "/status - Check bot health\n"
        "/addwallet <wallet> - Track a dev wallet\n"
        "/listwallets - See tracked wallets\n"
        "/removewallet <wallet> - Remove tracked wallet\n\n"
        "Or just send a token address for info!"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    count = len(user_watchlists.get(user_id, []))
    await update.message.reply_text(
        f"🤖 Bot is running.\nYou're tracking {count} developer wallet(s)."
    )

async def addwallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    args = context.args
    if not args:
        return await update.message.reply_text("Usage: /addwallet <wallet_address>")
    
    wallet = args[0]
    user_watchlists.setdefault(user_id, set()).add(wallet)
    await update.message.reply_text(f"✅ Wallet `{wallet}` added to your tracking list.", parse_mode='Markdown')

async def listwallets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    wallets = user_watchlists.get(user_id, [])
    if not wallets:
        await update.message.reply_text("You aren’t tracking any wallets yet.")
    else:
        wallet_list = "\n".join(wallets)
        await update.message.reply_text(f"📋 Tracked Wallets:\n{wallet_list}")

async def removewallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    args = context.args
    if not args:
        return await update.message.reply_text("Usage: /removewallet <wallet_address>")
    
    wallet = args[0]
    user_wallets = user_watchlists.get(user_id, set())
    if wallet in user_wallets:
        user_wallets.remove(wallet)
        await update.message.reply_text(f"🗑️ Removed `{wallet}` from your tracking list.", parse_mode='Markdown')
    else:
        await update.message.reply_text("That wallet wasn’t in your list.")

# TOKEN ADDRESS DETECTOR
async def handle_token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    token = update.message.text.strip()
    if token not in TOKEN_DEPLOYER_MAP:
        return await update.message.reply_text("❓ Unknown token address or not indexed yet.")
    
    deployer = TOKEN_DEPLOYER_MAP[token]
    info = TOKEN_INFO.get(token, {})
    cluster_note = ""

    if deployer in GOLDEN_CLUSTER:
        cluster_note = "🥇 *Golden Cluster*"
    elif deployer in BIG_GAINER_CLUSTER:
        cluster_note = "🔥 *Big Gainer Cluster*"
    else:
        cluster_note = "⚠️ Unknown/Unverified Deployer"

    reply = (
        f"📊 *Token Intelligence:*\n"
        f"Deployer: `{deployer}`\n"
        f"Cluster: {cluster_note}\n\n"
        f"Market Cap: {info.get('market_cap', 'Unknown')}\n"
        f"Status: {info.get('status', 'Unknown')}\n"
        f"Launched: {info.get('launch_age', 'Unknown')}"
    )

    await update.message.reply_text(reply, parse_mode='Markdown')

# MAIN
if __name__ == '__main__':
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(bot_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("addwallet", addwallet))
    app.add_handler(CommandHandler("listwallets", listwallets))
    app.add_handler(CommandHandler("removewallet", removewallet))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_token))

    app.run_polling()
