from flask import Flask, request
import requests
import os
import openai

app = Flask(__name__)

# 環境變數
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return "Xiaoya Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_message = data["message"].get("text", "（未辨識的訊息）")

        try:
            completion = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )
            reply = completion.choices[0].message.content.strip()

        except Exception as e:
            reply = f"⚠️ 發生錯誤：{str(e)}"

        requests.post(f"{BOT_URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": reply
        })

    return "OK"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
