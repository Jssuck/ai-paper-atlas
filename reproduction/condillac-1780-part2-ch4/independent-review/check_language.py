"""Independent, bounded behavioral oracle; no source-module test reuse.

Run from the model directory: python3 -B independent-review/check_language.py.
Expected answers enumerate integer-indexed candidate decoders and direct
per-observation disagreements, rather than reimplementing label aggregation.
Every check remains active under -O and -OO. Counts report contexts, not tests.
"""
from dataclasses import FrozenInstanceError, replace
from itertools import product
from pathlib import Path
import hashlib
import json
import platform
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from finite_language import (Problem, empirical_loss, fit, label_counts,
                             minimum_empirical_loss, predictions, refine, rename,
                             truth_errors)


class ReviewFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise ReviewFailure(message)


def raw_predictions(r, h):
    return tuple(h[label] for label in r)


def raw_loss(r, h, counts):
    result = 0
    for u, label in enumerate(r):
        for answer, multiplicity in enumerate(counts[u]):
            if h[label] != answer:
                result += multiplicity
    return result


def raw_errors(r, h, truths):
    return sum(h[label] != truths[u] for u, label in enumerate(r))


def make(r, h, counts, truths=None):
    labels = tuple(f"label-{i}" for i in range(len(h)))
    # Deliberately non-lexicographic answer order.
    answers = ("z", "a", "m")[:len(counts[0]) if counts else 3]
    truths = truths if truths is not None else (0,) * len(r)
    return Problem(tuple(f"object-{u}" for u in range(len(r))), labels, answers,
                   tuple(labels[i] for i in r), tuple(answers[i] for i in h),
                   tuple(answers[i] for i in truths), counts)


def majority(tally):
    """Full domain: |U|=2, |L|=|A|=3, all six counts in {0,1}."""
    candidates = tuple(product(range(3), repeat=3))
    for r in product(range(3), repeat=2):
        for entries in product(range(2), repeat=6):
            counts = (entries[:3], entries[3:])
            losses = {h: raw_loss(r, h, counts) for h in candidates}
            best = min(losses.values())
            optimal = tuple(h for h in candidates if losses[h] == best)
            zero = tuple(label for label in range(3)
                         if not any(counts[u][a] for u in range(2)
                                    for a in range(3) if r[u] == label))
            tally["majority_contexts"] += 1
            tally["majority_candidate_losses"] += len(candidates)
            for old in candidates:
                p = make(r, old, counts)
                expected = next(h for h in optimal
                                if all(h[label] == old[label] for label in zero))
                result = fit(p)
                require(result.h == tuple(p.answers[i] for i in expected),
                        f"majority/answer-order/zero-evidence mismatch: {r, counts, old}")
                require(predictions(p) == tuple(p.answers[i] for i in raw_predictions(r, old)),
                        "predictions differ from independent indexed composition")
                require(empirical_loss(p) == losses[old], "old empirical loss mismatch")
                require(empirical_loss(result) == best, "fit does not attain enumerated minimum")
                require(minimum_empirical_loss(p) == best, "minimum differs from enumeration")
                require(fit(result) == result, "fit is not idempotent")
                require(result == replace(p, h=result.h), "fit changed a non-decoder field")
                tally["fitted_old_decoders"] += 1


def adequacy(tally):
    """Full domain: |U|=3, |L|=2, |A|=3; no observations needed."""
    candidates = tuple(product(range(3), repeat=2))
    for r in product(range(2), repeat=3):
        for truths in product(range(3), repeat=3):
            p = make(r, (0, 0), ((0, 0, 0),) * 3, truths)
            direct = tuple(raw_errors(r, h, truths) for h in candidates)
            computed = tuple(truth_errors(replace(p, h=tuple(p.answers[i] for i in h)))
                             for h in candidates)
            require(computed == direct, "truth errors differ from objectwise oracle")
            constant_cells = all(r[u] != r[v] or truths[u] == truths[v]
                                 for u in range(3) for v in range(3))
            require((min(direct) == 0) == constant_cells,
                    "representation adequacy iff constant nonempty fibers failed")
            tally["adequacy_contexts"] += 1
            tally["adequacy_decoder_errors"] += len(candidates)


def refinements(tally):
    """All q:M3->L2 and s:U2->M3, four named count matrices; all old decoders.

    r=q(s) includes non-surjective q, s, r and more labels than objects.
    Truth-minimum comparisons additionally cover all nine truth assignments.
    """
    coarse_candidates = tuple(product(range(3), repeat=2))
    fine_candidates = tuple(product(range(3), repeat=3))
    matrices = (((0, 0, 0), (0, 0, 0)), ((1, 0, 0), (0, 1, 0)),
                ((0, 2, 0), (0, 0, 3)), ((1, 1, 1), (1, 1, 1)))
    for q in product(range(2), repeat=3):
        for s in product(range(3), repeat=2):
            r = tuple(q[i] for i in s)
            tally["refinement_structures"] += 1
            for truths in product(range(3), repeat=2):
                coarse_min = min(raw_errors(r, h, truths) for h in coarse_candidates)
                fine_min = min(raw_errors(s, h, truths) for h in fine_candidates)
                require(fine_min <= coarse_min, "truth optimum worsened under refinement")
                tally["refinement_truth_contexts"] += 1
                tally["refinement_truth_candidate_errors"] += 36
            for counts in matrices:
                coarse_min = min(raw_loss(r, h, counts) for h in coarse_candidates)
                fine_min = min(raw_loss(s, h, counts) for h in fine_candidates)
                require(fine_min <= coarse_min, "empirical optimum worsened under refinement")
                tally["refinement_empirical_contexts"] += 1
                tally["refinement_candidate_losses"] += 36
                for old in coarse_candidates:
                    p = make(r, old, counts, (1, 2))
                    fine = refine(p, ("third", "first", "second"),
                                  tuple(("third", "first", "second")[i] for i in s),
                                  tuple(p.labels[i] for i in q))
                    inherited = tuple(old[i] for i in q)
                    require(fine.h == tuple(p.answers[i] for i in inherited),
                            "refinement decoder is not old decoder composed with q")
                    require(predictions(fine) == predictions(p), "transport changed predictions")
                    require(empirical_loss(fine) == raw_loss(r, old, counts),
                            "transport changed empirical loss")
                    require(truth_errors(fine) == raw_errors(r, old, (1, 2)),
                            "transport changed truth errors")
                    require(minimum_empirical_loss(p) == coarse_min, "coarse minimum mismatch")
                    require(minimum_empirical_loss(fine) == fine_min, "fine minimum mismatch")
                    require(empirical_loss(fit(fine)) == fine_min, "fine fit is not optimal")
                    tally["inherited_decoders"] += 1


def edge_checks(tally):
    p = make((0, 0, 1), (2, 1, 2), ((0, 0, 0), (0, 0, 0), (2, 2, 0)), (0, 1, 2))
    require(label_counts(p) == ((0, 0, 0), (2, 2, 0), (0, 0, 0)), "aggregation mismatch")
    require(fit(p).h == ("m", "z", "m"), "used-zero, unused-zero, or positive tie convention")
    # Renaming may overlap/swizzle the old strings; transport is positional.
    for labels in (("label-2", "label-0", "label-1"), ("新名", "opaque", "borrowed")):
        renamed = rename(p, labels)
        require(renamed.r == tuple(labels[i] for i in (0, 0, 1)), "rename r mismatch")
        require(renamed.h == p.h, "positional rename changed h values")
        require(predictions(renamed) == predictions(p), "rename changed prediction")
        require(truth_errors(renamed) == truth_errors(p), "rename changed true error")
        require(empirical_loss(renamed) == empirical_loss(p), "rename changed empirical loss")
        require(fit(renamed) == rename(fit(p), labels), "fit and rename do not commute")
        require(rename(renamed, p.labels) == p, "rename inverse failed")
    # Correct but incomplete observations worsen true errors.
    unseen = make((0, 0, 0), (0,), ((0, 1, 0), (0, 0, 0), (0, 0, 0)), (1, 0, 0))
    require((empirical_loss(unseen), empirical_loss(fit(unseen))) == (1, 0), "unseen loss")
    require((truth_errors(unseen), truth_errors(fit(unseen))) == (1, 2), "unseen true error")
    noisy = make((0,), (0,), ((0, 10, 0),), (0,))
    require((empirical_loss(noisy), empirical_loss(fit(noisy))) == (10, 0), "noise loss")
    require((truth_errors(noisy), truth_errors(fit(noisy))) == (0, 1), "noise true error")
    require(fit(replace(noisy, f=("m",))).h == fit(noisy).h, "fit used truth")
    coarse = make((0, 0), (0,), ((2, 0, 0), (0, 3, 0)), (0, 1))
    fine = refine(fit(coarse), ("x", "y"), ("x", "y"), ("label-0", "label-0"))
    bad = replace(fine, h=("a", "z"))
    require((minimum_empirical_loss(coarse), minimum_empirical_loss(fine)) == (2, 0), "minima")
    require((empirical_loss(fit(coarse)), empirical_loss(bad)) == (2, 5), "arbitrary-rule counterexample")
    reused = make((0, 0), (0, 1), ((1, 0, 0), (1, 0, 0)))
    unchanged = replace(reused, r=("label-0", "label-1"))
    transported = refine(reused, reused.labels, unchanged.r, ("label-0", "label-0"))
    require((empirical_loss(reused), empirical_loss(unchanged), empirical_loss(transported))
            == (0, 1, 0), "unchanged dictionary incorrectly treated as transport")
    # Main paper 10.1 uses a different four-object example from examples.py.
    paper = make((0, 0, 1, 1), (1, 0),
                 ((0, 1), (1, 0), (0, 1), (0, 1)), (1, 0, 1, 1))
    require((truth_errors(paper), truth_errors(fit(paper))) == (3, 1), "paper 10.1 true errors")
    require((empirical_loss(paper), empirical_loss(fit(paper))) == (3, 1), "paper 10.1 losses")
    require(fit(paper).h == ("z", "a"), "paper 10.1 tie and fit")
    # More labels alone is not refinement; crossing old fibers is rejected below.
    empty = Problem((), ("u", "v"), ("yes", "no"), (), ("no", "yes"), (), ())
    require(fit(empty) == empty, "empty universe changed")
    require((predictions(empty), empirical_loss(empty), truth_errors(empty),
             minimum_empirical_loss(empty)) == ((), 0, 0, 0), "empty extension")
    singleton = Problem(("u",), ("c",), ("only",), ("c",), ("only",), ("only",), ((7,),))
    require(fit(singleton) == singleton and empirical_loss(singleton) == 0, "one answer")
    n = 10**100
    huge = make((0,), (0,), ((n, n + 1, n),))
    require(fit(huge).h == ("a",) and minimum_empirical_loss(huge) == 2*n, "integer exactness")
    try:
        p.h = ("z",) * 3
    except FrozenInstanceError:
        pass
    else:
        raise ReviewFailure("Problem is mutable")


def invalid_inputs(tally):
    p = make((0, 1), (0, 1), ((1, 0, 0), (0, 1, 0)), (0, 1))
    invalid = []
    # Exact tuple/string types, distinctness, and nonempty names.
    for field in ("objects", "labels", "answers"):
        for value in (None, [], "ab", 0, ("", "b"), ("a", "a"),
                      (0, "b"), (True, "b"), (False, "b"), (None, "b")):
            invalid.append((f"{field}={value!r}", lambda f=field, v=value: replace(p, **{f: v})))
    for field in ("labels", "answers"):
        invalid.append((f"{field}=()", lambda f=field: replace(p, **{f: ()})))
    for field in ("r", "h", "f"):
        for value in (None, [], "aa", (), ("bad",), ("bad", "bad"),
                      (True, False), (0, 1), ("label-0",) * 3):
            invalid.append((f"{field}={value!r}", lambda f=field, v=value: replace(p, **{f: v})))
    for value in (None, [], (), ((1, 0, 0),), [[1, 0, 0], [0, 1, 0]],
                  ([1, 0, 0], (0, 1, 0)), ((1, 0), (0, 1, 0)),
                  ((1, 0, 0, 0), (0, 1, 0)), ((-1, 0, 0), (0, 1, 0)),
                  ((True, 0, 0), (0, 1, 0)), ((False, 0, 0), (0, 1, 0)),
                  ((1.0, 0, 0), (0, 1, 0)), (("1", 0, 0), (0, 1, 0)),
                  ((None, 0, 0), (0, 1, 0))):
        invalid.append((f"counts={value!r}", lambda v=value: replace(p, counts=v)))
    for labels in (None, [], (), ("one",), ("same", "same"), ("", "ok"),
                   (True, "ok"), (0, "ok"), ("a", "b", "c")):
        invalid.append((f"rename={labels!r}", lambda v=labels: rename(p, v)))
    fine_args = [
        ([], ("x", "y"), ("label-0", "label-1")),
        ((), ("x", "y"), ()),
        (("x", "x"), ("x", "x"), ("label-0", "label-1")),
        ((True, "y"), (True, "y"), ("label-0", "label-1")),
        (("x", "y"), ["x", "y"], ("label-0", "label-1")),
        (("x", "y"), ("x",), ("label-0", "label-1")),
        (("x", "y"), ("x", "missing"), ("label-0", "label-1")),
        (("x", "y"), (True, False), ("label-0", "label-1")),
        (("x", "y"), (0, 1), ("label-0", "label-1")),
        (("x", "y"), ("x", "y"), ["label-0", "label-1"]),
        (("x", "y"), ("x", "y"), ("label-0",)),
        (("x", "y"), ("x", "y"), ("label-0", "missing")),
        (("x", "y"), ("x", "y"), (True, False)),
        (("x", "y"), ("x", "y"), (0, 1)),
        (("x", "y"), ("x", "x"), ("label-0", "label-1")),
        (("x", "y", "z"), ("x", "x"), ("label-0", "label-1", "label-1")),
    ]
    for args in fine_args:
        invalid.append((f"refine={args!r}", lambda a=args: refine(p, *a)))
    for name, action in invalid:
        try:
            action()
        except ValueError:
            tally["rejected_invalid_inputs"] += 1
        except Exception as exc:
            raise ReviewFailure(f"wrong validation exception for {name}: {type(exc).__name__}") from exc
        else:
            raise ReviewFailure(f"accepted invalid input: {name}")


def main():
    print(f"Python {platform.python_version()}; implementation={platform.python_implementation()}; optimize={sys.flags.optimize}", flush=True)
    print("finite_language.py sha256=" + hashlib.sha256((ROOT / "finite_language.py").read_bytes()).hexdigest(), flush=True)
    require(sys.flags.optimize in (0, 1, 2), "unexpected optimization mode")
    try:
        require(False, "intentional explicit-guard control")
    except ReviewFailure as exc:
        require(str(exc) == "intentional explicit-guard control", "guard wrong exception")
    else:
        raise ReviewFailure("explicit guard failed")
    tally = dict.fromkeys(("majority_contexts", "majority_candidate_losses", "fitted_old_decoders",
                          "adequacy_contexts", "adequacy_decoder_errors", "refinement_structures",
                          "refinement_truth_contexts", "refinement_truth_candidate_errors",
                          "refinement_empirical_contexts", "refinement_candidate_losses",
                          "inherited_decoders", "rejected_invalid_inputs"), 0)
    majority(tally)
    adequacy(tally)
    refinements(tally)
    edge_checks(tally)
    invalid_inputs(tally)
    expected = {"majority_contexts": 576, "majority_candidate_losses": 15552,
                "fitted_old_decoders": 15552, "adequacy_contexts": 216,
                "adequacy_decoder_errors": 1944, "refinement_structures": 72,
                "refinement_truth_contexts": 648, "refinement_truth_candidate_errors": 23328,
                "refinement_empirical_contexts": 288, "refinement_candidate_losses": 10368,
                "inherited_decoders": 2592,
                "rejected_invalid_inputs": 98}
    require(tally == expected, f"scope-count mismatch: {tally!r}")
    print(json.dumps(tally, sort_keys=True), flush=True)
    print("PASS: independent bounded domains, edge checks, input rejection, explicit guard control.")
    print("No mutation suite; no claim of universal validation, historical proof, or empirical generalization.")


if __name__ == "__main__":
    main()
