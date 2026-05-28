from flask import Flask, request
import requests
from openai import OpenAI

app = Flask(__name__)

# LINE
CHANNEL_ACCESS_TOKEN = "WCJj9rLrkhwyjkpRg3WCdvqBiTL8ob8ELb8r4q+VWqPkLRaA7wx5HrR5HqAQxC7KDWCgKoegQitrIRMS/8hHaHvyWm7RtznbmQ/b6L8dTXqar8xmiPJzzxTB+6UyTpEIfWcj+DGhLqLBTeFEYsjSrwdB04t89/1O/w1cDnyilFU="

# OpenAI
client = OpenAI(api_key="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")

@app.route("/callback", methods=['POST'])
def callback():
    body = request.json

    for event in body["events"]:
        if event["type"] == "message":
            reply_token = event["replyToken"]
            user_message = event["message"]["text"]

            ai_response = get_ai_response(user_message)
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
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "あなたは親切で丁寧な日本語アシスタントです。簡潔に回答してください。"},
            {"role": "user", "content": user_message}
        ],
        max_tokens=300
    )

    return response.choices[0].message.content
