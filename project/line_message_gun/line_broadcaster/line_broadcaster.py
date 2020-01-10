"""
line_broadcaster.py
[TESTING FUNCTION]
Connects to line's MessagingApi and broadcasts messages to user.
"""
from flask import (
    Blueprint, Flask, request, abort, current_app
)
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

# Reads tokens for line API access
from line_broadcaster.security_reader import SecurityReader
secretReader = SecurityReader()
lineApi = LineBotApi(secretReader.getToken())
lineWebhook = WebhookHandler(secretReader.getWebhookSecret())
secretReader.close()

bp = Blueprint("broadcaster", __name__, url_prefix="/line")

@bp.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    current_app.logger.info("Request body:" + body)
    print("--received request")
    #handle webhook body
    try:
        lineWebhook.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@lineWebhook.add(MessageEvent, message=TextMessage)
def handleMessage(event):
    if (event.message.text == "get id"):
        lineApi.reply_message(
            event.reply_token,
            TextSendMessage(text="Your secret mix is: " + event.source.user_id)
        )
    else:
        lineApi.reply_message(
            event.reply_token,
            TextSendMessage(text="test")
        )

def broadcastMessage(message="default message"):
    lineApi.broadcast(
        TextSendMessage(text=message)
    )

def multiCastMessage(userIdList):
    lineApi.multicast(
        userIdList,
        TextSendMessage(text="You've received some Secret Chikuma Mix.")
    )

if __name__ == "__main__":
    #broadcastMessage()
    multiCastMessage()
