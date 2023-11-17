from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)


app = Flask(__name__)

line_bot_api = LineBotApi('crMsoNUr1i3TCHe/dNJOQ3ZF2my3GeYF7oWv55gCT168IxGq55SJEyCJ2hmqeXrr3lruSOZksf3YfXvUuL9ez2AZt3DiyGy2zbvuQ2zn6O4vc+uUTqsgxwO5pK+lRaCiAo60OKlSjyR70E6/7au7VgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('638620b469622551637ecb7ec84fcbdb')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()