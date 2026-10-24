"""Original finite teaching model for Prior Analytics II.18; Python stdlib only."""
from itertools import product
import json

STEPS = (("A", ("D", "E")), ("B", ("F", "G")), ("C", ("A", "B")))
NODES = tuple("ABCDEFG")


def prepare(steps, values, target):
    """Validate a finite acyclic dependency graph; do not certify inference rules."""
    steps = tuple((out, tuple(ins)) for out, ins in steps)
    if not isinstance(values, dict) or any(type(v) is not bool for v in values.values()):
        raise ValueError("values must map proposition identifiers to actual booleans")
    if not values or any(not isinstance(k, str) or not k for k in values):
        raise ValueError("nonempty string proposition identifiers required")
    parents = {}
    for out, ins in steps:
        if out in parents or out not in values or len(ins) < 2 or len(set(ins)) != len(ins):
            raise ValueError("unique output and at least two distinct premises required")
        if any(x not in values for x in ins):
            raise ValueError("missing premise valuation")
        parents[out] = ins
    if target not in values:
        raise ValueError("unknown target")
    visiting, visited = set(), set()
    def visit(n):
        if n in visiting:
            raise ValueError("cyclic graph outside finite acyclic theorem")
        if n in visited:
            return
        visiting.add(n)
        for p in parents.get(n, ()):
            visit(p)
        visiting.remove(n)
        visited.add(n)
    for n in values:
        visit(n)
    return parents


def diagnose(steps, values, target):
    """Find false-source paths only after checking the local truth condition.

    'valuation_condition_holds' concerns this valuation, not universal validity.
    A false leaf is a candidate source, not a unique causal attribution.
    """
    parents = prepare(steps, values, target)
    ancestors = set()
    def collect(n):
        if n in ancestors:
            return
        ancestors.add(n)
        for p in parents.get(n, ()):
            collect(p)
    collect(target)
    violations = sorted(n for n in ancestors if n in parents and
                        all(values[p] for p in parents[n]) and not values[n])
    result = {"valuation_condition_holds": not violations,
              "violating_steps": violations, "target_value": values[target],
              "false_leaf_paths": [], "false_leaves": []}
    if violations or values[target]:
        return result
    paths = []
    def walk(n, trail):
        if n not in parents:
            paths.append(trail + [n])
        else:
            for p in parents[n]:
                if not values[p]:
                    walk(p, trail + [n])
    walk(target, [])
    result["false_leaf_paths"] = sorted(paths)
    result["false_leaves"] = sorted({path[-1] for path in paths})
    return result


def enumerate_records():
    records = []
    for bits in product((False, True), repeat=len(NODES)):
        values = dict(zip(NODES, bits))
        records.append({"values": values, **diagnose(STEPS, values, "C")})
    return records


def report():
    rows = enumerate_records()
    admitted = [r for r in rows if r["valuation_condition_holds"]]
    false = [r for r in admitted if not r["target_value"]]
    true_false_leaf = [r for r in admitted if r["target_value"] and
                       any(not r["values"][p] for p in "DEFG")]
    examples = {}
    for name, bits in {
        "one_false_source": (False, True, False, False, True, True, True),
        "two_false_sources": (False, False, False, False, True, False, True),
        "true_result_false_source": (True, True, True, False, True, True, True),
        "invalid_step_all_leaves_true": (True, True, False, True, True, True, True),
    }.items():
        vals = dict(zip(NODES, bits))
        examples[name] = {"values": vals, **diagnose(STEPS, vals, "C")}
    return {"scope": "seven propositions, three binary steps, one concrete truth valuation per record",
            "total_valuations": len(rows), "admissible_valuations": len(admitted),
            "false_target_admissible": len(false),
            "false_target_with_multiple_false_sources": sum(len(r["false_leaves"]) > 1 for r in false),
            "true_target_with_false_leaf": len(true_false_leaf),
            "examples": examples, "records": rows}

if __name__ == "__main__":
    print(json.dumps(report(), ensure_ascii=False, indent=2, sort_keys=True))
