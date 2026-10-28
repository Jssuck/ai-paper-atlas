"""Independent I.38 implementation audit; exact bounded checks, not a proof."""
from fractions import Fraction as Q
from itertools import product
import copy, hashlib, json, platform, sys
from geometry import make_certificate, verify_certificate

count = 0

def check(condition, label):
    global count
    count += 1
    if not condition:
        raise RuntimeError(label)

def build(o,u,v,t,a,d,s):
    def pt(x,y): return [str(Q(x)),str(Q(y))]
    return {'B':pt(*o),'C':pt(*(o[i]+u[i] for i in range(2))),
            'E':pt(*(o[i]+t*u[i] for i in range(2))),
            'F':pt(*(o[i]+(t+s)*u[i] for i in range(2))),
            'A':pt(*(o[i]+v[i]+a*u[i] for i in range(2))),
            'D':pt(*(o[i]+v[i]+d*u[i] for i in range(2)))}

frames = [((0,0),(3,0),(0,4)),((Q(1,7),Q(-3,5)),(Q(2,3),Q(3,7)),(Q(-1,5),Q(2,11))),
          ((5,-8),(0,-2),(-3,0)),((-4,2),(-3,2),(1,4))]
positive = 0
for (o,u,v),t,a,d,s in product(frames,[-2,Q(-1,2),0,Q(1,2),1,3],[-2,0,Q(3,2)],[-2,0,Q(3,2)],[-1,1]):
    data=build(o,u,v,t,a,d,s)
    cert=make_certificate(data)
    expected=abs(Q(u[0])*v[1]-Q(u[1])*v[0])/2
    check(verify_certificate(data,cert),'valid certificate')
    check({Q(cert['area'][k]) for k in ['ABC','DEF']}=={expected},'independent triangle oracle')
    check({Q(cert['area'][k]) for k in ['GBCA','DEFH']}=={2*expected},'independent whole oracle')
    check(all(Q(x)==expected for x in cert['halves'].values()),'four halves')
    check(all(Q(x)==0 for x in cert['parallel_checks'].values()),'parallel construction')
    changed=copy.deepcopy(data)
    changed['A']=[str(Q(data['A'][i])+u[i]) for i in range(2)]
    check(not verify_certificate(changed,cert),'same-area other apex binding')
    positive+=1

base=build((0,0),(4,0),(0,3),2,0,2,1)
invalid=[]
for key,point in [('C',['0','0']),('F',['8','0']),('D',['8','-3']),('A',['0','0']),('D',['8','4'])]:
    item=copy.deepcopy(base); item[key]=point; invalid.append(item)
item=copy.deepcopy(base);item['E']=['8','1'];item['F']=['12','1'];invalid.append(item)
item=copy.deepcopy(base);item['F']=['13','0'];invalid.append(item)
# Both triangles still area 6, but second base has length 6 and height 2.
item=copy.deepcopy(base);item['E']=['8','0'];item['F']=['14','0'];item['D']=['8','2'];invalid.append(item)
for item in invalid:
    try: make_certificate(item)
    except ValueError: check(True,'invalid rejected')
    else: check(False,'invalid accepted')
    check(not verify_certificate(item,make_certificate(base)),'invalid verify')

malformed=[]
for value in [True,False,0.0,1.5,None,Q(1,2),'2/4','0.5','+1','01','1/1','-0',' 1','1 ','1/0','NaN']:
    item=copy.deepcopy(base);item['A'][0]=value;malformed.append(item)
for item in [{},[],None,dict(base,extra=[0,0])]:malformed.append(item)
for item in malformed:
    try: make_certificate(item)
    except ValueError: check(True,'schema reject')
    else: check(False,'schema accepted')

cert=make_certificate(base)
def paths(value,prefix=()):
    yield prefix
    if type(value) is dict:
        for k,v in value.items(): yield from paths(v,prefix+(k,))
    if type(value) is list:
        for k,v in enumerate(value): yield from paths(v,prefix+(k,))
mutations=0
for path in list(paths(cert)):
    for replacement in [None,True,0,[],{},'tampered']:
        changed=copy.deepcopy(cert)
        if not path: changed=replacement
        else:
            node=changed
            for k in path[:-1]:node=node[k]
            node[path[-1]]=replacement
        check(not verify_certificate(base,changed),'certificate subtree mutation')
        mutations+=1
# Translation and reversed endpoint label bind distinct coordinates, despite same area.
for data in [build((10,20),(4,0),(0,3),2,0,2,1),build((0,0),(4,0),(0,3),3,0,2,-1)]:
    check(not verify_certificate(data,cert),'full input binding')
# All three colliding line names can be legal independently.
for data in [build((0,0),(4,0),(0,3),0,1,1,1),build((0,0),(4,0),(0,3),-1,0,2,-1),build((0,0),(4,0),(0,3),0,0,-2,1)]:
    check(verify_certificate(data,make_certificate(data)),'valid coincidence')
print(json.dumps({'python':platform.python_version(),'optimization':sys.flags.optimize,
 'positive_cases':positive,'invalid_geometry':len(invalid),'malformed_inputs':len(malformed),
 'certificate_subtree_mutations':mutations,'checks':count,'status':'PASS',
 'geometry_sha256':hashlib.sha256(open('geometry.py','rb').read()).hexdigest()},indent=2))
