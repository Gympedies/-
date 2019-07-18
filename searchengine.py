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
        self.con.execute('create table urllist(url)')
        self.con.execute('create table wordlist(word)')
        self.con.execute('create table wordlocation(urlid,wordid,location)')
        self.con.execute('create table link(fromid,toid)')
        self.con.execute('create table linkwords(wordid,linkid)')
        self.con.execute('create index wordidx on wordlist(word)')
        self.con.execute('create index urlidx on urllist(url)')
        self.con.execute('create index wordurlidx on wordlocation(wordid)')
        self.con.execute('create index urltoidx on link(toid)')
        self.con.execute('create index urlfromidx on link(fromid)')
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
    crawlers.createindextable()
    pages = "" #urlopen貌似不能直接访问https的网站
    crawlers.crawl(pages)
#搜索
class searcher:
    def __init__(self,dbname):
        self.con = sqlite.connect(dbname)
    def __del__(self):
        self.con.close()
    def getmatchrows(self,q):
        fieldlist = 'w0.urlid'
        tablelist = ''
        clauselist = ''
        wordids = []
        words = q.split(' ')
        tablenumber = 0
        for word in words:
            wordrow = self.con.execute("select rowid from wordlist where word = '%s" % word).fetchone()
            if wordrow!=None:
                wordid = wordrow[0]
                wordids.append(wordid)
                if tablenumber>0:
                    tablelist+=','
                    clauselist+=' and '
                    clauselist+='w%d.urlid=w%d.urlid and ' % (tablenumber-1,tablenumber)
                fieldlist+=',w%d.location' % tablenumber
                tablelist+='wordlocation w%d' % tablenumber
                clauselist+='w%d.wordid=%d' %(tablenumber,wordid)
                tablenumber+=1
        #多词查询
        fullquery = 'select %s from %s where %s' % (fieldlist,tablelist,clauselist)
        cur = self.con.execute(fullquery)
        rows = [row for row in cur]
        return rows,wordids
    #基于内容的排名 单词频度 文档位置 单词距离
    def getscoredlist(self,rows,wordids):
        totalscores = dict([(row[0],0) for row in rows])
        #评价函数
        weights = [(1.0,self.normalizescores(rows))]

        for (weight,scores) in weights:
            for url in totalscores:
                totalscores[url]+=weight*scores[url]
        return totalscores
    def geturlname(self,id):
        return self.con.execute(
            "select url from urllist where rowid=%d" % id).fetchone()[0]
    def query(self,q):
        row,wordids = self.getmatchrows(q)
        scores = self.getscoredlist(row,wordids)
        rankedscores = sorted([(score,url) for (score,url) in scores.items()],reverse = 1)
        for (score,urlid) in rankedscores:
            print ('%f\t%s' % (score,self.geturlname(urlid)))
    #归一化函数
    def normalizescores(self,scores,smallIsBetter=0):
        vsmall = 0.00001 #防止被0整除
        if smallIsBetter:
            minscore = min(scores.values())
            return dict([(u,float(minscore)/max(vsmall,1)) for (u,l) in scores.items()])
        else:
            maxscore = max(scores.values())
            if maxscore==0 : maxscore=vsmall
            return dict([(u,float(c)/maxscore)for (u,c) in scores.items()])
    #单词频度
    def frequrcyscore(self,rows):
        counts = dict([(row[0],0) for row in rows])
        for row in rows:counts[row[0]]+=1
        return self.normalizescores(counts)
    #文档位置
    def locationscore(self,rows):
        locations = dict([(row[0],1000000) for row in rows])
        for row in rows:
            loc = sum(row[1:])#单词可能出现在多个位置
            if loc<locations[row[0]]: locations[row[0]] = loc
        return self.normalizescores(locations,smallIsBetter=1)
    #单词距离
    def distancescore(self,rows):
        if len(rows[0])<=2 : return dict([(row[0],1.0)for row in rows])
        mindistance = dict([(row[0],1000000)for row in rows])
        for row in rows:
            dist = sum([abs(row[i]-row[i-1]) for i in range(2,len(row))])
            if dist<mindistance[row[0]]:mindistance[row[0]]=dist
        return self.normalizescores(mindistance,smallIsBetter=1)
    #利用外部指回链接
    def inboundlinkscore(self,rows):
        uniqueurl = set([row[0] for row in rows])
        inboundcount = dict([(u,self.con.execute('select count(*) from link where toid = %d' % u).fetchone([0]))] for u in uniqueurl)
        return self.normalizescores(inboundcount)
    #pageRank算法
    def calculatepagerank(self,iterations=20):
        #清除当前表格
        self.con.execute('drop table if exists pagerank')
        self.con.execute('create table pagerank(urlid primary key,score)')
        #初始化每个url，使其等于1
        self.con.execute('insert into pagerank select rowid,1.0 from urllist')
        self.con.commit()
        for i in range(iterations):
            print("iteration: %d" % (i))
            for(urlid,) in self.con.execute('select rowid from urllist'):
                pr = 0.15
                #遍历指向当前网页的所有其他网页
                for(linker, ) in self.con.execute('select distinct fromid from link where toid=%d' % urlid):
                    #获取rank值
                    linkingpr = self.con.execute('select score from pagerank where urlid=%d' % linker).fetchone()[0]
                    #获取链接总数
                    linkscount = self.con.execute('select count(*) from link where fromid=%d' % linker).fetchone()[0]
                    pr+=0.85*(linkingpr/linkscount)
                self.con.execute('update pagerank set score = %f where urlid=%d' % (pr,urlid))
            self.dbcommit()
    #使用文本链接的评价标准
    def linktextscore(self,rows,wordids):
        linkscores = dict([(row[0],0) for row in rows])    
        for wordid in wordids:
            cur = self.con.execute('select link.fromid,link.toid from linkwords,link where wordid=%d and linkwords.linkid = link.rowid' % wordid)
            for fromid,toid in cur:
                if toid in linkscores:
                    pr=self.con.execute('select score from pagerank where urlid=%d' % fromid).fetchone()[0]
                    linkscores[toid]+=pr
                maxscore=max(linkscores.values())
                normalizescores=dict([(u,float(1)/maxscore) for (u,l) in linkscores.items()])
                return normalizescores    
