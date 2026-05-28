from flask import Flask, request
import requests
from openai import OpenAI

app = Flask(__name__)

# LINEアクセストークン（そのまま使う）
CHANNEL_ACCESS_TOKEN = "WCJj9rLrkhwyjkpRg3WCdvqBiTL8ob8ELb8r4q+VWqPkLRaA7wx5HrR5HqAQxC7KDWCgKoegQitrIRMS/8hHaHvyWm7RtznbmQ/b6L8dTXqar8xmiPJzzxTB+6UyTpEIfWcj+DGhLqLBTeFEYsjSrwdB04t89/1O/w1cDnyilFU="

# OpenAI（※後で環境変数化が推奨）
client = OpenAI(api_key="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")


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
