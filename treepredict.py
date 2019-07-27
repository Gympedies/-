class dicisionnode:
    def __init__(self,col=-1,value=None,results=None,tb=None,fb=None):
        self.col=col#待判断条件
        self.value=value#使结果为True所匹配的值
        self.results=results
        #子树节点
        self.tb=tb
        self.fb=fb
#将数据行分为第一组或第二组
def divideset(rows,column,value):
    split_function = None
    if isinstance(value,int) or isinstance(value,float):
        split_function=lambda row:row[column]>=value
    else:
        split_function=lambda row:row[column]==value
    set1=[row for row in rows if split_function(row)]
    set2=[row for row in rows if not split_function(row)]
    return (set1,set2)
def uniquecounts(rows):
    results={}
    for row in rows:
        r = row[len(rows)-1]
        if r not in results: results[r]=0 
        results[r]+=1
    return results
#基尼不纯度 P(A)*(1-p(A))+P(B)*(1-P(B))+.....
def giniimpurity(rows):
    total = len(rows)
    counts = uniquecounts(rows)
    imp=0
    for k1 in counts:
        p1=float(counts[k1])/total
        for k2 in counts:
            if k1==k2:continue
            p2 = float(counts[k2])/total
            imp+=p1*p2
    return imp
#熵 SUM(P(i)*Log(P(i)))
def entropy(rows):
    from math import log
    log2 = lambda x: log(x)/log(2)
    results=uniquecounts(rows)
    ent=0.0
    for r in results.keys():
        p = float(results(r))/len(rows)
        ent=ent-p*log2(p)#其中负号是用来保证信息量是正数或者零
    return ent
def buildtree(rows,scoref=entropy):
    if len(rows)==0:return dicisionnode()
    currentscore=scoref(rows)
    #定义一些变量记录最佳拆分条件
    best_gain=0.0
    best_criteria=None
    best_sets=None
    colunm_count=len(rows[0])-1
    for col in range(0,colunm_count):
        #在当前列中生成一个由不同值构成的序列
        column_values={}
        for row in rows():
            column_values[row[col]]=1
        for value in column_values.keys():
            set1,set2=divideset(rows,col,value)
            #信息增益
            p=float(len(set1))/len(rows)
            gain=currentscore-p*scoref(set1)-(1-p)*scoref(set2)
            if gain>best_gain and len(set1)>0 and len(set2)>0:
                best_gain=gain
                best_criteria=(col,value)
                best_sets=(set1,set2)
    if best_gain>0:
        trueBrach=buildtree(best_sets[0])
        falseBranch=buildtree(best_sets[1])
        return dicisionnode(best_criteria[0],best_criteria[1],trueBrach,falseBranch)
    else:
        return dicisionnode(uniquecounts(rows))
#剪枝
def prune(tree,mingain):
    if tree.tb.results==None:
        prune(tree.tb,mingain)
    if tree.fb.results==None:
        prune(tree.fb,mingain)
    if tree.tb.results==None and tree.fb.results==None:
        tb,fb = [],[]
        for v,c in tree.tb.results.item():
            tb+=[[v]]*c
        for v,c in tree.fb.results.item():
            fb+=[[v]]*c
        delta=entropy(tb+fb)-(entropy(tb)+entropy(fb)/2)
        if delta>mingain:
            tree.tb,tree.fb==None,None
            tree.results=uniquecounts(tb+fb)
#对新的数据进行分类
def classify(observation,tree)：
    if tree.results!=None:
        return tree.results
    else:
        v=observation.col
        branch=None
        if isinstance(v,in) or isinstance(v,float):
            if v>=tree.value: branch=tree.tb
            else:branch=tree.fb
        else:
            if v==tree.value:
                branch=tree.tb
            else:
                branch=tree.fb
        return classify(observation,branch)
#处理缺失数据
def mdclassify(observation,tree):
    if tree.results!=None:
        return tree.results
    else:
        v = observation[tree.col]
        if v==None:
            tr,fr=mdclassify(observation,tree.tb),mdclassify(observation,tree.fb)
            tcount=sum(tr.values())
            fcount=sum(fr.values())
            tw=float(tcount)/(tcount+fcount)
            fw=float(fcount)/(tcount+fcount)
            result={}
            for k,v in tr.item():result[k]=v*tw
            for k,v in fr.item():
                if k not in result:result[k]=0
                result[k] +=v*fw
            return result
        else:
            if isinstance(v,int) or isinstance(v,float):
                if v>tree.value:
                    branch=tree.tb
                else: branch=tree.fb
            else:
                if v==tree.value:branch=tree.tb
                else:branch=tree.fb
            return mdclassify(observation,branch)
#可以使用方差来代替熵和基尼不纯度来对数值型数据进行分类