"""Independent set/member oracle; does not import production implementation."""
from itertools import combinations, product
import json

def powerset(n):
    return [frozenset(c) for k in range(n+1) for c in combinations(range(n),k)]

def inc(x,y):
    return all(e in y for e in x)

def main():
    counts=dict(worlds=0, observations=0, nonempty_observations=0,
                existential_failures=0,target_failures=0,universal_failures=0,
                deductive_premises=0,deductive_failures=0,coverage_premises=0,
                coverage_failures=0,bridge_pairs=0,bridge_equivalence_failures=0)
    for n in range(5):
        sets=powerset(n)
        for a,b,c,d in product(sets,repeat=4):
            counts['worlds']+=1
            known=inc(c,b) and inc(d,b) and inc(d,a)
            if known:
                counts['observations']+=1
                if len(d)>0:
                    counts['nonempty_observations']+=1
                    counts['existential_failures']+=int(not any(e in a for e in b))
                    counts['target_failures']+=int(not inc(c,a))
                    counts['universal_failures']+=int(not inc(b,a))
            if inc(b,a) and inc(c,b):
                counts['deductive_premises']+=1
                counts['deductive_failures']+=int(not inc(c,a))
            if inc(d,a) and inc(b,d):
                counts['coverage_premises']+=1
                counts['coverage_failures']+=int(not inc(b,a))
        for c,d in product(sets,repeat=2):
            violating=[a for a in sets if inc(d,a) and not inc(c,a)]
            counts['bridge_pairs']+=1
            counts['bridge_equivalence_failures']+=int((len(violating)==0)!=inc(c,d))
    expected={
      'worlds':sum(16**n for n in range(5)),
      'observations':sum(8**n for n in range(5)),
      'nonempty_observations':sum(8**n-6**n for n in range(5)),
      'deductive_premises':sum(8**n for n in range(5)),
      'coverage_premises':sum(8**n for n in range(5)),
      'bridge_pairs':sum(4**n for n in range(5)),
      'target_failures':sum(8**n-6**n-7**n+5**n for n in range(5)),
      'universal_failures':sum(8**n-2*6**n+4**n for n in range(5))}
    for k,v in expected.items():
        if counts[k]!=v: raise RuntimeError((k,counts[k],v))
    print(json.dumps({'counts':counts,'closed_form_checks':expected},sort_keys=True,indent=2))
if __name__=='__main__': main()
