"""Independent bounded audit; no imports of the author's test expectations.

Reference truth functions are integer-indexed tables, syntax uses Shannon
expansion rather than the author's DNF helper, and rule eligibility uses bit
masks. Explicit checks remain enabled under Python -O and -OO.
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import sys
import time
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import condillac_model as m
import mutation_check as mutations

COUNTS = Counter()
START = time.monotonic()


class AuditMismatch(Exception):
    pass


def check(condition, label):
    if not condition:
        raise AuditMismatch(label)
    COUNTS['explicit_checks'] += 1


def reject(error_type, action, label):
    try:
        action()
    except error_type:
        COUNTS['validation_rejections'] += 1
    else:
        raise AuditMismatch('Did not reject: ' + label)


def truth_rows(n):
    return tuple(tuple(bool((index >> (n - i - 1)) & 1) for i in range(n))
                 for index in range(1 << n))


def worlds(names):
    return tuple(dict(zip(names, row)) for row in truth_rows(len(names)))


def function_tables(n):
    return truth_rows(1 << n)


def syntax(names, table):
    # Shannon expansion, independently chosen rather than the production DNF.
    if not names:
        return m.Const(table[0])
    half = len(table) // 2
    low = syntax(names[1:], table[:half])
    high = syntax(names[1:], table[half:])
    return m.Or(m.And(m.Not(m.Var(names[0])), low), m.And(m.Var(names[0]), high))


def normalized(rows):
    return sorted(tuple(sorted(w.items())) for w in rows)


def expression_checks():
    for n in range(4):
        names = tuple('p' + str(i) for i in range(n))
        ws = worlds(names)
        check(m.enumerate_worlds(names) == ws, 'world enumeration order')
        for table in function_tables(n):
            expression = syntax(names, table)
            check(m.variables(expression) == frozenset(names), 'free names')
            for index, w in enumerate(ws):
                check(m.evaluate(expression, w) is table[index], 'Shannon truth function')
                COUNTS['expression_rows'] += 1
            COUNTS['expression_tables'] += 1


def definition_checks():
    # All f(p) and g(p,d1) for 0, 1, or 2 primitives, in both input orders.
    for n in range(3):
        names = tuple('p' + str(i) for i in range(n))
        ws = worlds(names)
        fs = function_tables(n)
        gs = function_tables(n + 1)
        old_formulas = [syntax(names, f) for f in fs]
        for f in fs:
            fd = m.Definition('d1', syntax(names, f))
            for g in gs:
                gd = m.Definition('d2', syntax(names + ('d1',), g))
                for definitions in ((fd, gd), (gd, fd)):
                    system = m.DefinitionSystem(names, definitions)
                    check(tuple(d.name for d in system.topological_definitions()) == ('d1', 'd2'),
                          'topological dependencies')
                    expanded_worlds = []
                    for index, w in enumerate(ws):
                        expected = dict(w, d1=f[index], d2=g[2 * index + int(f[index])])
                        actual = system.expand(w)
                        check(actual == expected, 'direct table expansion oracle')
                        check({name: actual[name] for name in names} == w, 'old projection')
                        check(m.satisfying_extensions(w, definitions) == (expected,), 'unique extension')
                        for table, old_formula in zip(fs, old_formulas):
                            check(m.evaluate(old_formula, actual) is table[index], 'old formula truth')
                            COUNTS['old_formula_rows'] += 1
                        expanded_worlds.append(actual)
                        COUNTS['definition_worlds'] += 1
                    check(system.worlds() == tuple(expanded_worlds), 'worlds API')
                    COUNTS['definition_systems_in_input_order'] += 1
    # Every subset and old formula for one explicit p/q system, including empty W.
    names = ('p', 'q')
    ws = worlds(names)
    system = m.DefinitionSystem(names, (m.Definition('d', m.And(m.Var('p'), m.Var('q'))),))
    for keep in truth_rows(4):
        selected = tuple(w for w, bit in zip(ws, keep) if bit)
        expanded = tuple(system.expand(w) for w in selected)
        for table in function_tables(2):
            formula = syntax(names, table)
            expected = all(value for value, bit in zip(table, keep) if bit)
            check(m.entails(selected, formula) is expected, 'subset old entailment')
            check(m.entails(expanded, formula) is expected, 'subset conservativity')
            COUNTS['subset_conservativity_cases'] += 1


def equation_checks():
    # All two-variable Boolean maps and all partial assignments to their LHSs.
    names = ('a', 'b')
    full_worlds = worlds(names)
    all_tables = function_tables(2)
    expressions = [syntax(names, table) for table in all_tables]
    for f, fexpr in zip(all_tables, expressions):
        for g, gexpr in zip(all_tables, expressions):
            equations = (m.Definition('a', fexpr), m.Definition('b', gexpr))
            for fixed in product((None, False, True), repeat=2):
                base = {name: value for name, value in zip(names, fixed) if value is not None}
                expected = tuple(w for index, w in enumerate(full_worlds)
                                 if all(w[key] is value for key, value in base.items())
                                 and w['a'] is f[index] and w['b'] is g[index])
                actual = m.satisfying_extensions(base, equations)
                check(normalized(actual) == normalized(expected), 'simultaneous equation oracle')
                check(base == {name: value for name, value in zip(names, fixed) if value is not None},
                      'equation does not overwrite fixed names')
                COUNTS['equation_cases'] += 1
                COUNTS['equation_solution_count_' + str(len(expected))] += 1
    for expr, count in ((m.Not(m.Var('d')), 0), (m.Var('d'), 2),
                        (m.And(m.Var('d'), m.Not(m.Var('d'))), 1)):
        check(len(m.satisfying_extensions({}, (m.Definition('d', expr),))) == count, 'three cycle outcomes')
        reject(ValueError, lambda e=expr: m.DefinitionSystem((), (m.Definition('d', e),)), 'compiler cycle')


def observation_checks():
    # Full powersets of domains on 0..2 primitives; 0..2 arbitrary features.
    for n in range(3):
        names = tuple('p' + str(i) for i in range(n))
        ws = worlds(names)
        tables = function_tables(n)
        expressions = {t: syntax(names, t) for t in tables}
        for k in range(3):
            coordinates = tuple('x' + str(i) for i in range(k))
            for feature_tables in product(tables, repeat=k):
                signatures = tuple(tuple(t[i] for t in feature_tables) for i in range(len(ws)))
                for target_table in tables:
                    for keep in truth_rows(len(ws)):
                        selected_indices = tuple(i for i, bit in enumerate(keep) if bit)
                        selected = tuple(ws[i] for i in selected_indices)
                        conflicting_pairs = [(i, j) for i in selected_indices for j in selected_indices
                                             if signatures[i] == signatures[j] and target_table[i] != target_table[j]]
                        expected = not conflicting_pairs
                        result = m.analyze_observations(selected, tuple(expressions[t] for t in feature_tables),
                                                        expressions[target_table])
                        check(result.definable is expected, 'pairwise fiber oracle')
                        if expected:
                            table = dict((signatures[i], target_table[i]) for i in selected_indices)
                            check(result.table == tuple(sorted(table.items())), 'actual observed rows only')
                            check(result.witness is None, 'successful result has no witness')
                            formula = m.observed_formula(result, coordinates)
                            for signature in truth_rows(k):
                                check(m.evaluate(formula, dict(zip(coordinates, signature))) is table.get(signature, False),
                                      'DNF matches observed and unobserved coordinates')
                                COUNTS['constructed_formula_rows'] += 1
                        else:
                            check(result.table == (), 'failure carries no successful table')
                            left, right = result.witness
                            i, j = ws.index(left), ws.index(right)
                            check(i in selected_indices and j in selected_indices, 'witness belongs to domain')
                            check(signatures[i] == signatures[j] and target_table[i] != target_table[j],
                                  'independent witness verification')
                            reject(ValueError, lambda: m.observed_formula(result, coordinates), 'conflicting analysis')
                        COUNTS['observation_cases'] += 1


def evidence_checks():
    for n in range(3):
        names = tuple('p' + str(i) for i in range(n))
        ws = worlds(names)
        tables = function_tables(n)
        exprs = {t: syntax(names, t) for t in tables}
        for keep in truth_rows(len(ws)):
            selected = tuple(w for w, bit in zip(ws, keep) if bit)
            for a in tables:
                expected = tuple(w for i, w in enumerate(ws) if keep[i] and a[i])
                check(m.filter_evidence(selected, exprs[a]) == expected, 'evidence removes exact rows')
                check(m.entails(selected, exprs[a]) is all(a[i] for i in range(len(ws)) if keep[i]),
                      'entailment table oracle')
                for b in tables:
                    both = tuple(w for i, w in enumerate(ws) if keep[i] and a[i] and b[i])
                    forward = m.filter_evidence(m.filter_evidence(selected, exprs[a]), exprs[b])
                    backward = m.filter_evidence(m.filter_evidence(selected, exprs[b]), exprs[a])
                    check(forward == backward == both, 'evidence composition and order')
                    COUNTS['evidence_pair_cases'] += 1


def names_from_mask(mask, names):
    return tuple(name for i, name in enumerate(names) if mask & (1 << i))


def rule_checks():
    # All sets of up to three rules on three names, including self-dependence.
    # A reference graph enumerates every reachable knowledge state; it does not
    # call forward_closure or use its synchronous fixed-point implementation.
    names = ('a', 'b', 'c')
    candidates = tuple((premises, conclusion) for premises in range(8) for conclusion in range(3))
    all_orders = tuple(order for length in range(4) for order in product(range(3), repeat=length))
    for size in range(4):
        for rule_bits in combinations(candidates, size):
            rules = tuple(m.Rule(frozenset(names_from_mask(p, names)), names[c]) for p, c in rule_bits)
            for seeds in range(8):
                seeds_as_names = names_from_mask(seeds, names)
                states = {seeds}
                pending = [seeds]
                while pending:
                    state = pending.pop()
                    for premises, conclusion in rule_bits:
                        destination = state | (1 << conclusion)
                        if state & premises == premises and destination not in states:
                            states.add(destination)
                            pending.append(destination)
                expected_mask = max(states, key=int.bit_count)
                check(all(state & expected_mask == state for state in states), 'unique largest reachable state')
                expected = frozenset(names_from_mask(expected_mask, names))
                check(m.forward_closure(seeds_as_names, rules) == expected, 'state-space closure oracle')
                planned = m.plan_learning(seeds_as_names, rules)
                plan_report = m.verify_order(seeds_as_names, rules, planned)
                check(plan_report.valid and plan_report.known == expected, 'plan soundness and completeness')
                # Check the implementation's deterministic first-enabled tie rule.
                state = seeds
                expected_plan = []
                while True:
                    available = [c for p, c in rule_bits if not state & (1 << c) and state & p == p]
                    if not available:
                        break
                    expected_plan.append(names[available[0]])
                    state |= 1 << available[0]
                check(planned == tuple(expected_plan), 'first enabled rule order')
                for order in all_orders:
                    state = seeds
                    failure_index = reason = None
                    missing = ()
                    for index, conclusion in enumerate(order):
                        if state & (1 << conclusion):
                            failure_index, reason = index, 'already known'
                            break
                        alternatives = [p for p, c in rule_bits if c == conclusion]
                        if not any(state & p == p for p in alternatives):
                            failure_index, reason = index, 'no enabled rule'
                            missing = tuple(frozenset(names_from_mask(p & ~state, names)) for p in alternatives)
                            break
                        state |= 1 << conclusion
                    report = m.verify_order(seeds_as_names, rules, tuple(names[i] for i in order))
                    check((report.valid, report.known, report.failure_index, report.reason, report.missing_alternatives)
                          == (failure_index is None, frozenset(names_from_mask(state, names)), failure_index, reason, missing),
                          'order prefix/certificate bitmask oracle')
                    COUNTS['order_cases'] += 1
                COUNTS['rule_seed_cases'] += 1
            COUNTS['rule_sets'] += 1


def validation_checks():
    for value in (0, 1, None, 'true', [], {}):
        reject(TypeError, lambda v=value: m.Const(v), 'constant bool type')
        reject(TypeError, lambda v=value: m.evaluate(m.Const(False), {'p': v}), 'unused world value type')
    for name in ('', 1, None):
        reject(ValueError, lambda v=name: m.Var(v), 'variable name')
        reject(ValueError, lambda v=name: m.enumerate_worlds((v,)), 'enumeration name')
        reject(ValueError, lambda v=name: m.Rule((v,), 'a'), 'premise name')
    for expr in (m.And(m.Const(False), m.Var('missing')), m.Or(m.Const(True), m.Var('missing'))):
        reject(ValueError, lambda e=expr: m.evaluate(e, {}), 'short-circuited free variable')
    for operation in (lambda: m.Not(True), lambda: m.And(m.Const(True), m.Expr()),
                      lambda: m.variables(object()), lambda: m.Definition('d', False)):
        reject(TypeError, operation, 'unsupported expression')
    for operation in (lambda: m.DefinitionSystem(('p', 'p'), ()),
                      lambda: m.DefinitionSystem(('p',), (m.Definition('p', m.Const(True)),)),
                      lambda: m.DefinitionSystem((), (m.Definition('d', m.Var('missing')),)),
                      lambda: m.DefinitionSystem(('p',), ()).expand({}),
                      lambda: m.DefinitionSystem(('p',), ()).expand({'p': True, 'extra': True}),
                      lambda: m.satisfying_extensions({}, (m.Definition('d', m.Var('missing')),)),
                      lambda: m.satisfying_extensions({}, (m.Definition('d', m.Const(True)),) * 2)):
        reject(ValueError, operation, 'definition/equation domain')
    for operation in (lambda: m.DefinitionSystem((), ('bad',)),
                      lambda: m.satisfying_extensions({}, ('bad',)),
                      lambda: m.forward_closure((), ('bad',)),
                      lambda: m.plan_learning((), ('bad',)),
                      lambda: m.verify_order((), ('bad',), ())):
        reject(TypeError, operation, 'unsupported item')
    for operation in (lambda: m.filter_evidence(({'p': False}, {}), m.Const(False)),
                      lambda: m.entails(({'p': False}, {}), m.Const(False)),
                      lambda: m.analyze_observations(({'p': False}, {}), (), m.Const(True)),
                      lambda: m.entails(({'p': False},), m.And(m.Const(False), m.Var('missing'))),
                      lambda: m.analyze_observations(({'p': False}, {'p': True}), (), m.Var('missing')),
                      lambda: m.verify_order((), (), ('unlicensed', ''))):
        reject(ValueError, operation, 'validate before early result')
    for value in (1, None, 'true'):
        reject(TypeError, lambda v=value: m.observed_formula(m.ObservationAnalysis(v, (), None), ()),
               'analysis requires exact bool')
    reject(TypeError, lambda: m.observed_formula(object(), ()), 'analysis record type')
    for analysis in (m.ObservationAnalysis(True, (((False,), 1),), None),
                     m.ObservationAnalysis(True, (((False,), False), ((False,), False)), None),
                     m.ObservationAnalysis(False, (), None),
                     m.ObservationAnalysis(True, (((False, True), False),), None)):
        reject(ValueError, lambda a=analysis: m.observed_formula(a, ('f',)), 'malformed formula table')
    tied = m.DefinitionSystem((), (m.Definition('c', m.Var('a')), m.Definition('a', m.Const(True)),
                                    m.Definition('b', m.Const(False))))
    check(tuple(d.name for d in tied.topological_definitions()) == ('a', 'c', 'b'), 'stable first-ready topology')
    untied = m.DefinitionSystem((), tuple(reversed(tied.definitions)))
    check(tuple(d.name for d in untied.topological_definitions()) == ('b', 'a', 'c'), 'reordered first-ready topology')
    check(normalized(tied.worlds()) == normalized(untied.worlds()), 'topology preserves interpretation')
    alternatives = (m.Rule(('a',), 'b'), m.Rule(('a',), 'c'))
    check(m.plan_learning(('a',), alternatives) == ('b', 'c'), 'rule tie order')
    check(m.plan_learning(('a',), tuple(reversed(alternatives))) == ('c', 'b'), 'reversed rule tie order')
    check(m.verify_order(('a',), alternatives, ('c', 'b')).valid, 'not every reverse fails')
    check(m.DefinitionSystem((), ()).worlds() == ({},), 'one empty world')
    check(m.satisfying_extensions({}, ()) == ({},), 'empty equations')
    check(m.entails((), m.Var('unbound_in_empty_domain')) is True, 'empty-domain entailment')
    check(m.filter_evidence((), m.Var('unbound_in_empty_domain')) == (), 'empty-domain evidence')
    # Input iterables can be generators; caller dictionaries and result copies are independent.
    original = {'p': True}
    system = m.DefinitionSystem(iter(('p',)), iter((m.Definition('d', m.Var('p')),)))
    expansion = system.expand(original)
    expansion['p'] = False
    check(original == {'p': True}, 'expansion copy')
    retained = m.filter_evidence(iter((original,)), m.Const(True))
    retained[0]['p'] = False
    check(original == {'p': True}, 'evidence copy')
    result = m.analyze_observations((original, {'p': False}), (), m.Var('p'))
    result.witness[0]['p'] = False
    check(original == {'p': True}, 'witness copy')
    duplicated = m.analyze_observations(({'p': True}, {'p': True}, {'p': False}), (m.Var('p'), m.Var('p')), m.Var('p'))
    check(duplicated.table == (((False, False), False), ((True, True), True)), 'duplicates do not change fibers')


def mutation_checks():
    for name, owner, attribute, replacement, probe in mutations.CASES:
        status, _ = mutations.classify(probe)
        check(status == 'pass', 'mutation baseline ' + name)
        with patch.object(owner, attribute, replacement):
            status, _ = mutations.classify(probe)
            check(status == 'behavior_mismatch', 'mutation semantic rejection ' + name)
        COUNTS['behavior_rejections'] += 1
    def crash():
        raise RuntimeError('independent simulated harness error')
    check(mutations.classify(crash)[0] == 'harness_error', 'crash is not successful mutation detection')
    check(mutations.classify(lambda: None)[0] == 'pass', 'no failure is not detection')
    # Make the complete harness experience unexpected failure; main must exit 1.
    import contextlib
    import io
    def crashing_expansion(self, world):
        raise RuntimeError('independent simulated mutant crash')
    case = ('simulated_crash', m.DefinitionSystem, 'expand', crashing_expansion, mutations.probe_expansion)
    with patch.object(mutations, 'CASES', (case,)):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = mutations.main()
        report = json.loads(buffer.getvalue())
        check(code == 1 and report['baseline_passes'] == 1 and report['harness_errors'] == 1 and report['behavior_detected'] == 0,
              'complete mutation harness refuses crashing probes')
    COUNTS['simulated_harness_errors_correctly_rejected'] += 1


def main():
    for function in (expression_checks, definition_checks, equation_checks, observation_checks,
                     evidence_checks, rule_checks, validation_checks, mutation_checks):
        function()
        print(json.dumps({'completed': function.__name__, 'elapsed_seconds': round(time.monotonic() - START, 3)}, sort_keys=True), flush=True)
    hashes = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
              for name in ('condillac_model.py', 'test_condillac_model.py', 'demo.py', 'mutation_check.py', 'test_mutation_check.py')}
    print(json.dumps({'result': 'PASS', 'python_optimization': sys.flags.optimize,
                      'counts': dict(sorted(COUNTS.items())), 'source_sha256': hashes}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
