# line bot sdk
# web app 首要檔案叫做 app.py (寫網站=架設伺服器) => flask & django
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

line_bot_api = LineBotApi('J4rXFm5uP+P2QqwsiT8M36LEfEALMTON+23qmvjvVwn5eTqmB94b63BQ14Nj3tlw97LskfvrcbFO6e12/H9M6uSHJKTkHA24Ttyr9mmB3b/nR35nD+ZKfQ1iITgUDPNyNRgMG2qyFqgUqLvjm1o7zQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('87bd0639ead3aacae83a579054178553')

# route 路徑: 如果有人去跑網址/callback，就會觸發執行以下 function
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

# 再觸發這個，執行 handler 來處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

# 直接執行這個檔案的時候才會執行裡面的內容
# 如果不加，在載入時(import)，就會執行這個程式 -> 不好
if __name__ == "__main__":
    app.run()