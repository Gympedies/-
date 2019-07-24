class decisionnode:
    def __init__(self,col=-1,value=None,results=None,tb=None,fb=None):
        self.col=col#待判断条件
        self.value=value#使结果为True所匹配的值
        self.results=results
        #子树节点
        self.tb=tb
        self.fb=fb
        