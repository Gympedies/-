import random
from math import sqrt,e
import matplotlib.pyplot as plt
import numpy as np
def wineprice(rating,age):
    peak_age=rating-50
    #根据等级来计算价格
    price=rating/2
    if age>peak_age:
        price=price*(5-(age-peak_age))
    else:
        price=price*(5*(age+1)/peak_age)
    if price<0:price=0
    return price
def wineset1():
    rows=[]
    for i in range(300):
        rating=(random.random())*50+50
        age=random.random()*50
        price=wineprice(rating,age)
        #加入噪声
        price*=(random.random()*0.4+0.8)
        rows.append({'input':(rating,age),'result':price})
    return rows
def euclidean(v1,v2):
    d=0.0
    for i in range(len(v1)):
        d+=(v1[i]-v2[i])**2        
    return sqrt(d)
def getdistances(data,vec1):
    distancelist=[]
    for i in range(len(data)):
        vec2=data[i]['input']
        distancelist.append([euclidean(vec1,vec2),i])
    distancelist.sort()
    return distancelist
def knnestimate(data,vec1,k=5):
    dlist=getdistances(data,vec1)
    avg=0.0
    for i in range(k):
        idx=dlist[i][1]
        avg+=data[idx]['result']
    avg=avg/k
    return avg
#可以对每个近邻加权重，距离越近，权重越高
#倒数 再加上一个常数 防止数字过大
def inverseweight(dist,num=1.0,const=1.0):
    return num/(dist+const)
#减法函数
def substractweight(dist,const=1.0):
    if dist>const: return 0
    else:return const-dist
#克服了前两个的缺点 即下降速度过快
def guassian(dist,sigma=10.0):
    return e**(-dist**2/(2*sigma**2))
def weightedknn(data,vec1,k=5,weightf=guassian):
    dlist=getdistances(data,vec1)
    avg=0.0
    totalweight=0.0
    for i in range(k):
        dist=dlist[i][0]
        idx=dlist[i][1]
        weight=weightf(dist)
        avg+=weight*data[idx]['result']
        totalweight+=weight
    avg=avg/totalweight
    return avg
#交叉验证
def dividedata(data,test=0.05):
    testset=[]
    trainset=[]
    for row in data:
        if random.random()<test:
            testset.append(row)
        else:
            trainset.append(row)
    return trainset,testset
def testalgorithm(algf,trainset,testset):
    error=0.0
    for row in testset:
        guess=algf(trainset,row['input'])
        error+=(row['result']-guess)**2
    return error/len(testset)
def crossvalidate(algf,data,trails=100,test=0.05):
    error=0.0
    for i in range(trails):
        trainset,testset=dividedata(data,test)
        error+=testalgorithm(algf,trainset,testset)
        print(('第%d次的误差') % (i))
        print(error)
    return error/trails
#值域不同的参数可能对函数产生较大影响
def wineset2():
    rows=[]
    for i in range(300):
        rating=(random.random())*50+50
        age=random.random()*50
        aisle=float(random.randint(1,20))
        bottlesize=[375.0,750.0,1500.0,3000.0][random.randint(0,3)]
        price=wineprice(rating,age)
        price*=(bottlesize/750)
        #加入噪声
        price*=(random.random()*0.4+0.8)
        rows.append({'input':(rating,age,aisle,bottlesize),'result':price})
    return rows
#可以对每个不同的参数进行不同程度的缩放
def rescale(data,scale):
    scaledata=[]
    for row in data:
        scaled=[scale[i]*row['input'][i] for i in len(scale)]
        scaledata.append({'input':scaled,'result':row['result']})
    return scaledata
#使用优化算法求出缩放列表的最优解
#有可能数据来自独立的不同群组，可以对其添加概率密度的参数
def wineset3():
    rows=wineset1()
    for row in rows:
        if random.random()<0.5:
            row['result']*=0.5
    return rows
#估计概率密度 在近邻位于目标数值范围的权重值之和/在近邻所有权重之和
def probguess(data,vec1,low,high,k=5,weightf=guassian):
    dlist=getdistances(data,vec1)
    nweight=0.0
    tweight=0.0
    for i in range(k):
        dist=dlist[i][0]
        idx=dlist[i][1]
        weight=weightf(dist)
        v=data[idx]['result']
        if v>=low and v<=high:
            nweight+=weight
        tweight+=weight
    if tweight==0:return 0
    return nweight/tweight
def createcostfunction(algf,data):
    def costf(data,scale):
        sdata=rescale(data,scale)
        return crossvalidate(algf,sdata,trails=10)
    return costf
def cumulativegraph(data,vec1,high,k=5,weightf=guassian):
    t1=np.arange(0.0,high,0.1)
    cprob=np.array([probguess(data,vec1,0,v,k,guassian) for v in t1])
    plt.plot(t1,cprob)
    plt.show()
if __name__ == "__main__":
    data=wineset1()
    cumulativegraph(data,(1,1),120)
