###################### 完整代码##############################
# 加载库
from itchat.content import *
import requests
import json
import itchat
#itchat.auto_login(hotReload = True)
itchat.auto_login(hotReload = False)

#过滤掉自动回复的数组
userList = ["super_y","沙的影子", "周宁", "猪林一克","mina","魏耀武","Leo♎"]  # 字符串数组
autoSendinfoALL = True

# 调用图灵机器人的api，采用爬虫的原理，根据聊天消息返回回复内容
def tuling(info):
  appkey = "e5ccc9c7c8834ec3b08940e290ff1559"
  url = "http://www.tuling123.com/openapi/api?key=%s&info=%s"%(appkey,info)
  req = requests.get(url)
  content = req.text
  data = json.loads(content)
  answer = data['text']
  print("info:"+info)
  print("answer:"+answer)
  return answer
# 对于群聊信息，定义获取想要针对某个群进行机器人回复的群ID函数
def group_id(name):
  df = itchat.search_chatrooms(name=name)
  return df[0]['UserName']
# 注册文本消息，绑定到text_reply处理函数
# text_reply msg_files可以处理好友之间的聊天回复
@itchat.msg_register([TEXT,MAP,CARD,NOTE,SHARING])
def text_reply(msg):
  autoSendinfo = True
  nickName =itchat.search_friends(userName=msg['FromUserName'])['NickName']  # 消息发送人昵称
  print("nickName="+nickName)

  nickName2 =itchat.search_friends(userName=msg['ToUserName'])['NickName']  # 消息接收人昵称
  print("nickName2="+nickName2)

  content= msg['Text']
  if (nickName=="super_y"):
    if(msg['Text']=="!Q"):
      userList.remove(nickName2) #如果没有 会报错 但不影响
    elif(msg['Text']=="!W"):
      userList.append(nickName2) #允许重复记录

  for item in userList:
     if(item==nickName):
       autoSendinfo=False
       break
  if autoSendinfo:
    itchat.send('%s' % '助手:'+tuling(msg['Text']),msg['FromUserName'])

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
  msg['Text'](msg['FileName'])
  return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])
# 现在微信加了好多群，并不想对所有的群都进行设置微信机器人，只针对想要设置的群进行微信机器人，可进行如下设置
@itchat.msg_register(TEXT, isGroupChat=True)
def group_text_reply(msg):
  # 当然如果只想针对@你的人才回复，可以设置if msg['isAt']:
  #item = group_id(u'装逼群') # 根据自己的需求设置
  #if msg['ToUserName'] == item:
  #nickName = itchat.search_friends(userName=msg['FromUserName'])['NickName']  # 消息发送人昵称
  #nickName = itchat.search_friends(userName=msg['FromUserName'])  # 消息发送人昵称
  ActualNickName=msg['ActualNickName']
  print("ActualNickName=" + ActualNickName)
  if (ActualNickName=="" or ActualNickName=="super_y" or ActualNickName=="杨超"):
    content1 = msg['Text'][-2:]#截取最后两位
    key = msg['Text'][0:-2].rstrip()
    print("content1=" + content1)
    if(content1=="!Q"):
      userList.remove(key) #如果没有 会报错 但不影响
    elif(content1=="!W"):
      userList.append(key)  # 允许重复记录
      print("key="+key)

  autoSendinfo = True
  ActualNickName="@"+ActualNickName

  gname='装逼群'
  #gname = '王者农药'
  from_group=''
  myroom = itchat.search_chatrooms(name=gname)
  for room in myroom:
    if room['NickName'] == gname:
      from_group = room['UserName']

  global autoSendinfoALL
  print(msg['FromUserName'] +"@@@@@@@@@" +from_group)
  if (msg['FromUserName']==from_group):
    print("msg['FromUserName'] = " + msg['FromUserName'])
    if (msg['Text']=="false"):
      autoSendinfoALL=False
    elif (msg['Text']=="true"):
      autoSendinfoALL=True
    if autoSendinfoALL:
      itchat.send(u'%s' % tuling(msg['Text'])+"。" ,msg['FromUserName'])

  else:
    if msg['isAt']:
      for item in userList:
        print("item=" + item + "@@@@@@@@@ActualNickName=" + ActualNickName)
        if (item == ActualNickName):
          autoSendinfo = False
          print("False")
          break
      if autoSendinfo:
        # itchat.send(u'%s' % tuling(msg['Text']),msg['FromUserName'])
        itchat.send(u'@%s\u2005 %s' % (msg['ActualNickName'], tuling(msg['Text']) + "。"), msg['FromUserName'])
itchat.run()

