"""Hand-sized invented examples; no claims about real etymology or psychology."""
from dataclasses import replace
from finite_language import Problem, fit, refine, rename


def cases() -> dict[str, tuple[tuple[str, Problem], ...]]:
    transparent = Problem(
        ("red-object", "blue-object"), ("red-origin", "blue-origin"), ("red", "blue"),
        ("red-origin", "blue-origin"), ("blue", "red"), ("red", "blue"), ((1, 0), (0, 1)))
    opaque = rename(replace(transparent, h=("red", "blue")), ("xi", "borrowed-symbol"))
    coarse = Problem(
        ("hot-object", "cold-object"), ("same",), ("cold", "hot"),
        ("same", "same"), ("cold",), ("hot", "cold"), ((0, 3), (2, 0)))
    coarse_fit = fit(coarse)
    fine = refine(coarse_fit, ("one", "two"), ("one", "two"), ("same", "same"))
    unseen = Problem(
        ("seen", "unseen-1", "unseen-2"), ("shared",), ("0", "1"),
        ("shared", "shared", "shared"), ("0",), ("1", "0", "0"),
        ((0, 3), (0, 0), (0, 0)))
    tied = Problem(
        ("left", "right", "unseen"), ("tied", "empty"), ("0", "1"),
        ("tied", "tied", "empty"), ("1", "1"), ("0", "1", "1"),
        ((1, 0), (0, 1), (0, 0)))
    noisy = Problem(
        ("object",), ("label",), ("no", "yes"), ("label",), ("no",), ("no",), ((0, 4),))
    reused = Problem(
        ("u", "v"), ("left", "right"), ("no", "yes"),
        ("left", "left"), ("no", "yes"), ("no", "no"), ((1, 0), (1, 0)))
    unchanged = replace(reused, r=("left", "right"))
    transported = refine(reused, reused.labels, ("left", "right"), ("left", "left"))
    return {
        "01_names_are_not_accuracy": (("transparent_wrong", transparent), ("opaque_correct", opaque)),
        "02_conflict_and_refinement": (("old", coarse), ("fit_coarse", coarse_fit),
            ("transport_fine", fine), ("fit_fine", fit(fine)),
            ("bad_fine_decoder", replace(fine, h=("cold", "hot")))),
        "03_unseen_regression": (("old", unseen), ("fit", fit(unseen))),
        "04_tie_and_zero_evidence": (("old", tied), ("fit", fit(tied))),
        "05_noisy_observation": (("old", noisy), ("fit", fit(noisy)),
            ("corrected_observations_fit", fit(replace(noisy, counts=((4, 0),))))),
        "06_unchanged_is_not_transport": (("old", reused), ("unchanged_h", unchanged),
            ("transport_h", transported), ("refit", fit(unchanged))),
        "07_bijective_renaming": (("original", coarse_fit),
            ("renamed", rename(coarse_fit, ("foreign-looking-token",)))),
    }
