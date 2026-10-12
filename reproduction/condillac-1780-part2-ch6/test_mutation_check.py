import unittest
import mutation_check as mutation


class HarnessClassificationTests(unittest.TestCase):
    def test_behavior_mismatch_is_detected(self):
        def mismatch():
            mutation.check_equal(0, 1)
        self.assertEqual(mutation.classify(mismatch)[0], "behavior_mismatch")

    def test_unexpected_exception_is_not_detection(self):
        def broken_probe():
            raise RuntimeError("test-only simulated harness failure")
        self.assertEqual(mutation.classify(broken_probe)[0], "harness_error")

    def test_passing_probe_is_not_detection(self):
        self.assertEqual(mutation.classify(lambda: None), ("pass", ""))


if __name__ == "__main__":
    unittest.main()
