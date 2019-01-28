###################### 完整代码 2.0 ##############################
# 加载库
from itchat.content import *
import requests
import json
import itchat
#itchat.auto_login(hotReload = True)
itchat.auto_login(hotReload = False)

#过滤掉自动回复的数组
userList = ["xxxx"]  # 字符串数组


autoSendinfoOne = True
autoSendinfoGroup = True


# 调用图灵机器人的api，采用爬虫的原理，根据聊天消息返回回复内容
def tuling(info):
  appkey = "e5ccc9c7c8834ec3b08940e290ff1559"
  url = "http://www.tuling123.com/openapi/api?key=%s&info=%s"%(appkey,info)
  req = requests.get(url)
  content = req.text
  data = json.loads(content)
  answer = data['text']
  #print("info:"+info)
  #print("answer:"+answer)
  return answer
# 对于群聊信息，定义获取想要针对某个群进行机器人回复的群ID函数
def group_id(name):
  df = itchat.search_chatrooms(name=name)
  return df[0]['UserName']
# 注册文本消息，绑定到text_reply处理函数
# text_reply msg_files可以处理好友之间的聊天回复

@itchat.msg_register([TEXT,MAP,CARD,NOTE,SHARING])
def text_reply(msg):
  global autoSendinfoOne
  autoSendinfo = True # 针对部分人开关
  nickName =itchat.search_friends(userName=msg['FromUserName'])['NickName']  # 消息发送人昵称
  #print("nickName="+nickName)
  nickName2 =itchat.search_friends(userName=msg['ToUserName'])['NickName']  # 消息接收人昵称
  #print("nickName2="+nickName2)

  print("reply#"+nickName+":"+msg['Text'])
  content= msg['Text']
  if (nickName=="admin"):# TODO 要调整下 自己的用户名 admin
    if(msg['Text']=="!R"):
      userList.remove(nickName2) #如果没有 会报错 但不影响
    elif(msg['Text']=="!W"):
      userList.append(nickName2) #允许重复记录
    elif (msg['Text'] == "!G"):
      autoSendinfoOne=False
    elif (msg['Text'] == "!K"):
      autoSendinfoOne=True
    elif (msg['Text'] == "!GA"):
      autoSendinfoOne = False
      autoSendinfoGroup = False
    elif (msg['Text'] == "!KA"):
      autoSendinfoOne = True
      autoSendinfoGroup=True
  else:
    if (msg['Text']=="false"):
      userList.append(nickName)
    elif (msg['Text']=="true"):
      userList.remove(nickName)  # 如果没有 会报错 但不影响

  #print("text_reply  autoSendinfoALL:")
  #print(autoSendinfoOne)
  if autoSendinfoOne:
    for item in userList:
        if(item==nickName):
          autoSendinfo=False
          break
    if autoSendinfo:
      #print("AUTO")
      itchat.send('%s' % '助手:'+tuling(msg['Text']),msg['FromUserName'])

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
  msg['Text'](msg['FileName'])
  return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])
# 现在微信加了好多群，并不想对所有的群都进行设置微信机器人，只针对想要设置的群进行微信机器人，可进行如下设置

@itchat.msg_register(TEXT, isGroupChat=True)
def group_text_reply(msg):
  global autoSendinfoGroup
  ActualNickName=msg['ActualNickName'] #发消息的人
  #msg1= msg['User']
  #msg2=msg1['NickName']
  groupName=msg['User']['NickName'] #这样也可以获取群名称
  print("group#"+groupName+"#"+ActualNickName+":"+msg['Text'])
  if (ActualNickName=="" or ActualNickName=="admin"):#TODO admin
    content1 = msg['Text'][-2:]#截取最后两位
    key = msg['Text'][0:-2].rstrip()
    print("content1=" + content1)
    if(content1=="!R"): #  remove name
      userList.remove(key) #如果没有 会报错 但不影响
    elif(content1=="!W"): # 写入 过滤
      userList.append(key)  # 允许重复记录
    elif(content1 == "!G"): #关闭
      autoSendinfoGroup=False
    elif (content1 == "!K"): #开启
      autoSendinfoGroup = True
  else:#成员
    if (msg['Text']=="false"):  # 写入
      userList.append(ActualNickName)
    elif (msg['Text']=="true"): # remove name
      userList.remove(ActualNickName)  # 如果没有 会报错 但不影响

  #print("group_text_reply  autoSendinfoALL:")
  #print(autoSendinfoGroup)
  if autoSendinfoGroup:
    autoSendinfo = True
    #ActualNickName="@"+ActualNickName
    gname='群名称'#TODO 根据自己微信群调整
    from_group=''
    myroom = itchat.search_chatrooms(name=gname)
    for room in myroom:
      if room['NickName'] == gname:
        from_group = room['UserName']

    if (msg['FromUserName']==from_group):# 针对指定的群 开启自动回复
      if autoSendinfoGroup:
        itchat.send(u'%s' % tuling(msg['Text'])+"。" ,msg['FromUserName'])
    else:# 针对其他群
      if msg['isAt']: #@
        for item in userList:
          if (item == ActualNickName):
            autoSendinfo = False
            break
        if autoSendinfo:
          #print("AUTO")
          itchat.send(u'@%s\u2005 %s' % (msg['ActualNickName'], tuling(msg['Text']) + "。"), msg['FromUserName'])
itchat.run()

