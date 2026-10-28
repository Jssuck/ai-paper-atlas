"""Independent review probes; explicit checks remain active under -O and -OO."""
import copy, itertools, json, sys
from fractions import Fraction as Q
from geometry import make_certificate, verify_certificate
counts = {'general_parameter_cases':0,'invalid_geometry_direct_rejections':0,'input_type_rejections':0,'certificate_tamper_rejections':0,'binding_rejections':0,'hand_checks':0}
def check(ok, msg):
    if not ok: raise RuntimeError(msg)
def enc(p): return {k:[str(x) for x in v] for k,v in p.items()}
def model(u,v,a,f,e,b=(Q(2,7),Q(-3,5))):
    def pt(t,h):return tuple(b[i]+t*u[i]+h*v[i] for i in range(2))
    return enc(dict(B=pt(0,0),C=pt(1,0),A=pt(a,1),D=pt(a+1,1),F=pt(f,0),G=pt(f+1,0),E=pt(e,1),H=pt(e+1,1)))
shifts=list(map(Q,['-3','-1','0','1/3','1','2']))
for u,v in itertools.product([(Q(2),Q(1)),(Q(0),Q(-3)),(Q(-2),Q(4))],[(Q(1),Q(3)),(Q(-3),Q(-1)),(Q(4),Q(-2))]):
    det=u[0]*v[1]-u[1]*v[0]
    if not det:continue
    for a,f,e in itertools.product(shifts,repeat=3):
        data=model(u,v,a,f,e);c=make_certificate(data)
        check(verify_certificate(data,c),'valid rejected')
        check(all(Q(z)==abs(det) for z in c['area'].values()),'independent determinant mismatch')
        check(Q(c['bridge']['upper_shift'])==e-a and Q(c['bridge']['lower_shift'])==f,'parameter map')
        check(c['bridge']['first_I35_shared_base']=='BC' and c['bridge']['second_I35_shared_base']=='EH','proof interface')
        counts['general_parameter_cases']+=1
base=model((Q(2),Q(0)),(Q(0),Q(3)),Q(0),Q(3),Q(2),(Q(0),Q(0)))
cert=make_certificate(base)
check(cert['area']==dict(ABCD='6',EFGH='6',EBCH='6'),'hand area')
check(cert['bridge']['BE_equals_CH_vector']==['4','3'],'hand bridge')
counts['hand_checks']+=2
bad=[]
for k in base:
    for axis in range(2):
        d=copy.deepcopy(base);d[k][axis]=str(Q(d[k][axis])+Q(1,7));bad.append(d)
# Equal lengths with reversed endpoint pairing, and degenerate height/base.
for keys in [('E','H'),('F','G')]:
    d=copy.deepcopy(base);d[keys[0]],d[keys[1]]=d[keys[1]],d[keys[0]];bad.append(d)
for u,v in [((Q(0),Q(0)),(Q(0),Q(3))),((Q(2),Q(0)),(Q(4),Q(0)))]:
    bad.append(model(u,v,Q(0),Q(3),Q(2)))
for d in bad:
    try:make_certificate(d)
    except ValueError:pass
    else:raise RuntimeError('illegal geometry accepted')
    check(not verify_certificate(d,cert),'nonempty valid certificate concealed invalid geometry')
    counts['invalid_geometry_direct_rejections']+=1
class IntSubclass(int):pass
class ListSubclass(list):pass
class DictSubclass(dict):pass
for value in [True,False,0.0,Q(0),IntSubclass(0),None,'00','-0','0/1',' 0','nan','1/0']:
    d=copy.deepcopy(base);d['A'][0]=value
    try:make_certificate(d)
    except ValueError:pass
    else:raise RuntimeError('bad scalar accepted')
    counts['input_type_rejections']+=1
for d in [DictSubclass(base),dict(base,A=ListSubclass(base['A'])),dict(base,A=tuple(base['A']))]:
    try:make_certificate(d)
    except ValueError:pass
    else:raise RuntimeError('bad container accepted')
    counts['input_type_rejections']+=1
def leaves(x,path=()):
    if type(x) is dict:
        for k,v in x.items():yield from leaves(v,path+(k,))
    elif type(x) is list:
        for k,v in enumerate(x):yield from leaves(v,path+(k,))
    else:yield path
for path in leaves(cert):
    for replacement in ['tampered',True,1,1.0,None]:
        c=copy.deepcopy(cert);p=c
        for key in path[:-1]:p=p[key]
        p[path[-1]]=replacement
        check(not verify_certificate(base,c),'tampered leaf accepted')
        counts['certificate_tamper_rejections']+=1
for a,f,e in [(Q(1),Q(3),Q(2)),(Q(0),Q(4),Q(2)),(Q(0),Q(3),Q(1))]:
    d=model((Q(2),Q(0)),(Q(0),Q(3)),a,f,e,(Q(0),Q(0)))
    check(not verify_certificate(d,cert),'same-area changed input accepted');counts['binding_rejections']+=1
# Counterexamples checked independently, not accepted as theorem instances.
check(2*3!=2*4 and 2*3!=3*3,'height/base counterexample')
check(2*(1+5)==2*(2+4) and 1*5!=2*4,'perimeter counterexample')
check(2*6==3*4,'converse counterexample')
crossed=[(Q(0),Q(0)),(Q(2),Q(0)),(Q(0),Q(3)),(Q(2),Q(3))]
shoelace=sum(crossed[i][0]*crossed[(i+1)%4][1]-crossed[i][1]*crossed[(i+1)%4][0] for i in range(4))
bh_mid=tuple((crossed[0][i]+crossed[3][i])/2 for i in range(2))
ce_mid=tuple((crossed[1][i]+crossed[2][i])/2 for i in range(2))
check(shoelace==0 and bh_mid==ce_mid==(Q(1),Q(3,2)),'crossed quadrilateral counterexample')
counts['hand_checks']+=4
print(json.dumps({'optimization':sys.flags.optimize,'counts':counts,'passed':True},sort_keys=True))
