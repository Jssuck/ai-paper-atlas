"""Independent finite checks for explicitly modern I.19 teaching semantics.

No imports from the author model. Exhaustion is bounded; proofs are in the audit.
"""
from itertools import product
from pathlib import Path
import hashlib
import json
import platform
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def regions(term, universe):
    possible = frozenset().union(*term)
    necessary = frozenset(universe).intersection(*term)
    return possible, necessary, possible - necessary


def predicates(a, b, c, actual, universe):
    a0, b0, c0 = a[actual], b[actual], c[actual]
    ap, an, ac = regions(a, universe)
    bp, bn, bc = regions(b, universe)
    cp, cn, cc = regions(c, universe)
    return {
        'N_e_AB': not bool(b0 & ap),
        'N_o_AB': bool(b0 - ap),
        'N_e_BA': not bool(a0 & bp),
        'N_e_AC': not bool(c0 & ap),
        'N_a_AC': c0 <= an,
        'C_a_AC': c0 <= ac,
        'C_i_AC': bool(c0 & ac),
        'C_a_AB': b0 <= ac,
        'C_i_AB': bool(b0 & ac),
        'P_a_AC': c0 <= ap,
        'P_i_AC': bool(c0 & ap),
        'D_e_BC': not bool(c0 & b0),
        'D_o_BC': bool(c0 - b0),
        'D_o_CB': bool(b0 - c0),
        'P_e_BC': c0 <= (frozenset(universe) - bn),
        'P_o_BC': bool(c0 - bn),
        'N_e_BC': not bool(c0 & bp),
        'C_e_BC': c0 <= bc,
        'Box_e_AB': all(not (aw & bw) for aw, bw in zip(a, b)),
        'Box_a_AC': all(cw <= aw for aw, cw in zip(a, c)),
        'B_rigid': all(bw == b0 for bw in b),
        'B_no_new_members': all(bw <= b0 for bw in b),
    }


def independently_expand(a, b, c, actual, universe):
    """Quantifier implementation, separately checks the set identities used above."""
    return {
        'N_e_AB': all(all(x not in aw for aw in a) for x in b[actual]),
        'C_a_AC': all(any(x in aw for aw in a) and any(x not in aw for aw in a) for x in c[actual]),
        'C_i_AC': any(any(x in aw for aw in a) and any(x not in aw for aw in a) for x in c[actual]),
        'P_e_BC': all(any(x not in bw for bw in b) for x in c[actual]),
        'P_o_BC': any(any(x not in bw for bw in b) for x in c[actual]),
    }


def finite_checks():
    checked = 0
    antecedents = dict.fromkeys(['universal_positive_possible', 'particular_positive_possible',
                                'universal_contingent', 'particular_contingent',
                                'reverse_particular', 'necessary_affirmative_mismatch',
                                'box_with_rigid_B', 'conversion_with_no_new_B'], 0)
    for n in (0, 1, 2):
        u = frozenset(range(n))
        subsets = [frozenset(x for x in u if mask & (1 << x)) for mask in range(1 << n)]
        for worlds in (1, 2):
            for flat in product(subsets, repeat=3 * worlds):
                a, b, c = flat[:worlds], flat[worlds:2 * worlds], flat[2 * worlds:]
                for actual in range(worlds):
                    t = predicates(a, b, c, actual, u)
                    q = independently_expand(a, b, c, actual, u)
                    require(all(t[key] == val for key, val in q.items()), 'Set/quantifier disagreement')
                    tests = [
                        ('universal_positive_possible', t['N_e_AB'] and t['P_a_AC'], t['D_e_BC']),
                        ('particular_positive_possible', t['N_e_AB'] and t['P_i_AC'], t['D_o_BC']),
                        ('universal_contingent', t['N_e_AB'] and t['C_a_AC'], t['D_e_BC'] and t['P_e_BC']),
                        ('particular_contingent', t['N_e_AB'] and t['C_i_AC'], t['D_o_BC'] and t['P_o_BC']),
                        ('reverse_particular', t['N_e_AC'] and t['C_i_AB'], t['D_o_CB']),
                        ('necessary_affirmative_mismatch', t['N_a_AC'] and t['C_a_AB'], t['D_e_BC']),
                        ('box_with_rigid_B', t['Box_e_AB'] and t['B_rigid'] and t['C_a_AC'], t['D_e_BC']),
                        ('conversion_with_no_new_B', t['N_e_AB'] and t['B_no_new_members'], t['N_e_BA']),
                    ]
                    for name, premise, conclusion in tests:
                        if premise:
                            antecedents[name] += 1
                            require(conclusion, name + ' failed')
                    checked += 1
    require(all(antecedents.values()), 'An implication had no satisfying antecedent')
    return {'configurations': checked, 'set_quantifier_comparisons': checked * 5,
            'true_antecedent_counts': antecedents, 'implication_failures': 0,
            'bounds': {'domain_sizes': [0, 1, 2], 'world_counts': [1, 2], 'actual': 'every world'}}


def example(name, n, a, b, c, true_keys, false_keys):
    terms = tuple(tuple(frozenset(s) for s in term) for term in (a, b, c))
    t = predicates(*terms, 0, frozenset(range(n)))
    for key in true_keys:
        require(t[key], name + ': expected true ' + key)
    for key in false_keys:
        require(not t[key], name + ': expected false ' + key)
    return {'name': name, 'domain': list(range(n)), 'actual': 0,
            'A': a, 'B': b, 'C': c, 'required_true': true_keys, 'required_false': false_keys,
            'truth': t}


def article_examples():
    return [
        example('article_5_3', 2, [[], [1]], [[0], [0]], [[1], [1]],
                ['N_e_AB', 'C_a_AC', 'D_e_BC', 'N_e_BC'], ['C_e_BC']),
        example('article_6_1_three_worlds', 2, [[], [1], []], [[0], [0], [0, 1]], [[1], [1], [1]],
                ['N_e_AB', 'C_a_AC', 'D_e_BC', 'N_e_BA', 'Box_e_AB'], ['N_e_BC']),
        example('article_6_1_nonempty_extension', 3, [[2], [1, 2], [2]], [[0], [0], [0, 1]], [[1], [1], [1]],
                ['N_e_AB', 'C_a_AC', 'D_e_BC', 'N_e_BA', 'Box_e_AB'], ['N_e_BC']),
        example('article_6_2', 2, [[0], [0]], [[1], [0, 1]], [[0], [0]],
                ['N_e_AB'], ['N_e_BA']),
        example('article_6_3', 2, [[], [0]], [[0, 1], [0, 1]], [[1], [1]],
                ['N_e_AC', 'C_i_AB', 'D_o_CB'], ['D_o_BC']),
        example('article_7_3_awake', 2, [[0], [1]], [[0, 1], [0, 1]], [[0], [1]],
                ['Box_a_AC', 'C_a_AB'], ['N_a_AC', 'D_e_BC']),
        example('article_7_3_box_negative', 1, [[], [0]], [[0], []], [[0], [0]],
                ['Box_e_AB', 'C_a_AC'], ['D_e_BC']),
        example('article_8_1_two_witnesses', 2, [[], [1]], [[0, 1], [0, 1]], [[1], [1]],
                ['N_o_AB', 'C_i_AC'], ['D_o_BC']),
    ]


def examples():
    return [
        example('no_necessary_conclusion_and_no_automatic_conversion', 2,
                [[0], []], [[1], [0, 1]], [[0], [0]],
                ['N_e_AB', 'C_a_AC', 'D_e_BC', 'P_e_BC'], ['N_e_BC', 'N_e_BA']),
        example('no_strong_contingent_conclusion', 2,
                [[0], []], [[1], [1]], [[0], [0]],
                ['N_e_AB', 'C_a_AC', 'D_e_BC', 'N_e_BC'], ['C_e_BC']),
        example('reverse_particular_not_convertible', 2,
                [[0], []], [[0, 1], [0, 1]], [[1], [1]],
                ['N_e_AC', 'C_i_AB', 'D_o_CB'], ['D_o_BC']),
        example('worldwise_negative_is_not_anchored_negative', 1,
                [[], [0]], [[0], []], [[0], [0]],
                ['Box_e_AB', 'C_a_AC'], ['N_e_AB', 'D_e_BC']),
        example('awake_can_change_extension_with_nonempty_subjects', 2,
                [[0], [1]], [[0, 1], [0, 1]], [[0], [1]],
                ['Box_a_AC', 'C_a_AB'], ['N_a_AC', 'D_e_BC']),
        example('empty_subject_universal_not_particular', 1,
                [[0], []], [[], []], [[], []],
                ['N_e_AB', 'C_a_AC', 'D_e_BC'], ['C_i_AC', 'D_o_BC']),
    ]


if __name__ == '__main__':
    result = {
        'scope': 'Independent bounded checks of modern definitions, not a proof of all models or ancient semantics.',
        'python': platform.python_version(), 'implementation': platform.python_implementation(),
        'optimization': sys.flags.optimize,
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'finite': finite_checks(), 'examples': examples(), 'article_examples': article_examples(),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
