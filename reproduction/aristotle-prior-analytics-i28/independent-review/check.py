"""Independent audit: bit-mask semantics, not model.true_fact/requirements."""
import json
from pathlib import Path
import sys
from dataclasses import replace
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import model

RULES = ('CF','CG','DF','BH','DG','BG')

def check(ok, message):
    if not ok: raise RuntimeError(message)

def main():
    rejected_inputs = 0
    bad_calls = [lambda: model.search([],a='A',e='A')]
    for value in ('', ' ', None, 7, [], {}):
        bad_calls.append(lambda v=value: model.normalize(('all',v,'M')))
        bad_calls.append(lambda v=value: model.search([],a=v,e='E'))
    for call in bad_calls:
        try: call()
        except ValueError: rejected_inputs += 1
        else: raise RuntimeError('malformed input not explicitly rejected')
    counts = {r: 0 for r in RULES}
    assignments = mutations = removals = 0
    for n in range(5):
        for a in range(1 << n):
            for e in range(1 << n):
                for m in range(1 << n):
                    assignments += 1
                    vals = {'A':a,'E':e,'M':m}
                    facts = set()
                    for x in vals:
                        if vals[x]: facts.add(('nonempty',x))
                        for y in vals:
                            if x == y: continue
                            if vals[x] & ~vals[y] == 0: facts.add(('all',x,y))
                            if vals[x] & vals[y] == 0:
                                facts.add(('none',*sorted((x,y))))
                    expected = {
                        'CF': not(m & ~a) and not(e & ~m),
                        'CG': not(m & ~a) and not(m & ~e) and bool(m),
                        'DF': not(m & a) and not(e & ~m),
                        'BH': not(a & ~m) and not(m & e),
                        'DG': not(m & a) and not(m & ~e) and bool(m),
                        'BG': not(a & ~m) and not(m & ~e) and bool(a),
                    }
                    got = model.search(facts)
                    check({c.rule for c in got} == {r for r in RULES if expected[r]}, 'coverage')
                    for c in got:
                        counts[c.rule] += 1
                        check(model.verify(c,facts), 'generated certificate rejected')
                        kind,s,p = c.conclusion
                        x,y = vals[s],vals[p]
                        truth = {'A':not(x & ~y),'E':not(x & y),'I':bool(x & y),'O':bool(x & ~y)}
                        check(truth[kind], 'unsound output')
                        for bad in [replace(c, rule='BF'), replace(c, middle='X'),
                                    replace(c, predicate=c.subject),
                                    replace(c, premises=c.premises[:-1]),
                                    replace(c, conclusion=('bogus',s,p))]:
                            mutations += 1
                            check(not model.verify(bad,facts), 'forgery accepted')
                        for premise in c.premises:
                            removals += 1
                            check(not model.verify(c, facts-{premise}), 'missing premise accepted')
    # Explicit guard: M nonempty is insufficient for inverse BG if A is empty.
    fs = {('all','A','M'),('all','M','E'),('nonempty','M')}
    check(not any(c.rule == 'BG' for c in model.search(fs)), 'BG existence misplaced')
    # Non-entailment of directed targets, independently searching nonempty masks.
    refutations = {}
    for scheme in ('BF','CH','DH'):
        counter = {}
        for a in range(1,8):
            for e in range(1,8):
                for m in range(1,8):
                    premise = {'BF':not(a & ~m) and not(e & ~m),
                               'CH':not(m & ~a) and not(m & e),
                               'DH':not(m & a) and not(m & e)}[scheme]
                    if not premise: continue
                    goals={'A':not(e & ~a),'E':not(e & a),'I':bool(e & a),'O':bool(e & ~a)}
                    for k,v in goals.items():
                        if not v: counter.setdefault(k,{'A':a,'E':e,'M':m})
                    if scheme=='CH': check(bool(a & ~e),'CH inverse particular lost')
        check(set(counter)==set('AEIO'),'missing nonentailment')
        refutations[scheme]=counter
    # 45a bridge: nonempty G under E can be excluded by B while B overlaps E.
    a,b,g,e=1,1,2,3
    check(not(a & ~b) and not(g & ~e) and not(b & g) and bool(g),'bad bridge premises')
    check(bool(e & ~a) and bool(b & e),'invalid bridge not witnessed')
    print(json.dumps({'malformed_inputs_rejected':rejected_inputs,'assignments':assignments,'certificates':sum(counts.values()),
          'by_rule':counts,'forgeries_rejected':mutations,'missing_premises_rejected':removals,
          'nonempty_countermodels':refutations,'scope':'finite 0..4 domain checks only; not a general completeness theorem'},indent=2))

if __name__=='__main__':main()
