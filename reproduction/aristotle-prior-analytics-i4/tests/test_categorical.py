"""Independent pointwise oracle plus boundaries, directions, and output contracts."""
import dataclasses
import itertools
import json
import pathlib
import subprocess
import sys
import unittest

from categorical import (KINDS, MODES, Model, all_forms, analyze_form,
                         conclusion_holds, models, nonproductive_witnesses,
                         premises_hold, universal_witness)
from walkthrough import build_report, human_report

ROOT = pathlib.Path(__file__).resolve().parents[1]
PYTHON = [sys.executable] + (["-" + "O" * sys.flags.optimize] if sys.flags.optimize else [])


def oracle(support, kind, subject, predicate):
    """Pointwise truth, independent of the implementation's set operations."""
    bit = {"P": 4, "M": 2, "S": 1}
    pairs = [(bool(t & bit[subject]), bool(t & bit[predicate])) for t in support]
    if kind == "A":
        return all(not x or y for x, y in pairs)
    if kind == "E":
        return all(not (x and y) for x, y in pairs)
    if kind == "I":
        return any(x and y for x, y in pairs)
    if kind == "O":
        return any(x and not y for x, y in pairs)
    raise ValueError(kind)


def oracle_premises(support, pair):
    return oracle(support, pair[0], "M", "P") and oracle(support, pair[1], "S", "M")


class ModelValidationTests(unittest.TestCase):
    def test_singleton_bit_encoding(self):
        for value in range(8):
            m = Model((value,))
            self.assertEqual(m.extension("P"), frozenset({value}) if value >= 4 else frozenset())
            self.assertEqual(m.extension("M"), frozenset({value}) if value in (2, 3, 6, 7) else frozenset())
            self.assertEqual(m.extension("S"), frozenset({value}) if value % 2 else frozenset())

    def test_masks_exhaustive_roundtrip(self):
        for mask in range(1, 256):
            self.assertEqual(Model.from_mask(mask).mask, mask)
        self.assertEqual(Model.from_mask(255).support, tuple(range(8)))

    def test_support_container_boundaries(self):
        for value in ([1], {1}, frozenset({1}), "1", 1, None, iter([1])):
            with self.subTest(value=repr(value)), self.assertRaises(TypeError):
                Model(value)

    def test_empty_domain_rejected(self):
        with self.assertRaises(ValueError):
            Model(())

    def test_support_numeric_type_boundaries(self):
        class MyInt(int):
            pass
        for value in (False, True, 1.0, "1", None, MyInt(1)):
            with self.subTest(value=repr(value)), self.assertRaises(TypeError):
                Model((value,))

    def test_support_range_and_order(self):
        for support in ((-1,), (8,), (256,), (1, 1), (2, 1), (0, 7, 3)):
            with self.subTest(support=support), self.assertRaises(ValueError):
                Model(support)

    def test_mask_numeric_boundaries(self):
        for value in (False, True, 1.0, "1", None):
            with self.subTest(value=value), self.assertRaises(TypeError):
                Model.from_mask(value)
        for value in (-1, 0, 256, 10**30):
            with self.subTest(value=value), self.assertRaises(ValueError):
                Model.from_mask(value)

    def test_immutable_model(self):
        m = Model((7,))
        with self.assertRaises(dataclasses.FrozenInstanceError):
            m.support = (1,)
        self.assertEqual(hash(m), hash(Model((7,))))

    def test_kind_string_and_substring_boundaries(self):
        m = Model((0,))
        for bad in ("", "AE", "a", " A", "O ", "X"):
            for call in (lambda: m.holds(bad, "S", "P"),
                         lambda: premises_hold(m, "I", bad),
                         lambda: analyze_form("A", "A", bad)):
                with self.subTest(bad=bad), self.assertRaises(ValueError):
                    call()
        for bad in (True, 1, None, ["A"]):
            with self.subTest(bad=bad), self.assertRaises(TypeError):
                m.holds(bad, "S", "P")

    def test_term_boundaries(self):
        m = Model((7,))
        for bad in ("", "PM", "p", "U"):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                m.extension(bad)
        for bad in (True, 4, None, ["P"]):
            with self.subTest(bad=bad), self.assertRaises(TypeError):
                m.extension(bad)

    def test_mode_boundaries(self):
        for bad in ("", "nonempty", "EMPTY-ALLOWED", "empty"):
            for call in (lambda: models(bad), lambda: all_forms(mode=bad),
                         lambda: Model((7,)).admitted(bad),
                         lambda: nonproductive_witnesses(mode=bad)):
                with self.subTest(bad=bad), self.assertRaises(ValueError):
                    call()
        for bad in (False, 0, None, ["empty-allowed"]):
            with self.subTest(bad=bad), self.assertRaises(TypeError):
                models(bad)

    def test_boolean_direction_is_strict(self):
        for bad in (0, 1, "false", None, [], (True,)):
            for call in (lambda: conclusion_holds(Model((7,)), "A", reverse=bad),
                         lambda: analyze_form("A", "A", "A", reverse=bad),
                         lambda: all_forms(reverse=bad)):
                with self.subTest(bad=bad), self.assertRaises(TypeError):
                    call()

    def test_model_argument_and_witness_boundaries(self):
        for bad in (None, (7,), {"support": [7]}, True):
            with self.assertRaises(TypeError):
                premises_hold(bad, "A", "A")
            with self.assertRaises(TypeError):
                conclusion_holds(bad, "A")
        for bad in ("I", "O", "", "AE"):
            with self.assertRaises(ValueError):
                universal_witness("A", "A", bad)


class SemanticTests(unittest.TestCase):
    def test_enumeration_complete_and_unique(self):
        values = models()
        self.assertEqual(len(values), 255)
        self.assertEqual({m.mask for m in values}, set(range(1, 256)))
        nonempty = models("all-nonempty")
        self.assertEqual(len(nonempty), 218)
        self.assertEqual(set(nonempty), {m for m in values
                                        if all(any(t & b for t in m.support) for b in (4, 2, 1))})

    def test_enumeration_cardinality_then_lexicographic(self):
        for mode in MODES:
            keys = [(len(m.support), m.support) for m in models(mode)]
            self.assertEqual(keys, sorted(keys))
        self.assertEqual(models()[0], Model((0,)))
        self.assertEqual(models("all-nonempty")[0], Model((7,)))

    def test_atomic_truth_against_independent_oracle(self):
        for m in models():
            for kind, subject, predicate in itertools.product(KINDS, "PMS", "PMS"):
                self.assertEqual(m.holds(kind, subject, predicate),
                                 oracle(m.support, kind, subject, predicate),
                                 (m.support, kind, subject, predicate))

    def test_complement_pairs_and_empty_vacuity(self):
        for m in models():
            for subject, predicate in itertools.product("PMS", repeat=2):
                self.assertNotEqual(m.holds("A", subject, predicate), m.holds("O", subject, predicate))
                self.assertNotEqual(m.holds("E", subject, predicate), m.holds("I", subject, predicate))
        empty = Model((0,))
        self.assertEqual([empty.holds(k, "S", "P") for k in KINDS], [True, True, False, False])

    def test_symmetry_and_direction(self):
        for m in models():
            for kind in "EI":
                self.assertEqual(m.holds(kind, "P", "S"), m.holds(kind, "S", "P"))
        m = Model((4, 7))
        self.assertTrue(m.holds("A", "S", "P"))
        self.assertFalse(m.holds("A", "P", "S"))
        self.assertFalse(m.holds("O", "S", "P"))
        self.assertTrue(m.holds("O", "P", "S"))

    def test_all_premise_pairs_have_models(self):
        for mode in MODES:
            for pair in itertools.product(KINDS, repeat=2):
                expected = sum(oracle_premises(m.support, pair) for m in models(mode))
                self.assertGreater(expected, 0)
                self.assertEqual(analyze_form(*pair, "A", mode=mode).premise_model_count, expected)

    def test_exact_forward_classification(self):
        expected = {"empty-allowed": {"AAA", "AII", "EAE", "EIO"},
                    "all-nonempty": {"AAA", "AAI", "AII", "EAE", "EAO", "EIO"}}
        for mode in MODES:
            results = all_forms(mode=mode)
            self.assertEqual(len(results), 64)
            self.assertEqual([r.form for r in results], ["".join(f) for f in itertools.product(KINDS, repeat=3)])
            self.assertEqual({r.form for r in results if r.valid}, expected[mode])

    def test_exact_reverse_classification(self):
        expected = {"empty-allowed": {"AII", "EAE", "IEO"},
                    "all-nonempty": {"AAI", "AEO", "AII", "EAE", "EAO", "IEO"}}
        for mode in MODES:
            self.assertEqual({r.form for r in all_forms(mode=mode, reverse=True) if r.valid}, expected[mode])

    def test_all_countermodels_independently_and_minimal(self):
        for mode, reverse in itertools.product(MODES, (False, True)):
            subject, predicate = ("P", "S") if reverse else ("S", "P")
            universe = models(mode)
            for result in all_forms(mode=mode, reverse=reverse):
                failures = [m for m in universe if oracle_premises(m.support, result.form[:2])
                            and not oracle(m.support, result.form[2], subject, predicate)]
                self.assertEqual(result.countermodel, failures[0] if failures else None,
                                 (mode, reverse, result.form))
                self.assertEqual(result.valid, not failures)

    def test_nonproductive_pairs_have_two_nonvacuous_witnesses(self):
        expected_pairs = {"AE", "AO", "EE", "EO", "IA", "IE", "II", "IO", "OA", "OE", "OI", "OO"}
        for mode in MODES:
            rows = nonproductive_witnesses(mode=mode)
            self.assertEqual({row["pair"] for row in rows}, expected_pairs)
            for row in rows:
                for kind in "AE":
                    data = row[kind + "_SP_witness"]
                    self.assertIsNotNone(data)
                    support = tuple(data["support"])
                    self.assertTrue(any(t & 1 for t in support))
                    self.assertTrue(oracle_premises(support, row["pair"]))
                    self.assertTrue(oracle(support, kind, "S", "P"))
                    expected = next(m for m in models(mode) if any(t & 1 for t in m.support)
                                    and oracle_premises(m.support, row["pair"])
                                    and oracle(m.support, kind, "S", "P"))
                    self.assertEqual(support, expected.support)

    def test_witness_absence_and_existential_weakening(self):
        self.assertIsNone(universal_witness("E", "A", "A"))
        self.assertIsNone(universal_witness("A", "A", "E"))
        for form in ("AAI", "EAO"):
            self.assertFalse(analyze_form(*form).valid)
            self.assertEqual(analyze_form(*form).countermodel, Model((0,)))
            self.assertTrue(analyze_form(*form, mode="all-nonempty").valid)

    def test_ie_reverse_does_not_supply_forward_conclusion(self):
        for mode in MODES:
            self.assertTrue(analyze_form("I", "E", "O", mode=mode, reverse=True).valid)
            self.assertFalse(any(analyze_form("I", "E", c, mode=mode).valid for c in KINDS))
        m = Model((1, 6))
        self.assertTrue(premises_hold(m, "I", "E"))
        self.assertTrue(conclusion_holds(m, "O", reverse=True))
        self.assertFalse(conclusion_holds(m, "I"))

    def test_support_compression_preserves_repeated_individuals(self):
        # Finite checks illustrate (but do not replace) the arbitrary-domain proof.
        for size in range(1, 4):
            for individual_types in itertools.product(range(8), repeat=size):
                compressed = Model(tuple(sorted(set(individual_types))))
                for kind, subject, predicate in itertools.product(KINDS, "PMS", "PMS"):
                    self.assertEqual(oracle(individual_types, kind, subject, predicate),
                                     compressed.holds(kind, subject, predicate))


class OutputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = build_report()

    def test_serialization_stable_and_schema(self):
        self.assertEqual(json.loads(json.dumps(self.report)), self.report)
        self.assertEqual(self.report, build_report())
        for mode in MODES:
            self.assertEqual(len(self.report["forms"][mode]), 64)
            self.assertEqual(len(self.report["reverse_forms"][mode]), 64)
            for row in self.report["forms"][mode]:
                self.assertEqual(row["valid"], row["minimal_countermodel"] is None)
                self.assertEqual(row["direction"], "S->P")

    def test_model_serialization(self):
        self.assertEqual(Model((0, 3, 6)).as_dict(), {
            "support": [0, 3, 6], "type_bits_PMS": ["000", "011", "110"],
            "cardinality": 3, "mask": 73, "U": [0, 3, 6],
            "P": [6], "M": [3, 6], "S": [3]})

    def test_pair_table_and_human_column_order(self):
        rows = self.report["premise_pair_table"]
        self.assertEqual(len(rows), 16)
        for row in rows:
            for mode, reverse in itertools.product(MODES, (False, True)):
                expected = "".join(c for c in KINDS
                                   if analyze_form(*row["pair"], c, mode=mode, reverse=reverse).valid)
                self.assertEqual(row[mode + ("_reverse" if reverse else "_forward")], expected)
        self.assertIn("AA | A | A | AI | 无 | I\n", human_report(self.report))
        self.assertIn("EI | O | O | O | 无 | 无\n", human_report(self.report))

    def test_cli_json_and_human(self):
        for fmt in ("json", "human"):
            process = subprocess.run(PYTHON + [str(ROOT / "walkthrough.py"), "--format", fmt],
                                     text=True, capture_output=True, check=True)
            self.assertEqual(process.stderr, "")
            if fmt == "json":
                self.assertEqual(json.loads(process.stdout), self.report)
            else:
                self.assertEqual(process.stdout, human_report(self.report))

    def test_cli_csv_shapes(self):
        import csv
        import io
        for fmt, count in (("pairs-csv", 16), ("forms-csv", 128)):
            process = subprocess.run(PYTHON + [str(ROOT / "walkthrough.py"), "--format", fmt],
                                     text=True, capture_output=True, check=True)
            self.assertEqual(len(list(csv.DictReader(io.StringIO(process.stdout)))), count)

    def test_cli_rejects_unknown_format(self):
        process = subprocess.run(PYTHON + [str(ROOT / "walkthrough.py"), "--format", "yaml"],
                                 text=True, capture_output=True)
        self.assertEqual(process.returncode, 2)
        self.assertIn("invalid choice", process.stderr)


if __name__ == "__main__":
    unittest.main()
