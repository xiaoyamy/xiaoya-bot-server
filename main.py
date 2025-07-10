
from flask import Flask, request
import requests
import os

app = Flask(__name__)
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.route('/')
def home():
    return "Xiaoya Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "（未辨識的訊息）")
        reply = f"小雅收到你的訊息囉：{text}"
        requests.post(f"{BOT_URL}/sendMessage", json={"chat_id": chat_id, "text": reply})
    return "OK"

if __name__ == '__main__':
    app.run()
