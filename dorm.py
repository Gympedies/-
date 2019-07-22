import random
import math
dorms=['zers','athna','hercules','bacchus','pluto']
prefs = [['toby',('bacchus','hercules')],
        ['steve',('zeus','pluto')],
        ['andrea',('athena','pluto')],
        ['sarah',('zeus','pluto')],
        ['dave',('athena','bacchus')],
        ['jeff',('hercules','pluto')],
        ['fred',('pluto','athena')],
        ['suzie',('bacchus','hercules')],
        ['laura',('bacchus','hercules')],
        ['neil',('hercules','athena')]]
domain = [(0,(len(dorms)*2)-i-1) for i in range(0,len(dorms)*2)]
def printsolution(vec):
    slots=[]
    for i in range(len(dorms)): slots+=[i,i]
    for i in range(len(vec)):
        x = int(vec[i])
        dorm  = dorms[slots[x]]
        print prefs[i][0],dorm
        del slots[x]