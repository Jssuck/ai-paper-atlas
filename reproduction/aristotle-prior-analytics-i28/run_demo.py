"""Produce deterministic, small finite evidence, with no external dependencies."""
import json
from collections import Counter
from dataclasses import asdict
from itertools import product
from model import (requirements, search, verify, true_fact, facts_from_model)


def finite_check(max_size=4):
    counts = Counter()
    assignments = 0
    certificates = 0
    for size in range(max_size + 1):
        subsets = [frozenset(i for i in range(size) if bits & (1 << i))
                   for bits in range(1 << size)]
        for a, e, m in product(subsets, repeat=3):
            assignments += 1
            model = dict(A=a, E=e, M=m)
            facts = facts_from_model(model)
            found = search(facts)
            # Explicit raises, not assert: still enforced under python -O.
            for c in found:
                if not verify(c, facts):
                    raise RuntimeError("invalid generated certificate")
                if not all(true_fact(f, model) for f in c.premises):
                    raise RuntimeError("false premise from semantic oracle")
                if not true_fact(c.conclusion, model):
                    raise RuntimeError("unsound finite instance")
                counts[c.rule] += 1
                certificates += 1
            expected = {r for r in ("CF", "CG", "DF", "BH", "DG", "BG")
                        if all(true_fact(f, model)
                               for f in requirements(r, "A", "E", "M"))}
            if {c.rule for c in found} != expected:
                raise RuntimeError("missed applicable core pattern")
    return {"domain_sizes": list(range(max_size + 1)),
            "assignments": assignments, "certificates_checked": certificates,
            "by_rule": dict(sorted(counts.items())),
            "qualification": "finite extensional checks, not a general theorem or full I.28 reproduction"}


def invalid_pairs():
    # All three classes nonempty: avoid explaining failures by empty terms.
    subsets = [frozenset(i for i in range(3) if bits & (1 << i))
               for bits in range(1, 8)]
    schemes = {
        "BF": [("all", "A", "M"), ("all", "E", "M")],
        "CH": [("all", "M", "A"), ("none", "M", "E")],
        "DH": [("none", "M", "A"), ("none", "M", "E")],
    }
    results = {}
    for name, facts in schemes.items():
        examples = {}
        for a, e, m in product(subsets, repeat=3):
            model = dict(A=a, E=e, M=m)
            if not all(true_fact(f, model) for f in facts):
                continue
            for goal in ("A", "E", "I", "O"):
                if goal not in examples and not true_fact((goal, "E", "A"), model):
                    examples[goal] = {k: sorted(v) for k, v in model.items()}
        if len(examples) != 4:
            raise RuntimeError("not all four directed targets refuted")
        results[name] = {"target_direction": "predicate A of subject E",
                         "false_goal_models": examples}
    return results


def main():
    examples = []
    for rule in ("CF", "CG", "DF", "BH", "DG", "BG"):
        facts = requirements(rule, "A", "E", "M")
        c = next(c for c in search(facts) if c.rule == rule)
        examples.append(asdict(c))
    output = {"core_examples": examples,
              "finite_check": finite_check(),
              "nonentailment_witnesses": invalid_pairs(),
              "not_implemented": ["textual emendation", "all syllogistic routes",
                                  "automatic acquisition or closure of facts",
                                  "identifying different names from equal extensions",
                                  "probabilistic or modal reasoning"]}
    print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
