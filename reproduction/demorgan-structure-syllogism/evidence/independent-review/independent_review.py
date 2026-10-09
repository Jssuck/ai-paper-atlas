"""Independent stdlib review checks; no imports from the supplied test suite.
Run from the reproduction root: python evidence/independent-review/independent_review.py
This script does not change the implementation or notebook.
"""
from collections import defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction as F
from itertools import product, combinations
from math import exp, log, fsum
from pathlib import Path
import hashlib, json, subprocess, sys, time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import demorgan as d
OUT = Path(__file__).resolve().parent
P = ('A','O','a','o','E','I','e','i')
R = ('D_sub','D','D_super','C_sub','C','C_super','P')


def truth(rows, i, j):
    # Directly quantify over independent membership tuples, not source set helpers.
    return dict(zip(P, (
        all(not t[i] or t[j] for t in rows), any(t[i] and not t[j] for t in rows),
        all(not t[j] or t[i] for t in rows), any(t[j] and not t[i] for t in rows),
        not any(t[i] and t[j] for t in rows), any(t[i] and t[j] for t in rows),
        all(t[i] or t[j] for t in rows), any(not t[i] and not t[j] for t in rows))))


def pair_relation(rows, i, j):
    # 00, 01, 10, 11 occupancy signatures encode the seven regions directly.
    signatures = {(1,1,0,1): 'D_sub', (1,0,0,1): 'D', (1,0,1,1): 'D_super',
                  (1,1,1,0): 'C_sub', (0,1,1,0): 'C', (0,1,1,1): 'C_super',
                  (1,1,1,1): 'P'}
    present = {(t[i],t[j]) for t in rows}
    return signatures[tuple(int(s in present) for s in product((0,1),repeat=2))]


def logic_check():
    atoms = list(product((0,1), repeat=3))
    models = []
    compositions = {(a,b): set() for a,b in product(R,repeat=2)}
    for mask in range(256):
        rows = [row for i,row in enumerate(atoms) if mask & (1 << i)]
        if not all({row[j] for row in rows} == {0,1} for j in range(3)):
            continue
        models.append((truth(rows,0,1),truth(rows,2,1),truth(rows,0,2)))
        compositions[pair_relation(rows,0,1),pair_relation(rows,2,1)].add(pair_relation(rows,0,2))
    assert len(models) == 193
    computed,count = d.composition_from_atoms()
    assert count == len(models) and computed == compositions
    entails = {(p,q): all(not row[p] or row[q] for row,_,_ in models) for p,q in product(P,repeat=2)}
    all_conclusions = {}
    for p,q in product(P,repeat=2):
        possible = [r for a,b,r in models if a[p] and b[q]]
        assert possible
        all_conclusions[p,q] = {s for s in P if all(r[s] for r in possible)}
    strong = {pair: {c for c in cs if not any(other != c and entails[other,c] for other in cs)}
              for pair,cs in all_conclusions.items()}
    valid = {pair:cs for pair,cs in strong.items() if cs}
    # Audit weakest premises using semantic preservation of each conclusion,
    # rather than comparing the source function's strongest-conclusion sets.
    removed = {pair for pair,cs in valid.items()
               if any(w != pair[slot] and entails[pair[slot],w] and not entails[w,pair[slot]]
                      and cs <= all_conclusions[(w,pair[1]) if slot == 0 else (pair[0],w)]
                      for slot in (0,1) for w in P)}
    kept = set(valid) - removed
    classes = {frozenset((pair,pair[::-1])) for pair in kept}
    assert len(valid) == 32 and len(kept) == 24 and len(classes) == 12
    assert sorted(''.join(x) for x in removed) == ['AA','Ae','EE','Ea','aE','aa','eA','ee']
    census=d.syllogism_census()
    assert census['strongest'] == {''.join(pair):sorted(cs) for pair,cs in valid.items()}
    assert all(pair[::-1] in kept for pair in kept)
    return {'proper_atom_models':len(models),'composition_cells':len(compositions),
            'premise_pairs':len(strong),'concluding_pairs':len(valid),
            'fully_weakened_directed':len(kept),'counterpart_classes':len(classes),
            'removed_pairs':sorted(''.join(p) for p in removed)}


def exact_law(ps, event):
    weights = {}
    for state in product((0,1),repeat=len(ps)):
        if not event(state): continue
        w=F(1)
        for bit,p in zip(state,ps): w *= p if bit else 1-p
        weights[state]=w
    total=sum(weights.values(),F(0))
    return {state:w/total for state,w in weights.items()} if total else None


def probability_check():
    grid=(F(0),F(1,2),F(1))
    multi=zero=0
    for n in (1,2,3):
        for parameters in product(grid,repeat=2*n):
            aa,mm=parameters[:n],parameters[n:]
            # Independently condition 2n Bernoulli flags on exactly one true
            # proposition and every successful proof implying its proposition.
            law=exact_law(parameters,lambda s: sum(s[n:])==1 and all(not s[i] or s[n+i] for i in range(n)))
            if law is None:
                try: d.hypothesis_weights(aa,mm)
                except ValueError: zero+=1
                else: raise AssertionError('Expected impossible conditioning')
            else:
                expected={i:sum(w for s,w in law.items() if s[n+i]) for i in range(n)}
                assert expected == d.hypothesis_weights(aa,mm)
                multi+=1
    witness=0
    for n in (1,2,3,4):
        for ps in product((F(0),F(1,3),F(1,2),F(1)), repeat=n):
            law=exact_law(ps,lambda s: all(s) or not any(s))
            if law is None:
                try: d.joint_testimony(ps)
                except ValueError: pass
                else: raise AssertionError('Expected impossible testimony agreement')
            else: assert sum(w for s,w in law.items() if s[0]) == d.joint_testimony(ps)
            witness+=1
    kcases=kzero=0
    for n in range(5):
        for es in product((F(0),F(1,2),F(2)),repeat=n):
            for k in range(n+1):
                law=exact_law(tuple(e/(1+e) for e in es),lambda s:sum(s)==k)
                if law is None:
                    try:d.exactly_k(es,k)
                    except ValueError:kzero+=1
                    else:raise AssertionError('Expected impossible k-event')
                else:
                    expected={tuple(i for i,b in enumerate(s) if b):w for s,w in law.items()}
                    assert expected == d.exactly_k(es,k)
                    kcases+=1
    return {'one_horn_valid':multi,'one_horn_zero_mass':zero,
            'nonempty_witness_vectors':witness,'exactly_k_valid':kcases,'exactly_k_zero_mass':kzero}


def interval_check():
    # Exact polygon clipping of the placement rectangle, not the closed CDF.
    def clip(poly,ax,ay,c):
        out=[]
        for p,q in zip(poly,poly[1:]+poly[:1]):
            fp=ax*p[0]+ay*p[1]-c; fq=ax*q[0]+ay*q[1]-c
            if fp<=0:out.append(p)
            if (fp<0 and fq>0) or (fp>0 and fq<0):
                t=fp/(fp-fq)
                out.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))
        return out
    cases=0
    for a,b in product((F(i,8) for i in range(1,8)),repeat=2):
        width,height=1-a,1-b
        for t in (F(i,8) for i in range(9)):
            if t>=min(a,b):expected=F(1)
            else:
                poly=[(F(0),F(0)),(width,F(0)),(width,height),(F(0),height)]
                poly=clip(poly,-1,1,a-t)
                poly=clip(poly,1,-1,b-t)
                area=abs(sum(p[0]*q[1]-q[0]*p[1] for p,q in zip(poly,poly[1:]+poly[:1])))/2
                expected=1-area/(width*height)
            assert expected==d.interval_overlap_cdf(a,b,t),(a,b,t,expected)
            cases+=1
    return {'exact_placement_polygon_cases':cases,'includes_zero_and_max_overlap':True}


def adaptive_integral(r, prior):
    # Independent integration on the logit scale: avoids a narrow endpoint
    # layer in mu, and does not use either implementation formula/quadrature.
    lr=log(r)
    def sigmoid(t):
        if t>=0:return 1/(1+exp(-t))
        e=exp(t);return e/(1+e)
    def f(t):
        e=exp(-abs(t)); jac=e/(1+e)**2
        return sigmoid(lr+t)*(jac if prior=='uniform' else 6*jac*jac)
    def simpson(a,b,fa,fm,fb): return (b-a)*(fa+4*fm+fb)/6
    def recurse(a,b,fa,fm,fb,whole,tol,depth):
        m=(a+b)/2; l=f((a+m)/2); rr=f((m+b)/2)
        left=simpson(a,m,fa,l,fm); right=simpson(m,b,fm,rr,fb)
        delta=left+right-whole
        if abs(delta)<=15*tol:return left+right+delta/15
        if depth==0:raise AssertionError('Independent quadrature did not converge')
        return recurse(a,m,fa,l,fm,left,tol/2,depth-1)+recurse(m,b,fm,rr,fb,right,tol/2,depth-1)
    parts=[]
    for a in range(-60,60,5):
        b=a+5; fa,fm,fb=f(a),f((a+b)/2),f(b)
        parts.append(recurse(a,b,fa,fm,fb,simpson(a,b,fa,fm,fb),2e-15,24))
    return fsum(parts)


def decimal_formula(r,prior):
    with localcontext() as ctx:
        ctx.prec=100
        r=Decimal(str(r))
        if r==1:return 0.5
        if prior=='uniform': val=r/(r-1)*(1-r.ln()/(r-1))
        else: val=r/(r-1)**4*(6*r*r.ln()+2+3*r-6*r*r+r**3)
        return float(val)


def numeric_check():
    primary=[]
    for prior in ('uniform','beta22'):
        for r in (0.1,0.25,0.5,1,2,4,10):
            independent=adaptive_integral(r,prior)
            actual=d.averaged_authority(r,prior)
            assert abs(independent-actual)<1e-11
            assert abs(independent-decimal_formula(r,prior))<1e-12
            primary.append({'prior':prior,'r':r,'absolute_error':abs(independent-actual)})
    edges=[]
    for prior in ('uniform','beta22'):
        for r in (0.99,1.01,1.01000001,1e-10,1e6,1e78):
            expected=decimal_formula(r,prior)
            item={'prior':prior,'r':r,'reference':expected}
            try:
                actual=d.averaged_authority(r,prior)
                item.update(actual=actual,absolute_error=abs(actual-expected))
            except Exception as exc:item['error']=type(exc).__name__+': '+str(exc)
            # Report behavior without converting diagnostic edge tests to
            # silently passing accuracy claims.
            edges.append(item)
    q=d.averaged_authority_quadrature(1e-10,'uniform')
    series_cases=0
    for prior in ('uniform','beta22'):
        for r in (0.99,1.01,1.01000001,1.000000000000001,0.999999999999999):
            h=F(str(r))-1
            # Integrate the geometric series term by term using exact moments.
            exact=F(1,2)+sum((-1)**(k-1)*h**k*(F(1,(k+1)*(k+2)) if prior=='uniform'
                       else F(12,(k+2)*(k+3)*(k+4))) for k in range(1,65))
            assert abs(d.averaged_authority(r,prior)-float(exact))<1e-14
            series_cases+=1
        for r in (1e-300,1e-78,1e78,1e300):
            actual=d.averaged_authority(r,prior)
            assert 0<=actual<=1
            assert abs(actual+d.averaged_authority(1/r,prior)-1)<1e-14
    return {'independent_integral_cases':len(primary),'max_primary_absolute_error':max(x['absolute_error'] for x in primary),
            'near_one_exact_moment_series_cases':series_cases,'edge_diagnostics':edges,'fixed_simpson_boundary_layer':{'r':1e-10,'prior':'uniform',
            'computed':q,'reference':decimal_formula(1e-10,'uniform'),'absolute_error':abs(q-decimal_formula(1e-10,'uniform'))}}


def counts_check():
    counts={'pair_models_n_0_to_5':sum(4**n for n in range(6)),
            'form_models_n_0_to_4':sum(4**n for n in range(5)),
            'proper_pairs_n_2_to_5':sum((2**n-2)**2 for n in range(2,6)),
            'proper_triples_n_2_to_5':sum((2**n-2)**3 for n in range(2,6)),
            'overlap_pairs_n_1_to_7':sum(4**n for n in range(1,8)),
            'cardinality_groups_n_1_to_7':sum((n+1)**2 for n in range(1,8)),
            'subset_pairs_n_0_to_6':sum(4**n for n in range(7)),
            'subset_groups_n_0_to_6':sum((n+1)**2 for n in range(7))}
    assert list(counts.values()) == [1365,341,1136,29968,21844,203,5461,140]
    return counts


def notebook_check():
    notebook=json.loads((ROOT/'tutorial.ipynb').read_text())
    code=[c for c in notebook['cells'] if c['cell_type']=='code']
    # Execute in a separate process; never write the submitted notebook.
    harness="""import json, contextlib, io
n=json.load(open('tutorial.ipynb')); state={'__name__':'__independent_notebook__'}
for i,c in enumerate(n['cells']):
 if c['cell_type']=='code': exec(compile(''.join(c['source']),f'review-cell-{i}','exec'),state)
print('Independent notebook replay completed without modifying the notebook.')
"""
    p=subprocess.run([sys.executable,'-c',harness],cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (OUT/'notebook-replay.txt').write_text(p.stdout+f'\n[exit code: {p.returncode}]\n')
    assert p.returncode==0
    return {'code_cells':len(code),'fresh_process_replay_exit_code':p.returncode,'notebook_modified':False}


def main():
    start=time.perf_counter()
    result={'logic':logic_check(),'probability':probability_check(),'intervals':interval_check(),'enumeration_counts':counts_check(),
            'p401_numerics':numeric_check(),'notebook':notebook_check()}
    result['reviewed_sha256']={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
         for name in ('demorgan.py','tests/test_demorgan.py','demo.py','tutorial.ipynb')}
    result['elapsed_seconds']=round(time.perf_counter()-start,6)
    (OUT/'independent-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
