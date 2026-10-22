"""I.28 six matching patterns: explicit premises, not a complete prover.

All classes are interpreted as sets. Empty classes are allowed; particular
conclusions require an explicit nonempty premise. No closed-world negation.
"""
from dataclasses import dataclass
from typing import FrozenSet, Tuple

Fact = Tuple[str, ...]


def validate_term(term):
    if not isinstance(term, str) or not term.strip():
        raise ValueError("term names must be nonempty strings")


def validate_endpoints(a, e):
    validate_term(a)
    validate_term(e)
    if a == e:
        raise ValueError("predicate and subject must be distinct terms")


def normalize(fact: Fact) -> Fact:
    if not isinstance(fact, tuple) or not fact:
        raise ValueError("a fact must be a nonempty tuple")
    for term in fact[1:]:
        validate_term(term)
    if fact[0] == "nonempty" and len(fact) == 2:
        return fact
    if fact[0] in ("all", "none") and len(fact) == 3:
        if fact[0] == "none":
            return ("none", *sorted(fact[1:]))
        return fact
    raise ValueError("unknown fact or wrong arity")


@dataclass(frozen=True)
class Certificate:
    rule: str
    predicate: str
    subject: str
    middle: str
    premises: Tuple[Fact, ...]
    conclusion: Fact


def requirements(rule, a, e, m):
    """Directions: all(x,y) means x subset y, not 'all y are x'."""
    validate_endpoints(a, e)
    validate_term(m)
    if m in (a, e):
        raise ValueError("middle must differ from both extremes")
    specs = {
        "CF": (("all", m, a), ("all", e, m)),
        "CG": (("all", m, a), ("all", m, e), ("nonempty", m)),
        "DF": (("none", m, a), ("all", e, m)),
        "BH": (("all", a, m), ("none", m, e)),
        "DG": (("none", m, a), ("all", m, e), ("nonempty", m)),
        "BG": (("all", a, m), ("all", m, e), ("nonempty", a)),
    }
    return tuple(normalize(x) for x in specs[rule])


def conclusion(rule, a, e):
    return ({"CF": "A", "CG": "I", "DF": "E", "BH": "E",
             "DG": "O", "BG": "I"}[rule], e, a)


def indexes(facts, a, e):
    validate_endpoints(a, e)
    fs = frozenset(normalize(x) for x in facts)
    terms = {v for f in fs for v in f[1:]} - {a, e}
    return {
        "B": {m for m in terms if ("all", a, m) in fs},
        "C": {m for m in terms if ("all", m, a) in fs},
        "D": {m for m in terms if normalize(("none", m, a)) in fs},
        "F": {m for m in terms if ("all", e, m) in fs},
        "G": {m for m in terms if ("all", m, e) in fs},
        "H": {m for m in terms if normalize(("none", m, e)) in fs},
    }


def search(facts, a="A", e="E"):
    """Find exact middle-name matches; no inference from mere overlap.

    Missing witnesses suppress particular certificates, not universal ones.
    Empty result means only no certificate in these explicitly supplied facts.
    """
    validate_endpoints(a, e)
    fs = frozenset(normalize(x) for x in facts)
    ix = indexes(fs, a, e)
    results = []
    for rule in ("CF", "CG", "DF", "BH", "DG", "BG"):
        for m in sorted(ix[rule[0]] & ix[rule[1]]):
            req = requirements(rule, a, e, m)
            if all(f in fs for f in req):
                results.append(Certificate(rule, a, e, m, req,
                                           conclusion(rule, a, e)))
    return results


def verify(cert, facts):
    """Check certificate against explicit knowledge, including provenance slots.

    This checks a rule instance, not the empirical truth of input assertions.
    The separate semantic evaluator below can check a supplied finite model.
    """
    try:
        a, e, m = cert.predicate, cert.subject, cert.middle
        validate_endpoints(a, e)
        validate_term(m)
        if len({a, e, m}) != 3:
            return False
        req = requirements(cert.rule, a, e, m)
        fs = frozenset(normalize(x) for x in facts)
        return (cert.premises == req and all(x in fs for x in req)
                and cert.conclusion == conclusion(cert.rule, a, e))
    except (KeyError, ValueError, TypeError, AttributeError):
        return False


def true_fact(fact, model):
    kind = fact[0]
    if kind == "nonempty":
        return bool(model[fact[1]])
    x, y = model[fact[1]], model[fact[2]]
    if kind in ("all", "A"):
        return x <= y
    if kind in ("none", "E"):
        return not (x & y)
    if kind == "I":
        return bool(x & y)
    if kind == "O":
        return bool(x - y)
    raise ValueError(kind)


def facts_from_model(model):
    """Test oracle only: not the search engine's knowledge acquisition method."""
    facts = set()
    for x in model:
        if model[x]:
            facts.add(("nonempty", x))
        for y in model:
            if x != y:
                for kind in ("all", "none"):
                    fact = normalize((kind, x, y))
                    if true_fact(fact, model):
                        facts.add(fact)
    return frozenset(facts)
