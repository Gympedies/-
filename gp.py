from random import randint, random,choice
from copy import deepcopy
from math import log
class fwrapper:
    def __init__(self,function,childcount,name):
        self.function=function
        self.childcount=childcount
        self.name=name
class node:
    def __init__(self,fw,children):
        self.function=fw.function
        self.children=fw.children
        self.name=fw.name
    def evaluate(self,inp):
        results=[n.evaluate(inp) for n in self.children]
        return self.function(results)
class paramnode:
    def __init__(self,idx):
        self.idx=idx
    def evaluate(self,inp):
        return inp[self.idx]
class constnode:
    def __init__(self,v):
        self.v=v
    def evaluate(self,inp):
        return self.v
