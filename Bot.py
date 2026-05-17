import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from wallet import create_wallet
from database import init_db, get_user, save_user
from hyperliquid_client import HLClient

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Welcome fren!\n"
        "Commands:\n"
        "/wallet - create/view wallet\n"
        "/buy COIN SIZE\n"
        "/sell COIN SIZE"
    )

async def wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tid = update.effective_user.id
    user = await get_user(tid)

    if user:
        return await update.message.reply_text(
            f"👛 Your wallet:\n{user['wallet_address']}"
        )

    priv, addr = create_wallet()
    await save_user(tid, priv, addr)

    await update.message.reply_text(
        f"🎉 Wallet created!\nAddress: {addr}"
    )

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tid = update.effective_user.id
    user = await get_user(tid)

    if not user:
        return await update.message.reply_text("❌ Use /wallet first")

    if len(context.args) < 2:
        return await update.message.reply_text("Usage: /buy COIN SIZE")

    coin = context.args[0].upper()
    size = float(context.args[1])

    client = HLClient(user["wallet_private_key"])
    result = client.buy(coin, size)

    if "error" in result:
        return await update.message.reply_text("❌ " + result["error"])

    client.fee()

    await update.message.reply_text(f"🟢 LONG executed!\n{coin} x{size}")

async def sell(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tid = update.effective_user.id
    user = await get_user(tid)

    if not user:
        return await update.message.reply_text("❌ Use /wallet first")

    if len(context.args) < 2:
        return await update.message.reply_text("Usage: /sell COIN SIZE")

    coin = context.args[0].upper()
    size = float(context.args[1])

    client = HLClient(user["wallet_private_key"])
    result = client.sell(coin, size)

    if "error" in result:
        return await update.message.reply_text("❌ " + result["error"])

    client.fee()

    await update.message.reply_text(f"🔴 SHORT executed!\n{coin} x{size}")

async def main():
    await init_db()

    app = ApplicationBuilder().token(
        __import__("config").TELEGRAM_BOT_TOKEN
    ).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("wallet", wallet))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(CommandHandler("sell", sell))

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
