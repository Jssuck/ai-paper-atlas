"""Focused behavioral and validation tests; unittest checks survive -O/-OO."""
from dataclasses import FrozenInstanceError, replace
import unittest
from examples import cases
from finite_language import (Problem, empirical_loss, fit, label_counts,
                             minimum_empirical_loss, predictions, refine, rename, truth_errors)


def base() -> Problem:
    return Problem(("u", "v"), ("c", "d"), ("no", "yes"),
                   ("c", "c"), ("no", "yes"), ("yes", "no"), ((0, 3), (2, 0)))


class FiniteLanguageTests(unittest.TestCase):
    def test_weighted_majority(self):
        p = base()
        self.assertEqual(fit(p).h, ("yes", "yes"))
        self.assertEqual(empirical_loss(p), 3)
        self.assertEqual(empirical_loss(fit(p)), 2)

    def test_residual_from_conflicting_cell(self):
        self.assertEqual(minimum_empirical_loss(base()), 2)
        self.assertEqual(label_counts(base()), ((2, 3), (0, 0)))

    def test_positive_tie_uses_declared_order_not_lexicographic_order(self):
        p = Problem(("u",), ("c",), ("z", "a", "m"), ("c",), ("a",), ("a",), ((2, 2, 1),))
        self.assertEqual(fit(p).h, ("z",))
        self.assertEqual(empirical_loss(fit(p)), 3)

    def test_zero_evidence_preserves_old_decoder(self):
        p = replace(base(), counts=((0, 0), (0, 0)))
        self.assertEqual(fit(p).h, p.h)
        self.assertEqual(minimum_empirical_loss(p), 0)

    def test_unused_label_preserves_old_decoder(self):
        self.assertEqual(fit(base()).h[1], "yes")

    def test_empty_universe(self):
        p = Problem((), ("unused",), ("no", "yes"), (), ("yes",), (), ())
        self.assertEqual(fit(p), p)
        self.assertEqual(predictions(p), ())
        self.assertEqual((empirical_loss(p), minimum_empirical_loss(p), truth_errors(p)), (0, 0, 0))

    def test_one_answer(self):
        p = Problem(("u",), ("c",), ("only",), ("c",), ("only",), ("only",), ((7,),))
        self.assertEqual(fit(p), p)
        self.assertEqual(empirical_loss(p), 0)

    def test_large_integer_counts_are_exact(self):
        n = 10**40
        p = replace(base(), counts=((n, n + 1), (0, 0)))
        self.assertEqual(fit(p).h[0], "yes")
        self.assertEqual(minimum_empirical_loss(p), n)

    def test_truth_does_not_enter_fit(self):
        p = base()
        self.assertEqual(fit(p).h, fit(replace(p, f=("no", "yes"))).h)

    def test_fit_is_idempotent(self):
        self.assertEqual(fit(fit(base())), fit(base()))

    def test_joint_renaming(self):
        p = base()
        q = rename(p, ("d", "c"))
        self.assertEqual(q.r, ("d", "d"))
        self.assertEqual(predictions(p), predictions(q))
        self.assertEqual(fit(q), rename(fit(p), ("d", "c")))
        self.assertEqual(empirical_loss(p), empirical_loss(q))
        self.assertEqual(truth_errors(p), truth_errors(q))

    def test_refinement_transports_then_fit_improves(self):
        p = fit(base())
        q = refine(p, ("one", "two"), ("one", "two"), ("c", "c"))
        self.assertEqual(predictions(q), predictions(p))
        self.assertEqual(empirical_loss(q), 2)
        self.assertEqual(empirical_loss(fit(q)), 0)

    def test_refinement_can_have_more_than_two_labels(self):
        p = Problem(("u", "v", "w"), ("c",), ("a", "b", "c"),
                    ("c", "c", "c"), ("a",), ("a", "b", "c"), ((1, 0, 0), (0, 1, 0), (0, 0, 1)))
        q = refine(p, ("x", "y", "z"), ("x", "y", "z"), ("c", "c", "c"))
        self.assertEqual(minimum_empirical_loss(p), 2)
        self.assertEqual(minimum_empirical_loss(q), 0)

    def test_names_do_not_guarantee_accuracy(self):
        wrong, right = (p for _, p in cases()["01_names_are_not_accuracy"])
        self.assertEqual((truth_errors(wrong), truth_errors(right)), (2, 0))

    def test_empirical_improvement_can_worsen_universe_truth(self):
        old, new = (p for _, p in cases()["03_unseen_regression"])
        self.assertEqual((empirical_loss(old), empirical_loss(new)), (3, 0))
        self.assertEqual((truth_errors(old), truth_errors(new)), (1, 2))
        self.assertEqual(predictions(old)[1:], ("0", "0"))
        self.assertEqual(predictions(new)[1:], ("1", "1"))

    def test_noise_can_reinforce_falsehood(self):
        old, new, corrected = (p for _, p in cases()["05_noisy_observation"])
        self.assertEqual((empirical_loss(old), empirical_loss(new)), (4, 0))
        self.assertEqual((truth_errors(old), truth_errors(new), truth_errors(corrected)), (0, 1, 0))

    def test_unchanged_decoder_is_not_transport(self):
        old, unchanged, transported, fitted = (p for _, p in cases()["06_unchanged_is_not_transport"])
        self.assertEqual([empirical_loss(p) for p in (old, unchanged, transported, fitted)], [0, 1, 0, 0])

    def test_bad_fine_decoder_can_worsen_empirical_loss(self):
        stages = dict(cases()["02_conflict_and_refinement"])
        self.assertEqual(empirical_loss(stages["fit_coarse"]), 2)
        self.assertEqual(empirical_loss(stages["bad_fine_decoder"]), 5)
        self.assertEqual(minimum_empirical_loss(stages["bad_fine_decoder"]), 0)

    def test_invalid_domains_rejected(self):
        for patch in ({"objects": ("u", "u")}, {"labels": ()}, {"answers": ()},
                      {"labels": ("c", "c")}, {"answers": ("no", "no")},
                      {"objects": ["u", "v"]}, {"labels": ("", "d")}, {"answers": ("no", 1)}):
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                replace(base(), **patch)

    def test_invalid_maps_rejected(self):
        for patch in ({"r": ("c",)}, {"r": ("c", "missing")}, {"h": ("no",)},
                      {"h": ("no", "missing")}, {"f": ("no", "missing")}, {"f": ["no", "yes"]}):
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                replace(base(), **patch)

    def test_invalid_counts_rejected(self):
        for counts in (((0, 1),), ((0, 1, 2), (0, 0)), ((-1, 2), (0, 0)),
                       ((True, 2), (0, 0)), ((1.0, 2), (0, 0)), [[0, 1], [0, 0]], ([0, 1], (0, 0))):
            with self.subTest(counts=counts), self.assertRaises(ValueError):
                replace(base(), counts=counts)

    def test_invalid_renamings_rejected(self):
        for labels in (("a",), ("a", "a"), ["a", "b"]):
            with self.subTest(labels=labels), self.assertRaises(ValueError):
                rename(base(), labels)

    def test_invalid_refinements_rejected(self):
        for new_r, parents in ((("x", "y"), ("c", "d")),
                               (("x", "missing"), ("c", "c")),
                               (("x", "y"), ("c",)), (("x", "y"), ("c", "missing"))):
            with self.subTest(new_r=new_r, parents=parents), self.assertRaises(ValueError):
                refine(base(), ("x", "y"), new_r, parents)

    def test_problem_does_not_mutate_inputs(self):
        p = base()
        fit(p)
        self.assertEqual(p.h, ("no", "yes"))
        with self.assertRaises(FrozenInstanceError):
            p.h = ("yes", "no")


if __name__ == "__main__":
    unittest.main(verbosity=2)
