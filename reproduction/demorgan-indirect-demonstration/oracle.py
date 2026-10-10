"""Set-extension cross-check, separately composed from recursive Model.force."""
from itertools import product
from logic import formula_suite, labeled_preorders, Model, powerset


def denotation(model, formula):
    """Bottom-up sets of forcing worlds; no call to Model.force or future."""
    universe = frozenset(range(model.frame.n))
    valuation = dict(model.valuation)
    known = {}
    pending = [(formula, False)]
    while pending:
        node, expanded = pending.pop()
        if node in known:
            continue
        if not expanded:
            pending.append((node, True))
            pending.extend((child, False) for child in node.args)
            continue
        if node.op == "atom":
            known[node] = valuation[node.name]
        elif node.op == "bottom":
            known[node] = frozenset()
        else:
            left, right = (known[x] for x in node.args)
            if node.op == "and":
                known[node] = left & right
            elif node.op == "or":
                known[node] = left | right
            else:
                bad = left - right
                known[node] = universe - frozenset(
                    w for w, v in model.frame.relation if v in bad)
    return known[formula]


def exhaustive_small_frames(max_worlds=3):
    if type(max_worlds) is not int or not 1 <= max_worlds <= 3:
        raise ValueError("This bounded oracle supports 1 to 3 worlds")
    formulas = formula_suite()
    by_size = []
    for n in range(1, max_worlds + 1):
        stats = {"worlds": n, "frames": 0, "models": 0, "world_evaluations": 0,
                 "formula_world_comparisons": 0,
                 "forward_counterexamples": 0, "reverse_counterexamples": 0,
                 "persistence_violations": 0}
        for frame in labeled_preorders(n):
            stats["frames"] += 1
            upsets = [s for s in powerset(range(n)) if frame.is_upset(s)]
            for p_true, q_true in product(upsets, repeat=2):
                model = Model.from_mapping(frame, {"p": p_true, "q": q_true})
                stats["models"] += 1
                stats["world_evaluations"] += n
                for name, formula in formulas.items():
                    expected = denotation(model, formula)
                    actual = frozenset(w for w in range(n) if model.force(w, formula))
                    if actual != expected:
                        raise AssertionError(("recursive/set oracle disagreement", n, name))
                    if not frame.is_upset(actual):
                        stats["persistence_violations"] += 1
                        raise AssertionError(("nonpersistent formula", n, name))
                    stats["formula_world_comparisons"] += n
                    if name == "forward_contraposition":
                        stats["forward_counterexamples"] += n - len(actual)
                    if name == "reverse_contraposition":
                        stats["reverse_counterexamples"] += n - len(actual)
        by_size.append(stats)
    return {"bound": max_worlds, "frames_are": "all labeled preorders",
            "atoms": ["p", "q"], "formulas": list(formulas),
            "formula_count": len(formulas), "by_size": by_size,
            "totals": {key: sum(row[key] for row in by_size)
                       for key in by_size[0] if key != "worlds"}}
