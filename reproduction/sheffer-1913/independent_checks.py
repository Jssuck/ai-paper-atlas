"""Independent audit computations; direct guarded expressions and bitset semantics."""
from itertools import product
from collections import Counter
from fractions import Fraction
import json, time
import sheffer as candidate

started = time.perf_counter()

def independent_report(n, table):
    # No reuse of candidate ASTs, evaluator, or closed_signature implementation.
    # None propagates an out-of-K subexpression; roots are guarded too.
    def f(x,y):
        if x is None or y is None: return None
        z = table[x*n+y]
        return z if 0 <= z < n else None
    def d(x): return f(x,x)
    report = {'P1': {'holds': n>=2}, 'P2': {'holds': all(0<=v<n for v in table)}}
    formulas = [(3,1,lambda a:(d(d(a)),a)),
                (4,2,lambda a,b:(f(a,f(b,d(b))),d(a))),
                (5,3,lambda a,b,c:(d(f(a,f(b,c))),f(f(d(b),a),f(d(c),a))))]
    for label,arity,formula in formulas:
        checked=skipped=failures=0
        for args in product(range(n),repeat=arity):
            lhs,rhs=formula(*args)
            if lhs is None or rhs is None: skipped+=1
            else:
                checked+=1
                failures+=lhs!=rhs
        report[f'P{label}']={'holds':failures==0, 'checked':checked, 'guard_skipped':skipped,'failures':failures}
    return report

def sig(r): return ''.join('1' if r[f'P{i}']['holds'] else '0' for i in range(1,6))

hist={
 'consistency':(2,(1,0,0,0)),
 'P1':(1,(0,)),
 'P2':(2,(0,2,2,1)),
 'P3':(2,(0,0,0,0)),
 'P5':(3,(0,1,2,2,2,0,1,0,1)),
}
results={'historical_models':{name:independent_report(n,t) for name,(n,t) in hist.items()}}
assert [sig(v) for v in results['historical_models'].values()]==['11111','01111','10111','11011','11110']
# Entire finite closed-table space, independently formed signature histograms.
results['closed_enumeration']=[]
for n in (1,2,3):
    counts=Counter()
    for t in product(range(n),repeat=n*n):
        own_sig=sig(independent_report(n,t))
        reference_sig=''.join('1' if x else '0' for x in candidate.closed_signature(n,t))
        assert own_sig==reference_sig
        counts[own_sig]+=1
    reference=candidate.enumerate_closed(n)
    assert dict(counts)==reference['signature_counts']
    results['closed_enumeration'].append({'n':n,'tables':sum(counts.values()),'all_five':counts['11111'],'signature_counts':dict(sorted(counts.items()))})
# Compare nonclosed reports against a different design: the candidate AST engine.
count=0
for n in (0,1,2):
    for table in product(range(n+1), repeat=n*n):
        own=independent_report(n,table)
        ref=candidate.FiniteKRule(tuple(range(n)),table).check()
        assert sig(own)==sig(ref)
        for label in ('P3','P4','P5'):
            assert own[label]=={key:ref[label][key] for key in own[label]}
        if n<2: assert all(own[f'P{i}']['holds'] for i in (3,4,5))
        count+=1
results['nonclosed_comparisons']={'tables':count,'scope':'All 0-, 1-, and 2-element rules with one external-output symbol; exact guards/counts match.'}
# Distinct, larger models using Boolean set bitmasks. Check both basis meanings,
# reconstructed operations/constants and every Huntington identity listed.
results['powerset_models']=[]
for n in (2,4,8):
    top=n-1
    for basis in ('nor','nand'):
        f=(lambda a,b:top^(a|b)) if basis=='nor' else (lambda a,b:top^(a&b))
        d=lambda a:f(a,a)
        join=lambda a,b:d(f(a,b))
        meet=lambda a,b:f(d(a),d(b))
        z=f(0,d(0));u=d(z)
        assert sig(independent_report(n,tuple(f(a,b) for a,b in product(range(n),repeat=2))))=='11111'
        for a,b,c in product(range(n),repeat=3):
            assert f(a,b)==f(b,a)
            assert f(a,d(a))==z
            assert join(a,z)==meet(a,u)==a
            assert join(a,d(a))==u and meet(a,d(a))==z
            assert join(a,meet(b,c))==meet(join(a,b),join(a,c))
            assert meet(a,join(b,c))==join(meet(a,b),meet(a,c))
            assert meet(d(a),d(b))==f(a,b)
            assert join(a,b)==((a|b) if basis=='nor' else (a&b))
            assert meet(a,b)==((a&b) if basis=='nor' else (a|b))
        results['powerset_models'].append({'size':n,'basis':basis,'z':z,'u':u,'all_checks_passed':True})
# Fresh, truth-vector evaluator, independent of candidate eval_formula/equivalent.
mask=15
vectors={'p':0b1100,'q':0b1010}
def vector(t):
    kind=t[0]
    if kind=='var':return vectors[t[1]]
    a=vector(t[1])
    if kind=='not':return mask^a
    b=vector(t[2])
    return {'or':lambda:a|b,'and':lambda:a&b,'imp':lambda:(mask^a)|b,
            'nor':lambda:mask^(a|b),'nand':lambda:mask^(a&b)}[kind]()
def basis_only(t,basis):return t[0]=='var' or (t[0]==basis and len(t)==3 and all(basis_only(x,basis) for x in t[1:]))
# Broader than shipped regression: depth 2 over NOT, OR, AND, implication.
forms={('var','p'),('var','q')}
for _ in range(2):
    old=forms
    forms={('var','p'),('var','q')}|{('not',x) for x in old}|{(op,x,y) for op in ('or','and','imp') for x in old for y in old}
comparisons=0
for t in forms:
    for basis in ('nor','nand'):
        out=candidate.translate(t,basis)
        assert basis_only(out,basis)
        assert vector(t)==vector(out)
        comparisons+=4
results['independent_truth_vectors']={'source_formulas':len(forms),'bases':2,'valuations':4,'comparisons':comparisons,'mismatches':0}
# Independent Fraction operator, no use of candidate term or Linear machinery.
f=lambda a,b:-(a+b)/2
d=lambda a:f(a,a)
samples=[Fraction(k,den) for k in range(-3,4) for den in range(1,5)]
samples=sorted(set(samples))
for a,b,c in product(samples,repeat=3):
    assert d(d(a))==a
    assert (f(a,f(b,d(b)))==d(a))==(a==0)
    assert d(f(a,f(b,c)))==f(f(d(b),a),f(d(c),a))==a/2-b/4-c/4
results['rational_regression']={'distinct_samples':len(samples),'triples':len(samples)**3,'all_checks_passed':True,'scope':'Finite regression only; universal algebraic derivation separately reviewed.'}
# Audit the corrected rational API with values beyond float precision.
big_values=(2**54+1,-(2**60+3),10**100+1)
for a in big_values:
    da=candidate.rational_bar(a,a)
    assert isinstance(da,Fraction)
    assert candidate.rational_bar(da,da)==a
rejected=((1.0,1),(1,float('nan')),(True,1))
for a,b in rejected:
    try: candidate.rational_bar(a,b)
    except TypeError: pass
    else: raise AssertionError('Inexact or unsupported input accepted')
results['exact_integer_api_regression']={'large_integers':len(big_values),'invalid_inputs_rejected':len(rejected),'all_checks_passed':True}
results['elapsed_seconds']=round(time.perf_counter()-started,3)
print(json.dumps(results,ensure_ascii=False,indent=2))
