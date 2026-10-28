"""Independent finite checks: fixtures never call geometry.construct."""
import copy,json,io,contextlib
from pathlib import Path
from fractions import Fraction as F
from geometry import verify

BORDERS={'CH':('C','D','H','L'),'HF':('H','M','F','G'),
 'DM':('D','B','M','H'),'LG':('L','H','G','E'),
 'CM':('C','B','M','L'),'DF':('D','B','F','G'),
 'AL':('A','C','L','K'),'AH':('A','D','H','K'),
 'gnomon':('C','B','F','G','H','L'),'square':('C','B','F','E')}

def fixture(origin,axis,hand,m,n):
    # Set two unequal pieces to ratio (m+2n):m. Offset/half = n/(m+n).
    t=F(n,m+n); x,y=axis;u=(F(x),F(y));v=(-hand*F(y),hand*F(x))
    C=tuple(map(F,origin));
    def add(p,q):return tuple(a+b for a,b in zip(p,q))
    def mul(k,p):return tuple(k*a for a in p)
    A=add(C,mul(-1,u));B=add(C,u);E=add(C,v);D=add(C,mul(t,u))
    # Interpolate directly on diagonal E--B at coefficient t.
    H=add(mul(1-t,E),mul(t,B))
    p={'A':A,'B':B,'C':C,'D':D,'E':E,'F':add(B,v),'H':H,
       'G':add(D,v),'L':add(C,mul(1-t,v)),
       'M':add(B,mul(1-t,v)),'K':add(A,mul(1-t,v))}
    S=x*x+y*y; a=F(m,m+n);b=F(n,m+n)
    expected={'CH':a*b*S,'HF':a*b*S,'DM':a*a*S,'LG':b*b*S,
      'CM':a*S,'DF':a*S,'AL':a*S,'AH':a*(a+2*b)*S,
      'gnomon':(a*a+2*a*b)*S,'square':S}
    return {'points':p,'regions':copy.deepcopy(BORDERS)},(C,u,v,t),expected

counts={'external_valid':0,'area_comparisons':0,'tamper_rejections':0,'invalid_rejections':0}
def reject(c,args,category):
    try: verify(c,*args)
    except ValueError:counts[category]+=1
    else:raise RuntimeError('invalid certificate accepted')

for origin in [(0,0),(7,-3),(F(-2,7),F(5,11))]:
 for axis in [(1,0),(3,4),(-4,3),(F(2,3),F(-5,7))]:
  for hand in [-1,1]:
   for m,n in [(1,1),(2,1),(1,3),(5,2),(7,11),(13,1),(1,13),(4,9),(17,19),(3,2)]:
    c,args,expected=fixture(origin,axis,hand,m,n)
    result=verify(c,*args);counts['external_valid']+=1
    for name,value in expected.items():
     if result[name]!=value:raise RuntimeError('area mismatch '+name)
     counts['area_comparisons']+=1
    for name in c['points']:
     for coordinate in [0,1]:
      bad=copy.deepcopy(c);p=list(bad['points'][name]);p[coordinate]+=F(1,17);bad['points'][name]=p
      reject(bad,args,'tamper_rejections')
    for name in c['regions']:
     bad=copy.deepcopy(c);bad['regions'][name]=bad['regions'][name][::-1]
     reject(bad,args,'tamper_rejections')
    bad=copy.deepcopy(c);bad['points']={k:(x+1,y-1) for k,(x,y) in bad['points'].items()}
    reject(bad,args,'tamper_rejections')
    bad=copy.deepcopy(c);bad['points']['H']=bad['points']['L']
    reject(bad,args,'tamper_rejections')
    # Input mismatch, although candidate's lengths and areas are unchanged.
    C,u,v,t=args;reject(c,((C[0]+1,C[1]),u,v,t),'tamper_rejections')

c,args,_=fixture((0,0),(3,4),1,3,2)
for bad in [None,[],0,True,{'points':{}},{'points':{},'regions':{}},{**c,'extra':1}]:reject(bad,args,'invalid_rejections')
for field in ['points','regions']:
 for val in [None,[],0,'bad']:
  bad=copy.deepcopy(c);bad[field]=val;reject(bad,args,'invalid_rejections')
for val in [None,[],[0],[0,0,0],{'x':0,'y':0},[True,0],[0.0,0],['0',0]]:
 bad=copy.deepcopy(c);bad['points']['H']=val;reject(bad,args,'invalid_rejections')
for field in ['points','regions']:
 bad=copy.deepcopy(c);bad[field].pop(next(iter(bad[field])));reject(bad,args,'invalid_rejections')
for val in [0,1,-1,2,F(-1,3),True,False,0.4,'2/5',None]:
 reject(c,(*args[:3],val),'invalid_rejections')
for idx in [0,1,2]:
 for val in [None,[0],[0,0,0],['0',0],[True,0],[0.0,0]]:
  a=list(args);a[idx]=val;reject(c,a,'invalid_rejections')
for u,v in [((0,0),(0,0)),((1,0),(0,2)),((5,0),(3,4)),((1,0),(1,0))]:
 reject(c,(args[0],u,v,args[3]),'invalid_rejections')

nb=json.loads(Path('teaching.zh-CN.ipynb').read_text());scope={};cells=0
for cell in nb['cells']:
 if cell['cell_type']!='code':continue
 cells+=1
 if cell['execution_count'] is not None:raise RuntimeError('non-kernel count present')
 out=io.StringIO()
 with contextlib.redirect_stdout(out):exec(compile(''.join(cell['source']),'<independent-notebook>','exec'),scope)
 expected=''.join(''.join(o.get('text',[])) for o in cell['outputs'])
 if out.getvalue()!=expected:raise RuntimeError('notebook output mismatch')
counts.update(notebook_code_cells=cells,notebook_outputs_match=True,kernel_started=False)
print(json.dumps(counts,indent=2))
