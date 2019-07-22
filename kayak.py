import time
import urllib.request as ur
import xml.dom.minidom as dm
kayakkey = 'YOURKEYHERE'
#使用密钥开启一个会话
def getkayaksession():
    url = 'https://www.cn.kayak.com/k/ident/apisession?token=%s&version=1' % kayakkey
    doc = dm.parseString(ur.urlopen(url))
    sid = doc.getElementsByTagName('sid')[0].firstChild.data
    return sid
#开始搜索
def flightsearch(sid,origin,destination,depart_data):
    url='https://www.cn.kayak.com/s/apisearch?basicmode=true&oneway=y&origin=%s' % origin
    url+='&destination=%s&depart_data=%s' %(destination,depart_data)
    url+='&return_data=none&depart_time=a&return_time=a'
    url+='&travelers=1&cabin=e&action=doFlights&apimode=1'
    url+='&_sid_=%s&version=1' % sid
    doc = dm.parseString(ur.urlopen(url).read())
    #返回的searchid其实没有结果
    searchid = doc.getElementsByTagName('searchchild')[0].firstChild.data
    return searchid
#不断的请求 直到没有新的结果
def flightsearchresults(sid,searchchild):
    def parseprice(p):
        return float(p[1:].replace(',',''))
    while 1:
        time.sleep(2)
        url = 'http://www.cn.kayak.com/s/basic/flight?'
        url+= 'serachid=%s&c=5&apimode=1&_sid_=%s&version=1' % (searchchild,sid)
        doc = dm.parseString(ur.urlopen(url).read())
        #寻找morepending标签，并等待不为true
        morepending = doc.getElementsByTagName('morepending')[0].firstChild
        if morepending==None or morepending.data == 'false': break
    url = 'http://www.cn.kayak.com/s/basic/flight?'
    url+='serachid=%s&c=999&apimode=1&_sid_=%s&version=1' % (searchchild,sid)
    doc = dm.parseString(ur.urlopen(url).read())
    price = doc.getElementsByTagName('price')
    departure = doc.getElementsByTagName('departure')
    arrivals = doc.getElementsByTagName('arrivals')
    return zip([p.firstChild.data.split(' ')[1] for p in departure],
                [p.firstChild.data.split(' ')[1] for p in arrivals],
                [p.firstChild.data.split(' ')[1] for p in price])
def createschedule(people,dest,dep,ret):
    sid = getkayaksession()
    flights = {}
    for p in people:
        name,origin=p
        searchchild = flightsearch(sid,origin,dest,dep)
        flights[(origin,dest)] = flightsearchresults(sid,searchchild)
        searchchild = flightsearch(sid,dest,origin,ret)
        flights[(dest,origin)] = flightsearchresults(sid,searchchild)
    return flights

