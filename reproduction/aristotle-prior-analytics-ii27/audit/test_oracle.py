"""Independent oracle checks, including deliberately corrupted producer results."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from independent_oracle import pointwise, possible_pairings, validate


class OracleTests(unittest.TestCase):
    def test_second_nonempty_counterexample(self):
        self.assertEqual(pointwise((1, 1), (1, 0), (0, 1))[1], (True, False))

    def test_third_overreach(self):
        values = pointwise((1, 0), (1, 1), (1, 0))
        self.assertEqual(values[2], (True, True))
        self.assertEqual(values[3], (True, False))

    def test_empty_not_a_witness(self):
        values = pointwise((), (), ())
        self.assertEqual(values[2], (False, False))
        self.assertEqual(values[4], (True, False))

    def test_observation_ambiguity(self):
        self.assertEqual(possible_pairings([]), [[0, 1], [1, 0]])
        self.assertEqual(possible_pairings([(1, 1, 1, 1)]), [[0, 1], [1, 0]])
        self.assertEqual(possible_pairings([(1, 0, 1, 0)]), [[0, 1]])
        self.assertEqual(possible_pairings([(1, 0, 1, 0), (1, 0, 0, 1)]), [])

    def test_known_good_and_mutations(self):
        source = Path(__file__).resolve().parent.parent / 'logs/results-normal.json'
        self.assertEqual(validate(source)['status'], 'PASS')
        original = json.loads(source.read_text())
        mutations = []
        bad = copy.deepcopy(original); bad['routes']['first']['countermodels'] = 1; mutations.append(bad)
        bad = copy.deepcopy(original); bad['routes']['second_affirmative']['first_countermodel']['A'] = 0; mutations.append(bad)
        bad = copy.deepcopy(original); bad['identification']['separated_mappings'] = []; mutations.append(bad)
        bad = copy.deepcopy(original); bad['identification']['rows']['separated'][1][0] = False; mutations.append(bad)
        bad = copy.deepcopy(original); bad['majority']['universal'] = True; mutations.append(bad)
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / 'mutant.json'
            for data in mutations:
                target.write_text(json.dumps(data))
                with self.assertRaises(RuntimeError):
                    validate(target)


if __name__ == '__main__':
    unittest.main()
