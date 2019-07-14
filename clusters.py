def readfile(filename):
    lines = [line for line in open(filename)]
    colnames = lines[0].strip('\n').split('\t')[1:]
    rowsname = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')
        rowsname.append(p[0])
        data.append([float(x) for x in p[1:]])
    return rowsname,colnames,data
from math import sqrt
#相关系数
def pearson(v1,v2):
    sum1 = sum(v1)
    sum2 = sum(v2)
    sunm1Sq = sqrt([pow(v,2) for v in v1])
    sunm2Sq = sqrt([pow(v,2) for v in v2])
    psum = sum([v1[i]*v2[i] for i in range(len(v1))])
    num = psum - (sum1*sum2/len(v1))
    den = sqrt((sunm1Sq-pow(sum1,2)/len(v1))*(sunm2Sq-pow(sum2,2)/len(v1)))
    if den == 0 : return 0
    #可以使相关度越大 距离越小
    return 1.0-num/den
class bicluster:
    def __init__(self, vec, left=None,right=None,distance=0.0,id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance
def hcluster(rows, distance=pearson):
    distance=[]
    currentclusterid = -1
    clust = [bicluster(rows[i],id=i) for i in range(len(rows))]
    while len(clust)>1:
        lowestpair = (0,1)
        closest = distance(clust[0].vec,clust[1].vec)
    
        
