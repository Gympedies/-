from sqlite3 import dbapi2 as sqlite
class classifier:
    def __init__(self,getfeatures,filename=None):
        self.fc={}#分类中不同特征的数量
        self.cc={}#分类被使用的次数
        self.getfeatures = getfeatures
        classifier.__init__(self,getfeatures)
        self.thresholds = {}
    def setthresholds(self,cat,t):
        self.thresholds[cat] = t 
    def getthresholds(self,cat):
        if cat not in self.thresholds: return 1.0
        return self.thresholds[cat]
    #增加特征/分类计数值
    def incf(self,f,cat):
        self.fc.setdefault(f,{})
        self.fc[f].setdefault(cat,0)
        self.fc[f][cat]+=1
    #增加某一分类的特征值次数
    def incc(self,cat):
        self.cc.setdefault(cat,0)
        self.cc[cat]+=1
    #增加某一特征在某一分类中的次数
    def fcount(self,f,cat):
        if f in self.fc and cat in self.fc[f]:
            return float(self.fc[f][cat])
        return 0.0
    #属于某一分类的内容项数量
    def catcount(self,cat):
        if cat in self.cc:
            return float(self.cc[cat])
        return 0
    #所有内容项的数量
    def totalcount(self):
        return sum(self.cc.values())
    #所有分类的列表
    def categories(self):
        return self.cc.keys()
    def train(self,item,cat):
        features=self.getfeatures(item)
        for f in features:
            self.incf(f,cat)
        self.incc(cat)
    def fprob(self,f,cat):
        if self.catcount(cat)==0:return 0
        return self.fcount(f,cat)/self.catcount(cat)
    def weightedprob(self,f,cat,prf,weight=1.0,ap=0.5):
        basicprob=prf(f,cat)
        totals = sum([self.fcount(f,c)] for c in self.categories())
        bp=((weight*ap)+(totals*basicprob))/(weight+totals)
        return bp
    def classify(self,item,default=None):
        max = 0.0
        #寻找最大概率的分类
        for cat in self.categories():
            probs[cat] = self.prob(item,cat)
            if probs[cat]>max:
                max=probs[cat]
                best = cat
        #寻找次最大的分类同时倍数大于阈值
        for cat in probs：
            if cat==best: continue
            if probs[cat]*self.getthresholds(best)>probs[best]: return default
        return best
class naivebayes(classifier):
    def docprob(self,item,cat):
        features=self.getfeatures(item)
        p =1
        for f in features: p*=self.weightedprob(f,cat,self.fprob)
        return p
    #贝叶斯定理 P(A|B) = P(B|A)*P(A)/P(B)
    def prob(self,item,cat):
        catprob = self.catcount(cat)/self.totalcount()
        docprob = self.docprob(item,cat)
        return catprob*docprob
#费舍尔方法
class fisherclassifier(classifier):
    def __init__(self,getfeatures):
        classifier.__init__(self,getfeatures)
        self.minimums= {}
    def cprob(self,f,cat):
        #特征在分类中的频率
        clf = self.fprob(f,cat)
        if clf ==0: return 0
        #特征在所有分类的频率和
        freqsum = sum([self.fprob(f,c)] for c in self.categories())
        #概率等于在该分类中的频率除以总体概率
        p=clf/freqsum
        return p
    def fisherprob(self,item,cat):
        #将所有概率相乘
        p=1
        features=self.getfeatures(item)
        for f in features:
            p*=(self.weightedprob(f,cat,self.cprob))
        #取自然对数 乘-2
        fscore=-2*math.log(p)

        #利用倒置对数卡方函数求得概率
        return self.invchi2(fscore,len(features)*2)
    #对数卡方函数
    def invchi2(self,chi,df):
        m=chi/2.0
        sum=term=math.exp(-m)
        for i in range(1,df/2):
            term*=m/i
            sum+=term
        return min(sum,1.0)   
  