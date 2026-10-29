"""Independent finite regression; explicit failures survive -O/-OO.
Oracle uses the expanded product, not production's difference-of-squares path.
This shares the coordinate model; it is not an axiomatic geometry prover.
"""
from fractions import Fraction as F
from decimal import Decimal
from geometry import construct, sqrt_interval, check_interval
import json

def require(ok, name):
    if not ok: raise RuntimeError(name)

def check(a,b):
    r=construct(a,b); area=F(a)*F(b)
    require(r['area']==area and r['side_squared']==area,'product oracle')
    require(r==construct(b,a),'exchange')
    if a==b:
        require(r['branch']=='already_square' and r['side']==a,'square branch')
        require('offset' not in r and 'I47' not in r['checks'],'no degenerate certificate')
    else:
        require(r['branch']=='semicircle','unequal branch')
        require(r['B']==0 and r['E']==max(a,b) and r['F']==a+b,'endpoints')
        require(2*r['G']==r['F'] and r['G']==r['radius'],'midpoint and radius')
        require(2*r['offset']==abs(a-b),'offset')
        require(r['radius_squared']==(F(a)**2+2*area+F(b)**2)/4,'expanded radius')
        require(r['offset_squared']==(F(a)**2-2*area+F(b)**2)/4,'expanded offset')
        require(r['radius_squared']-r['offset_squared']==area,'circle altitude')
        require(0<r['G']<r['E']<r['F'],'original normalized order')
    require(all(r['checks'].values()),'checks')
    return r

def main():
    grid=0
    for a in range(1,41):
        for b in range(1,41): check(F(a,7),F(b,11));grid+=1
    scale=0
    for a,b in ((1,1),(9,4),(2,1),(F(3,2),F(2,3))):
        base=check(a,b)
        for k in (F(1,100),F(3,7),1,17,10**20):
            r=check(a*k,b*k)
            require(r['side_squared']==base['side_squared']*k*k,'scale square');scale+=1
    boundary=0
    for e in (6,30,100):
        tiny=F(1,10**e)
        for a,b in ((1,1+tiny),(1,1-tiny),(tiny,tiny),(tiny,tiny/10),(1/tiny,tiny),(1/tiny,1/tiny)):
            check(a,b); boundary+=1
    hand=0
    for a,b,expected in ((9,4,36),(2,1,2),(F(3,2),F(2,3),1),(7,7,49),(F(1,3),F(1,12),F(1,36)),(10**120,F(1,10**120),1)):
        require(check(a,b)['side_squared']==expected,'hand area');hand+=1
    roots=0
    for area in (F(1,10**201),F(1,13),F(1,36),F(1),F(2),F(36),F(90,7),F(10**200)):
        for n in (0,1,7,80,200):
            lo,hi=sqrt_interval(area,n)
            require(isinstance(lo,F) and isinstance(hi,F),'rational root bounds')
            require(0<=lo<=hi and lo*lo<=area<=hi*hi,'root inclusion')
            require(hi-lo<=max(F(1),area)/2**n,'absolute width')
            require(check_interval(area,lo,hi),'postcondition');roots+=1
    invalid=0
    for x in (True,False,1.0,float('nan'),float('inf'),'2',None,1j,[],{},Decimal('2')):
        for pair in ((x,1),(1,x)):
            try:construct(*pair)
            except TypeError:invalid+=1
            else:raise RuntimeError('invalid type accepted')
    for x in (0,-1,F(-1,10)):
        for pair in ((x,1),(1,x)):
            try:construct(*pair)
            except ValueError:invalid+=1
            else:raise RuntimeError('nonpositive accepted')
    for n in (True,False,1.0,'2',None,-1,10001):
        try:sqrt_interval(2,n)
        except (TypeError,ValueError):invalid+=1
        else:raise RuntimeError('invalid steps accepted')
    require(not check_interval(2,2,3) and not check_interval(2,-1,2) and not check_interval(2,2,1),'false intervals')
    require(F(13,2)**2!=36 and F(5,2)**2!=36 and F(9,2)**2-F(5,2)**2!=36,'wrong construction counterexamples')
    print(json.dumps(dict(status='PASS',rational_pairs=grid,scaled_pairs=scale,boundary_pairs=boundary,hand_certificates=hand,root_intervals=roots,invalid_inputs=invalid,false_intervals=3,wrong_constructions=3),sort_keys=True))
if __name__=='__main__':main()
