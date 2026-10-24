"""Finite teaching diagnostics for Posterior Analytics I.5, not epistemic certification."""
from fractions import Fraction
from itertools import product
import json


def checked_mask(mask, size):
    if type(size) is not int or size < 0:
        raise ValueError('size must be a nonnegative integer')
    if type(mask) is not int or not 0 <= mask < (1 << size):
        raise ValueError('mask outside finite universe')
    return mask


def coverage_report(target, property_mask, parts, size):
    """Separate extensional coverage from truth. Never reports explanatory knowledge."""
    checked_mask(target, size)
    checked_mask(property_mask, size)
    parts = tuple(checked_mask(p, size) for p in parts)
    union = 0
    for part in parts:
        union |= part
    missing = target & ~union
    failures = union & ~property_mask
    return {'covered': missing == 0, 'all_parts_sound': failures == 0,
            'target_true': target & ~property_mask == 0,
            'missing_mask': missing, 'part_counterexamples_mask': failures,
            'outside_target_mask': union & ~target,
            'target_counterexamples_mask': target & ~property_mask,
            'extensional_certificate': missing == 0 and failures == 0}


def available_routes(routes, retained):
    """Check externally declared sufficient support sets; does not validate any proof."""
    retained = frozenset(retained)
    routes = tuple(frozenset(route) for route in routes)
    return tuple(i for i, required in enumerate(routes) if required <= retained)


def extensional_candidates(classes, property_mask, size):
    """All named classes whose listed members satisfy P, including empty classes."""
    checked_mask(property_mask, size)
    return tuple(name for name, mask in classes.items()
                 if checked_mask(mask, size) & ~property_mask == 0)


def alternation(a, b, c, d):
    """Restricted positive rational illustration, not ancient general magnitude theory."""
    values = (a, b, c, d)
    if any(not isinstance(x, (int, Fraction)) or isinstance(x, bool) or x <= 0
           for x in values):
        raise ValueError('four positive integers or Fractions required')
    a, b, c, d = map(Fraction, values)
    return {'premise': a / b == c / d, 'conclusion': a / c == b / d}


def enumerate_models():
    counts = {'coverage_cases': 0, 'coverage_certificates': 0,
              'coverage_oracle_mismatches': 0, 'coverage_implication_failures': 0,
              'support_cases': 0, 'support_oracle_mismatches': 0,
              'ratio_cases': 0, 'ratio_premises_true': 0,
              'ratio_implication_failures': 0}
    size = 3
    for t, p, a, b in product(range(8), repeat=4):
        r = coverage_report(t, p, (a, b), size)
        ts = {i for i in range(size) if t >> i & 1}
        ps = {i for i in range(size) if p >> i & 1}
        ab = {i for i in range(size) if a >> i & 1 or b >> i & 1}
        expected = {'covered': ts <= ab, 'all_parts_sound': ab <= ps,
                    'target_true': ts <= ps,
                    'extensional_certificate': ts <= ab and ab <= ps}
        counts['coverage_cases'] += 1
        counts['coverage_oracle_mismatches'] += int(any(r[k] != v for k, v in expected.items()))
        counts['coverage_certificates'] += int(r['extensional_certificate'])
        counts['coverage_implication_failures'] += int(r['extensional_certificate'] and not r['target_true'])
    features = ('triangle', 'isosceles', 'bronze')
    for req, kept in product(range(8), repeat=2):
        route = [features[i] for i in range(3) if req >> i & 1]
        retained = [features[i] for i in range(3) if kept >> i & 1]
        got = bool(available_routes((route,), retained))
        expected = all(not (req >> i & 1) or bool(kept >> i & 1) for i in range(3))
        counts['support_cases'] += 1
        counts['support_oracle_mismatches'] += int(got != expected)
    for a, b, c, d in product(range(1, 7), repeat=4):
        r = alternation(a, b, c, d)
        counts['ratio_cases'] += 1
        counts['ratio_premises_true'] += int(r['premise'])
        counts['ratio_implication_failures'] += int(r['premise'] and not r['conclusion'])
    return counts


if __name__ == '__main__':
    result = enumerate_models()
    print(json.dumps(result, indent=2, sort_keys=True))
    if any(result[k] for k in ('coverage_oracle_mismatches', 'coverage_implication_failures',
                              'support_oracle_mismatches', 'ratio_implication_failures')):
        raise SystemExit(1)
