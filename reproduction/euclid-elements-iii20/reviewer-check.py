"""Independent finite audit: circle order and rational complex arithmetic.
Run: python reviewer-check.py (also -O and -OO). No production helper is
used to obtain expected values. This is not a general theorem prover.
"""
from fractions import Fraction as Q
from itertools import permutations
from functools import cmp_to_key
from geometry import evaluate

def mul(z,w):return (z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
def div(z,w):
    den=w[0]**2+w[1]**2
    return ((z[0]*w[0]+z[1]*w[1])/den,(z[1]*w[0]-z[0]*w[1])/den)
def delta(z,w):return (z[0]-w[0],z[1]-w[1])
def cmp(z,w):
    hz=0 if z[1]>0 or (z[1]==0 and z[0]>0) else 1
    hw=0 if w[1]>0 or (w[1]==0 and w[0]>0) else 1
    if hz!=hw:return -1 if hz<hw else 1
    t=z[0]*w[1]-z[1]*w[0]
    return -1 if t>0 else (1 if t<0 else 0)
def oracle(A,B,C,O):
    a,b,c=[delta(p,O) for p in (A,B,C)]
    order=sorted((('a',a),('b',b),('c',c)),key=cmp_to_key(lambda x,y:cmp(x[1],y[1])))
    labels=[x[0] for x in order];j=labels.index('b')
    s=1 if labels[(j+1)%3]=='c' else -1
    central=div(c,b);central=(central[0],s*central[1])
    # Relative ray quotient q; square and divide by its squared magnitude.
    q=div(delta(C,A),delta(B,A));sq=mul(q,q);norm=q[0]**2+q[1]**2
    doubled=(sq[0]/norm,abs(q[1])/q[1]*sq[1]/norm)
    arc='minor' if central[1]>0 else ('major' if central[1]<0 else 'semicircle')
    # Solve u*lambda+v*mu=O-A using exact Gaussian elimination.
    u,v,w=delta(B,A),delta(C,A),delta(O,A)
    mat=[[u[0],v[0],w[0]],[u[1],v[1],w[1]]]
    if not mat[0][0]:mat.reverse()
    p=mat[0][0];mat[0]=[x/p for x in mat[0]]
    f=mat[1][0];mat[1]=[x-f*y for x,y in zip(mat[1],mat[0])]
    mu=mat[1][2]/mat[1][1];lam=mat[0][2]-mat[0][1]*mu
    location='inside' if min(lam,mu)>0 else ('boundary' if min(lam,mu)==0 else 'outside')
    return dict(central=central,doubled=doubled,arc=arc,orientation=s,center_location=location,side_through_center=(lam==0 or mu==0),base_diameter=(b[0]+c[0]==0 and b[1]+c[1]==0))
def require(ok,message):
    if not ok:raise RuntimeError(message)
def points():
    ts=[Q(-5),Q(-3),Q(-2),Q(-1),Q(-1,3),Q(0),Q(1,3),Q(1),Q(2),Q(3),Q(5)]
    return [((1-t*t)/(1+t*t),2*t/(1+t*t)) for t in ts]+[(Q(-1),Q(0))]
def xf(p,kind):
    if not kind:return p
    x,y=p
    return (Q(11,7)+Q(7,3)*(Q(3,5)*x+Q(4,5)*y),Q(-13,11)+Q(7,3)*(Q(4,5)*x-Q(3,5)*y))
count=mutations=0
for A0,B0,C0 in permutations(points(),3):
    for kind in (0,1):
        A,B,C=[xf(p,kind) for p in (A0,B0,C0)];O=xf((Q(0),Q(0)),kind)
        expected=oracle(A,B,C,O);actual=evaluate(A,B,C,O)
        require(actual==expected,'oracle mismatch');require(expected['central']==expected['doubled'],'independent identity mismatch')
        count+=1
        for field in ('central','doubled','arc','orientation','center_location','side_through_center','base_diameter'):
            bad=dict(actual);value=bad[field]
            if isinstance(value,tuple):bad[field]=(value[0]+1,value[1])
            elif isinstance(value,bool):bad[field]=not value
            elif isinstance(value,str):bad[field]='invalid'
            else:bad[field]=-value
            require(bad!=expected,'mutation escaped independent comparison');mutations+=1
# These are rejected calls, not valid configurations proving a false theorem.
invalid=[((1.,0),(0,1),(-1,0)),((True,0),(0,1),(-1,0)),((1,0),(0,2),(-1,0)),((1,0),(1,0),(0,1)),((0,0),(0,0),(0,0)),((1,0,0),(0,1),(-1,0)),((0,0),(1,0),(0,1))]
for triple in invalid:
    try:evaluate(*triple)
    except (ValueError,TypeError):pass
    else:raise RuntimeError('invalid input accepted')
print('PASS independent exact configurations:',count)
print('PASS output mutations rejected by independent full-record comparison:',mutations)
print('PASS invalid input rejections:',len(invalid))
print('Oracle: cyclic circle order, rational complex quotient, Gaussian elimination.')
print('Finite regression audit; not a proof over arbitrary real coordinates.')
# Read-only independent notebook replay: compare output, never rewrite artifact.
import json,io,contextlib
from pathlib import Path
import xml.etree.ElementTree as ET
notebook=json.loads(Path('teaching.zh-CN.ipynb').read_text());scope={};cells=0
for cell in notebook['cells']:
    if cell['cell_type']!='code':continue
    cells+=1;out=io.StringIO()
    with contextlib.redirect_stdout(out):exec(compile(''.join(cell['source']),'review-cell','exec'),scope)
    saved=''.join(''.join(x['text']) for x in cell['outputs'] if x['output_type']=='stream' and x['name']=='stdout')
    require(out.getvalue()==saved,'notebook output mismatch')
svg=Path('diagram.svg').read_text();root=ET.fromstring(svg)
require('script' not in svg and 'href=' not in svg,'unexpected SVG active/external content')
print('PASS read-only notebook replay:',cells,'code cells; NOT kernel')
print('PASS SVG XML/static safety:',len(list(root.iter())),'elements; visual browser review separate')
