"""Original typed-certificate teaching model. Not an Aristotle formalization."""
from dataclasses import dataclass
from itertools import product
import json

@dataclass(frozen=True, order=True)
class Atom:
    domain: str
    predicate: str

@dataclass(frozen=True)
class Rule:
    source: Atom
    target: Atom
    kind: str = "local"
    bridge_id: str = ""

@dataclass(frozen=True)
class Bridge:
    name: str
    source: Atom
    target: Atom

@dataclass(frozen=True)
class Step:
    rule: Rule
    premise_index: int


def allowed(rule, bridges=()):
    """Policy only: common axioms are instantiated locally, never wildcard casts."""
    if rule.kind in ("local", "common"):
        return rule.source.domain == rule.target.domain and rule.bridge_id == ""
    if rule.kind == "bridge":
        return (rule.source.domain != rule.target.domain and
                any(b.name == rule.bridge_id and b.source == rule.source and
                    b.target == rule.target for b in bridges))
    return False


def verify(facts, steps, goal, bridges=()):
    """Facts and registry are assumptions. Reject forward references and wrong types."""
    known = list(facts)
    for step in steps:
        i = step.premise_index
        if type(i) is not int or not 0 <= i < len(known):
            return False
        if known[i] != step.rule.source or not allowed(step.rule, bridges):
            return False
        known.append(step.rule.target)
    return goal in known


def closure(facts, rules, bridges=()):
    known = set(facts)
    eligible = [r for r in rules if allowed(r, bridges)]
    while True:
        enlarged = known | {r.target for r in eligible if r.source in known}
        if enlarged == known:
            return known
        known = enlarged


def semantic_entailments(atoms, facts, rules, bridges=()):
    """Independent truth-table oracle for the *accepted material implications*."""
    eligible = [r for r in rules if allowed(r, bridges)]
    models = []
    for bits in product((False, True), repeat=len(atoms)):
        val = dict(zip(atoms, bits))
        if all(val[a] for a in facts) and all(not val[r.source] or val[r.target] for r in eligible):
            models.append(val)
    if not models:
        raise RuntimeError("Positive implication theories should have all-true model")
    return {a for a in atoms if all(v[a] for v in models)}


def examples():
    g = Atom("geometry", "relation")
    o = Atom("optics", "relation")
    a = Atom("arithmetic", "relation")
    registry = (Bridge("geometry_to_optics", g, o),)
    r = Rule(g, o, "bridge", "geometry_to_optics")
    return {
        "local": verify([g], [Step(Rule(g, Atom("geometry", "consequence")), 0)], Atom("geometry", "consequence")),
        "common_name_no_cast": verify([a], [Step(Rule(a, g, "common"), 0)], g),
        "no_bridge": verify([g], [Step(r, 0)], o),
        "declared_bridge": verify([g], [Step(r, 0)], o, registry),
        "reverse_not_licensed": verify([o], [Step(Rule(o, g, "bridge", "geometry_to_optics"), 0)], g, registry),
        "beauty_not_licensed": verify([g], [Step(Rule(g, Atom("optics", "beautiful"), "bridge", "geometry_to_optics"), 0)], Atom("optics", "beautiful"), registry),
        "false_assumption_still_accepted": verify([Atom("geometry", "false_external_fact")], [], Atom("geometry", "false_external_fact")),
    }


def enumerate_checks():
    # Six directed domain pairs can be selected in 64 ways. Each registry maps p only.
    ds = ("D0", "D1", "D2")
    pairs = [(x, y) for x in ds for y in ds if x != y]
    atoms = [Atom(d, p) for d in ds for p in ("p", "q")]
    policy_cases = mismatches = 0
    for mask in range(64):
        selected = {pair for i, pair in enumerate(pairs) if mask >> i & 1}
        bs = tuple(Bridge(x + "_" + y, Atom(x, "p"), Atom(y, "p")) for x, y in selected)
        for src, dst in product(atoms, repeat=2):
            if src.domain == dst.domain:
                r = Rule(src, dst)
                expected = True
            else:
                r = Rule(src, dst, "bridge", src.domain + "_" + dst.domain)
                expected = ((src.domain, dst.domain) in selected and src.predicate == dst.predicate == "p")
            policy_cases += 1
            mismatches += allowed(r, bs) != expected
    # 4 candidate edges, 4 bridge subsets, 16 fact subsets. 16 valuations each oracle.
    a, b, c, d = (Atom("D0", "p"), Atom("D0", "q"), Atom("D1", "p"), Atom("D1", "q"))
    aa = (a, b, c, d)
    candidates = (Rule(a, b), Rule(c, d, "common"), Rule(b, c, "bridge", "bc"), Rule(d, a, "bridge", "da"))
    bridges = (Bridge("bc", b, c), Bridge("da", d, a))
    closure_cases = differences = 0
    for rm, bm, fm in product(range(16), range(4), range(16)):
        rs = tuple(r for i, r in enumerate(candidates) if rm >> i & 1)
        bs = tuple(b for i, b in enumerate(bridges) if bm >> i & 1)
        fs = {a for i, a in enumerate(aa) if fm >> i & 1}
        closure_cases += 1
        differences += closure(fs, rs, bs) != semantic_entailments(aa, fs, rs, bs)
    return {"policy_cases": policy_cases, "policy_mismatches": mismatches,
            "closure_cases": closure_cases, "truth_valuations_per_case": 16,
            "closure_truth_mismatches": differences, "examples": examples()}

if __name__ == "__main__":
    result = enumerate_checks()
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["policy_mismatches"] or result["closure_truth_mismatches"]:
        raise SystemExit(1)
