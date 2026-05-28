from flask import Flask, request
import requests
from openai import OpenAI

app = Flask(__name__)

# LINEアクセストークン（そのまま使う）
CHANNEL_ACCESS_TOKEN = "アクセストークン"

# OpenAI（※後で環境変数化が推奨）
client = OpenAI(api_key="シークレットキー")


@app.route("/callback", methods=['POST'])
def callback():
    body = request.json

    for event in body.get("events", []):
        if event.get("type") == "message":
            reply_token = event.get("replyToken")
            message = event.get("message", {})
            user_message = message.get("text", "")

            # AI応答
            ai_response = get_ai_response(user_message)

            # LINEへ返信
            reply(reply_token, ai_response)

    return "OK"


def reply(reply_token, text):
    url = "https://api.line.me/v2/bot/message/reply"

    headers = {
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text",
                "text": text
            }
        ]
    }

    requests.post(url, headers=headers, json=data)


def get_ai_response(user_message):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # ← 安定モデル
            messages=[
                {
                    "role": "system",
                    "content": "あなたは企業の問い合わせ対応担当です。日本語で丁寧に簡潔に回答してください。"
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_tokens=300
        )

        return response.choices[0].message.content

    except Exception as e:
        print("OPENAI ERROR:", e)
        return "現在AI応答に問題が発生しています。時間をおいて再度お試しください。"


if __name__ == "__main__":
    app.run(port=5000)
