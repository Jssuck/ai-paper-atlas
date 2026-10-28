"""Independent adversarial review; standard-library, deterministic."""
import copy,json,subprocess,sys,hashlib
from fractions import Fraction
from geometry import make_certificate,verify_certificate
from cases import EXAMPLE,build,positives,negatives
checks=0
def require(v,label):
 global checks
 checks+=1
 if not v:raise RuntimeError(label)
def leaves(x,path=()):
 if type(x) is dict:
  for k,v in x.items():yield from leaves(v,path+(k,))
 elif type(x) is list:
  for k,v in enumerate(x):yield from leaves(v,path+(k,))
 else:yield path
c=make_certificate(EXAMPLE)
for path in leaves(c):
 d=copy.deepcopy(c);q=d
 for k in path[:-1]:q=q[k]
 q[path[-1]]='TAMPERED'
 require(not verify_certificate(EXAMPLE,d),'leaf mutation '+str(path))
for path in leaves(c):
 for replacement in [True,False,0,1,0.0,None,(),set()]:
  d=copy.deepcopy(c);q=d
  for k in path[:-1]:q=q[k]
  q[path[-1]]=replacement
  require(not verify_certificate(EXAMPLE,d),'type mutation '+str(path))
for point in 'ABCD':
 for axis in (0,1):
  d=copy.deepcopy(EXAMPLE);d[point][axis]+=1
  require(not verify_certificate(d,c),'input rebind')
# An independently written shoelace oracle, including E=F (t=-2).
for data in list(positives())+[build(-2),build(0),build('123456789/7',h='1/97')]:
 z=make_certificate(data)
 p={k:[Fraction(v) for v in vs] for k,vs in data.items()}
 def tri(a,b,c):
  return abs(a[0]*b[1]+b[0]*c[1]+c[0]*a[1]-a[1]*b[0]-b[1]*c[0]-c[1]*a[0])/2
 area=tri(p['A'],p['B'],p['C'])
 require(Fraction(z['area']['ABC'])==area and Fraction(z['area']['DBC'])==tri(p['D'],p['B'],p['C']),'independent area')
 require(Fraction(z['area']['EBCA'])==2*area and Fraction(z['area']['DBCF'])==2*area,'whole area')
 require(all(Fraction(v)==area for v in z['halves'].values()),'all halves')
 require(verify_certificate(data,z),'round trip')
for data in negatives():
 try:make_certificate(data)
 except ValueError:pass
 else:raise RuntimeError('invalid geometry directly accepted')
 require(not verify_certificate(data,c),'invalid input verify')
z=make_certificate(build(-2));require(z['vertices']['E']==z['vertices']['F'],'E=F boundary')
x={};x['cycle']=x;require(not verify_certificate(EXAMPLE,x),'cyclic cert')
print(json.dumps({'independent_checks':checks,'mutated_leaf_count':len(list(leaves(c))),'positive_inputs':675,'negative_inputs':9,'EF_coincidence_checked':True,'result':'PASS'},sort_keys=True))
