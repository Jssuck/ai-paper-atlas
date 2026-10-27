"""Independent bounded audit, not a general theorem proof."""
import copy
import contextlib
from fractions import Fraction as Q
import hashlib
import io
import itertools
import json
from pathlib import Path
import re
import unittest
from geometry import make_certificate, verify_certificate


def require(ok, message):
    if not ok: raise RuntimeError(message)


def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def pt(a): return [str(x) for x in a]
def data(t,u,v,mode,origin=(Q(2,3),Q(-4,5))):
    f=add(origin,t)
    return {'E':pt(origin),'F':pt(f),'B':pt(add(origin,u)),'D':pt(add(f,v)),'case':mode}

counts={'positive':0,'negative':0,'certificate_attacks':0,'input_attacks':0,'notebook_cells':0}
vs=[(Q(x),Q(y)) for x,y in itertools.product(range(-2,3),repeat=2) if x or y]
# Independent acceptance oracle uses line direction and side, not implementation angle keys.
for t,u,v,mode in itertools.product(vs,vs,vs,('corresponding','interior_sum')):
    d=data(t,u,v,mode)
    expected=cross(t,u)*cross(t,v)>0 and cross(u,v)==0
    try: c=make_certificate(d)
    except ValueError:
        require(not expected,'valid parallel configuration rejected')
        counts['negative']+=1
    else:
        require(expected,'invalid or intersecting configuration accepted')
        require(verify_certificate(d,c),'fresh certificate rejected')
        counts['positive']+=1

base=data((Q(3,2),Q(-2,3)),(Q(1,3),Q(2,5)),(Q(2,3),Q(4,5)),'corresponding')
cert=make_certificate(base)
# Every certificate leaf is attacked, with JSON and non-JSON type replacements.
def leaves(x,path=()):
    if isinstance(x,dict):
        for k,v in x.items(): yield from leaves(v,path+(k,))
    elif isinstance(x,list):
        for k,v in enumerate(x): yield from leaves(v,path+(k,))
    else: yield path,x
for path,old in leaves(cert):
    for replacement in (True,False,None,0,1,1.0,'changed',[],{},float('nan')):
        if type(old) is type(replacement) and old==replacement: continue
        attacked=copy.deepcopy(cert); node=attacked
        for key in path[:-1]: node=node[key]
        node[path[-1]]=replacement
        require(not verify_certificate(base,attacked),'certificate leaf mutation accepted')
        counts['certificate_attacks']+=1
for key in cert:
    attacked=copy.deepcopy(cert);del attacked[key]
    require(not verify_certificate(base,attacked),'missing field accepted');counts['certificate_attacks']+=1
for key in ('E','F','B','D'):
    for axis in (0,1):
        for bad in (True,1,1.0,None,'1/0','01','2/2','NaN',[],{}):
            d=copy.deepcopy(base);d[key][axis]=bad
            try: make_certificate(d)
            except ValueError: pass
            else: raise RuntimeError('malformed input accepted')
            require(not verify_certificate(d,cert),'malformed expected input accepted')
            counts['input_attacks']+=1
# Every point rebinding plus branch changes is checked against an otherwise valid certificate.
for key in ('E','F','B','D'):
    d=copy.deepcopy(base);d[key][0]=str(Q(d[key][0])+1)
    require(not verify_certificate(d,cert),'point binding missed');counts['input_attacks']+=1
d=copy.deepcopy(base);d['case']='interior_sum'
require(not verify_certificate(d,cert),'branch binding missed');counts['input_attacks']+=1
# Full valid translation preserves all angle data but must invalidate old binding.
d=copy.deepcopy(base)
for key in ('E','F','B','D'): d[key][0]=str(Q(d[key][0])+7)
require(verify_certificate(d,make_certificate(d)),'valid translation rejected')
require(not verify_certificate(d,cert),'translated input binding missed');counts['input_attacks']+=1
# Article examples in API mapping: article G/H -> E/F; B=G+b,D=H+d.
for mode in ('corresponding','interior_sum'):
    require(verify_certificate(data((0,2),(2,1),(4,2),mode,(0,0)),make_certificate(data((0,2),(2,1),(4,2),mode,(0,0)))),'article positive')
    for v in ((2,-1),(-2,1)):
        try: make_certificate(data((0,2),(2,1),v,mode,(0,0)))
        except ValueError: pass
        else: raise RuntimeError('article counterexample accepted')
require(add((0,0),(2,1))==add((0,2),(2,-1)),'article intersection arithmetic')
# Re-execute notebook without modifying its stored output; compare outputs except unittest timing.
nb=json.loads(Path('teaching.zh-CN.ipynb').read_text());scope={'__name__':'notebook'}
for cell in nb['cells']:
    if cell['cell_type']!='code':continue
    out=io.StringIO()
    with contextlib.redirect_stdout(out),contextlib.redirect_stderr(out):
        exec(compile(''.join(cell['source']),'independent-notebook','exec'),scope)
    recorded=''.join(''.join(o.get('text',[])) for o in cell.get('outputs',[]))
    norm=lambda s: re.sub(r'Ran (\d+) tests in [\d.]+s',r'Ran \1 tests in <elapsed>s',s)
    require(norm(out.getvalue())==norm(recorded),'notebook output mismatch')
    counts['notebook_cells']+=1
print(json.dumps({'passed':True,'counts':counts,'finite_scope':'vectors with components -2..2, rational translation; two branches','notebook_method':'compile/exec, not kernel; only test elapsed time normalized'},ensure_ascii=False,indent=2))
