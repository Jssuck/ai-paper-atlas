"""Independent bounded audit: determinants/cross-products, never RREF oracle.
Run with python3 or python3 -OO. Does not import the author's test suite.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import sys
import condillac_model as m

HERE = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def semantic_key(rows):
    """Independent complete two-variable Q-affine classifier.
    Cramer's rule for a nonparallel pair; cross-products for parallel rows.
    """
    rows = tuple(tuple(F(v) for v in row) for row in rows)
    if any(a == b == 0 and c != 0 for a,b,c in rows):
        return ('none',)
    active = [row for row in rows if row[0] or row[1]]
    if not active:
        return ('plane',)
    a,b,c = active[0]
    for d,e,f in active[1:]:
        det = a*e-b*d
        if det:
            r,l = (b*f-c*e)/det, (c*d-a*f)/det
            if all(x*r+y*l+z == 0 for x,y,z in rows):
                return ('point',r,l)
            return ('none',)
    # Every normal vector parallel. Compare full augmented triples.
    pivot = a if a else b
    normalized = (a/pivot,b/pivot,c/pivot)
    for d,e,f in active:
        factor = d if a else e
        if (d/factor,e/factor,f/factor) != normalized:
            return ('none',)
    return ('line',)+normalized

def tuples(rows):
    return tuple((row.r,row.l,row.c) for row in rows)

def main():
    before = sha(HERE/'condillac_model.py')
    semantic_to_canonical, canonical_to_semantic = {},{}
    counts = dict(systems=0, row_operations=0, transfer_cases=0, physical_grid_cases=0, input_rejections=0)
    kinds = {'none':'none','plane':'infinite','line':'infinite','point':'unique'}
    # All ordered pairs in [-2,2]^3 plus all triples in [-1,1]^3.
    pairs = product(tuple(product(range(-2,3),repeat=3)),repeat=2)
    triples = product(tuple(product(range(-1,2),repeat=3)),repeat=3)
    def check(raw):
        key = semantic_key(raw)
        rows = tuple(m.Aff(*row) for row in raw)
        result = m.solve(rows)
        require(result['kind']==kinds[key[0]], f'kind mismatch {raw}: {key} {result}')
        if key[0]=='point':
            require(result['point']==key[1:],f'point mismatch {raw}')
        else:
            require(result['point'] is None,f'nonpoint witness {raw}')
        canon = tuples(m.canonical(rows))
        require(semantic_to_canonical.setdefault(key,canon)==canon, f'noncanonical {raw}')
        require(canonical_to_semantic.setdefault(canon,key)==key, f'canonical collision {raw}')
        require(m.equivalent(rows,m.canonical(rows)),f'equivalence failed {raw}')
        ops = [('swap',0,1),('scale',0,F(-3,2)),('scale',1,F(2,3)),('add',0,1,F(-2,3)),('add',1,0,F(3,2))]
        for op in ops:
            transformed=m.row_step(rows,op)
            require(semantic_key(tuples(transformed))==key,f'row operation failed {raw} {op}')
            counts['row_operations']+=1
        counts['systems']+=1
    for raw in pairs: check(raw)
    for raw in triples: check(raw)
    for raw in [(),((0,0,0),),((0,0,1),),((0,2,-3),),((2,0,-3),)]:
        rows=tuple(m.Aff(*x) for x in raw)
        result=m.solve(rows); key=semantic_key(raw)
        require(result['kind']==kinds[key[0]],f'empty/single row failed {raw}')
    for a,b,k in product(range(-2,4),repeat=3):
        raw=((1,-1,-2*a),(1,-k,(k+1)*b))
        require(tuples(m.transfer(a,b,k))==raw,f'transfer syntax mismatch {a,b,k}')
        key=semantic_key(raw)
        if k!=1:
            l=F(2*a+(k+1)*b,k-1); r=l+2*a
            require(key==('point',r,l),'general formula mismatch')
        else:
            require(key[0]==('line' if a+b==0 else 'none'),'degenerate formula mismatch')
        counts['transfer_cases']+=1
    for r,l,a,b in product([F(-1),F(0),F(1,2),F(1),F(2),F(3)],repeat=4):
        expected=all(x in (0,1,2,3) for x in (r,l,a,b)) and r-a>=0 and l-b>=0
        require(m.feasible(r,l,a,b)==expected,f'physical mismatch {r,l,a,b}')
        counts['physical_grid_cases']+=1
    require(m.solve(m.transfer())['point']==(7,5),'historical solution')
    require(m.solve(m.sequential())['point']==(4,2),'sequential counterexample')
    require(not m.equivalent(m.transfer(),(m.equation(m.L,5),)),'dropped equation unnoticed')
    require(m.holds((m.equation(m.L,5),),0,5) and not m.holds(m.transfer(),0,5),'consequence witness')
    require(m.equation(m.R+2,2*m.L-3).at(7,5)==2,'printed error witness')
    require(m.solve(m.transfer(1,1,4))['point']==(F(13,3),F(7,3)),'noninteger example')
    require(not m.feasible(F(13,3),F(7,3)),'noninteger rejected')
    for fn in [lambda:m.Aff(r=True),lambda:m.R+True,lambda:m.R-True,lambda:m.equation(m.R,True),lambda:m.R*True,lambda:m.transfer(True),lambda:m.row_step(m.transfer(),('scale',0,0)),lambda:m.row_step(m.transfer(),('add',0,0,-1))]:
        try: fn()
        except (ValueError,TypeError): counts['input_rejections']+=1
        else: raise RuntimeError('invalid input silently accepted')
    require(sha(HERE/'condillac_model.py')==before,'model changed during run')
    print(json.dumps({'status':'PASS','oracle':'Cramer determinant + cross-product affine classification; independent direct transfer/physical arithmetic','python':sys.version,'optimization':sys.flags.optimize,'model_sha256':before,'script_sha256':sha(Path(__file__)), 'counts':counts,'distinct_semantic_classes':len(semantic_to_canonical),'scope':'All 15625 ordered two-row systems with coefficients -2..2; all 19683 ordered three-row systems with coefficients -1..1. Bounded evidence, not a theorem proof.'},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
