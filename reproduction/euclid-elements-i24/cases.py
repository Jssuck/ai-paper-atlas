from fractions import Fraction as Q
from geometry import pair

def case(a=1,b=1,s=Q(1,3),t=1,reflection=1):
    return dict(a=pair(Q(a)),b=pair(Q(b)),s=pair(Q(s)),t=pair(Q(t)),reflection=reflection)

def positives():
    ts=[Q(1,10),Q(1,3),Q(1),Q(3),Q(10)]
    return [case(a,b,s,t,r) for a in (Q(1,2),1,2,3,5) for b in (Q(1,2),1,3)
            for i,s in enumerate(ts) for t in ts[i+1:] for r in (-1,1)]

def negatives():
    out=[]
    for k,v in [('a',[0,1]),('b',[-1,1]),('s',[0,1]),('s',[2,1]),('t',[1,3]),
                ('a',[True,1]),('a',[1,False]),('a',[1.0,1]),('a',[2,2]),
                ('a',[1,-2]),('a',[1,0]),('a',[1]),('a','1'),('reflection',True),
                ('reflection',0),('reflection',1.0)]:
        d=case();d[k]=v;out.append(d)
    d=case();d['extra']=0;out.append(d)
    d=case();del d['a'];out.append(d)
    out.extend([None,[],True])
    return out
