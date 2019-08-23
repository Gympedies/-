import numpy as np
import random 
def difcost(a,b):
    dif=0
    for i in range(np.shape(a)[0]):
        for j in range(np.shape(a)[1]):
            dif+=pow(a[i,j]-b[i,j],2)
    return dif
def factorize(v,pc=10,iter=50):
    ic=np.shape(v)[0]
    fc=np.shape(v)[1]
    w=np.matrix([[random.random() for j in range(pc)]for i in range(ic)])
    h=np.matrix([[random.random() for j in range(fc)]for i in range(pc)])
    for i in range(iter):
        wh=w*h
        cost=difcost(wh,v)
        if i%10==0: print(cost)
        if cost==0: break
        hn=(w.T*v)
        hd=w.T*w*h
        h=np.matrix(np.array(h)*np.array(hn)/np.array(hd))
        wn=(v*h.T)
        wd=(w*h*h.T)
        w=np.matrix(np.array(w)*np.array(wn)/np.array(wd))
    return w,h
def showfeatures(w,h,titles,wordvec,out='feature.txt'):
    outfile=open(out,'w')
    pc,wc=np.shape(h)
    toppartterns=[[]for i in range(len(titles))]
    partternnames=[]
    for i in range(pc):
        slist=[]
        for j in range(wc):
            slist.append((h[i,j],wordvec[j]))
        slist.sort()
        slist.reverse()
        n=[s[1] for s in slist[0:6]]
        outfile.write(str(n)+'\n')
        partternnames.append(n)
        flist=[]
        for j in range(len(titles)):
            flist.append((w[i][j],titles[j]))
            toppartterns[j].append(w[j,i],i,titles[j])
        flist.sort()
        flist.reverse()
        for f in flist[0:3]:
            outfile.write(str(f)+'\n')
        outfile.write('\n')
    outfile.close()
    return toppartterns, partternnames



