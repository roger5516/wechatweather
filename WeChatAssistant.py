# -*- coding: utf-8 -*-
import json
import getWeatherCityCode
import itchat
from itchat.content import *

import os
thispath = os.getcwd()

resultpath = thispath + r'\citydict'
fileerreo = thispath + r'\fileerror'

print(resultpath)

# 获取城市编码
with open(resultpath, 'r', encoding='utf-8') as f:
    cityjson = json.load(f)
    # cityjson = json.loads(cityjson)

cityname = '大荔'
cityname1 = cityname + '县'
cityname2 = cityname + '市'
cityname3 = cityname + '区'
cityname4 = cityname[:-1]

citylist = []
citylist.append(cityname)
citylist.append(cityname1)
citylist.append(cityname2)
citylist.append(cityname3)
citylist.append(cityname4)

print(citylist)
print([cityjson.get(i) for i in citylist])
citycodelist = [cityjson.get(i) for i in citylist]
print(citycodelist)

for i in citycodelist:
    if i is not None:
        print(i)


itchat.login


Help="友情提示：成功登录"

itchat.send(Help,toUserName='filehelper')

chatroom = itchat.get_chatrooms(update = True)
roomdict = {}
for i in chatroom:
    print(i['UserName'],i['NickName'])
    roomdict[i['NickName']] = i['UserName']


@itchat.msg_register(TEXT,isGroupChat=True)
def getcity(msg):
    if msg.isAt:
        for i in msg:
            pass
            # print(i,':',msg[i])
        if msg['FromUserName'] == roomdict['213搞基群'] or msg['FromUserName'] == roomdict['浐灞二路业主群'] :
            textlist = msg['Text'].split('\u2005')
            if len(textlist) >1:
                print( textlist)
                cityname=textlist[1]

                if len(cityname) < 2 :
                    itchat.send('抱歉，没有您查询的信息', msg['FromUserName'])
                    with open(fileerreo, 'w', encoding='utf-8') as f:
                        f.writelines(cityname)
                    return

                print(cityname)
                cityname1 = cityname + '县'
                cityname2 = cityname + '市'
                cityname3 = cityname + '区'
                cityname4 = cityname[:-1]

                citylist =[]
                citylist.append(cityname)
                citylist.append(cityname1)
                citylist.append(cityname2)
                citylist.append(cityname3)
                citylist.append(cityname4)

                citycodelist = [cityjson.get(i) for i in citylist]

                citycode = None
                for i in citycodelist:
                    if i is not None:
                        citycode = i
                        break

                if citycode is None:
                    itchat.send('抱歉，没有您查询的信息', msg['FromUserName'])
                    with open(fileerreo, 'w', encoding='utf-8') as f:
                        f.writelines(cityname)
                    return
                result=getWeatherCityCode.getweather(citycode)
                itchat.send(result,msg['FromUserName'])

itchat.run(blockThread=False)









#
#
#
#
#
