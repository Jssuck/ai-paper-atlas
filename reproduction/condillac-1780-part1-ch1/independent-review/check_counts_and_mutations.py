"""Independent closed-form count check and live-oracle mutation sensitivity."""
import json
from itertools import product
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import model
from independent_oracle import require, run


def combinatorial_counts():
    model_count = sum(4 ** n for n in range(1, 5))
    truth_count = sum(n * 4 ** n for n in range(1, 5))
    # For an ordered distinct pair, both binary functions agree in one quarter
    # of all tables; each of the 15 query sequences retains that pair.
    indistinguishable = 15 * sum(n * (n - 1) * 4 ** (n - 1) for n in range(1, 5))
    # A truthful constant query has no gain. Once a query has been asked, it
    # never shrinks again; only the first occurrence of q0 or q1 can contribute.
    # Compute by full-signature cell occupancies, aggregating ordered tuples of
    # world signatures rather than instantiating Model/Belief or replaying tables.
    gains = 0
    signatures = tuple(product(range(2), repeat=2))
    sequences = tuple(s for length in range(4) for s in product(range(2), repeat=length))
    for n in range(1, 5):
        for assignment in product(signatures, repeat=n):
            for truth in assignment:
                for sequence in sequences:
                    seen = set()
                    for q in sequence:
                        if q in seen:
                            continue
                        if not seen:
                            distinct = len({s[q] for s in assignment}) > 1
                        else:
                            previous = next(iter(seen))
                            distinct = len({s[q] for s in assignment
                                            if s[previous] == truth[previous]}) > 1
                        gains += int(distinct)
                        seen.add(q)
    actual = {"models": model_count, "true_world_cases": truth_count,
              "histories": 15 * truth_count, "accepted_transitions": 34 * truth_count,
              "distinguishing_transitions": gains, "refusal_checks": 34 * truth_count,
              "full_fiber_checks": truth_count,
              "indistinguishable_pair_history_checks": indistinguishable}
    expected = {"models": 340, "true_world_cases": 1252, "histories": 18780,
                "accepted_transitions": 42568, "distinguishing_transitions": 20256,
                "refusal_checks": 42568, "full_fiber_checks": 1252,
                "indistinguishable_pair_history_checks": 13080}
    require(actual == expected, (actual, expected))
    return actual


def mutation_sensitivity():
    cls = model.Belief
    original = {name: getattr(cls, name) for name in
                ("candidates", "consult", "recognizes", "distinguishes", "observe")}
    mutants = {
        "omit_filtering": ("candidates", property(lambda self: self.model.worlds)),
        "ignore_refusal": ("consult", lambda self, q, truth, *, accept=True:
                           original["consult"](self, q, truth, accept=True)),
        "recognize_ambiguous": ("recognizes", lambda self: self.candidates[0]),
        "never_distinguish": ("distinguishes", lambda self, q: False),
        "forget_history": ("observe", lambda self, q, value:
                           model.Belief(self.model, (model.Evidence(q, value),))),
    }
    detected = {}
    for label, (attribute, replacement) in mutants.items():
        setattr(cls, attribute, replacement)
        try:
            run()
        except RuntimeError as error:
            detected[label] = str(error)
        finally:
            setattr(cls, attribute, original[attribute])
        require(label in detected, f"oracle failed to detect {label}")
    return detected


if __name__ == "__main__":
    print(json.dumps({"status": "PASS", "author_counts_independently_confirmed":
                      combinatorial_counts(), "synthetic_mutations_detected": mutation_sensitivity()},
                     ensure_ascii=False, indent=2))
