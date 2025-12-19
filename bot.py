import requests
import re
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_CREDIT = "@abinjmoffical"

GATEWAYS = {
    "Stripe": {
        "patterns": ["js.stripe.com", "__stripe_mid", "stripe.publishablekey"],
        "flow": "2D / 3D (Bank dependent)",
        "requires": "Card Number, Expiry, CVV (OTP if 3D)"
    },
    "Shopify": {
        "patterns": ["cdn.shopify.com", "shopify-checkout"],
        "flow": "Mostly 3D",
        "requires": "Card, CVV, OTP"
    },
    "Razorpay": {
        "patterns": ["checkout.razorpay.com"],
        "flow": "3D",
        "requires": "Card, CVV, OTP"
    },
    "PayU": {
        "patterns": ["secure.payu.in", "bolt.min.js"],
        "flow": "3D",
        "requires": "Card, CVV, OTP"
    },
    "Paytm": {
        "patterns": ["securegw.paytm.in"],
        "flow": "3D",
        "requires": "OTP / App approval"
    },
    "Adyen": {
        "patterns": ["checkoutshopper"],
        "flow": "2D / 3D",
        "requires": "Card, CVV (OTP possible)"
    },
    "Braintree": {
        "patterns": ["braintreegateway.com"],
        "flow": "2D",
        "requires": "Card, CVV"
    },
    "Checkout.com": {
        "patterns": ["checkout.com/js"],
        "flow": "2D / 3D",
        "requires": "Card, CVV (OTP possible)"
    },
    "Interac": {
        "patterns": ["interac.ca"],
        "flow": "Redirect / 3D-like",
        "requires": "Bank Login / OTP"
    }
}

def analyze_site(url: str):
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(url, headers=headers, timeout=12)
    except Exception as e:
        return {"error": str(e)}

    content = r.text.lower()

    detected_gateways = []
    for gw, data in GATEWAYS.items():
        for pattern in data["patterns"]:
            if pattern.lower() in content:
                detected_gateways.append(gw)
                break

    cloudflare = (
        "cloudflare" in r.headers.get("Server", "").lower()
        or "__cf_chl" in content
    )

    captcha = bool(re.search(r"captcha|hcaptcha|recaptcha", content))

    return {
        "gateways": detected_gateways,
        "cloudflare": cloudflare,
        "captcha": captcha
    }

async def gateway(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Usage:\n/gateway https://example.com"
        )
        return

    url = context.args[0]
    if not url.startswith("http"):
        url = "https://" + url

    user = update.effective_user.username
    checked_by = f"@{user}" if user else "Unknown"

    result = analyze_site(url)

    if "error" in result:
        await update.message.reply_text(f"❌ Error:\n{result['error']}")
        return

    text = (
        "❄️ 𝙂𝘼𝙏𝙀𝙒𝘼𝙔 𝙇𝙊𝙊𝙆𝙐𝙋 ❄️\n"
        f"🔰 𝙎𝙄𝙏𝙀 ➜ {url}\n\n"
    )

    if result["gateways"]:
        text += "🔰 𝙂𝘼𝙏𝙀𝙒𝘼𝙔 ➜ " + ", ".join(result["gateways"]) + "\n\n"
        for gw in result["gateways"]:
            info = GATEWAYS.get(gw)
            text += (
                f"• {gw}\n"
                f"  ↳ Flow: {info['flow']}\n"
                f"  ↳ Requires: {info['requires']}\n\n"
            )
    else:
        text += "🔰 𝙂𝘼𝙏𝙀𝙒𝘼𝙔 ➜ Not Detected\n\n"

    if result["captcha"]:
        text += "🛑 CAPTCHA detected.\n"
    if result["cloudflare"]:
        text += "🛑 Cloudflare protection detected.\n"

    text += (
        f"\n𝘾𝙝𝙚𝙘𝙠𝙚𝙙 𝘽𝙮 {checked_by}\n"
        f"𝘽𝙤𝙩 𝘽𝙮 {BOT_CREDIT}"
    )

    await update.message.reply_text(text)

def main():
    app = ApplicationBuilder().token(
        "8354463122:AAF9nR5ePOHFdGYPUPglqypAraar-CqH6PY"
    ).build()

    app.add_handler(CommandHandler("gateway", gateway))
    app.run_polling()

if __name__ == "__main__":
    main()