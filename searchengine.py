import urllib.request
from BeautifulSoups import *
from urllib.parse import urljoin
import sqlite3.dbapi2 as sqlite
ignore = set(['set','of'])
class crawler:
    #初始化并传入数据库
    def __init__(self,dbname):
        self.con = sqlite.connect(dbname)
    def __del__(self):
        self.con.close()
    def dbcommit(self):
        self.con.commit()
    #获取条目id 若条目不在 传入数据库
    def getentryid(self,table,field,value,createnew=True):
        return None
    #建立网页索引
    def addtoindex(self,url,soup):
        print('Indexing %s' % url)
    #提取文字
    def gettextonly(self,soup):
        return None
    #分词
    def separatewords(self,text):
        return None
    #如果url建立过索引 返回true
    def isindexed(self,url):
        return False
    #添加一个关联网页的链接
    def addlinkref(self,urlFrom,urlTo,linkText):
        pass
    #广度优先索引建立索引
    def crawl(self,pages,depth=2):
        pass
    def createindextable(self):
        pass
    def crawl(self,pages,depth=2):
        for i in range(depth):
            newpages = set()
            for page in pages:
                try:
                    c = urllib.request.urlopen(page)
                except:
                    print('can not open page: %s' % page)
                    continue
                soup = BeautifulSoup(c.read())
                self.addtoindex(page,soup)

                links = soup('a')
                for link in links:
                    if('href' in dict(link.attribute)):
                        url = urljoin(page,link['ref'])
                        if(url.find("'")!=-1): continue
                        url = url.split('#')[0]
                        if(url[0:4]=='http' and not self.isindexed(url)):
                            newpages.add(url)
                        linkText = self.gettextonly(link)
                        self.addlinkref(page,url,linkText)
                    self.dbcommit()
                pages = newpages
    def createindextable(self):
        self.con.execute('')
        self.dbcommit()
    