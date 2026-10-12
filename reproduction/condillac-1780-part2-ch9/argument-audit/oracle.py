"""Independent finite checks of article claims, not general proofs.
Run with Python standard library; counts are explicit check calls only.
"""
from itertools import product, combinations
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
import sys, json, platform
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import model
counts=Counter()
def check(name, condition):
    if not condition: raise RuntimeError(name)
    counts[name]+=1

def cells(f): return [tuple(i for i,x in enumerate(f) if x==v) for v in dict.fromkeys(f)]
def sufficient(f,q): return all(len({q[i] for i in c})==1 for c in cells(f))
def decoder_exists(f,q):
    keys=list(dict.fromkeys(f))
    return any(all(g[keys.index(f[i])]==q[i] for i in range(len(q))) for g in product((0,1),repeat=len(keys)))
for n in range(1,5):
    H=tuple(map(str,range(n))); bits=list(product((0,1),repeat=n))
    for a in bits:
      for b in bits:
        tests={'a':dict(zip(H,a)),'b':dict(zip(H,b))}
        for ya,yb in product((0,1),repeat=2):
          sa={i for i in range(n) if a[i]==ya}; sb={i for i in range(n) if b[i]==yb}
          got=model.consistent(H,tests,[('a',ya),('b',yb)])
          check('intersection_filter',got==tuple(str(i) for i in sorted(sa&sb)))
          check('idempotence',model.consistent(H,tests,[('a',ya)]*2)==tuple(str(i) for i in sorted(sa)))
          check('contradiction',model.consistent(H,tests,[('a',ya),('a',1-ya)])==())
          for q in bits:
            if sa&sb and all(q[i] for i in sa): check('nonempty_monotonicity',all(q[i] for i in sa&sb))
        subsets=[(),('a',),('b',),('a','b')]
        valid=[]
        for U in subsets:
          f=tuple(tuple(tests[t][h] for t in U) for h in H)
          pairwise=all(any(tests[t][H[i]]!=tests[t][H[j]] for t in U) for i,j in combinations(range(n),2))
          check('full_state_pairwise',pairwise==(len(set(f))==n))
          if pairwise: valid.append(U)
          for q in bits:
            target=all(q[i]==q[j] or any(tests[t][H[i]]!=tests[t][H[j]] for t in U) for i,j in combinations(range(n),2))
            check('target_pairwise_decoder',target==decoder_exists(f,q))
        optimum=min(map(len,valid)) if valid else None
        got=model.minimal_separating(H,tests)
        check('full_state_minimum', (None if got is None else len(got))==optimum)
    for f in product(range(3),repeat=n):
      expected=sum(F(sum(f[j]==f[i] for j in range(n)),n) for i in range(n))
      check('expected_survivors',model.expected_ambiguity(H,dict(zip(H,f)))==expected)
      for q in bits: check('fiber_decoder',sufficient(f,q)==decoder_exists(f,q))
      for r in product(range(2),repeat=3):
        coarse=tuple(r[x] for x in f)
        ec=sum(F(len(c)**2,n) for c in cells(coarse))
        check('partition_refinement',expected<=ec)
        strict=len(cells(f))>len(cells(coarse))
        check('strict_refinement',(expected<ec)==strict)
        for q in bits:
          if sufficient(coarse,q): check('coarsening_direction',sufficient(f,q))
    for p in product(range(3),repeat=n):
      if not sum(p):continue
      prior={h:F(p[i],sum(p)) for i,h in enumerate(H)}
      for L in product((F(0),F(1,2),F(1)),repeat=n):
        Z=sum(prior[h]*L[i] for i,h in enumerate(H))
        likelihood=dict(zip(H,L))
        if not Z:
          try: model.posterior(H,prior,likelihood)
          except ValueError: check('zero_evidence_rejected',True)
          else: check('zero_evidence_rejected',False)
          continue
        post=model.posterior(H,prior,likelihood)
        check('bayes_normalized',sum(post.values())==1)
        check('bayes_exact',all(post[h]==prior[h]*L[i]/Z for i,h in enumerate(H)))
        if all(p[i]>0 for i in range(n) if L[i]>0):
          for q in bits:
            prob=sum(post[h] for i,h in enumerate(H) if q[i])
            structural=all(q[i] for i in range(n) if L[i]>0)
            check('positive_support_equivalence',(prob==1)==structural)
            check('structural_api',model.structural_certainty(H,likelihood,{h:bool(q[i]) for i,h in enumerate(H)})==structural)
check('empty_not_certain',model.certain((),{}) is False)
check('converse_counterexample',all(not q or e for q,e in [(1,1),(0,1)]) and not all(not e or q for q,e in [(1,1),(0,1)]))
check('zero_prior_counterexample',model.posterior(('A','B'),{'A':1,'B':0},{'A':1,'B':1})['A']==1 and not model.structural_certainty(('A','B'),{'A':1,'B':1},{'A':True,'B':False}))
check('worked_bayes', F(1,2)/(F(1,2)+F(1,6))==F(3,4))
check('repeated_odds',F(9,10)==F(3*3,1+3*3))
check('target_vs_count',sufficient((0,1,1,1),(1,0,0,0)) and not sufficient((0,0,1,1),(1,0,0,0)))
print(json.dumps({'status':'pass','python':platform.python_version(),'optimization':sys.flags.optimize,'counts':dict(sorted(counts.items())),'total_explicit_checks':sum(counts.values()),'scope':'n=1..4; two binary tests; ternary features; Boolean targets; prior integer weights0..2 normalized; likelihoods0,1/2,1; target decoder oracle is audit-only, not production API'},indent=2))
