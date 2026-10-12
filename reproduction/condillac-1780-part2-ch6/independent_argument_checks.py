#!/usr/bin/env python3
"""Second-review finite checks; these are evidence about code, not proofs.

Uses direct bit-table/equation arithmetic and state-space reachability as
oracles. No imports from the implementation's tests and no bare assertions.
"""
from itertools import combinations, permutations, product
import hashlib
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ANNEX = HERE if (HERE / 'condillac_model.py').is_file() else HERE.parent / 'release/reproduction/condillac-1780-part2-ch6'
MODEL_HASH_BEFORE = hashlib.sha256((ANNEX/'condillac_model.py').read_bytes()).hexdigest()
sys.dont_write_bytecode = True
sys.path.insert(0, str(ANNEX))
import condillac_model as m


def check(ok, detail):
    if not ok:
        raise RuntimeError(detail)


def formula(names, values):
    result = m.Const(False)
    for row, output in zip(product((False, True), repeat=len(names)), values):
        if output:
            clause = m.Const(True)
            for name, value in zip(names, row):
                clause = m.And(clause, m.Var(name) if value else m.Not(m.Var(name)))
            result = m.Or(result, clause)
    return result


bits2 = tuple(product((False, True), repeat=2))
tables2 = tuple(product((False, True), repeat=4))
expr_pq = tuple(formula(('p', 'q'), t) for t in tables2)
expr_pd = tuple(formula(('p', 'd1'), t) for t in tables2)
expr_qd = tuple(formula(('q', 'd2'), t) for t in tables2)
counts = {}

# Every chain d1=f(p,q), d2=g(p,d1), d3=h(q,d2), including reverse input.
count = 0
for fi, gi, hi in product(range(16), repeat=3):
    f, g, h = tables2[fi], tables2[gi], tables2[hi]
    definitions = (m.Definition('d1', expr_pq[fi]),
                   m.Definition('d2', expr_pd[gi]),
                   m.Definition('d3', expr_qd[hi]))
    system = m.DefinitionSystem(('p', 'q'), tuple(reversed(definitions)))
    for row, (p, q) in enumerate(bits2):
        x = f[row]
        y = g[2*int(p)+int(x)]
        z = h[2*int(q)+int(y)]
        # Independent finite equation semantics does not call evaluate.
        solutions = tuple((a,b,c) for a,b,c in product((False,True), repeat=3)
                          if a == f[row] and b == g[2*int(p)+int(a)]
                          and c == h[2*int(q)+int(b)])
        check(solutions == ((x,y,z),), 'bit equation oracle uniqueness')
        actual = system.expand({'p':p, 'q':q})
        check(actual == {'p':p,'q':q,'d1':x,'d2':y,'d3':z}, 'expansion versus bit oracle')
        count += 1
counts['three_definition_world_cases'] = count

worlds = tuple({'p':p,'q':q} for p,q in bits2)
subsets = tuple(tuple(i for i,b in enumerate(mask) if b)
                for mask in product((False,True), repeat=4))
count = 0
for subset in subsets:
    selected = tuple(worlds[i] for i in subset)
    for fi, ti in product(range(16), repeat=2):
        f, t = tables2[fi], tables2[ti]
        # Enumerate all four total unary Boolean decoders directly.
        possible = any(all(decoder[int(f[i])] == t[i] for i in subset)
                       for decoder in product((False,True), repeat=2))
        result = m.analyze_observations(selected, (expr_pq[fi],), expr_pq[ti])
        check(result.definable == possible, 'fiber decision versus all unary decoders')
        if possible:
            answer = m.observed_formula(result, ('x',))
            for i in subset:
                check(m.evaluate(answer, {'x':f[i]}) == t[i], 'DNF on actual signatures')
            for bit in (False,True):
                if bit not in tuple(f[i] for i in subset):
                    check(m.evaluate(answer, {'x':bit}) is False, 'unseen signature convention')
        else:
            u,v = result.witness
            i,j = bits2.index((u['p'],u['q'])), bits2.index((v['p'],v['q']))
            check(i in subset and j in subset and f[i] == f[j] and t[i] != t[j], 'witness meaning')
        # Appending a deterministic function of the existing feature cannot help.
        derived = m.Not(expr_pq[fi])
        derived_result = m.analyze_observations(selected, (expr_pq[fi],derived), expr_pq[ti])
        check(derived_result.definable == possible, 'derived-feature no information gain')
        count += 1
counts['partial_domain_observation_cases'] = count

count = 0
for subset in subsets:
    selected = tuple(worlds[i] for i in subset)
    for ei, fi in product(range(16), repeat=2):
        a = m.filter_evidence(m.filter_evidence(selected, expr_pq[ei]), expr_pq[fi])
        b = m.filter_evidence(m.filter_evidence(selected, expr_pq[fi]), expr_pq[ei])
        expected = tuple(worlds[i] for i in subset if tables2[ei][i] and tables2[fi][i])
        check(a == b == expected, 'evidence intersection and commutation')
        count += 1
counts['evidence_pair_cases'] = count

# All 0--3-rule systems on three names, every seed set.
# Oracle searches all reachable knowledge states, rather than iterating the
# closure operator or intersecting closed supersets used in supplied tests.
names = ('a','b','c')
knowledge = tuple(frozenset(n for n,b in zip(names,mask) if b)
                  for mask in product((False,True), repeat=3))
rule_universe = tuple((a,c) for a in knowledge for c in names)
count = order_count = 0
for nr in range(4):
    for raw_rules in combinations(rule_universe, nr):
        rules = tuple(m.Rule(a,c) for a,c in raw_rules)
        for seeds in knowledge:
            reachable, todo = {seeds}, [seeds]
            while todo:
                prior = todo.pop()
                for a,c in raw_rules:
                    if a <= prior and c not in prior:
                        after = prior | {c}
                        if after not in reachable:
                            reachable.add(after)
                            todo.append(after)
            oracle = frozenset().union(*reachable)
            check(oracle in reachable, 'reachable-state union must itself be reachable')
            actual = m.forward_closure(seeds, rules)
            check(actual == oracle, 'closure versus state-space oracle')
            plan = m.plan_learning(seeds, rules)
            prior = seeds
            for c in plan:
                check(c not in prior and any(a<=prior and b==c for a,b in raw_rules), 'plan transition')
                prior = prior | {c}
            check(prior == oracle, 'plan completeness')
            # Exhaustively examine all nonrepeating proposed orders, including empty.
            for length in range(4):
                for order in permutations(names,length):
                    prior, legal, fail = seeds, True, None
                    for index,c in enumerate(order):
                        if c in prior or not any(a<=prior and b==c for a,b in raw_rules):
                            legal, fail = False,index
                            break
                        prior = prior | {c}
                    report = m.verify_order(seeds,rules,order)
                    check(report.valid == legal and report.known == prior, 'order result and last legal state')
                    check(report.failure_index == fail, 'first failure index')
                    if not legal and report.reason == 'no enabled rule':
                        expected = tuple(a-prior for a,c in raw_rules if c == order[fail])
                        check(report.missing_alternatives == expected, 'all-premise alternative witness')
                    order_count += 1
            count += 1
counts['three_name_rule_system_seed_cases'] = count
counts['three_name_proposed_orders'] = order_count
check(hashlib.sha256((ANNEX/'condillac_model.py').read_bytes()).hexdigest() == MODEL_HASH_BEFORE, 'source changed during run')
print(json.dumps({'status':'passed', 'recorded_at_utc':datetime.now(timezone.utc).isoformat(), 'python':sys.version, 'optimization':sys.flags.optimize,
                  'model_sha256':MODEL_HASH_BEFORE,
                  'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  'scope':counts,
                  'limits':'Bounded code checks only; general results require mathematical proofs.'},
                 ensure_ascii=False,indent=2))
