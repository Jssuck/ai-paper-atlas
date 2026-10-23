"""Original finite Horn dependency teaching model; not a natural-language judge."""
from dataclasses import dataclass
from itertools import combinations, product
import json

@dataclass(frozen=True)
class Rule:
    premises: tuple[str, ...]
    conclusion: str
    def __post_init__(self):
        if not isinstance(self.premises, tuple) or not self.premises:
            raise ValueError('premises must be a nonempty tuple')
        if any(not isinstance(x, str) or not x for x in self.premises):
            raise ValueError('atoms must be nonempty strings')
        if len(set(self.premises)) != len(self.premises):
            raise ValueError('duplicate premise')
        if not isinstance(self.conclusion, str) or not self.conclusion:
            raise ValueError('conclusion must be a nonempty string')

def facts(values):
    if isinstance(values, (str, bytes)):
        raise ValueError('use an iterable of atoms, not a string')
    result = frozenset(values)
    if any(not isinstance(x, str) or not x for x in result):
        raise ValueError('atoms must be nonempty strings')
    return result

def ruleset(values):
    result = tuple(values)
    if any(not isinstance(x, Rule) for x in result):
        raise ValueError('expected Rule objects')
    return result

def closure(rules, seeds):
    rules = ruleset(rules)
    known = set(facts(seeds))
    while True:
        new = {r.conclusion for r in rules if set(r.premises) <= known}
        if new <= known:
            return frozenset(known)
        known.update(new)

def subsets(items):
    items = tuple(sorted(facts(items)))
    for n in range(len(items) + 1):
        for sub in combinations(items, n):
            yield frozenset(sub)

def supports(rules, target, candidate_facts):
    rules = ruleset(rules)  # materialize once, including generators
    if not isinstance(target, str) or not target:
        raise ValueError('target must be a nonempty atom')
    minimal = []
    for sub in subsets(candidate_facts):
        if any(old <= sub for old in minimal):
            continue
        if target in closure(rules, sub):
            minimal.append(sub)
    return tuple(minimal)

def semantic_consequences(rules, seeds, atoms):
    rules, seeds, atoms = ruleset(rules), facts(seeds), facts(atoms)
    mentioned = seeds | {r.conclusion for r in rules} | {x for r in rules for x in r.premises}
    if not mentioned <= atoms:
        raise ValueError('atom universe omits mentioned atoms')
    models = [m for m in subsets(atoms) if seeds <= m and
              all(not set(r.premises) <= m or r.conclusion in m for r in rules)]
    return frozenset.intersection(*models)  # positive Horn always has all-true model

def examples():
    R = lambda a,b: Rule((a,),b)
    cases = [
      ('direct_self', [R('T','T')], [], ['T'], 'T'),
      ('three_cycle', [R('B','A'),R('C','B'),R('A','C')], [], ['A','B','C'], 'A'),
      ('cycle_with_external_support', [R('B','A'),R('C','B'),R('A','C'),R('E','C')], ['E'], ['E'], 'A'),
      ('irrelevant_cycle', [R('A','B'),R('B','A'),R('E','T')], ['E'], ['E'], 'T'),
      ('uncertain_premise_not_accepted', [R('U','T')], [], ['U'], 'T'),
      ('same_rule_premise_accepted', [R('U','T')], ['U'], ['U'], 'T'),
      ('explicit_equivalence_bridge', [R('T','Q'),R('Q','T')], [], ['Q','T'], 'T'),
      ('one_way_not_reversible', [R('T','Q')], ['Q'], ['Q'], 'T'),
      ('alternative_independent_route', [R('T','Q'),R('Q','T'),R('E','T')], ['E'], ['E','T'], 'T'),
      ('conjunctive_premises_incomplete', [Rule(('P','Q'),'T')], ['P'], ['P','Q'], 'T'),
      ('conjunctive_premises_complete', [Rule(('P','Q'),'T')], ['P','Q'], ['P','Q'], 'T'),
      ('ungrounded_acyclic_chain', [R('U','V'),R('V','T')], [], ['U'], 'T'),
    ]
    return [{'id':name, 'rules':[{'premises':list(r.premises),'conclusion':r.conclusion} for r in rr],
             'accepted_external_seeds':ss, 'target':t, 'closure':sorted(closure(rr,ss)),
             'target_reached':t in closure(rr,ss),
             'candidate_external_facts':cc,
             'minimal_candidate_supports':[sorted(s) for s in supports(rr,t,cc)]}
            for name,rr,ss,cc,t in cases]

def exhaustive():
    atoms = ('A','B','C')
    edges = [Rule((a,),b) for a,b in product(atoms,repeat=2)]
    comparisons = 0
    for mask in range(1 << len(edges)):
        rr = [r for i,r in enumerate(edges) if mask >> i & 1]
        for seed in subsets(atoms):
            observed, expected = closure(rr,seed), semantic_consequences(rr,seed,atoms)
            if observed != expected:
                raise RuntimeError((mask, seed, observed, expected))
            comparisons += 1
    # Additional two-premise AND rule: all eight seeds.
    rr = [Rule(('A','B'),'C')]
    for seed in subsets(atoms):
        if closure(rr,seed) != semantic_consequences(rr,seed,atoms):
            raise RuntimeError('conjunction mismatch')
    return {'unary_graphs':512,'seed_sets_per_graph':8,'closure_semantic_comparisons':comparisons,
            'conjunctive_comparisons':8,'models_considered_per_comparison':8}

if __name__ == '__main__':
    print(json.dumps({'scope':'finite positive Horn teaching reconstruction',
                      'exhaustive':exhaustive(),'examples':examples()},ensure_ascii=False,indent=2,sort_keys=True))
