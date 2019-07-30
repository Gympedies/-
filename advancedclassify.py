import math
class matchrow:
    def __init__(self,row,allnum=False):
        if allnum:
            self.data=[float(row[i]) for i in range(len(row)-1)]
        else:
            self.data=row[0:len(row)-1]
        self.match=int(row[len(row)-1])
def loadmatch(f,allnum=False):
    rows=[]
    for line in open(f):
        rows.append(matchrow(line.split(','),allnum))
    return rows
#线性分类器
def lineartrain(rows):
    averages={}
    counts={}
    for row in rows:
        c1=row.match
        averages.setdefault(c1,[0.0]*(len(row.data)))
        counts.setdefault(c1,0)
        for i in len(row.data):
            averages[c1][i]+=float(row.data[i])
        counts[c1]+=1
    for c1,avg in averages.items():
        for i in range(len(avg)):
            avg[i]/=counts[c1]
    return averages
def dotproduct(v1,v2):
    return sum([v1[i]*v2[i]] for i in range(len(v1)))
# class=sign((X-(M0+M1)/2)*(M0-M1))
def dbclassify(point,avgs):
    b=(dotproduct(avgs[1],avgs[1])-dotproduct(avgs[0],avgs[0]))/2
    y=dotproduct(point,avgs[0])-dotproduct(point,avgs[1])+b
    if y>0: return 0
    else:return 1
def yesno(v):
    if v=='yes': return 1
    elif v=='no': return -1
    else: return 0
def matchcount(interest1,interest2):
    l1=interest1.split(',')
    l2=interest2.split(',')
    x=0
    for v in l1:
        if v in l2: x+=1
    return x
def miledistance(a1,a2):
    la1,lo1=getlocation(a1)
    la2,lo2=getlocation(a2)
    latdif=69.1*(la2-la1)
    lodif=53.0*(lo2-lo1)
    return (latdif**2-lodif**2)**0.5
#获取两点之间的距离
yahookey=''
from xml.dom.minidom import parseString
import urllib.request as ur
loccache={}
def getlocation(address):
    if address in loccache: return loccache[address]
    data = ur.urlopen('').read()
    doc=parseString(data)
    lat=doc.getElementsByTagName('Latitude')[0].firstchild.nodevalue
    lo=doc.getElementsByTagName('longtitude')[0].firstchild.nodevalue
    loccache[address]=(float(lat),float(lo))
    return loccache[address]
def loadnumerical():
    oldrows=loadmatch('matchmaker.csv')
    newrows=[]
    for row in oldrows:
        d=row.data
        data=[float(d[0]),yesno(d[1]),yesno(d[2]),float(d[5]),yesno(d[6]),yesno(d[7]),matchcount(d[3],d[8]),miledistance(d[4],d[9]),row.match]
        newrows.append(matchrow(data))
    return newrows
#对数据进行缩放，先减去最小值，再除最大值与最小值的差
def scaledata(rows):
    low=[999999999.0]*len(rows[0].data)
    high=[-999999999.0]*len(rows[0].data)
    for row in rows:
        d=row.data
        for i in range(len(d)):
            if d[i]<low[i]: low[i]=d[i]
            if d[i]>high[i]:high[i]=d[i]
    def scaleinput(d):
        return [(d.data[i]-low[i])/(high[i]-low[i]) for i in range(len(row))]
    newrows=[matchrow(scaleinput(row.data)+[row.match]) for row in rows]
    return newrows,scaleinput
#核方法
#径向基函数
def rbf(v1,v2,gamma=20):
    dv=[v1[i]-v2[i] for i in range(len(v1))]
    l=veclength(dv)
    return math.e**(-gamma*l)
def nlclassify(point,rows,offset,gamma=10):
    sum0=0.0
    sum1=0.0
    count0=0
    count1=0
    for row in rows:
        if row.match==0:
            sum0+=rbf(point,row.data,gamma)
            count0+=1
        else:
            sum1+=rbf(point,row.data,gamma)
            count+=1
    y=(1.0/count0)*sum0-(1.0/count1)*sum1+offset
    if y<0:return 0
    else: return 1
def getoffset(rows,gamma=10):
    l0=[]
    l1=[]
    for row in rows:
        if row.match==0:l0.append(row.data)
        else: l1.append(row.data)
    sum0=sum(sum([rbf(v1,v2,gamma) for v1 in l0]) for v2 in l0)
    sum1=sum(sum([rbf(v1,v2,gamma) for v1 in l1])for v2 in l1)
    return (1.0/len(l1)**2)*sum1-(1.0/(len(l0)**2))*sum0 
