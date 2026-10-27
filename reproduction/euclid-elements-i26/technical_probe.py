"""Independent finite audit: direct rational oracle, input and certificate attacks.
Run: python3 technical_probe.py > technical-probe.json
This is not a general geometric proof or a proof assistant kernel.
"""
from fractions import Fraction as F
from copy import deepcopy
import hashlib, json, platform
from pathlib import Path
from geometry import make_certificate, verify_certificate

def check(condition, name):
    if not condition: raise RuntimeError(name)

def rejects_input(value, name):
    try:
        make_certificate(value)
    except ValueError:
        return
    raise RuntimeError('invalid input was accepted: '+name)

def enc(points): return [[str(F(x)),str(F(y))] for x,y in points]
def data(p,q,branch): return {'triangle_1':enc(p),'triangle_2':enc(q),'side_case':branch}
def sides(t):
    return [sum((t[i][a]-t[j][a])**2 for a in (0,1)) for i,j in ((0,1),(1,2),(0,2))]
def key(t,i):
    u=[t[(i+1)%3][a]-t[i][a] for a in (0,1)]
    v=[t[(i+2)%3][a]-t[i][a] for a in (0,1)]
    return F(sum(u[a]*v[a] for a in (0,1)),abs(u[0]*v[1]-u[1]*v[0]))
def leaves(x,path=()):
    if type(x) is dict:
        for k,v in x.items():yield from leaves(v,path+(k,))
    elif type(x) is list:
        for k,v in enumerate(x):yield from leaves(v,path+(k,))
    else:yield path,x
def replace(obj,path,value):
    target=obj
    for p in path[:-1]:target=target[p]
    target[path[-1]]=value

positive=0; rejected_scalings=0; sign_classes=set()
for x in range(-3,5):
 for y in range(1,7):
  p=[(F(x,2),F(y,3)),(F(0),F(0)),(F(5),F(0))]
  for rotation in ((F(1),F(0)),(F(3,5),F(4,5)),(F(-5,13),F(12,13))):
   for mirror in (-1,1):
    c,s=rotation
    q=[(c*a-s*mirror*b+F(2,7),s*a+c*mirror*b-F(5,11)) for a,b in p]
    for branch in ('included','opposite'):
     d=data(p,q,branch);cert=make_certificate(d)
     check(verify_certificate(d,cert),'positive certificate')
     check(cert['squared_sides_AB_BC_AC']==[[str(z) for z in sides(t)] for t in (p,q)],'side oracle')
     check(cert['angle_keys']==[[str(key(t,i)) for i in range(3)] for t in (p,q)],'angle oracle')
     sign_classes.update((v>0)-(v<0) for v in [key(p,i) for i in range(3)])
     positive+=1
     scaled=[(2*a,2*b) for a,b in q]
     rejects_input(data(p,scaled,branch),'scale premises')
     rejected_scalings+=1
check(sign_classes=={-1,0,1},'sharp right obtuse coverage')
p=[(F(0),F(3)),(F(0),F(0)),(F(4),F(0))]
q=[(F(10),F(3)),(F(10),F(0)),(F(6),F(0))]
mutations=0
for branch in ('included','opposite'):
 d=data(p,q,branch);cert=make_certificate(d)
 for path,value in leaves(cert):
  for replacement in (True,False,0,1,1.0,None,[],{},'tampered'):
   if type(value) is type(replacement) and value==replacement:continue
   bad=deepcopy(cert);replace(bad,path,replacement)
   check(not verify_certificate(d,bad),'certificate leaf '+repr(path));mutations+=1
 for field in cert:
  bad=deepcopy(cert);del bad[field]
  check(not verify_certificate(d,bad),'missing field');mutations+=1
 bad=deepcopy(cert);bad['extra']=0
 check(not verify_certificate(d,bad),'extra field');mutations+=1
 other=data([(a+1,b+1) for a,b in p],[(a+1,b+1) for a,b in q],branch)
 check(not verify_certificate(d,make_certificate(other)),'other valid input');mutations+=1
 for field in ('triangle_1','triangle_2'):
  for i in range(3):
   for j in range(2):
    for replacement in (True,1,1.0,None,'0/0','2/2','nan','+1','01'):
     bad=deepcopy(d);bad[field][i][j]=replacement
     rejects_input(bad,'input coordinate types');mutations+=1
 for bad_triangle in ([['0','0'],['0','0'],['1','1']],[['0','0'],['1','1'],['2','2']]):
  bad=deepcopy(d);bad['triangle_1']=bad_triangle
  rejects_input(bad,'degeneracy');mutations+=1
 # Different JSON container types must not exploit Python structural equality.
 bad=deepcopy(cert);bad['angle_keys']=tuple(bad['angle_keys'])
 check(not verify_certificate(d,bad),'tuple versus list');mutations+=1

# Verify the article's separate SSA and incorrectly paired-side countermodels.
a=[(F(0),F(0)),(F(5),F(0)),(F(4),F(3))]
b=[(F(0),F(0)),(F(5),F(0)),(F(12,5),F(9,5))]
check(key(a,0)==key(b,0),'SSA angle')
check(sides(a)[:2]==sides(b)[:2]==[25,10],'SSA known edges')
check(sides(a)[2]==25 and sides(b)[2]==9,'SSA unequal edge')
wrong=[(F(3,4)*a,F(3,4)*b) for a,b in p]
check([key(p,i) for i in range(3)]==[key(wrong,i) for i in range(3)],'wrong-side angles')
check(sides(p)[0]==sides(wrong)[1]==9 and sides(p)!=sides(wrong),'wrong-side edges')
rejects_input(data(p,wrong,'included'),'wrong-side premises')
# Tiny exact perturbation is not silently rounded away.
bad=data(p,q,'included');bad['triangle_2'][0][1]='3000000000000000000001/1000000000000000000000'
rejects_input(bad,'tiny perturbation premises')
report={'method':'independent finite rational oracle and adversarial field mutations; not general proof',
 'python':platform.python_version(),'positive_cases':positive,'scaled_cases_rejected':rejected_scalings,'invalid_input_rejection_method':'make_certificate must raise ValueError; independent of certificate comparison',
 'certificate_and_input_attacks_rejected':mutations,'angle_sign_classes':sorted(sign_classes),
 'article_SSA_counterexample':{'known_squared_edges':[25,10],'remaining_squared_edges':[25,9]},
 'article_wrong_side_counterexample':'verified','tiny_exact_perturbation':'rejected','all_checks_passed':True,
 'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'geometry_sha256':hashlib.sha256(Path('geometry.py').read_bytes()).hexdigest()}
print(json.dumps(report,ensure_ascii=False,indent=2))
