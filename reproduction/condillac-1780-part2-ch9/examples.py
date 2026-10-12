"""Deterministic worked examples. All names are deliberately schematic."""
import json
from fractions import Fraction
from model import consistent, certain, expected_ambiguity, minimal_separating, posterior, structural_certainty


def results():
    h = ('both', 'alternate', 'neither')
    cause = dict(zip(h, (True, False, False)))
    effect = dict(zip(h, (True, True, False)))
    observed = consistent(h, {'effect': effect}, [('effect', True)])
    planets = ('similar_inhabited', 'similar_empty', 'different_empty')
    similarity = dict(zip(planets, (True, True, False)))
    inhabited = dict(zip(planets, (True, False, False)))
    matched = consistent(planets, {'similar': similarity}, [('similar', True)])
    gold = ('observed_sample_only', 'same_sample_new_property')
    tests = {'malleable': dict.fromkeys(gold, True)}
    gold_s = consistent(gold, tests, [('malleable', True)])
    worlds = ('00', '01', '10', '11')
    experiments = {
        'first_bit': {w: w[0] for w in worlds},
        'second_bit': {w: w[1] for w in worlds},
        'rare_11': {w: w == '11' for w in worlds},
    }
    b = ('target', 'alternative')
    q = {'target': True, 'alternative': False}
    likelihood = dict.fromkeys(b, Fraction(1, 2))
    p = posterior(b, {'target': 1, 'alternative': 0}, likelihood)
    return {
        'cause_implies_effect': certain(h, {w: not cause[w] or effect[w] for w in h}),
        'effect_observed_candidates': list(observed),
        'effect_implies_cause': certain(observed, {w: cause[w] for w in observed}),
        'similarity_candidates': list(matched),
        'similarity_guarantees_inhabitants': certain(matched, {w: inhabited[w] for w in matched}),
        'gold_malleability_observed': certain(gold_s, {w: True for w in gold_s}),
        'gold_unobserved_property_certain': certain(gold_s, dict(zip(gold_s, (False, True)))),
        'contradictory_observations': list(consistent(h, {'effect': effect}, [('effect', True), ('effect', False)])),
        'empty_state_certain': certain((), {}),
        'expected_survivors': {t: str(expected_ambiguity(worlds, table)) for t, table in experiments.items()},
        'minimal_separating_tests': list(minimal_separating(worlds, experiments)),
        'zero_prior_posterior': {w: str(v) for w, v in p.items()},
        'zero_prior_structural_certainty': structural_certainty(b, likelihood, q),
        'positive_prior_posterior': {w: str(v) for w, v in posterior(b, {'target': 1, 'alternative': 1}, {'target': Fraction(3,4), 'alternative': Fraction(1,4)}).items()},
        'zero_likelihood_structural_certainty': structural_certainty(b, {'target': 1, 'alternative': 0}, q),
    }

if __name__ == '__main__':
    print(json.dumps(results(), ensure_ascii=False, indent=2, sort_keys=True))
