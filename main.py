@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_message = data["message"].get("text", "（未辨識的訊息）")

        try:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_message}]
            )
            reply = completion.choices[0].message.content.strip()
        except Exception as e:
            reply = f"小雅遇到錯誤了：{str(e)}"

        requests.post(f"{BOT_URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": reply
        })
    return "OK"
