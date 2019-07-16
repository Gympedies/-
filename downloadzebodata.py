from BeautifulSoup import BeautifulSoup
import urllib.request
import re
targeturl = ''
chare = re.compile(r'[!-\.&]')
itemowners = {}
dropwords=['a','new','some','more','the']
currentuser = 0
for i in range(1,51):
    c = urllib.request.urlopen(targeturl+'%d' % i)
    soup = BeautifulSoup(c.read())
    for td in soup('td'):
        if('class' in dict(td.arrtrs) and dt['class']=='bgverdanasmall'):
            items=[re.sub(chare,'', a.contents[0].lower()).strip() for a in td('a')]

