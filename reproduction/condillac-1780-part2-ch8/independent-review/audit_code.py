"""Independent finite audit using explicit flat complete-policy enumeration.

Reconstructed after loss of the shared workspace; new outputs must be generated
by real runs. Standard library only; all checks survive Python -O and -OO.
"""
from collections import Counter
from dataclasses import FrozenInstanceError
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import platform
import random
import sys

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
import condillac_model as m
from examples import chips, query_example, selector, causal_toy, causal_run
COUNT = Counter()


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def reject(label, call, expected=(TypeError, ValueError, KeyError)):
    try:
        call()
    except expected:
        COUNT['negative_contract_cases'] += 1
        return
    raise RuntimeError('invalid operation accepted: ' + label)


def policy_fits(target, questions, selected, height, root):
    """Exhaust every question assignment on a full r-ary tree of given height.

    Simulate worlds to heap-array leaf positions. Repetition and unused positions
    are allowed, so every shorter adaptive policy can be padded to this form.
    """
    labels = [tuple(dict.fromkeys(q)) for q in questions]
    radix = max(len(values) for values in labels)
    response = [tuple(labels[j].index(v) for v in q) for j, q in enumerate(questions)]
    nodes = sum(radix ** d for d in range(height))
    for tail in product(range(len(questions)), repeat=nodes - 1):
        assignment = (root,) + tail
        leaves = {}
        valid = True
        for i in selected:
            position = 0
            for _ in range(height):
                q = assignment[position]
                position = radix * position + 1 + response[q][i]
            if position in leaves and leaves[position] != target[i]:
                valid = False
                break
            leaves[position] = target[i]
        if valid:
            return True
    return False


def oracle(target, questions, selected):
    if not selected:
        return None, None
    if len({target[i] for i in selected}) == 1:
        return 0, None
    if any(target[a] != target[b] and all(q[a] == q[b] for q in questions)
           for a in selected for b in selected):
        return None, None
    for height in range(1, len(questions)):
        for root in range(len(questions)):
            if policy_fits(target, questions, selected, height, root):
                return height, root
    # Querying every table once is an upper bound. If no smaller height worked,
    # every genuinely splitting first question can start a depth-|Q| policy.
    root = next(j for j, q in enumerate(questions) if len({q[i] for i in selected}) > 1)
    return len(questions), root


def inspect_tree(node, target, questions, selected, used=()):
    check(node.candidates == selected and all(type(i) is int for i in node.candidates), 'candidate indices differ')
    if not selected:
        check(node.status == 'inconsistent' and node.depth is None, 'empty tree not inconsistent')
        return None
    if node.status == 'impossible':
        check(node.depth is None and node.witness is not None, 'missing impossibility marker')
        a, b = node.witness
        check(a in selected and b in selected and target[a] != target[b], 'invalid witness pair')
        check(all(q[a] == q[b] for q in questions), 'witness can be distinguished')
        return None
    if node.status == 'identified':
        check(node.depth == 0 and not node.branches, 'invalid terminal node')
        check(all(target[i] == node.answer for i in selected), 'incorrect leaf answer')
        return 0
    check(node.status == 'measurement', 'unknown node status')
    q = node.question_index
    check(type(q) is int and 0 <= q < len(questions) and q not in used, 'invalid/repeated question')
    values = tuple(dict.fromkeys(questions[q][i] for i in selected))
    check(len(values) > 1 and tuple(k for k, _ in node.branches) == values, 'wrong branch labels/order')
    costs = []
    for value, child in node.branches:
        subset = tuple(i for i in selected if questions[q][i] == value)
        cost = inspect_tree(child, target, questions, subset, used + (q,))
        check(cost is not None, 'finite tree has impossible branch')
        costs.append(cost)
    cost = 1 + max(costs)
    check(node.depth == cost, 'stored depth differs from actual worst cost')
    return cost


def check_case(target, questions, selected, category):
    n = len(target)
    u = m.Universe(('index',), tuple((i,) for i in range(n)))
    p = m.Problem(u, m.Table(u, 'answer', target),
                  (m.Constraint(u, 'selected', tuple(i in selected for i in range(n))),))
    qs = tuple(m.Table(u, 'q' + str(i), q) for i, q in enumerate(questions))
    depth, root = oracle(target, questions, selected)
    node = m.minimax_tree(p, qs)
    check(node.depth == depth, 'optimal depth differs from policy enumeration')
    if depth is not None and depth > 0:
        check(node.question_index == root, 'earliest optimal root differs')
    inspect_tree(node, target, questions, selected)
    if depth is not None:
        lengths = []
        for i in selected:
            current, path = node, []
            while current.status == 'measurement':
                q = current.question_index
                path.append('q' + str(q))
                current = next(child for value, child in current.branches if value == questions[q][i])
            check(current.answer == target[i], 'independent traversal answer differs')
            check(m.follow_tree(p, qs, node, i) == (target[i], tuple(path)), 'replay helper differs')
            lengths.append(len(path))
            COUNT['independent_world_traversals'] += 1
        check(max(lengths) == depth, 'worst realized path differs')
    COUNT[category] += 1


def decision_checks():
    for n in range(1, 5):
        vectors = tuple(product((0, 1), repeat=n))
        for target in vectors:
            for a in vectors:
                for b in vectors:
                    check_case(target, (a, b), tuple(range(n)), 'exhaustive_binary_two_question_cases')
    rng = random.Random(17801798)
    for _ in range(100):
        n = rng.randrange(1, 7)
        target = tuple(rng.choice((0, 'answer', (2, 'nested'))) for _ in range(n))
        qs = tuple(tuple(rng.randrange(3) for _ in range(n)) for _ in range(3))
        selected = tuple(i for i in range(n) if rng.randrange(2))
        check_case(target, qs, selected, 'seeded_multivalued_three_question_cases')
    worlds = tuple(product((0, 1), repeat=4))
    qs = tuple(tuple(w[j] for w in worlds) for j in range(4))
    check_case(tuple(sum(w) % 2 for w in worlds), qs, tuple(range(16)), 'four_question_parity_cases')
    for p, tables in (selector(), causal_toy()):
        check_case(p.target.values, tuple(q.values for q in tables), tuple(range(len(p.universe.worlds))),
                   'published_example_tree_cases')
    check_case((), (), (), 'empty_tree_cases')


def semantic_checks():
    for n in range(5):
        u = m.Universe(('index',), tuple((i,) for i in range(n)))
        for target in product((0, 1), repeat=n):
            problems = []
            for mask in product((False, True), repeat=n):
                selected = tuple(i for i in range(n) if mask[i])
                p = m.Problem(u, m.Table(u, 'target', target), (m.Constraint(u, 'mask', mask),))
                problems.append((p, selected))
                answers = tuple(dict.fromkeys(target[i] for i in selected))
                status = 'inconsistent' if not selected else 'identified' if len(answers) == 1 else 'underdetermined'
                actual = m.analyze(p)
                check((actual.status, actual.candidates, actual.answers) == (status, selected, answers), 'analysis differs')
                if status == 'identified':
                    check(actual.answer == answers[0], 'unique answer differs')
                else:
                    reject('nonidentified answer', lambda a=actual: a.answer, ValueError)
                COUNT['analysis_cases'] += 1
                for code in product((0, 1), repeat=n):
                    report = m.compression(p, m.Table(u, 'encoding', code))
                    pairs = [(a, b) for a in selected for b in selected
                             if a < b and code[a] == code[b] and target[a] != target[b]]
                    check(report.sufficient == (not pairs) and report.vacuous == (not selected), 'fiber criterion differs')
                    if pairs:
                        check(report.witness in pairs and report.decoder == (), 'invalid fiber witness')
                        reject('insufficient decoder', lambda r=report: r.decode(0), ValueError)
                    else:
                        decoder = tuple((c, target[next(i for i in selected if code[i] == c)])
                                        for c in dict.fromkeys(code[i] for i in selected))
                        check(report.decoder == decoder and report.witness is None, 'decoder differs')
                        for i in selected:
                            check(report.decode(code[i]) == target[i], 'decoder answer differs')
                        reject('unsupported decoder code', lambda r=report: r.decode('absent'), KeyError)
                    COUNT['fiber_cases'] += 1
            for (left, a), (right, b) in product(problems, repeat=2):
                r = m.compare_rewrite(left, right)
                check(r.worlds_preserved == (a == b), 'world equality differs')
                check(r.answers_preserved == ({target[i] for i in a} == {target[i] for i in b}), 'answer equality differs')
                check(r.nonvacuous == bool(a and b), 'nonvacuity differs')
                check(r.lost_worlds == tuple(i for i in a if i not in b), 'lost worlds differ')
                check(r.gained_worlds == tuple(i for i in b if i not in a), 'gained worlds differ')
                check(m.candidates(m.add_evidence(left, right.constraints[0])) == tuple(i for i in a if i in b),
                      'evidence is not conjunction')
                COUNT['rewrite_and_evidence_cases'] += 1
    full, known, narrower = query_example()
    check(len(m.candidates(known)) == 2 and m.analyze(known).answer == 0, 'query confused with world identity')
    reject('evidence is not equivalent rewrite', lambda: m.translation_chain((full, known)), ValueError)
    reject('answer preservation is weaker', lambda: m.translation_chain((known, narrower)), ValueError)
    check(len(m.translation_chain((known, narrower), 'answers')) == 1, 'answer-relative translation failed')
    original, expanded, eliminated, solved, _ = chips()
    check(m.analyze(original).answer == (7, 5), 'chips answer differs')
    check(len(m.translation_chain((original, expanded, eliminated, solved))) == 3, 'chips translations differ')
    check(m.analyze(chips(6)[0]).status == 'inconsistent', 'finite bound not honored')


def negative_checks():
    class IntChild(int): pass
    class StrChild(str): pass
    class TupleChild(tuple): pass
    u = m.Universe(('i',), ((0,), (1,)))
    t = m.Table(u, 't', (0, 1)); p = m.Problem(u, t); q = (t,)
    tree = m.minimax_tree(p, q)
    for value in (True, False, 0.0, 1.0, IntChild(1), StrChild('x'), TupleChild((1,)), None, [], {}, set()):
        reject('world coordinate type', lambda v=value: m.Universe(('i',), ((v,),)))
        reject('nested value type', lambda v=value: m.Table(u, 'v', ((v,), 0)))
        reject('nested decoder type', lambda v=value: m.compression(p, t).decode((v,)))
    for value in (True, False, IntChild(0), 0.0, '0', None):
        reject('replay index type', lambda v=value: m.follow_tree(p, q, tree, v), TypeError)
    for value in (-1, 2, 100):
        reject('replay range', lambda v=value: m.follow_tree(p, q, tree, v), ValueError)
    for fields in ((), [], ['i'], ('',), (' ',), (True,), ('i', 'i'), (StrChild('i'),)):
        reject('fields', lambda v=fields: m.Universe(v, ()))
    for worlds in ([], ((0,), (0,)), ((),), ((0, 1),), ([0],)):
        reject('world shape', lambda v=worlds: m.Universe(('i',), v))
    for values in ([0, 1], (), (0,), (0, 1, 2)):
        reject('table totality', lambda v=values: m.Table(u, 't', v))
    for mask in ([True, False], (0, 1), (True,), (True, None), (True, IntChild(1))):
        reject('constraint mask', lambda v=mask: m.Constraint(u, 'c', v))
    for name in ('', ' ', 0, None, StrChild('name')):
        reject('table name', lambda v=name: m.Table(u, v, (0, 1)))
    v = m.Universe(('i',), ((1,), (0,))); other = m.Table(v, 'other', (1, 0))
    for call in (lambda: m.Problem(u, other), lambda: m.Problem(u, t, []),
                 lambda: m.Problem(u, t, (t,)), lambda: m.add_evidence(p, t),
                 lambda: m.compression(p, other), lambda: m.minimax_tree(p, [t]),
                 lambda: m.minimax_tree(p, (other,)), lambda: m.minimax_tree(p, (t, t)),
                 lambda: m.analyze(None), lambda: m.compare_rewrite(p, m.Problem(v, other)),
                 lambda: m.translation_chain((p,)), lambda: m.translation_chain([p, p]),
                 lambda: m.translation_chain((p, p), 'syntax')):
        reject('cross-object contract', call)
    for factory in (m.table, m.constraint):
        reject('factory universe', lambda f=factory: f(None, 'name', lambda w: 0), TypeError)
        reject('factory callback', lambda f=factory: f(u, 'name', None), TypeError)
    reject('truthy predicate', lambda: m.constraint(u, 'c', lambda w: 1), TypeError)
    calls = []
    sampled = m.table(u, 'sample', lambda w: (calls.append(w), w[0])[1])
    check(calls == list(u.worlds), 'callback initial calls differ')
    for _ in range(3):
        m.analyze(m.Problem(u, sampled)); m.minimax_tree(p, (sampled,)); m.compression(p, sampled)
    check(calls == list(u.worlds), 'callback re-executed')
    reject('frozen table', lambda: setattr(sampled, 'name', 'changed'), FrozenInstanceError)
    nested = m.Table(u, 'nested', ((0, ('a',)), (1, ('b',))))
    np = m.Problem(u, nested); nt = m.minimax_tree(np, (nested,))
    for i in range(2):
        check(m.follow_tree(np, (nested,), nt, i)[0] == nested.values[i], 'nested replay failed')
        check(m.compression(np, nested).decode(nested.values[i]) == nested.values[i], 'nested decoder failed')
    for model in ('M1', 'M2'):
        for bit in (0, 1):
            for intervention in (None, 0, 1):
                expected = (bit, bit) if intervention is None else ((intervention, intervention) if model == 'M1' else (intervention, bit))
                check(causal_run(model, bit, intervention) == expected, 'structural assignment differs')
                COUNT['causal_mechanism_cases'] += 1
    for args in (('M3', 0, None), (StrChild('M1'), 0, None), ('M1', True, None),
                 ('M1', IntChild(0), None), ('M2', 0, False), ('M2', 0, IntChild(1)),
                 ('M1', 0, 1.0), ('M1', -1, None), ('M2', 0, 2)):
        reject('causal input', lambda args=args: causal_run(*args), ValueError)
    _, observations = causal_toy()
    check(observations[0].values == (((0, 0), (1, 1)), ((0, 0), (1, 1))), 'natural observation differs')
    check_case(('M1', 'M2'), (observations[0].values, ((1, 1), (1, 0))), (0, 1), 'causal_augmented_question_cases')
    reject('bool bound', lambda: chips(True), ValueError)
    reject('zero bound', lambda: chips(0), ValueError)


def main():
    reviewed = [BASE / 'condillac_model.py', BASE / 'examples.py', Path(__file__)]
    before = {str(p.relative_to(BASE)): sha256(p.read_bytes()).hexdigest() for p in reviewed}
    semantic_checks(); negative_checks(); decision_checks()
    after = {str(p.relative_to(BASE)): sha256(p.read_bytes()).hexdigest() for p in reviewed}
    check(before == after, 'reviewed source changed during run')
    print(json.dumps({'status': 'PASS', 'python': platform.python_version(), 'optimization': sys.flags.optimize,
                      'oracle': 'explicit flat complete-policy enumeration and independently simulated leaf answers',
                      'seed': 17801798, 'counts': dict(sorted(COUNT.items())), 'sha256': after,
                      'limits': 'finite checks only; exact noiseless unit-cost questions; matching generated trees only; no general proof or psychological validation'},
                     ensure_ascii=False, indent=2))


if __name__ == '__main__': main()
