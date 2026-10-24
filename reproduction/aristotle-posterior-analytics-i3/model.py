"""Original finite teaching model, not Aristotle's text or a theory of knowledge."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Rule:
    premises: frozenset[str]
    conclusion: str


def validate(atoms, seeds, rules):
    atoms, seeds, rules = frozenset(atoms), frozenset(seeds), tuple(rules)
    if not atoms or any(not isinstance(x, str) or not x for x in atoms):
        raise ValueError('atoms must be nonempty strings in a nonempty vocabulary')
    if not seeds <= atoms:
        raise ValueError('unknown seed')
    for r in rules:
        if not isinstance(r, Rule) or not r.premises or not r.premises <= atoms or r.conclusion not in atoms:
            raise ValueError('rules require nonempty known premises and a known conclusion')
    return atoms, seeds, rules


def closure(atoms, seeds, rules):
    """Synchronous least fixed point; rank is derivation round, not certainty."""
    atoms, seeds, rules = validate(atoms, seeds, rules)
    reached = set(seeds)
    ranks = {x: 0 for x in seeds}
    witnesses = {}
    level = 0
    while True:
        added = {}
        for i, r in enumerate(rules):
            if r.premises <= reached and r.conclusion not in reached:
                added.setdefault(r.conclusion, i)
        if not added:
            return frozenset(reached), ranks, witnesses
        level += 1
        for x, i in added.items():
            ranks[x] = level
            witnesses[x] = i
        reached.update(added)


def certificate_ok(atoms, seeds, rules, reached, ranks, witnesses):
    atoms, seeds, rules = validate(atoms, seeds, rules)
    reached = frozenset(reached)
    if not seeds <= reached <= atoms or set(ranks) != reached or set(witnesses) != reached - seeds:
        return False
    if any(type(v) is not int or v < 0 for v in ranks.values()):
        return False
    for x in reached:
        if x in seeds:
            if ranks[x] != 0:
                return False
        else:
            i = witnesses[x]
            if type(i) is not int or not 0 <= i < len(rules):
                return False
            r = rules[i]
            if r.conclusion != x or not r.premises <= reached:
                return False
            if not all(ranks[p] < ranks[x] for p in r.premises):
                return False
    return True


def truth_oracle(atoms, seeds, rules):
    """Independent semantic oracle: intersection of every satisfying valuation."""
    atoms, seeds, rules = validate(atoms, seeds, rules)
    names = sorted(atoms)
    models = []
    for bits in range(1 << len(names)):
        world = frozenset(x for i, x in enumerate(names) if bits & (1 << i))
        if seeds <= world and all(not r.premises <= world or r.conclusion in world for r in rules):
            models.append(world)
    # Positive Horn theories always have the all-true valuation.
    common = set(names)
    for world in models:
        common.intersection_update(world)
    return frozenset(common), tuple(models)


def inclusion_cycle(a, b, c):
    """The input sets are extensions, not claims about their explanatory order."""
    return a <= b and b <= c and c <= a


def finite_chain(length, with_root):
    if type(length) is not int or length < 1:
        raise ValueError('positive integer length required')
    atoms = tuple(f'p{i}' for i in range(length))
    rules = tuple(Rule(frozenset([atoms[i+1]]), atoms[i]) for i in range(length-1))
    seeds = [atoms[-1]] if with_root else []
    return atoms, seeds, rules
