####################################################################################################
#トグル
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

from time import time
from datetime import timedelta
from argparse import ArgumentParser
import sys
#import RPi.GPIO as GPIO
###########.envから抽出###########
from dotenv import load_dotenv
load_dotenv()
import os
############## API ##############
channel_secret = os.getenv('channel_secret')
channel_access_token = os.getenv('channel_access_token')

openai_api_key = os.getenv('openai_api_key')
#################################
app = Flask(__name__)
line_bot_api = LineBotApi(channel_access_token)  #チャネルアクセストークン
handler = WebhookHandler(channel_secret)  #チャネルシークレット
#handler = WebhookHandler(channel_secret)  #チャネルシークレット
#####################################
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)
###################################################################################################
#######################XXXXXXXX#########################
########################################################


###################################################################################################
#####################開閉プログラム#######################
########################################################
# # サーボモータを回す関数の登録
# SERVO_PIN = 18
# SERVO_OPEN_STATE = YYY（開錠状態）
# SERVO_CLOSE_STATE = ZZZ（施錠状態）

# def KeyOpener():
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setup(SERVO_PIN, GPIO.OUT)
#     servo = GPIO.PWM(SERVO_PIN, 50)
#     servo.start(0.0)
#     servo.ChangeDutyCycle(SERVO_OPEN_STATE)
#     time.sleep(1.0)
#     GPIO.cleanup()

# def KeyCloser():
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setup(SERVO_PIN, GPIO.OUT)
#     servo = GPIO.PWM(SERVO_PIN, 50)
#     servo.start(0.0)
#     servo.ChangeDutyCycle(SERVO_CLOSE_STATE)
#     time.sleep(1.0)
#     GPIO.cleanup()

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# @handler.add(MessageEvent, message=TextMessage)
# def message_text(event):
    text = event.message.text

    # テキストの内容で条件分岐
    if text == '🔑🔓':
        TextSendMessage('ᴜɴʟᴏᴄᴋɪɴɢ🔑...ᴡᴇʟᴄᴏᴍᴇ!!')
        # 鍵開ける
        ###KeyOpener()
        # 返事
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage('ᴜɴʟᴏᴄᴋɪɴɢ🔑\n\nᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴍʏ ᴡᴏʀʟᴅ🌴')
        )
    elif text == '🔒':
        TextSendMessage('ʟᴏᴄᴋɪɴɢ🔒')
        # 鍵閉める
        ###KeyCloser()
        # 返事
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage('ʟᴏᴄᴋɪɴɢ🔒')
        )
    else:
        # 木霊
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )

###################################################################################################
#######################Chat-GPT#########################
########################################################
import openai
 
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # ユーザーからのメッセージを取得
    user_message = event.message.text
 
    # OpenAIのGPT-4を使ってユーザーからのメッセージに返答を生成
    response = openai.ChatCompletion.create(
        model="gpt-3.5", 
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message},
        ],
    )
 
    # OpenAIからの返答を取得
    gpt_response = response['choices'][0]['message']['content']
 
    # メッセージを返送
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=gpt_response))
 

########################################################
########################################################
if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port ] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=5000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
######################################################################################
