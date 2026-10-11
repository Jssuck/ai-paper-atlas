"""Separately authored bounded audit: bit-set intersection, arbitrary evidence.

This is not the author's exhaustive.py and does not import its helpers.
Expected answers use integer bit masks, not model methods or a replay of the
production candidate comprehension. Includes false-but-consistent, impossible,
out-of-range, ternary, zero-query and three-query histories. No assert statements.
"""
from collections import Counter
from itertools import product
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from model import Belief, Evidence, InconsistentEvidence, Model, Observation


def require(condition, context):
    if not condition:
        raise RuntimeError(context)


def run():
    counts = Counter()
    configurations = [(n, 2, 2) for n in range(1, 5)]
    configurations += [(n, 0, 2) for n in range(1, 5)]
    configurations += [(n, 1, 3) for n in range(1, 4)]
    configurations += [(n, 3, 2) for n in range(1, 4)]
    for n, m, k in configurations:
        worlds = tuple(f"world {i}" for i in range(n))
        queries = tuple(f"query {q}" for q in range(m))
        full = (1 << n) - 1
        atoms = tuple(product(range(m), range(k)))
        histories = tuple(h for length in range(4)
                          for h in product(atoms, repeat=length))
        for flat in product(range(k), repeat=n * m):
            # World-major generation, unlike the author's query-major oracle.
            rows = tuple(flat[i*m:(i+1)*m] for i in range(n))
            masks = {}
            for q in range(m):
                for value in range(k):
                    mask = 0
                    for i, row in enumerate(rows):
                        if row[q] == value:
                            mask |= 1 << i
                    masks[q, value] = mask
            model = Model(worlds, tuple(
                Observation(queries[q], tuple(str(row[q]) for row in rows))
                for q in range(m)))
            counts["models"] += 1
            for i, row in enumerate(rows):
                expected_mask = full
                for q, value in enumerate(row):
                    expected_mask &= masks[q, value]
                expected = tuple(w for j, w in enumerate(worlds)
                                 if expected_mask & (1 << j))
                require(model.signature(worlds[i]) == tuple(map(str, row)), "signature")
                require(model.fiber(worlds[i]) == expected, "full signature block")
                counts["signature_and_fiber_checks"] += 1

            for history in histories:
                counts["arbitrary_histories"] += 1
                expected_mask = full
                outside_range = False
                for atom in history:
                    expected_mask &= masks[atom]
                    outside_range |= masks[atom] == 0
                evidence = tuple(Evidence(queries[q], str(v)) for q, v in history)
                try:
                    state = Belief(model, evidence)
                except InconsistentEvidence:
                    require(not outside_range and expected_mask == 0,
                            (n, m, k, flat, history, "wrong inconsistency rejection"))
                    counts["inconsistent_histories_rejected"] += 1
                    continue
                except ValueError:
                    require(outside_range, (history, "wrong range rejection"))
                    counts["out_of_range_histories_rejected"] += 1
                    continue
                require(not outside_range and expected_mask != 0, "bad history accepted")
                counts["accepted_histories"] += 1
                expected = tuple(w for i, w in enumerate(worlds)
                                 if expected_mask & (1 << i))
                require(state.candidates == expected, (flat, history, "candidate mismatch"))
                require(state.recognizes() == (expected[0] if len(expected) == 1 else None),
                        "recognition must be exactly singleton")
                require(state.history == evidence, "history not retained")
                reverse = Belief(model, tuple(reversed(evidence)))
                require(reverse.candidates == expected, "order changed candidate set")
                counts["order_invariance_checks"] += 1

                for q in range(m):
                    live_blocks = sum(bool(expected_mask & masks[q, v]) for v in range(k))
                    require(state.distinguishes(queries[q]) == (live_blocks > 1),
                            "distinguishing query classification")
                    for value in range(k):
                        counts["arbitrary_extension_checks"] += 1
                        next_mask = expected_mask & masks[q, value]
                        try:
                            new = state.observe(queries[q], str(value))
                        except InconsistentEvidence:
                            require(masks[q, value] != 0 and next_mask == 0,
                                    "wrong extension inconsistency")
                            continue
                        except ValueError:
                            require(masks[q, value] == 0, "wrong extension range rejection")
                            continue
                        require(next_mask != 0, "empty extension accepted")
                        new_expected = tuple(w for i, w in enumerate(worlds)
                                             if next_mask & (1 << i))
                        require(new.candidates == new_expected, "extension intersection")
                        require(new.history == evidence + (Evidence(queries[q], str(value)),),
                                "append changed prefix")
                        require(state.history == evidence and state.candidates == expected,
                                "old state mutated")
                        require((next_mask != expected_mask) == (live_blocks > 1),
                                "strict shrink iff query distinguishing")
                        counts["accepted_extensions"] += 1
                    # Check a truthful transition from every surviving possible truth.
                    for i in range(n):
                        if not expected_mask & (1 << i):
                            continue
                        feedback = state.consult(queries[q], worlds[i])
                        require(feedback.history[-1].outcome == str(rows[i][q]), "truth lookup")
                        require(worlds[i] in feedback.candidates, "surviving truth lost")
                        require(state.consult(queries[q], worlds[i], accept=False) is state,
                                "refusal identity")
                        counts["truthful_and_refusal_extensions"] += 1

    require(counts["models"] == 967, "closed-form model count")
    require(counts["arbitrary_histories"] == 181720, "closed-form history count")
    require(counts["arbitrary_histories"] == counts["accepted_histories"]
            + counts["inconsistent_histories_rejected"]
            + counts["out_of_range_histories_rejected"], "history partition")
    return dict(sorted(counts.items()))


if __name__ == "__main__":
    print(json.dumps({"status": "PASS", "oracle": "world-major integer bit masks",
                      "maximum_arbitrary_history_length": 3, "counts": run()},
                     ensure_ascii=False, indent=2))
