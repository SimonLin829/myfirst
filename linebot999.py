# 套件準備
import requests
import json
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent,TemplateSendMessage, ButtonsTemplate, PostbackAction, URIAction,
    CarouselTemplate,CarouselColumn,MessageEvent, TextMessage,
    TextSendMessage, ImageSendMessage, MessageAction,ConfirmTemplate,QuickReply,QuickReplyButton,
)
import datetime
today = datetime.date.today()
# Web Application 準備
app = Flask(__name__)
line_bot_api = LineBotApi("m56TRmt+7nk5XEjKuSQnf2wv4WatylCZY5PQxo3eG5dOGGuxFHGGrLGPFagNdVOLrD4qh++Pft+Ks8q9qZcGhzKhH/9QasYV/arh2XO+wxF9jG1Bp8qOvUxC8hP+1fN0mGEM/A+Sh2CD6FgY1sRkGAdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("c4f9c9a5cba28df93bcabe046a4f82c9")


# Line　Messaging api 的入口
@app.route("/callback", methods=["POST"])
def callback():
    print("用戶傳訊息囉")
    # 把信件內容取出來
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        # 交給handler做處理
        handler.handle(body, signature)

    # 如果是不合法的信件，則忽略不做暫用ngrok
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return "OK"

# 用戶關注我們的時候:
#     取他個資
#     發歡迎的文字消息
#     發歡迎的圖片消息
#     發一個按鍵範本消息
# 告訴handler收到關注事件的時候，做下面的辦法
@handler.add(FollowEvent)
def handle_follow_event(event):
    # 取用戶個資
    # line_bot_api get user profile
    user_profile = line_bot_api.get_profile(event.source.user_id)

    # 把用戶個資打印出來
    print(user_profile.user_id)
    print(user_profile.display_name)
    print(user_profile.picture_url)
    print(user_profile.status_message)

    user_id_array = []
    user_id_array.append(user_profile.user_id)
    line_bot_api.set_default_rich_menu("richmenu-8b955072ab003e314754f16ebb41ab51")
    # 可以把用戶個資存到資料庫，或存到檔案裏面
    # python variable to json save file
    # 將用戶資訊存在檔案內
    with open("./users.txt", "a") as myfile:
        myfile.write(json.dumps(vars(user_profile), sort_keys=True))
        myfile.write("\r\n")

    # 請line_bot_api發文字消息給用戶
    text_send_message = TextSendMessage("哈囉~歡迎使用醫院小幫手，點擊服務選單使用想要的功能。")
    ConfirmTemplate_1 = TemplateSendMessage(
        alt_text="Confirm template",
        template=ConfirmTemplate(
            text="很高興認識你" + user_profile.display_name + "請問有在本院看過醫生嗎?",
            actions=[
                MessageAction(
                    label="有",
                    text="有",

                ),
                MessageAction(
                    label="沒有",
                    text="沒有",

                )
            ]
        )
    )


    # 請line_bot_api 一口氣回復多消息給用戶
    line_bot_api.reply_message(
        event.reply_token,
        [
            text_send_message,
            # image_send_message,
            ConfirmTemplate_1,
            # buttons_template_message,
            # buttons_template_message2
        ]
    )
@handler.add(MessageEvent, message=TextMessage)
def handle_message_1(event):
    #其他功能
    if event.message.text == "就醫":
        buttons_template_message_0 = TemplateSendMessage(
            alt_text="Buttons template",
            template=ButtonsTemplate(
                title="其他功能",
                text="請選擇",
                actions=[
                    URIAction(
                        label="地理位置",
                        uri="https://line.me/R/nv/location/"
                    ),
                    URIAction(
                        label="心動拍拍",
                        uri="https://line.me/R/nv/camera/"
                    ),
                    URIAction(
                        label="google",
                        uri="https://www.google.com/"
                    ),
                    URIAction(
                        label="打電話",
                        uri="tel://034257387"
                    )
                ]
            )
        )
        line_bot_api.reply_message(
            event.reply_token,
            [buttons_template_message_0])
    #follow_event後續
    if event.message.text == "有":
        ConfirmTemplate_2 = TemplateSendMessage(
            alt_text="Confirm template",
            template=ConfirmTemplate(
                text="要透過本服務登入你就醫的醫院帳戶嗎？登入後我可以提供更加個人化的服務，像帶入常用醫師供你快速掛號，或是提醒你就診請至智慧手機上確認訊息內容。",
                actions=[
                    URIAction(
                        label="好",
                        uri="https://example.com/"),
                    MessageAction(
                        label="先不用",
                        text="先不用",

                    )
                ]
            )
        )

        line_bot_api.reply_message(
            event.reply_token,
            [ConfirmTemplate_2])
    if event.message.text == "先不用":
        buttons_template_message_2 = TemplateSendMessage(
            alt_text="Buttons template",
            template=ButtonsTemplate(

                text="那現在還能為您做什麼呢?",
                actions=[
                    MessageAction(
                        label="該看哪一科",
                        text="該看哪一科"
                    ),
                    URIAction(
                        label="我要掛號",
                        uri="https://example.com/"
                    ),
                    URIAction(
                        label="電話諮詢",
                        uri="tel://034257387"
                    )
                ]
            )
        )
        line_bot_api.reply_message(
            event.reply_token,
            [buttons_template_message_2])
    if event.message.text == "沒有":
        text_send_message_1 = TextSendMessage("若您不曾在本院看過醫生，我們還未幫你建立醫院資料，但您還是可用下面服務選單功能。")
        text_send_message_2 = TextSendMessage("未來如有完成初診後，就可以建立醫院帳戶，便可更快速完成預約或查詢。")
        buttons_template_message_1 = TemplateSendMessage(
            alt_text="Buttons template",
            template=ButtonsTemplate(

                text="那現在還能為您做什麼呢?",
                actions=[
                    MessageAction(
                        label="該看哪一科",
                        text ="該看哪一科"
                    ),
                    URIAction(
                        label="我要掛號",
                        uri="https://example.com/"
                    ),
                    URIAction(
                        label="電話諮詢",
                        uri="tel://034257387"
                    )
                ]
            )
        )

        line_bot_api.reply_message(
            event.reply_token,
            [text_send_message_1,
             text_send_message_2,
             buttons_template_message_1,

             ]
        )
    #我要掛號部分QuickReplyButton
    if event.message.text == "我要掛號":
        text_message = TextSendMessage(text="好的，請問要掛哪個醫生呢",
                                       quick_reply=QuickReply(items=[
                                           QuickReplyButton(action=MessageAction(label="王曉明", text="王曉明")),
                                           QuickReplyButton(action=MessageAction(label="王大明", text="王大明")),
                                           QuickReplyButton(action=MessageAction(label="林雨叡", text="林雨叡"))
                                       ]))
        line_bot_api.reply_message(
            event.reply_token,
            [text_message])
    if event.message.text == "王曉明":
        text_message = TextSendMessage(text="請選擇日期",
                                       quick_reply=QuickReply(items=[
                                           QuickReplyButton(action=PostbackAction(label="星期一上午", display_text="星期一上午",data="date=111&size=big")),
                                           QuickReplyButton(action=PostbackAction(label="星期一上午", display_text="星期一上午",data="date=222&size=big")),
                                           QuickReplyButton(action=PostbackAction(label="星期一上午", display_text="星期一上午",data="date=333&size=big"))
                                       ]))
        line_bot_api.reply_message(
            event.reply_token,
            [text_message])
    #該看哪一科TemplateSendMessage
    if event.message.text == "該看哪一科":
        carousel_template_message = TemplateSendMessage(
            alt_text="Carousel template",
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(

                        title="哪裡不舒服?",
                        text="請選擇部位",
                        actions=[
                            MessageAction(
                                label="頭部",
                                text="頭部"
                            ),
                            MessageAction(
                                label="胸部",
                                text="胸部"
                            ),
                            MessageAction(
                                label="腹部",
                                text="腹部"
                            )
                        ]
                    ),
                    CarouselColumn(

                        title="哪裡不舒服?",
                        text="請選擇部位",
                        actions=[
                            MessageAction(
                                label="腿部",
                                text="腿部"
                            ),
                            MessageAction(
                                label="手部",
                                text="手部"
                            ),
                            MessageAction(
                                label="背部",
                                text="背部"
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(
            event.reply_token,
            [carousel_template_message])

    if event.message.text == "頭部":
        carousel_template_message_2 = TemplateSendMessage(
            alt_text="Carousel template",
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url="https://i.imgur.com/Ey9EoMF.jpg",
                        text="眼部",
                        actions=[
                            URIAction(
                                label="查看眼部症狀",
                                uri="https://example.com/"
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url="https://i.imgur.com/X71k0XX.jpg",
                        text="頭部",
                        actions=[
                            URIAction(
                                label="查看頭部症狀",
                                uri="https://example.com/")]
                            ),
                            CarouselColumn(
                                thumbnail_image_url="https://i.imgur.com/AywGzvn.jpg",
                                text="耳部",
                                actions=[
                                    URIAction(
                                        label="查看耳部症狀",
                                        uri="https://example.com/")]
                                    ),
                                    CarouselColumn(
                                        thumbnail_image_url="https://i.imgur.com/ueoKKQ6.jpg",
                                        text="喉嚨",
                                        actions=[
                                            URIAction(
                                                label="查看喉嚨症狀",
                                                uri="https://example.com/"
                                            )]
                    )
                ]
            )
        )
    line_bot_api.reply_message(
        event.reply_token,
        [carousel_template_message_2])

#postback部分
"""
當用戶點擊PostbackAction，會發出PostbackEvent
我們要告訴handler接收PostbackEvent

並且解析裡面的data欄位，麻煩用querystring做設計

再用條件式做判斷

"""
from linebot.models import (
    PostbackEvent
)
@handler.add(PostbackEvent)
def handle_postback_event(event):
    print(event)

    # 取出data，解析欄位
    # 判斷欄位的關鍵字
    if event.postback.data == "date=111&size=big":
        line_bot_api.reply_message(event.reply_token, TextSendMessage("以幫您預約星期一上午"))
    if event.postback.data == "date=222&size=big":
        line_bot_api.reply_message(event.reply_token, TextSendMessage("以幫您預約星期三上午"))
    if event.postback.data == "date=333&size=big":
        line_bot_api.reply_message(event.reply_token, TextSendMessage("以幫您預約星期五上午"))
# 運行wb　application
#
if __name__ == "__main__":
    app.run(host="0.0.0.0")