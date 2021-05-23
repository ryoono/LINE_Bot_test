# -*- coding: utf-8 -*-

import os
import sys
from argparse import ArgumentParser

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

# 環境変数を参照し変数に格納
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# Webhookからのリクエストをチェック(LINEトークから)
# LINEからはhttp://~/callbackに送信する設定になっている
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
        abort(400)

    return 'OK'

# Webhookからのリクエストをチェック(GASからのモーニング割り込み？)
# GASからはhttp://~/morningに送信する設定になっている
@app.route("/morning", methods=['POST'])
def morning():
    # MEMO 朝の定期実行コードを記述する
    pass

# LINEでMessageEvent（普通のメッセージを送信された場合）が起こった場合に実行
# reply_messageの第一引数のevent.reply_tokenは、イベントの応答に用いるトークン
# 第二引数には、linebot.modelsに定義されている返信用のTextSendMessageオブジェクト
@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    line_bot_api.reply_message(
        event.reply_token,
        #TextSendMessage(text=event.message.text)
        TextSendMessage(text='固定メッセージテスト')
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
