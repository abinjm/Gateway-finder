from telegram.ext import CommandHandler
from validator import add_proxy, list_proxies, remove_proxy, proxy_alive, add_item, list_items, remove_item, gate_check

--- Proxy commands ---

async def addpxy(update, context):
if not context.args:
await update.message.reply_text("Usage: /addpxy ip:port[:user:pass]")
return
add_proxy(context.args[0])
await update.message.reply_text("✅ Proxy added")

async def proxy(update, context):
rows = list_proxies()
if not rows:
await update.message.reply_text("No proxies saved")
return
msg = "\n".join(f"{i}. {p}" for i, p in rows)
await update.message.reply_text(msg)

async def rmpxy(update, context):
if not context.args:
await update.message.reply_text("Usage: /rmpxy id|all")
return
remove_proxy(context.args[0])
await update.message.reply_text("✅ Removed")

async def Pchk(update, context):
alive = [p for _, p in list_proxies() if proxy_alive(p)]
if alive:
await update.message.reply_text(f"Alive proxy → {alive[0]}")
else:
await update.message.reply_text("No alive proxy")

async def chk(update, context):
await Pchk(update, context)

--- Item/CC commands ---

async def additem(update, context):
if not context.args:
await update.message.reply_text("Usage: /additem <item>")
return
add_item(context.args[0])
await update.message.reply_text("✅ Item added")

async def listitem(update, context):
rows = list_items()
if not rows:
await update.message.reply_text("No items saved")
return
msg = "\n".join(f"{i}. {p}" for i, p in rows)
await update.message.reply_text(msg)

async def rmitem(update, context):
if not context.args:
await update.message.reply_text("Usage: /rmitem id|all")
return
remove_item(context.args[0])
await update.message.reply_text("✅ Removed")

async def checkitem(update, context):
ok, msg = gate_check()
await update.message.reply_text(msg)

--- /help command ---

async def help_cmd(update, context):
msg = """
Proxy Commands:
/addpxy ip:port[:user:pass] - Add proxy
/proxy - List proxies
/rmpxy <id|all> - Remove proxy
/Pchk - Check alive proxy

Item/CC Commands:
/additem <item> - Add CC, token, or URL
/listitem - List items
/rmitem <id|all> - Remove item
/checkitem - Check valid item

General:
/chk - Shortcut for /Pchk
/help - Show this message
"""
await update.message.reply_text(msg)

--- register commands ---

def register_commands(app):
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("chk", chk))
app.add_handler(CommandHandler("Pchk", Pchk))
app.add_handler(CommandHandler("addpxy", addpxy))
app.add_handler(CommandHandler("proxy", proxy))
app.add_handler(CommandHandler("rmpxy", rmpxy))
app.add_handler(CommandHandler("additem", additem))
app.add_handler(CommandHandler("listitem", listitem))
app.add_handler(CommandHandler("rmitem", rmitem))
app.add_handler(CommandHandler("checkitem", checkitem))

Now make file as cmd py or validator py tell one