from flask import Flask, request
import requests
import openai
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return "Xiaoya Bot is running with GPT!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        # 呼叫 OpenAI GPT 回應
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是個貼心可愛的助手，名字叫小雅。"},
                    {"role": "user", "content": text}
                ]
            )
            reply = response.choices[0].message["content"].strip()
        except Exception as e:
            reply = f"發生錯誤：{str(e)}"

        # 發送訊息回 Telegram
        requests.post(f"{BOT_URL}/sendMessage", json={"chat_id": chat_id, "text": reply})

    return "OK"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
