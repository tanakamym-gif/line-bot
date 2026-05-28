from flask import Flask, request
import requests

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = "ここにアクセストークン"

@app.route("/callback", methods=['POST'])
def callback():
    body = request.json

    for event in body["events"]:
        if event["type"] == "message":
            reply_token = event["replyToken"]
            user_message = event["message"]["text"]

            reply(reply_token, user_message)

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
            {"type": "text", "text": f"あなたが言った: {text}"}
        ]
    }

    requests.post(url, headers=headers, json=data)
