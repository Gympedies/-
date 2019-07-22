class classifier:
    def __init__(self,getfeatures,filename=None):
        self.fc={}#分类中不同特征的数量
        self.cc={}#分类被使用的次数
        self.getfeatures = getfeatures
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
      