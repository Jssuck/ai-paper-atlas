"""Run focused tests and bounded exhaustive oracles, including under -O/-OO.

The oracle enumerates candidate decoders and computes their loss directly on
integer-indexed raw data. It does not use the implementation's aggregation or
fitting functions to select its expected optimum.
"""
from dataclasses import replace
from itertools import permutations, product
import json
import platform
import sys
import unittest
from finite_language import (Problem, empirical_loss, fit, minimum_empirical_loss,
                             predictions, refine, rename, truth_errors)
import test_finite_language


class VerificationFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationFailure(message)


def raw_loss(r, h, counts):
    return sum(counts[u][a] for u in range(2) for a in range(2) if h[r[u]] != a)


def make_problem(r, h, counts):
    labels, answers = ("c0", "c1"), ("0", "1")
    return Problem(("u0", "u1"), labels, answers,
                   tuple(labels[x] for x in r), tuple(answers[x] for x in h), ("0", "1"), counts)


def run_oracles() -> dict[str, int]:
    maps = tuple(product(range(2), repeat=2))
    matrices = tuple(((a, b), (c, d)) for a, b, c, d in product(range(3), repeat=4))
    tally = {key: 0 for key in ("majority_contexts", "candidate_losses", "truth_variants",
             "bijective_renamings", "refinement_contexts", "refinement_candidate_losses",
             "inherited_decoder_transports", "explicit_failure_control")}

    # This checks the failure path itself. It is not a mutation-coverage claim.
    try:
        require(False, "intentional validation control")
    except VerificationFailure as exc:
        if str(exc) != "intentional validation control":
            raise
        tally["explicit_failure_control"] += 1
    else:
        raise VerificationFailure("validation guard disappeared")

    for r, counts, old in product(maps, matrices, maps):
        p = make_problem(r, old, counts)
        result = fit(p)
        losses = {candidate: raw_loss(r, candidate, counts) for candidate in maps}
        best = min(losses.values())
        tally["candidate_losses"] += len(losses)
        # Of the minimizing decoders, require old answers at zero-evidence labels;
        # then take the first whole decoder in the fixed answer order.
        zero_labels = tuple(label for label in range(2)
                            if sum(sum(counts[u]) for u in range(2) if r[u] == label) == 0)
        admissible = tuple(candidate for candidate, loss in losses.items()
                           if loss == best and all(candidate[label] == old[label] for label in zero_labels))
        require(bool(admissible), "no admissible optimum")
        expected = tuple(str(x) for x in min(admissible))
        require(result.h == expected, f"wrong tie/zero/majority answer: {r, counts, old}")
        require(empirical_loss(p) == raw_loss(r, old, counts), "old empirical loss differs")
        require(empirical_loss(result) == best, "fitted decoder is not an optimum")
        require(minimum_empirical_loss(p) == best, "residual differs from brute optimum")
        require(empirical_loss(result) <= empirical_loss(p), "fit increased empirical loss")
        require(fit(result) == result, "fit is not idempotent")
        tally["majority_contexts"] += 1

        for truths in maps:
            variant = replace(p, f=tuple(str(x) for x in truths))
            fitted_variant = fit(variant)
            direct_predictions = tuple(int(result.h[r[u]]) for u in range(2))
            expected_errors = sum(direct_predictions[u] != truths[u] for u in range(2))
            require(fitted_variant.h == result.h, "truth leaked into fitting")
            require(truth_errors(fitted_variant) == expected_errors, "truth error differs")
            require(empirical_loss(fitted_variant) == best, "truth changed empirical loss")
            tally["truth_variants"] += 1

        for names in permutations(("opaque", "borrowed")):
            renamed = rename(p, names)
            require(predictions(renamed) == predictions(p), "renaming changed predictions")
            require(empirical_loss(renamed) == empirical_loss(p), "renaming changed empirical loss")
            require(truth_errors(renamed) == truth_errors(p), "renaming changed truth errors")
            require(fit(renamed) == rename(result, names), "fit and renaming did not commute")
            tally["bijective_renamings"] += 1

    for q, fine_r, counts in product(maps, maps, matrices):
        coarse_r = tuple(q[x] for x in fine_r)
        coarse_best = min(raw_loss(coarse_r, h, counts) for h in maps)
        fine_best = min(raw_loss(fine_r, h, counts) for h in maps)
        tally["refinement_candidate_losses"] += 2 * len(maps)
        require(fine_best <= coarse_best, "refinement increased attainable minimum")
        for old in maps:
            p = make_problem(coarse_r, old, counts)
            refined = refine(p, ("f0", "f1"), tuple(f"f{x}" for x in fine_r),
                             tuple(f"c{x}" for x in q))
            require(predictions(refined) == predictions(p), "transport changed predictions")
            require(empirical_loss(refined) == empirical_loss(p), "transport changed loss")
            require(truth_errors(refined) == truth_errors(p), "transport changed truth errors")
            require(minimum_empirical_loss(p) == coarse_best, "coarse minimum differs")
            require(minimum_empirical_loss(refined) == fine_best, "fine minimum differs")
            require(empirical_loss(fit(refined)) == fine_best, "fine fit differs from optimum")
            tally["inherited_decoder_transports"] += 1
        tally["refinement_contexts"] += 1

    expected = {"majority_contexts": 1296, "candidate_losses": 5184, "truth_variants": 5184,
                "bijective_renamings": 2592, "refinement_contexts": 1296,
                "refinement_candidate_losses": 10368, "inherited_decoder_transports": 5184,
                "explicit_failure_control": 1}
    require(tally == expected, f"enumeration incomplete: {tally}")
    return tally


def main() -> int:
    print(f"Python {platform.python_version()}; implementation={platform.python_implementation()}; optimize={sys.flags.optimize}", flush=True)
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_finite_language)
    result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)
    if not result.wasSuccessful():
        print("FAILED: focused tests")
        return 1
    try:
        tally = run_oracles()
    except VerificationFailure as exc:
        print(f"FAILED: exhaustive oracle: {exc}")
        return 1
    print("Oracle domains: |U|=|L|=|A|=2; each observation count in {0,1,2}.")
    print(json.dumps(tally, sort_keys=True))
    print(f"PASS: {result.testsRun} focused test methods and all declared bounded oracle domains.")
    print("These finite checks do not replace the general proofs in MODEL.zh-CN.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
