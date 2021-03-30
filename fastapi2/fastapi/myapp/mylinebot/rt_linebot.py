from fastapi import APIRouter, Request, HTTPException
from fastapi.logger import logger
import copy


## import linebot related
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, FlexSendMessage,
    LocationSendMessage, ImageSendMessage, StickerSendMessage,
    CarouselTemplate,CarouselColumn,URITemplateAction,TemplateSendMessage
)
from aiolinebot import AioLineBotApi

from imgdetect import mydetect as dt

# your linebot message API - Channel access token (from LINE Developer)
line_bot_api = AioLineBotApi('9KPRlGqBTTSzEObzFzuPhrWWRTz02I7r7/cL4kiEGLfWLi.........')
# your linebot message API - Channel secret
handler = WebhookHandler('15b33b...........') 

from .utils import *
icnt = imgCounter(ipath)

router = APIRouter()

@router.post("")
async def linebot01(request: Request):
    # get X-Line-Signature header value
    signature = dict(request.headers)['x-line-signature']

    # get request body as text
    body = await request.body()
    body = body.decode("utf-8")
    logger.info("Request body: " + body)

    # handle webhook body
    try:
        print('receive msg')
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        raise HTTPException(status_code=404, detail="Item not found")
    return 'OK'


tmpl_tbl = {"type":"bubble","body":{"type":"box","layout":"vertical","contents": []}}
tmpl_row = {"type":"box","layout":"horizontal","contents":[]}
tmpl_col = {"type":"box","layout":"vertical","contents":[]}
tmpl_itm = {"type":"box","layout":"vertical","contents":[]}
tmpl_txt = {"type":"text","flex":0,"wrap":True,"margin":"2px", "text": ""}

def mk_item(text, flex=None):
    oText = tmpl_txt.copy()
    oText['text'] = text
    oItem = copy.deepcopy(tmpl_itm)
    oItem['contents'] = [oText]
    if flex:
        oItem['flex'] = flex
    return oItem

def mk_items(tmpl, ilist, flex=None):
    oItms = copy.deepcopy(tmpl)
    if flex:
        oItms['contents'] = [ mk_item(i, flex=flex[k]) for k,i in enumerate(ilist) ]
    else:
        oItms['contents'] = [ mk_item(i) for i in ilist ]
    return oItms

def mk_group(tmpl, ilist, flex=None):
    oGrp = copy.deepcopy(tmpl)
    oGrp['contents'] = ilist
    if flex:
        oGrp['flex'] = flex
    return oGrp


# handle linebot message
@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event): # 將照片儲存在本地端
    # line_bot_api.reply_message(event.reply_token, TextSendMessage(text='稍等一下'))
    image_content = line_bot_api.get_message_content(event.message.id)
    image_path = icnt.getName(3, image_content.content_type)

    with open(image_path, 'wb') as fd:
        for chunk in image_content.iter_content():
            fd.write(chunk)
    retList = dt.aiPredict(image_path)

    oTbl = copy.deepcopy(tmpl_tbl)
    for row in retList:
        item1 = mk_item(row[0], flex=1)
        item2 = mk_group(tmpl_col, [
            mk_items(tmpl_row, row[1:4], [4,4,3]), 
            mk_items(tmpl_row, row[4:7], [4,4,3])], flex=4)
        oTbl['body']['contents'].append(mk_group(tmpl_row, [item1, item2]))

    line_bot_api.reply_message( event.reply_token, FlexSendMessage(alt_text='營養成份', contents=oTbl) )
    return

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    #button 1
    text = event.message.text
    if text == "食物小百科":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請上傳清晰食物照片")
            )
    #button 2
    elif text == "食譜推薦":
        reply_cols = [
        CarouselColumn(
            thumbnail_image_url='https://tokyo-kitchen.icook.network/uploads/recipe/cover/231185/6054dd528fc38777.jpg',
            title='專屬於您的推薦食譜',
            text='請點擊連結',
            actions=[
                URITemplateAction(label='日式南瓜燉肉 電鍋健康低脂料理～', uri='https://icook.tw/recipes/231185'),
                URITemplateAction(label='低脂便當菜《香菜雞胸肉餅便當》', uri='https://icook.tw/recipes/252050'),
                URITemplateAction(label='低脂高麗菜豬肉水煎包', uri='https://icook.tw/recipes/226424')
            ]),
        CarouselColumn(
            thumbnail_image_url='https://tokyo-kitchen.icook.network/uploads/recipe/cover/97426/eff6b0db072efdf7.jpg',
            title='專屬於您的推薦食譜',
            text='請點擊連結',
            actions=[
                URITemplateAction(label='高纖早餐☼蘋果地瓜瑪芬', uri='https://icook.tw/recipes/97426'),
                URITemplateAction(label='高纖青醬花枝義大利麵', uri='https://icook.tw/recipes/133527'),
                URITemplateAction(label='高纖奇亞籽牛奶', uri='https://icook.tw/recipes/83221')
            ]),
        CarouselColumn(
            thumbnail_image_url='https://tokyo-kitchen.icook.network/uploads/recipe/cover/215588/afa1dd2d3737ddcd.jpg',
            title='專屬於您的推薦食譜',
            text='請點擊連結',
            actions=[
                URITemplateAction(label='雞胸起司雲蒸蛋', uri='https://icook.tw/recipes/215588'),
                URITemplateAction(label='彩色雜菜煲~瘦身晚餐', uri='https://icook.tw/recipes/124418'),
                URITemplateAction(label='雜菌瘦身鍋', uri='https://icook.tw/recipes/113707')
            ])
        ]

        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text="food_recommend",
                template=CarouselTemplate(columns=reply_cols)
            )
        )
