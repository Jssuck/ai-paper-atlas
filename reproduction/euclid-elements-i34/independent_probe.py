"""Independent review probe: exact oracle, invalid geometry and certificate attacks."""
import copy, hashlib, io, contextlib, json, sys
from fractions import Fraction as Q
from pathlib import Path
from geometry import make_certificate, verify_certificate

def need(x,msg):
    if not x: raise RuntimeError(msg)
def minus(a,b):return (a[0]-b[0],a[1]-b[1])
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def n2(v):return v[0]*v[0]+v[1]*v[1]
def area(a,b,c):return abs(det(minus(b,a),minus(c,a)))/2
def enc(p):return [str(x) for x in p]
def rejected(d):
    try:make_certificate(d)
    except ValueError:return
    raise RuntimeError('illegal geometry or type accepted')
counts=dict(positive=0,illegal_geometry=0,certificate_attacks=0,illegal_inputs=0)
vec=[(Q(x),Q(y)) for x in range(-2,3) for y in range(-2,3) if (x,y)!=(0,0)]
for u in vec:
 for v in vec:
  if det(u,v)==0:continue
  for a in [(Q(0),Q(0)),(Q(2,7),Q(-5,3))]:
   for s in [Q(1),Q(-2),Q(1,11)]:
    U=tuple(s*x for x in u);V=tuple(s*x for x in v)
    A=a;B=tuple(a[i]+U[i] for i in (0,1));C=tuple(a[i]+V[i] for i in (0,1));D=tuple(a[i]+U[i]+V[i] for i in (0,1))
    data={k:enc(p) for k,p in zip('ABCD',[A,B,C,D])};cert=make_certificate(data)
    need(verify_certificate(data,cert),'positive rejected')
    sides=cert['opposite_sides_squared'];need(Q(sides['AB'])==Q(sides['CD'])==n2(U),'u side');need(Q(sides['AC'])==Q(sides['BD'])==n2(V),'v side')
    al=cert['alternate_angles'];op=cert['opposite_angles']
    need(al['ABC']==al['BCD'] and al['ACB']==al['CBD'],'alternate')
    need(op['BAC']==op['CDB'] and op['ABD']==op['ACD'],'opposite')
    tri=cert['triangles'];need(tri['ABC_squared']==tri['DCB_squared'],'triangle correspondence')
    # Shoelace on the actual A-C-D-B boundary, independent of implementation area field.
    boundary=[A,C,D,B];polygon=abs(sum(det(boundary[i],boundary[(i+1)%4]) for i in range(4)))/2
    need(Q(cert['area']['ABC'])==area(A,B,C)==area(D,C,B)==polygon/2,'area partition')
    need(Q(cert['area']['parallelogram'])==polygon,'polygon')
    need(Q(tri['BC_side_A'])*Q(tri['BC_side_D'])<0,'strict separation')
    counts['positive']+=1
    for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]:
     bad=copy.deepcopy(data);bad['D']=enc((D[0]+dx,D[1]+dy));rejected(bad);counts['illegal_geometry']+=1
# Boundary degeneracies not covered by perturbing D.
for d in [dict(A=[0,0],B=[0,0],C=[1,1],D=[1,1]),dict(A=[0,0],B=[4,0],C=[1,0],D=[5,0]),dict(A=[0,0],B=[1,1],C=[2,2],D=[3,3])]:
 rejected(d);counts['illegal_geometry']+=1
base={'A':[0,0],'B':[4,0],'C':[1,3],'D':[5,3]};cert=make_certificate(base)
def paths(o,p=()):
 yield p,o
 if type(o) is dict:
  for k,v in o.items():yield from paths(v,p+(k,))
 elif type(o) is list:
  for k,v in enumerate(o):yield from paths(v,p+(k,))
def changed(path,new):
 c=copy.deepcopy(cert)
 if not path:return new
 o=c
 for k in path[:-1]:o=o[k]
 o[path[-1]]=new;return c
for path,value in paths(cert):
 for bad in [None,True,False,0,1,0.0,float('nan'),(),{},[], 'tampered']:
  if type(bad)==type(value) and bad==value:continue
  need(not verify_certificate(base,changed(path,bad)),'cert mutation accepted');counts['certificate_attacks']+=1
for key in cert:
 c=copy.deepcopy(cert);del c[key];need(not verify_certificate(base,c),'deleted cert key');counts['certificate_attacks']+=1
c=copy.deepcopy(cert);c['extra']='x';need(not verify_certificate(base,c),'extra cert key');counts['certificate_attacks']+=1
for dx,dy in [(1,0),(0,1),(-2,7)]:
 d={k:[p[0]+dx,p[1]+dy] for k,p in base.items()};need(not verify_certificate(d,cert),'input rebind');counts['certificate_attacks']+=1
bad_scalars=[True,False,None,0.0,float('inf'),float('nan'),Q(1),[],{},(), '00','0/1','01','1/0','2/4',' 1','1 ','+1','1.0','NaN','']
for k in 'ABCD':
 for i in (0,1):
  for value in bad_scalars:
   d=copy.deepcopy(base);d[k][i]=value;rejected(d);counts['illegal_inputs']+=1
for d in [None,[],(),{},dict(base,E=[2,2]),{k:v for k,v in base.items() if k!='D'}]:rejected(d);counts['illegal_inputs']+=1
for k in 'ABCD':
 for value in [None,(),(0,0),[],[0],[0,0,0],{},'00']:
  d=copy.deepcopy(base);d[k]=value;rejected(d);counts['illegal_inputs']+=1
# Article arithmetic and the stronger-vs-weaker claim distinctions.
need(n2((Q(5),Q(3)))==34 and n2((Q(-3),Q(3)))==18,'diagonal counterexample')
need(area((Q(6),Q(3)),(Q(1),Q(3)),(Q(4),Q(0)))==Q(15,2),'one-pair counterexample')
need(area((Q(0),Q(0)),(Q(4),Q(0)),(Q(0),Q(3)))==area((Q(0),Q(0)),(Q(6),Q(0)),(Q(0),Q(2)))==6,'equal-area counterexample')
need(det((Q(3),Q(2)),(Q(-3),Q(3)))==15,'exercise')
nb=json.loads(Path('teaching.zh-CN.ipynb').read_text());ns={};cells=0
for cell in nb['cells']:
 if cell['cell_type']!='code':continue
 cells+=1;out=io.StringIO()
 with contextlib.redirect_stdout(out):exec(compile(''.join(cell['source']),'independent-cell-'+str(cells),'exec'),ns)
 expected=''.join(''.join(x.get('text',[])) for x in cell['outputs'] if x['output_type']=='stream')
 need(out.getvalue()==expected,'notebook output mismatch')
print(json.dumps({'review':'I.34 independent probe','optimization':sys.flags.optimize,'counts':counts,'notebook_cells':cells,'notebook_method':'stdlib compile/exec; not kernel','article_sha256':hashlib.sha256(Path('../../papers/ancient/euclid-elements-i34.zh-CN.md').read_bytes()).hexdigest(),'status':'passed'},sort_keys=True))
