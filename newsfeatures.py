import feedparser
import re
feedlist=['http://today.reuters.com/rss/topNews']
def scripHTML(h):
    p=''
    s=0
    for c in h:
        if c=='<':s=1
        elif c=='>':
            s=0
            p+=' '
        elif s==0: p+=c
    return p
def separatewords(text):
    splitter=re.compile('\\W*')
    return [s.lower() for s in splitter.split(text) if len(s)>3]
def getarticlewords():
    allwords={}
    articlewords=[]
    articletitles=[]
    ec=0
    for feed in feedlist:
        f = feedparser.parse(feed)
        for e in f.entries:
            if e.title in articletitles:continue
            txt=e.title.encode('utf-8')+scripHTML(e.description.encode('utf-8'))
            words=separatewords(txt)
            articletitles.append(e.title)
            articlewords.append({})
            for word in words:
                allwords.setdefault(word,0)
                allwords[word]+=1
                articlewords[ec].setdefault(word,0)
                articlewords[ec][word]+=1
            ec+=1
    return allwords,articlewords,articletitles
def makematrix(allw,articlew):
    wordvec=[]
    for w,c in allw.items():
        if c>3 and c<len(articlew)*0.6:
            wordvec.append(w)
    l1=[[(word in f and f[word] or 0)for word in wordvec]for f in articlew]
    return l1,wordvec
if __name__ == "__main__":
    allw,artw,artt=getarticlewords()
    wordmatrix,wordvec=makematrix(allw,artw)
    print(wordvec[0:10])