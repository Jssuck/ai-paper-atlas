"""Finite positive Horn teaching model; no claim of scientific-genus discovery."""
from itertools import combinations, product
import json


def subsets(items):
    items = tuple(sorted(items))
    return [frozenset(c) for n in range(len(items)+1) for c in combinations(items,n)]


def normalize(rules):
    result = []
    for body, head in rules:
        body = frozenset(body)
        if not body:
            raise ValueError('empty bodies excluded: declare initial facts explicitly')
        if not isinstance(head,str) or any(not isinstance(x,str) for x in body):
            raise ValueError('atoms must be strings')
        result.append((body,head))
    return tuple(sorted(set(result),key=lambda r:(r[1],tuple(sorted(r[0])))))


def derive(seeds,rules):
    """Return least closure and an ordered certificate (body,head) per new atom."""
    rules = normalize(rules)
    known = set(seeds)
    certificate = []
    changed = True
    while changed:
        changed = False
        for body,head in rules:
            if body <= known and head not in known:
                known.add(head)
                certificate.append((body,head))
                changed = True
    return frozenset(known),tuple(certificate)


def check_certificate(seeds,rules,certificate,target):
    allowed = set(normalize(rules))
    known = set(seeds)
    for body,head in certificate:
        step = (frozenset(body),head)
        if step not in allowed or not step[0] <= known or head in known:
            return False
        known.add(head)
    return target in known


def typed_rules(rules,genus,bridges=()):
    """Require a declared type for every atom; exact cross-type rules need a bridge."""
    rules = normalize(rules)
    bridges = set(normalize(bridges))
    accepted,rejected = [],[]
    for body,head in rules:
        atoms = body | {head}
        if not atoms <= genus.keys():
            rejected.append((body,head))
        elif len({genus[a] for a in atoms}) == 1 or (body,head) in bridges:
            accepted.append((body,head))
        else:
            rejected.append((body,head))
    return tuple(accepted),tuple(rejected)


def minimal_supports(target,roots,rules):
    """All inclusion-minimal sufficient subsets of the declared root facts."""
    found = []
    for s in subsets(roots):
        if any(old <= s for old in found):
            continue
        if target in derive(s,rules)[0]:
            found.append(s)
    return tuple(found)


def shares_root(a,b):
    return bool(set(a)&set(b))


def examples():
    rules = [(('p',),'u'),(('q',),'v'),(('u','v'),'w')]
    closure,cert = derive({'p','q'},rules)
    genus = {'p':'N','u':'N','q':'G','v':'G','w':'G'}
    good,bad = typed_rules(rules,genus)
    bridged,_ = typed_rules(rules,genus,[(('u','v'),'w')])
    return {
      'roots':['p','q'], 'closure':sorted(closure),
      'certificate':[{'body':sorted(b),'head':h} for b,h in cert],
      'certificate_valid':check_certificate({'p','q'},rules,cert,'w'),
      'w_minimal_supports':[sorted(s) for s in minimal_supports('w',{'p','q'},rules)],
      'without_bridge_w': 'w' in derive({'p','q'},good)[0],
      'with_declared_bridge_w':'w' in derive({'p','q'},bridged)[0],
      'rejected_rules':[{'body':sorted(b),'head':h} for b,h in bad],
      'shared_generic_rule_does_not_supply_roots':sorted(derive(set(),rules)[0]),
      'same_label_without_rule': 'b' in derive({'a'},[])[0],
      'shared_roots_nontransitive': {'AB':shares_root({'p'},{'p','q'}),'BC':shares_root({'p','q'},{'q'}),'AC':shares_root({'p'},{'q'})},
      'missing_bridge_status':'not derivable in the declared finite rule set; not an impossibility claim about science'
    }


def exhaustive():
    atoms = frozenset('pqr')
    candidates = [(b,h) for h in sorted(atoms) for b in subsets(atoms-{h}) if b]
    counts = dict(rule_sets=0,seed_cases=0,certificate_checks=0,monotonicity_checks=0,
                  closure_idempotence_failures=0,certificate_failures=0,monotonicity_failures=0,
                  support_soundness_failures=0,support_minimality_failures=0)
    for flags in product((False,True), repeat=len(candidates)):
        rules = [r for r,f in zip(candidates,flags) if f]
        counts['rule_sets'] += 1
        closures = {}
        for seeds in subsets(atoms):
            counts['seed_cases'] += 1
            closed,cert = derive(seeds,rules)
            closures[seeds] = closed
            counts['closure_idempotence_failures'] += derive(closed,rules)[0] != closed
            for target in closed:
                counts['certificate_checks'] += 1
                counts['certificate_failures'] += not check_certificate(seeds,rules,cert,target)
            for target in atoms:
                for support in minimal_supports(target,seeds,rules):
                    counts['support_soundness_failures'] += target not in derive(support,rules)[0]
                    counts['support_minimality_failures'] += any(target in derive(support-{a},rules)[0] for a in support)
        for a in subsets(atoms):
            for b in subsets(atoms):
                if a <= b:
                    counts['monotonicity_checks'] += 1
                    counts['monotonicity_failures'] += not closures[a] <= closures[b]
    return counts


if __name__ == '__main__':
    print(json.dumps({'model':'finite positive nonempty-body Horn rules, explicit declared types',
                      'examples':examples(),'exhaustive':exhaustive()},ensure_ascii=False,indent=2))
