from flask import Blueprint, request, render_template, make_response
from xml.etree import ElementTree as ET
import time
import requests
from settings import TULING_URL, TULING_STR

wx_bp = Blueprint('wx_bp', __name__)

def tuling(text, userid):
    print(type(text), type(userid))
    TULING_STR['perception']['inputText']['text'] = text
    TULING_STR['userInfo']['userId'] = '111'
    res = requests.post(TULING_URL, json=TULING_STR)
    print(res.json().get("results")[0].get("values").get("text"))
    return res.json().get("results")[0].get("values").get("text")


@wx_bp.route('/', methods=['GET', 'POST'])
def index():
    # 配置微信服务器
    # if request.method == 'GET':
    #     echostr = request.args.get('echostr')
    #     return echostr
    #
    if request.method == 'GET':
        return render_template('index.html')

    else:
        print('这里是POST请求')
        data = request.get_data()
        print(data)
        xml = ET.fromstring(data)  # 实例化一个xml对象
        ToUserName = xml.findtext('.//ToUserName')
        FromUserName = xml.findtext('.//FromUserName')
        CreateTime = xml.findtext('.//CreateTime')
        Content = xml.findtext('.//Content')
        print(Content)

        Content = tuling(Content, ToUserName)

        MsgId = xml.findtext('.//MsgId')
        print(ToUserName, FromUserName, CreateTime, Content, MsgId)

        res = '''<xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[%s]]></Content>
        </xml>'''

        response = make_response(res % (FromUserName, ToUserName, str(int(time.time())), Content))
        response.content_type = 'application/xml'
        return response