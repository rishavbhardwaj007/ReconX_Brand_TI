# utils/telegram_utils.py

import os
import requests

def send_telegram_alert(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    response = requests.post(url, json=payload)
    return response.status_code == 200

def search_telegram(brand):
    # Placeholder logic (replace with real source like tgstat or your DB)
    if "@" in brand or brand.lower() in ["testbrand", "examplecorp"]:
        return f"⚠️ Potential Telegram mention of `{brand}` found."
    return "No mentions found on Telegram."
