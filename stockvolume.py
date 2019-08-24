import nmf
import urllib.request
import numpy as np 
tickers=['YHOO','AVP','BIIB','BP','CL','CVX','DNA','EXPE','GOOG','PG','XOM','AMGN']
shortest=300
prices={}
dates=None
for t in tickers:
    rows = urllib.request.urlopen('http://')
    prices[t]=[float(r.split(',')[5])for r in rows[1:] if r.strip()!='']
    if len(prices[t])<shortest:
        shortest=len(prices[t])
    if not dates:
        dates=[r.split(',')[0] for r in rows[1:] if r.strip()!='']
l1=[[prices[tickers[i]][j] for i in range(len(tickers))]for j in range(shortest)]
w,h = nmf.factorize(np.matrix(l1),pc=5)
for i in range(np.shape(h)[0]):
    print('feature %d' % i)
    o1=[(h[i,j],tickers[j]) for j in range(np.shape(h)[1])]
    o1.sort()
    o1.reverse()
    for j in range(12):
        print(o1[j])
    porder=[(w[d,i],d) for d in range(300)]
    porder.sort()
    porder.reverse()
    print([(p[0],dates[p[1]]) for p in porder[0:3]])

