"""Independent finite coordinate/JSON probes; not a general proof."""
from fractions import Fraction as Q
import copy, json
from geometry import pair, classify, certify, verify, verify_json, load_json

def demand(ok, label):
    if not ok: raise RuntimeError(label)

def point(b,t):
    return (b*(1-t*t)/(1+t*t), b*2*t/(1+t*t))

def tri(a,b,t):
    x,y=point(b,t)
    return {'a2':pair(a*a),'b2':pair(x*x+y*y),'dot':pair(a*x)}

def base(a,b,t):
    x,y=point(b,t)
    return (a-x)**2+y*y

def paths(x,p=()):
    if type(x) is dict:
        for k,v in x.items(): yield from paths(v,p+(k,))
    elif type(x) is list:
        for k,v in enumerate(x): yield from paths(v,p+(k,))
    else: yield p,x

def mutated(x,p,value):
    z=copy.deepcopy(x); o=z
    for k in p[:-1]:o=o[k]
    o[p[-1]]=value
    return z

counts={'greater':0,'equal':0,'less':0}; positives=0
params=[Q(1,100),Q(1,4),Q(1,2),Q(2,3),Q(1),Q(3,2),Q(2),Q(4),Q(100)]
for a in (Q(1,3),Q(1),Q(2),Q(7,2)):
 for b in (Q(1,5),Q(1),Q(3),Q(11,3)):
  for t in params:
   for s in params:
    data={'ABC':tri(a,b,t),'DEF':tri(a,b,s)}
    m=classify(data); rel='greater' if t>s else 'equal' if t==s else 'less'
    demand(m['angle_relation']==rel,'half-angle independent order')
    demand(Q(*m['BC2'])==base(a,b,t),'coordinate BC distance')
    demand(Q(*m['EF2'])==base(a,b,s),'coordinate EF distance')
    demand(Q(*m['base_gap'])==base(a,b,t)-base(a,b,s),'independent gap')
    counts[rel]+=1
    if t>s:
     demand(verify(data,certify(data)),'positive certificate'); positives+=1
    else:
     try: certify(data)
     except ValueError: pass
     else: raise RuntimeError('nonpositive base accepted')

data={'ABC':tri(Q(2),Q(3),Q(1)),'DEF':tri(Q(2),Q(3),Q(1,2))}
c=certify(data); attacks=0
for owner in ('data','certificate'):
 x=data if owner=='data' else c
 for p,v in paths(x):
  if type(v) is int:
   for replacement in (bool(v),float(v)):
    z=mutated(x,p,replacement)
    demand(not verify(z,c) if owner=='data' else not verify(data,z),'numeric type attack '+str(p));attacks+=1
# Every JSON object disallows extra and missing fields, not just top level.
def objects(x,p=()):
 if type(x) is dict:
  yield p
  for k,v in x.items():yield from objects(v,p+(k,))
 elif type(x) is list:
  for k,v in enumerate(x):yield from objects(v,p+(k,))
for owner,x in (('data',data),('certificate',c)):
 for p in objects(x):
  z=copy.deepcopy(x);o=z
  for k in p:o=o[k]
  o['unexpected']=0
  demand(not verify(z,c) if owner=='data' else not verify(data,z),'extra nested key');attacks+=1
for raw in ('{"a":{"x":0,"x":1}}','{"x":NaN}','{"x":Infinity}','{"x":-Infinity}'):
 try:load_json(raw)
 except ValueError:pass
 else:raise RuntimeError('JSON parser accepted attack')
 attacks+=1
# Different adjacent lengths with identical sum/dot have identical old metrics.
x={'ABC':{'a2':[4,1],'b2':[9,1],'dot':[0,1]},'DEF':{'a2':[4,1],'b2':[9,1],'dot':[3,1]}}
y=copy.deepcopy(x)
for k in y:y[k]['a2']=[5,1];y[k]['b2']=[8,1]
demand(not verify(y,certify(x)),'full input binding');attacks+=1
# Correspondence exchange is not silently allowed.
y=copy.deepcopy(x);y['DEF']['a2'],y['DEF']['b2']=y['DEF']['b2'],y['DEF']['a2']
demand(not verify(y,certify(x)),'ordered corresponding sides');attacks+=1
for bad in ([2,2],[0,2],[1,-1],[1,0]):
 y=copy.deepcopy(data);y['ABC']['dot']=bad
 demand(not verify(y,c),'noncanonical rational');attacks+=1
print(json.dumps({'coordinate_pairs':sum(counts.values()),'relations':counts,'positive_certificates':positives,'rejected_attacks':attacks,'method':'independent rational coordinates via positive half-angle parameter, explicit squared distances; finite only'},indent=2))
