from telegram import Update
from telegram.ext import CallbackContext
from keys import generate_key, redeem_key

ADMIN_ID = 7937333659  # Replace with your Telegram ID

async def gkey(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_ID:
        return
    if not context.args:
        await update.message.reply_text("Usage: /gkey 1d | 10d | 30d | 1m | 6m")
        return
    key = generate_key(context.args[0])
    if not key:
        await update.message.reply_text("Invalid duration")
    else:
        await update.message.reply_text(f"Generated key:\n`{key}`", parse_mode="Markdown")

async def redeem(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("Usage: /redeem samcc_xxxxxx")
        return
    success, result = redeem_key(update.effective_user.id, context.args[0])
    if success:
        await update.message.reply_text("✅ Key redeemed. Premium activated.")
    else:
        await update.message.reply_text(f"❌ {result}")