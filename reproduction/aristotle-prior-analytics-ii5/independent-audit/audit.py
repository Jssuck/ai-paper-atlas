#!/usr/bin/env python3
"""Independent II.5 audit: pointwise quantifiers, no author predicate imports."""
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
BASE = HERE.parent

def evaluate(rows):
    # rows have one Boolean triple (A,B,C) per actual object.
    def incl(i,j): return all(not r[i] or r[j] for r in rows)
    def disj(i,j): return all(not(r[i] and r[j]) for r in rows)
    def some(i,j): return any(r[i] and r[j] for r in rows)
    def notsome(i,j): return any(r[i] and not r[j] for r in rows)
    bridge = all(r[0] or r[1] for r in rows)
    valid = [
      (incl(2,1) and incl(1,0),incl(2,0)),
      (incl(2,0) and incl(1,2),incl(1,0)),
      (incl(2,0) and incl(0,1),incl(2,1)),
      (incl(2,1) and disj(1,0),disj(2,0)),
      (disj(2,0) and incl(1,2),disj(1,0)),
      (disj(2,0) and bridge,incl(2,1)),
      (some(2,0) and incl(0,1),some(2,1)),
      (notsome(2,0) and bridge,some(2,1)),
      # Two further forward particular arguments stated in the paper.
      (incl(1,0) and some(2,1),some(2,0)),
      (disj(1,0) and some(2,1),notsome(2,0)),
    ]
    invalid = [
      (incl(2,0) and incl(2,1),incl(1,0)),
      (incl(2,0) and incl(1,0),incl(2,1)),
      (disj(2,0) and disj(1,0),incl(2,1)),
      (notsome(2,0) and notsome(1,0),some(2,1)),
      (some(2,0) and some(1,2),incl(1,0)),
      (notsome(2,0) and some(1,2),disj(1,0)),
    ]
    return valid, invalid

TYPES = list(product((False, True), repeat=3))
def count(domain):
    stats = {'models':0,'valid':[[0,0] for _ in range(10)],'invalid':[[0,0] for _ in range(6)]}
    for rows in domain:
        stats['models'] += 1
        for key,pairs in zip(('valid','invalid'),evaluate(rows)):
            for counter,(p,q) in zip(stats[key],pairs):
                counter[0] += bool(p)
                counter[1] += bool(p and not q)
    return stats

def nonempty(rows): return all(any(r[i] for r in rows) for i in range(3))
def require(stats):
    assert all(p>0 and f==0 for p,f in stats['valid'])
    assert all(f>0 for p,f in stats['invalid'])

occupied = [[TYPES[i] for i in range(8) if mask & (1<<i)] for mask in range(1,256)]
compressed = {'nonempty_universe':count(occupied), 'all_terms_nonempty':count(r for r in occupied if nonempty(r))}
assert [compressed[k]['models'] for k in compressed] == [255,218]
for stats in compressed.values(): require(stats)
# Match author artifacts by schema name, not positional JSON order.
author=json.loads((BASE/'results.json').read_text())
vnames=['affirmative_forward','recover_B_subset_A','recover_C_subset_B','negative_forward','recover_negative_major','recover_with_complement_bridge','particular_affirmative_recovery','particular_negative_recovery']
inames=['conclusion_and_unchanged_minor_do_not_recover_major','conclusion_and_unchanged_major_do_not_recover_minor','simple_E_conversion_not_complement_bridge','separate_negative_witnesses_not_shared_witness','particular_affirmative_does_not_recover_universal','particular_negative_does_not_recover_universal']
for domain,stats in compressed.items():
    for key,names in [('valid',vnames),('invalid',inames)]:
        for name,(p,f) in zip(names,stats[key]):
            assert author[key][domain][name]['premise_models']==p
            assert author[key][domain][name]['counterexamples']==f
    for name in inames:
        m=author['invalid'][domain][name]['smallest_countermodel']
        rows=[tuple(x in m[t] for t in ('A','B','C')) for x in m['U']]
        p,q=evaluate(rows)[1][inames.index(name)]
        assert p and not q
        if domain=='all_terms_nonempty':assert nonempty(rows)
# Separate labeled-universe enumeration includes duplicate membership types.
labeled=count(rows for n in range(1,5) for rows in product(TYPES,repeat=n))
assert labeled['models']==4680
require(labeled)
# Literal all-nonempty paper examples, indexed by the invalid schema they refute.
examples=[({1,2},{1},{1,2},{1},0),({1,2},{1,2},{1},{2},1),
          ({0,1,2},{0},{1},{2},2),({0,1,2},{0},{1},{2},3),
          ({1,2},{1},{1,2},{1},4),({0,1},{0},{0,1},{1},5)]
for U,A,B,C,k in examples:
    assert A and B and C and (A|B|C)<=U
    p,q=evaluate([tuple(x in S for S in (A,B,C)) for x in U])[1][k]
    assert p and not q
# Independently reconstruct paper's V=A<=C account, not author short Q-loop.
deps={'P':{'P'},'R':{'R'},'V':{'V'}}
deps['T']=deps['R']|deps['V']
deps['S']=deps['V']|deps['P']
deps['V_derived']=deps['S']|deps['T']
assert deps['V_derived']=={'P','R','V'}
# A strict chain satisfies P,R but not V.
C={1};B={1,2};A={1,2,3}
assert C<=B<=A and not A<=C
out={'compressed':compressed,'labeled_universes_1_to_4':labeled,
     'author_all_counts_and_12_countermodels_match':True,
     'literal_paper_counterexamples_checked':len(examples),
     'six_relation_V_dependencies':sorted(deps['V_derived']),
     'scope':'finite pointwise checks; not a general historical semantics proof'}
print(json.dumps(out,indent=2,sort_keys=True))
