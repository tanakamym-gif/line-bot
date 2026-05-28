from flask import Flask, request
import requests

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = "WCJj9rLrkhwyjkpRg3WCdvqBiTL8ob8ELb8r4q+VWqPkLRaA7wx5HrR5HqAQxC7KDWCgKoegQitrIRMS/8hHaHvyWm7RtznbmQ/b6L8dTXqar8xmiPJzzxTB+6UyTpEIfWcj+DGhLqLBTeFEYsjSrwdB04t89/1O/w1cDnyilFU="

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
            {"type": "text", "text": f"あなたが言った: {text}"}
        ]
    }

    requests.post(url, headers=headers, json=data)

def get_ai_response(user_message):
    url = "https://defaulta7a81c19a27344e19693b110b3b63c.a9.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/aa60a640e2d344a8bc943568d6c5b277/triggers/manual/paths/invoke?api-version=1"

    response = requests.post(url, json={
        "message": user_message
    })

    result = response.json()
    return result["reply"]
    
