"""Independent bounded oracle: all n=1..4, two binary functions, |history|<=3.

The bounds are fixed and deliberately small. This is finite regression evidence,
not a proof for all finite models, an empirical experiment, or a benchmark.
"""
from itertools import product
import json
from model import Belief, Model, Observation


def require(condition: bool, detail: object) -> None:
    # Do not use assert: checks must remain active under python -O.
    if not condition:
        raise AssertionError(detail)


def run() -> dict[str, int]:
    counts = dict(models=0, true_world_cases=0, histories=0,
                  accepted_transitions=0, distinguishing_transitions=0,
                  refusal_checks=0, full_fiber_checks=0,
                  indistinguishable_pair_history_checks=0)
    sequences = tuple(seq for length in range(4)
                      for seq in product(range(2), repeat=length))
    for n in range(1, 5):
        worlds = tuple(f"w{i}" for i in range(n))
        for bits in product((0, 1), repeat=2 * n):
            # Raw integer tables form the independent oracle. It does not call
            # model.outcome, candidates, fiber, or signature to predict results.
            raw = (bits[:n], bits[n:])
            model = Model(worlds, tuple(
                Observation(f"q{q}", tuple(str(v) for v in raw[q]))
                for q in range(2)
            ))
            counts["models"] += 1
            for truth in range(n):
                counts["true_world_cases"] += 1
                expected_fiber_indices = {
                    w for w in range(n)
                    if raw[0][w] == raw[0][truth]
                    and raw[1][w] == raw[1][truth]
                }
                expected_fiber = tuple(worlds[w] for w in sorted(expected_fiber_indices))
                require(model.fiber(worlds[truth]) == expected_fiber, (n, bits, truth))
                full = Belief(model).consult("q0", worlds[truth]).consult("q1", worlds[truth])
                require(full.candidates == expected_fiber, (n, bits, truth, "full fiber"))
                require((full.recognizes() is not None) == (len(expected_fiber) == 1),
                        (n, bits, truth, "singleton iff full recognition"))
                counts["full_fiber_checks"] += 1
                for sequence in sequences:
                    counts["histories"] += 1
                    state = Belief(model)
                    seen = []
                    expected_indices = set(range(n))
                    for q in sequence:
                        query = f"q{q}"
                        old = state
                        prior = set(expected_indices)
                        distinguishing = len({raw[q][w] for w in prior}) > 1
                        require(state.distinguishes(query) == distinguishing,
                                (n, bits, truth, sequence, "distinguishes"))
                        refusal = state.consult(query, worlds[truth], accept=False)
                        require(refusal is state, "refusal must preserve the exact state")
                        counts["refusal_checks"] += 1
                        state = state.consult(query, worlds[truth])
                        seen.append(q)
                        expected_indices = {
                            w for w in range(n)
                            if all(raw[j][w] == raw[j][truth] for j in seen)
                        }
                        expected = tuple(worlds[w] for w in sorted(expected_indices))
                        require(state.candidates == expected, (n, bits, truth, sequence))
                        require(truth in expected_indices, "truth must survive truthful history")
                        require(expected_indices <= prior, "candidates cannot grow")
                        require(state.history[:-1] == old.history, "accepted history retained")
                        require(len(state.history) == len(old.history) + 1, "one appended record")
                        require(state.history[-1].query == query, "query retained")
                        require(state.history[-1].outcome == str(raw[q][truth]), "outcome retained")
                        require(len(old.history) == len(seen) - 1, "old state immutable")
                        if distinguishing:
                            require(expected_indices < prior, "distinguishing query must shrink")
                            counts["distinguishing_transitions"] += 1
                        else:
                            require(expected_indices == prior, "constant query cannot shrink")
                        counts["accepted_transitions"] += 1
                    # Covers empty histories too. Oracle computed directly from raw tables.
                    final_oracle = tuple(
                        worlds[w] for w in range(n)
                        if all(raw[q][w] == raw[q][truth] for q in sequence)
                    )
                    require(state.candidates == final_oracle, "history signature fiber")
                    recognized = final_oracle[0] if len(final_oracle) == 1 else None
                    require(state.recognizes() == recognized, "recognition iff singleton")
                    require(worlds[truth] in state.candidates, "truth retained, including empty history")
                    for indistinguishable in expected_fiber_indices - {truth}:
                        require(worlds[indistinguishable] in state.candidates,
                                "available observations cannot separate equal full signatures")
                        counts["indistinguishable_pair_history_checks"] += 1
    require(counts["models"] == 340, "model enumeration count")
    require(counts["true_world_cases"] == 1252, "truth assignment count")
    require(counts["histories"] == 18780, "history enumeration count")
    require(counts["accepted_transitions"] == 42568, "transition enumeration count")
    require(counts["refusal_checks"] == 42568, "refusal enumeration count")
    require(counts["full_fiber_checks"] == 1252, "fiber enumeration count")
    return counts


if __name__ == "__main__":
    print(json.dumps({"status": "PASS", "bounds": {
        "world_count": [1, 2, 3, 4], "binary_queries": 2,
        "maximum_history_length": 3,
    }, "counts": run()}, ensure_ascii=False, indent=2))
