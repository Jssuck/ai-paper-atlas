"""Independent Boolean-model oracle; expected answers never use derive/normalize.
Run: python independent_oracle.py > independent-results.json
Only the explicitly stated three-atom finite syntax is exhaustively checked.
"""
from itertools import combinations, product
import hashlib
import json
from pathlib import Path
import model

ATOMS = ('p', 'q', 'r')
SETS = tuple(frozenset(a for i, a in enumerate(ATOMS) if mask & (1 << i))
             for mask in range(8))
RULES = tuple((body, head) for head in ATOMS for body in SETS
              if body and head not in body)

def models(seeds, rules):
    return tuple(v for v in SETS if seeds <= v and
                 all(not body <= v or head in v for body, head in rules))

def consequence(seeds, rules):
    satisfying = models(seeds, rules)
    if not satisfying:
        raise RuntimeError('Positive rules must admit all-true assignment')
    return frozenset(a for a in ATOMS if all(a in v for v in satisfying))

def certificate_expected(seeds, rules, certificate, target):
    known = set(seeds)
    for body, head in certificate:
        if (frozenset(body), head) not in rules or not set(body) <= known or head in known:
            return False
        known.add(head)
    return target in known

def run():
    counts = dict(rule_sets=0, closure_cases=0, support_cases=0,
                  certificate_cases=0, typed_cases=0, boundary_checks=0)
    failures = []
    def check(ok, label):
        if not ok:
            failures.append(label)
    for mask in range(1 << len(RULES)):
        rules = tuple(r for i, r in enumerate(RULES) if mask & (1 << i))
        counts['rule_sets'] += 1
        expected = {s: consequence(s, rules) for s in SETS}
        for seeds in SETS:
            actual, cert = model.derive(seeds, rules)
            counts['closure_cases'] += 1
            check(actual == expected[seeds], f'closure:{mask}:{sorted(seeds)}')
            for target in ATOMS:
                candidates = [s for s in SETS if s <= seeds and target in expected[s]]
                supports = frozenset(s for s in candidates if not any(t < s for t in candidates))
                check(frozenset(model.minimal_supports(target, seeds, rules)) == supports,
                      f'support:{mask}:{sorted(seeds)}:{target}')
                counts['support_cases'] += 1
                # Valid, reordered, duplicated and foreign-rule certificates.
                for c in (cert, tuple(reversed(cert)), cert + cert,
                          cert + ((frozenset({'foreign'}), target),)):
                    want = certificate_expected(seeds, rules, c, target)
                    check(model.check_certificate(seeds, rules, c, target) == want,
                          f'certificate:{mask}:{sorted(seeds)}:{target}')
                    counts['certificate_cases'] += 1
                check(certificate_expected(seeds, rules, cert, target) == (target in expected[seeds]),
                      f'generated_certificate:{mask}:{sorted(seeds)}:{target}')
        # Every partial two-label assignment (missing/N/G) and three bridge policies.
        for labels in product((None, 'N', 'G'), repeat=3):
            genus = {a: t for a, t in zip(ATOMS, labels) if t is not None}
            for bridges in ((), rules, rules[::2]):
                wanted = set()
                for body, head in rules:
                    members = body | {head}
                    if all(a in genus for a in members):
                        if all(genus[a] == genus[head] for a in body) or (body, head) in bridges:
                            wanted.add((body, head))
                good, bad = model.typed_rules(rules, genus, bridges)
                check(set(good) == wanted and set(bad) == set(rules) - wanted,
                      f'types:{mask}:{labels}:{len(bridges)}')
                counts['typed_cases'] += 1
    # Additional legal reflexive heads, outside the nine-rule exhaustive family.
    for body in (frozenset({'p'}), frozenset({'p','q'})):
        rules = ((body, 'p'), (frozenset({'p'}), 'r'))
        for s in SETS:
            check(model.derive(s,rules)[0] == consequence(s,rules), 'reflexive_boundary')
            counts['boundary_checks'] += 1
    try:
        model.derive(set(), [((), 'p')])
        check(False, 'empty_body_not_rejected')
    except ValueError:
        pass
    counts['boundary_checks'] += 1
    # Both truth values of t remain possible when not entailed, not universally false.
    vals = models(frozenset({'p'}), ((frozenset({'p'}), 'q'),))
    check(any('r' in v for v in vals) and any('r' not in v for v in vals), 'nonentailment')
    counts['boundary_checks'] += 1
    roots = (frozenset({'p'}), frozenset({'p','q'}), frozenset({'q'}))
    check(model.shares_root(roots[0],roots[1]) and model.shares_root(roots[1],roots[2])
          and not model.shares_root(roots[0],roots[2]), 'nontransitive')
    counts['boundary_checks'] += 1
    # Inclusion-minimal supports may have different cardinalities.
    mixed = ((frozenset({'p'}), 'r'), (frozenset({'q','s'}), 'r'))
    check(set(model.minimal_supports('r', {'p','q','s'}, mixed)) ==
          {frozenset({'p'}), frozenset({'q','s'})}, 'inclusion_not_cardinality')
    counts['boundary_checks'] += 1
    return {'method':'Boolean satisfying valuations and their intersection; no derive in expected computation',
            'scope':'3 atoms, 9 nonempty-body rules excluding reflexive heads; additional stated boundary tests',
            'counts':counts, 'failure_count':len(failures), 'failures':failures,
            'model_sha256':hashlib.sha256(Path('model.py').read_bytes()).hexdigest()}

if __name__ == '__main__':
    result = run()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result['failure_count']:
        raise SystemExit(1)
