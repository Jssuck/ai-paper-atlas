"""Independent bounded oracle for the II.VIII teaching model.

Expected answers use integer bit masks and partition refinement. Optimal depth is
found by breadth-wise closure of bounded-depth decision-tree existence, not the
model's recursive minimax implementation. No author tests are imported, and no
checks rely on Python assert statements.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import json
import platform
import sys

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))
import condillac_model as m

COUNTS = Counter()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def expect_error(function, errors=(TypeError, ValueError, KeyError)):
    try:
        function()
    except errors:
        COUNTS['rejected_inputs'] += 1
        return
    raise RuntimeError('expected rejection was not raised')


def partitions(n):
    """Each set partition once, as its first-occurrence integer labelling."""
    if n == 0:
        return [()]
    rows = [(0,)]
    while len(rows[0]) < n:
        rows = [row + (value,) for row in rows
                for value in range(max(row) + 2)]
    return rows


def indices(mask, n):
    return tuple(i for i in range(n) if mask & (1 << i))


def blocks(values):
    result = {}
    for i, value in enumerate(values):
        result[value] = result.get(value, 0) | (1 << i)
    return tuple(result.values())


def depths_by_bounded_existence(target, questions):
    """Minimal height at which a valid answer tree exists for every nonempty set.

    R[0] contains exactly target-homogeneous sets. R[d+1] additionally contains
    sets having a question all of whose nonempty intersections lie in R[d].
    Taking a snapshot each round prevents within-round recursive minimization.
    """
    n = len(target)
    all_masks = range(1, 1 << n)
    target_blocks = blocks(target)
    question_blocks = [blocks(q) for q in questions]
    result = {mask: 0 for mask in all_masks
              if any(mask & block == mask for block in target_blocks)}
    for height in range(1, n):
        previous = set(result)
        additions = []
        for mask in all_masks:
            if mask in result:
                continue
            for cells in question_blocks:
                if all((mask & cell) in previous
                       for cell in cells if mask & cell):
                    additions.append(mask)
                    break
        for mask in additions:
            result[mask] = height
    return result


def expected_pairwise(target, questions, mask):
    members = indices(mask, len(target))
    return all(target[a] == target[b] or any(q[a] != q[b] for q in questions)
               for a, b in combinations(members, 2))


def make_problem(u, target, mask):
    return m.Problem(u, m.Table(u, 'target', target),
                     (m.Constraint(u, 'given', tuple(bool(mask & (1 << i))
                                                    for i in range(len(target)))),))


def validate_tree(node, mask, target, questions, depths):
    n = len(target)
    require(node.candidates == indices(mask, n), 'tree candidate set changed')
    expected = depths.get(mask)
    require(node.depth == expected, 'tree height differs from independent oracle')
    if mask == 0:
        require(node.status == 'inconsistent', 'empty set was treated as solved')
        return
    if expected is None:
        require(node.status == 'impossible', 'inseparable pair not reported')
        require(node.witness is not None, 'missing impossibility witness')
        a, b = node.witness
        require(a in indices(mask, n) and b in indices(mask, n), 'witness outside candidates')
        require(target[a] != target[b] and all(q[a] == q[b] for q in questions),
                'impossibility witness is invalid')
        return
    if expected == 0:
        require(node.status == 'identified', 'homogeneous target not solved')
        require(all(node.answer == target[i] for i in indices(mask, n)), 'leaf answer wrong')
        return
    require(node.status == 'measurement', 'positive finite depth needs a measurement')
    valid_roots = []
    for j, q in enumerate(questions):
        cells = [mask & cell for cell in blocks(q) if mask & cell]
        if all(cell in depths for cell in cells) and 1 + max(depths[cell] for cell in cells) == expected:
            valid_roots.append(j)
    require(node.question_index == min(valid_roots), 'wrong earliest optimal-question tie break')
    q = questions[node.question_index]
    expected_branches = {}
    for i in indices(mask, n):
        expected_branches[q[i]] = expected_branches.get(q[i], 0) | (1 << i)
    require(len(node.branches) == len(expected_branches), 'wrong branch count')
    seen = set()
    for value, child in node.branches:
        require(value in expected_branches and value not in seen, 'extra or duplicate branch')
        seen.add(value)
        validate_tree(child, expected_branches[value], target, questions, depths)


def check_decision_family(u, target, questions, masks, category):
    depths = depths_by_bounded_existence(target, questions)
    tables = tuple(m.Table(u, f'q{j}', q) for j, q in enumerate(questions))
    for mask in masks:
        p = make_problem(u, target, mask)
        node = m.minimax_tree(p, tables)
        validate_tree(node, mask, target, questions, depths)
        require((mask in depths) == expected_pairwise(target, questions, mask),
                'bounded-tree and pairwise criteria disagree')
        if mask in depths:
            for i in indices(mask, len(target)):
                answer, path = m.follow_tree(p, tables, node, i)
                require(answer == target[i] and len(path) <= depths[mask], 'replay incorrect')
                COUNTS['world_replays'] += 1
        COUNTS[category] += 1


def exhaustive_decisions():
    for n in range(1, 5):
        u = m.Universe(('world',), tuple((i,) for i in range(n)))
        masks = range(1, 1 << n)
        # Both labels describe the same binary partition, so first label is 0.
        binary = [(0,) + tail for tail in product((0, 1), repeat=n - 1)]
        for target in partitions(n):
            for family_bits in range(1 << len(binary)):
                qs = tuple(q for j, q in enumerate(binary) if family_bits & (1 << j))
                check_decision_family(u, target, qs, masks, 'binary_family_problem_cases')
        # Every pair of arbitrary finite-answer partitions, plus empty/singleton families.
        arbitrary = partitions(n)
        for target in arbitrary:
            for size in range(3):
                for qs in combinations(arbitrary, size):
                    check_decision_family(u, target, qs, masks, 'multivalued_family_problem_cases')


def exhaustive_semantics():
    for n in range(0, 5):
        u = m.Universe(('world',), tuple((i,) for i in range(n)))
        for target in partitions(n):
            ps = [make_problem(u, target, mask) for mask in range(1 << n)]
            for mask, p in enumerate(ps):
                a = m.analyze(p)
                members = indices(mask, n)
                expected_answers = set(target[i] for i in members)
                expected_status = ('inconsistent' if mask == 0 else
                                   'identified' if len(expected_answers) == 1 else 'underdetermined')
                require(a.candidates == members and set(a.answers) == expected_answers and a.status == expected_status,
                        'analysis classification mismatch')
                if a.status == 'identified':
                    require(a.answer in expected_answers, 'unique answer mismatch')
                else:
                    expect_error(lambda a=a: a.answer)
                COUNTS['analysis_cases'] += 1
                for encoding in partitions(n):
                    c = m.compression(p, m.Table(u, 'code', encoding))
                    bad_pairs = [(i, j) for i, j in combinations(members, 2)
                                 if encoding[i] == encoding[j] and target[i] != target[j]]
                    require(c.sufficient == (not bad_pairs) and c.vacuous == (mask == 0),
                            'fiber criterion mismatch')
                    if bad_pairs:
                        require(c.witness in bad_pairs, 'wrong compression witness')
                        expect_error(lambda c=c: c.decode(0))
                    else:
                        for i in members:
                            require(c.decode(encoding[i]) == target[i], 'decoder mismatch')
                    COUNTS['compression_cases'] += 1
            for left, right in product(range(1 << n), repeat=2):
                report = m.compare_rewrite(ps[left], ps[right])
                la = {target[i] for i in indices(left, n)}
                ra = {target[i] for i in indices(right, n)}
                require(report.worlds_preserved == (left == right), 'world preservation mismatch')
                require(report.answers_preserved == (la == ra), 'answer preservation mismatch')
                require(report.nonvacuous == bool(left and right), 'nonvacuity mismatch')
                require(report.lost_worlds == indices(left & ~right, n), 'wrong lost-world witness')
                require(report.gained_worlds == indices(right & ~left, n), 'wrong gained-world witness')
                COUNTS['rewrite_cases'] += 1


def reexpression_and_named_examples():
    # A deterministic second encoding can merge old cells, never split them.
    for n in range(1, 5):
        u = m.Universe(('world',), tuple((i,) for i in range(n)))
        for target in partitions(n):
            for mask in range(1 << n):
                p = make_problem(u, target, mask)
                for code in partitions(n):
                    original = m.compression(p, m.Table(u, 'r', code))
                    for merge in partitions(max(code) + 1):
                        recoded = tuple(merge[value] for value in code)
                        after = m.compression(p, m.Table(u, 'h(r)', recoded))
                        require(not after.sufficient or original.sufficient,
                                'deterministic re-expression created identifiability')
                        COUNTS['deterministic_reexpression_cases'] += 1
    # Independent expected examples, including the selector's larger eight-world domain.
    import examples
    for bound in range(1, 13):
        chain = examples.chips(bound)
        for p in chain[:4]:
            actual = {p.universe.worlds[i] for i in m.candidates(p)}
            require(actual == ({(7, 5)} if bound >= 7 else set()), 'chip chain wrong')
            COUNTS['chip_bounded_system_cases'] += 1
        p = chain[4]
        actual = {p.universe.worlds[i] for i in m.candidates(p)}
        require(actual == {(y + 2, y) for y in range(1, bound - 1)}, 'incomplete chip data wrong')
    p, qs = examples.selector()
    raw_target = tuple(a if s == 0 else b for s, a, b in p.universe.worlds)
    require(p.target.values == raw_target, 'selector target is mistranscribed')
    raw_qs = tuple(tuple(w[j] for w in p.universe.worlds) for j in range(3))
    require(tuple(q.values for q in qs) == raw_qs, 'selector observations wrong')
    for family_bits in range(8):
        family = tuple(q for j, q in enumerate(raw_qs) if family_bits & (1 << j))
        check_decision_family(p.universe, raw_target, family, range(1, 256),
                              'selector_subproblem_cases')
    require(depths_by_bounded_existence(raw_target, raw_qs)[255] == 2,
            'selector depth must equal two')
    for j, k in combinations(range(3), 2):
        require(any(raw_target[a] != raw_target[b]
                    and raw_qs[j][a] == raw_qs[j][b] and raw_qs[k][a] == raw_qs[k][b]
                    for a, b in combinations(range(8), 2)), 'fixed pair unexpectedly identifies target')
    # Two explicit structures with identical observations but different S->F roles.
    def direct(u, intervention=None):
        sensation = u if intervention is None else intervention
        return sensation, sensation  # S=U, F=S
    def common(u, intervention=None):
        sensation = u if intervention is None else intervention
        return sensation, u  # S=U, F=U
    observations_direct = {direct(u) for u in (0, 1)}
    observations_common = {common(u) for u in (0, 1)}
    require(observations_direct == observations_common, 'causal observation mismatch')
    # An externally fixed S changes the first defining equation in each toy model.
    require(direct(1, 0) == (0, 0) and common(1, 0) == (0, 1),
            'different dependence roles were not represented by the equations')
    # All twelve outcomes of the main text's forward/reverse structures, given
    # as a literal table independently of the author's control flow.
    expected_causal = {
        ('M1', 0, None): (0, 0), ('M1', 1, None): (1, 1),
        ('M1', 0, 0): (0, 0), ('M1', 0, 1): (1, 1),
        ('M1', 1, 0): (0, 0), ('M1', 1, 1): (1, 1),
        ('M2', 0, None): (0, 0), ('M2', 1, None): (1, 1),
        ('M2', 0, 0): (0, 0), ('M2', 0, 1): (1, 0),
        ('M2', 1, 0): (0, 1), ('M2', 1, 1): (1, 1),
    }
    for args, outcome in expected_causal.items():
        require(examples.causal_run(*args) == outcome, 'structural-model execution mismatch')
        COUNTS['causal_execution_cases'] += 1
    for args in (('M3', 0), ('M1', True), ('M1', 2), ('M2', 0, True),
                 ('M2', 0, 0.0), ('M1', 0, 2)):
        expect_error(lambda args=args: examples.causal_run(*args))
    p, qs = examples.causal_toy()
    require(p.target.values == ('M1', 'M2'), 'causal toy model labels differ from main text')
    require(qs[0].values == (((0, 0), (1, 1)), ((0, 0), (1, 1))),
            'causal observation must be the two natural outcomes for each mechanism')
    require(m.minimax_tree(p, qs).status == 'impossible', 'co-presence cannot select an origin')
    COUNTS['named_argument_examples'] += 3


def edge_contracts():
    empty = m.Universe(('world',), ())
    p = m.Problem(empty, m.Table(empty, 'target', ()))
    require(m.minimax_tree(p, ()).status == 'inconsistent', 'empty universe not inconsistent')
    u = m.Universe(('world',), ((0,), (1,), (2,)))
    p = m.Problem(u, m.Table(u, 'nested', (('a', (1,)), ('a', (1,)), ('b', (2,)))))
    q = m.Table(u, 'nested code', (('x', (0,)), ('x', (0,)), ('y', (1,))))
    tree = m.minimax_tree(p, (q,))
    require(tree.depth == 1 and m.compression(p, q).sufficient, 'nested values failed')
    for i in range(3):
        require(m.follow_tree(p, (q,), tree, i)[0] == p.target.values[i], 'nested replay failed')
    called = []
    def sample(w):
        called.append(w)
        return w[0] % 2
    sampled = m.table(u, 'sampled', sample)
    require(called == list(u.worlds), 'callback must be sampled exactly once per world')
    for _ in range(3):
        m.minimax_tree(p, (sampled,))
    require(called == list(u.worlds), 'callback was re-executed during analysis')
    wrong_u = m.Universe(('world',), ((3,), (4,), (5,)))
    for fn in (
        lambda: m.Universe(('world',), ((True,),)),
        lambda: m.Universe(('world',), ((1,), (1,))),
        lambda: m.Universe(('world', 'world'), ((1, 2),)),
        lambda: m.Table(u, 'bad', (0, 1)),
        lambda: m.Table(u, 'bad', (0, True, 1)),
        lambda: m.Table(u, 'bad', (0, ('a', False), 1)),
        lambda: m.Constraint(u, 'bad', (1, 0, 1)),
        lambda: m.Problem(u, m.Table(wrong_u, 'target', (1, 2, 3))),
        lambda: m.minimax_tree(p, [q]),
        lambda: m.minimax_tree(p, (q, q)),
        lambda: m.follow_tree(p, (q,), tree, True),
        lambda: m.follow_tree(p, (q,), tree, 4),
        lambda: m.compression(p, q).decode('unknown'),
        lambda: m.translation_chain((p,)),
        lambda: m.translation_chain((p, p), preservation='consequence'),
    ):
        expect_error(fn)
    COUNTS['explicit_edge_groups'] += 4


def digest(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': sha256(data).hexdigest()}


def main():
    files = {'condillac_model.py': BASE / 'condillac_model.py', 'examples.py': BASE / 'examples.py', Path(__file__).name: Path(__file__)}
    before = {name: digest(path) for name, path in files.items()}
    exhaustive_semantics()
    exhaustive_decisions()
    reexpression_and_named_examples()
    edge_contracts()
    after = {name: digest(path) for name, path in files.items()}
    require(before == after, 'audited file changed while checks were running')
    print(json.dumps({'status': 'PASS', 'python': platform.python_version(),
                      'optimization': sys.flags.optimize, 'counts': dict(sorted(COUNTS.items())),
                      'fingerprints': after,
                      'oracle': 'bitmask partitions and iterative bounded-depth tree-existence closure',
                      'scope': 'all candidate subsets; all target partitions on at most four labelled worlds; all families of binary partitions and every at-most-two family of arbitrary finite-answer partitions; not an unbounded proof'},
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
