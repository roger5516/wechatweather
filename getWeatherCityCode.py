# -*- coding: utf-8 -*-
import urllib.request
import urllib
import json
import time
from  xml.dom import minidom


# 获取天气
def getweather(citycode):
    timestamp = int(time.time()*1000)
    url ='http://d1.weather.com.cn/sk_2d/'+ citycode +'.html?_='+str(timestamp)
    # print(url)
    headers = {
    'Accept': '*/*',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Connection':'keep-alive',
    'DNT':'1',
    'Host':'d1.weather.com.cn',
    'Referer':'http://m.weather.com.cn/mweather/101020100.shtml',
    'User-Agent':'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Mobile Safari/537.36'
    }
    req = urllib.request.Request(url=url, headers=headers)
    data = urllib.request.urlopen(req).read().decode("utf-8")
    data = json.loads(data[13:])
    result=  '''%s 实时天气: %s %s %s%s,空气质量 %s ,相对湿度 %s \n（来自中国天气网，更新时间 %s %s分 \n 点击查看详情: http://m.weather.com.cn/mweather/%s.shtml ）''' % (   data['cityname'], data['weather'], data['temp'], data['WD'], data['WS'], data['aqi'], data['sd'], data['date'], data['time'], data['city'])

    # print(data)
    # for i in data:
    #     print(i,':',data[i])
    return result

def get_attrvalue(node, attrname):
    return node.getAttribute(attrname) if node else ''

def get_xmlnode(node, name):
    return node.getElementsByTagName(name) if node else []
    # 获取城市编码

def getdata(cityname):
    url ='http://flash.weather.com.cn/wmaps/xml/'+ cityname +'.xml'
    headers = {
    'Accept': '*/*',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Connection':'keep-alive',
    'DNT':'1',
     'Host':'flash.weather.com.cn',
    'Referer':'http://m.weather.com.cn/mweather/101020100.shtml',
    'User-Agent':'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Mobile Safari/537.36'
    }
    try :
        req = urllib.request.Request(url=url, headers=headers)
        data = urllib.request.urlopen(req).read().decode("utf-8")
    except :
        return None
    # print(data)
    doc = minidom.parseString(data)
    cityname = doc.documentElement
    city_nodes = get_xmlnode(cityname, 'city')
    return city_nodes

def getnode(city_nodes,pynamelist,citydict):
    for node in city_nodes:
        pyName = get_attrvalue(node, 'pyName')
        cityname = get_attrvalue(node, 'cityname')
        url = get_attrvalue(node, 'url')
        quName = get_attrvalue(node, 'quName')
        # print(pyName,quName, cityname, url)
        if pyName == '':
            # print('1111',pyName,quName, cityname, url)
            if citydict.get(cityname) == None or citydict.get(cityname) =="":
                citydict[cityname] = url
        else:
            if pyName not in pynamelist:
                pynamelist.append(pyName)
                # print('2222',pyName,quName, cityname, url)
                if citydict.get(cityname) == None or citydict.get(cityname) == "":
                    citydict[cityname] = url

                mai(pyName, pynamelist,citydict)

def mai(pyName,pynamelist,citydict):
    data = getdata(pyName)
    # print(data)
    if data is None:
        pass
    else:
        getnode(data, pynamelist,citydict)

def getCityCode(resultpath):
    pyName='china'
    pynamelist = []
    citydict = {}
    # resultpath = r'E:\ipython-notebook\myPyProject\tmp\citydict'
    mai(pyName,pynamelist,citydict)

    citydict['杭州'] = '101210101'
    citydict['北京'] = '101010100'
    citydict['天津'] = '101030100'
    citydict['上海'] = '101020100'
    citydict['香港'] = '101320101'
    citydict['澳门'] = '101330101'
    citydict["西沙"] = '101310302'
    citydict["南沙"] = '101310304'
    citydict["钓鱼岛"] = '101231001'
    citydict["三沙市"] = '101310301'
    citydict["三沙"] = '101310301'

    del citydict["市中心"]
    s = json.dumps(citydict,ensure_ascii=False)
    with open(resultpath, 'w',encoding='utf-8') as f:
        f.write(json.dumps(citydict, ensure_ascii=False))
        print('写文件完成')


    # with open(resultpath, 'r',encoding='utf-8') as f:
    #     cityjson = json.load(f)
    #     cityjson = json.loads(cityjson)
    # print(cityjson)
    # cityjson['杭州'] = '101210101'
    # cityjson['北京'] = '101010100'
    # cityjson['天津'] = '101030100'
    # cityjson['上海'] = '101020100'
    # cityjson['香港'] = '101320101'
    # cityjson['澳门'] = '101330101'
    # cityjson["西沙"] = '101310302'
    # cityjson["南沙"] = '101310304'
    # cityjson["钓鱼岛"] = '101231001'

    # print(len(cityjson))
    #
    # for i in cityjson:
    #     print(i, cityjson[i])


if __name__ == '__main__':
    resultpath = r'E:\ipython-notebook\myPyProject\tmp\citydict'
    getCityCode(resultpath)

    # with open(resultpath, 'r',encoding='utf-8') as f:
    #     cityjson = json.load(f)
    #     cityjson = json.loads(cityjson)
    # citycode = cityjson.get( '南京' )
    # if citycode != None:
    #     weatherdata = getweather(citycode)
    #     print('''%s 实时天气 %s %s %s%s,空气质量 %s ,相对湿度 %s \n（来自中国天气网，更新时间 %s %s分）\n 点击查看详情: http://m.weather.com.cn/mweather/%s.shtml ''' %(  weatherdata['cityname'], weatherdata['weather'] , weatherdata['temp'] , weatherdata['WD'],weatherdata['WS'] , weatherdata['aqi'] , weatherdata['sd'] ,weatherdata['date'], weatherdata['time']  , weatherdata['city']     ) )
    #
    # else:
    #     pass



