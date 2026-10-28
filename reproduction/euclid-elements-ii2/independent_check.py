"""Independent deterministic cross-check; finite evidence, not general proof."""
from fractions import Fraction as Q
from copy import deepcopy
from geometry import construct,verify,area

def require(condition,message):
    if not condition:raise RuntimeError(message)

n=0;mutations=0
for a,b in [(1,0),(0,2),(3,4),(-5,12),(Q(2,7),Q(-3,5))]:
    for sign in [-1,1]:
        A=(Q(7,3),Q(-11,4));B=(A[0]+a,A[1]+b);D=(A[0]-sign*b,A[1]+sign*a)
        for k in range(1,10):
            t=Q(k,10);c=construct(A,B,D,t)
            require(verify(A,B,D,t,c),'valid candidate rejected')
            expected=a*a+b*b
            require(area(c['square'])==expected,'square area differs from squared side')
            require(area(c['AF'])==t*expected,'left area differs')
            require(area(c['CE'])==(1-t)*expected,'right area differs')
            n+=1
            for name in 'ABCDEF':
                bad=deepcopy(c);x,y=bad['points'][name];bad['points'][name]=(x+Q(1,101),y)
                require(verify(A,B,D,t,bad) is False,'moved point accepted');mutations+=1
            for name in ['square','AF','CE']:
                bad=deepcopy(c);bad[name]=bad[name][::-1]
                require(verify(A,B,D,t,bad) is False,'reversed binding accepted');mutations+=1
base=((0,0),(5,0),(0,5),Q(2,5));c=construct(*base)
for badpoints in [list('ABCDEF'),tuple('ABCDEF'),set('ABCDEF'),'ABCDEF',None,{},1]:
    bad=deepcopy(c);bad['points']=badpoints
    require(verify(*base,bad) is False,'malformed points not rejected');mutations+=1
for args in [((0,0),(5,0),(3,4),Q(2,5)),((0,0),(5,0),(0,4),Q(2,5))]:
    require(verify(*args,c) is False,'nonsquare accepted');mutations+=1
print({'valid_configurations':n,'rejected_mutations':mutations,'exact_arithmetic':True,'scope':'finite modern coordinate cross-check'})
