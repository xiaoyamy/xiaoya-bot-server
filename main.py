from flask import Flask, request
import requests
import os
from openai import OpenAI

app = Flask(__name__)

# 從環境變數讀取 Telegram Bot Token 和 OpenAI API 金鑰
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BOT_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# 初始化 OpenAI 客戶端
client = OpenAI(api_key=OPENAI_API_KEY)

@app.route('/')
def home():
    return "Xiaoya Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_message = data["message"].get("text", "（無法辨識的訊息）")
        
        try:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )
            reply = completion.choices[0].message.content.strip()
        except Exception as e:
            reply = f"⚠️ 發生錯誤：{e}"

        # 發送訊息回 Telegram
        requests.post(f"{BOT_URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": reply
        })

    return "OK"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
