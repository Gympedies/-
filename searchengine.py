import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sqlite3.dbapi2 as sqlite
import re
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
        #建立数据库语句
        self.dbcommit()
    def gettextonly(self,soup):
        v = soup.string #获取标签内的文字 如果有多个标签有文字 返回None
        if soup==None:
            c = soup.contents #获取子标签的列表
            resulttext = ''
            for t in c:
                subtext = self.gettextonly(t)
                resulttext+=subtext+"\n"
            return resulttext
        else:
            return v.strip()
    def separatewords(self,text):
        splitter = re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if s!='']
    def addtoindex(self,url,soup):
        if self.isindexed(url): return
        print('indexing'+url)
        #获取每个单词
        text = self.gettextonly(soup)
        words = self.separatewords(text)
        #得到URL的id
        urlid = self.getentryid('urllist','url',url)
        #将每个单词关联与url关联
        for i in range(len(words)):
            word = words[i]
            if word in ignore: continue
            wordid = self.getentryid('wordlist','word',word)
            self.con.execute("insert into wordlocation(urlid,wordid,location) values (%d,%d,%d) " % (urlid,wordid,i))
    def getentryid(self,table,field,value,createnew=True):
        cur = self.con.execute("select  rowid from %s where %s = '%s'" % (table,field,value))
        res = cur.fetchone()
        if res==None:
            cur = con.execute("insert into %s (%s) values ('%s)" % (table,field,value))
            return cur.lastrowid
        else:
            return res[0]
    def isindexed(self,url):
        u = self.con.execute \
            ("select rowid from urllist where url='%s'" % url).fetchone()
        if u!=None:
            v = self.con.execute('select * from wordlocation where urlid=%d' % u[0]).fetchone()
            if v!=None:
                return True
        return False
if __name__ == "__main__":
    crawlers = crawler('searchindex.db')
    pages = "" #urlopen貌似不能直接访问https的网站
    crawlers.crawl(pages)
#搜索
class searcher:
    def __init__(self,dbname):
        self.con = sqlite.connect(dbname)
    def __del__(self):
        self.con.close()
    def getmatchrows(self,q):
        