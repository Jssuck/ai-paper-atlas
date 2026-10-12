"""Author tests, including bounded exhaustive checks; not independent validation."""
import itertools
import math
import unittest
from model import Language, pack, unpack, version_space


def tiny_language():
    return Language({"agent": ("A", "B"), "patient": ("A", "B"), "act": ("help", "avoid")},
                    (("agent", "act"), ("patient", "act")))


def oracle_orders(labels, edges):
    return tuple(order for order in itertools.permutations(labels)
                 if all(order.index(a) < order.index(b) for a, b in edges))


def oracle_candidates(language, prefix):
    codes = dict(language.lexicon)
    labels = tuple(feature for feature, _ in language.schema)
    result = set()
    for values in itertools.product(*(domain for _, domain in language.schema)):
        assignment = dict(zip(labels, values))
        for order in oracle_orders(labels, language.edges):
            observed = tuple(codes[(feature, assignment[feature])] for feature in order)
            if observed[:len(prefix)] == prefix:
                result.add(values)
    return frozenset(result)


class LanguageTests(unittest.TestCase):
    def test_context_order_set(self):
        self.assertEqual(set(tiny_language().orders),
                         {("agent", "patient", "act"), ("patient", "agent", "act")})

    def test_round_trip_alternate_order(self):
        language = tiny_language()
        for order in language.orders:
            self.assertEqual(language.decode(pack(language.encode(("A", "B", "help"), order))),
                             ("A", "B", "help"))

    def test_prefix_counts(self):
        language = tiny_language()
        tokens = language.encode(("A", "B", "help"), language.orders[0])
        self.assertEqual([len(language.candidates(tokens[:k])) for k in range(4)], [8, 4, 2, 1])

    def test_true_message_remains(self):
        language = tiny_language()
        message = ("A", "B", "help")
        tokens = language.encode(message, language.orders[0])
        for k in range(4):
            self.assertIn(message, language.candidates(tokens[:k]))

    def test_unlabeled_collision(self):
        language = tiny_language()
        self.assertEqual(language.aggregate(("A", "B", "help")),
                         language.aggregate(("B", "A", "help")))
        self.assertNotEqual(language.labeled(("A", "B", "help")),
                            language.labeled(("B", "A", "help")))

    def test_aggregate_keeps_multiplicity(self):
        self.assertEqual(tiny_language().aggregate(("A", "A", "help")), (("A", 2), ("help", 1)))

    def test_colliding_dictionary(self):
        language = Language({"x": ("0", "1")}, lexicon={("x", "0"): "?", ("x", "1"): "?"})
        self.assertFalse(language.injective)
        self.assertEqual(language.candidates(("?",)), frozenset({("0",), ("1",)}))
        with self.assertRaises(ValueError):
            language.decode(pack(("?",)))

    def test_injectivity_is_sufficient_not_necessary(self):
        language = Language({"x": ("0",), "y": ("0",)}, lexicon={("x", "0"): "?", ("y", "0"): "?"})
        self.assertFalse(language.injective)
        self.assertEqual(language.decode(pack(("?", "?"))), ("0", "0"))

    def test_framing_distinguishes_boundaries(self):
        self.assertNotEqual(pack(("a", "bc")), pack(("ab", "c")))
        self.assertEqual("".join(("a", "bc")), "".join(("ab", "c")))

    def test_framing_special_characters(self):
        tokens = ("", '"', "\\", "[x,y]", "\n", "动作", "] , [")
        self.assertEqual(unpack(pack(tokens)), tokens)

    def test_impossible_prefixes(self):
        language = tiny_language()
        tokens = language.encode(("A", "B", "help"), language.orders[0])
        for prefix in (("unknown",), tokens + (tokens[0],), (tokens[2],), (tokens[0], tokens[0])):
            self.assertEqual(language.candidates(prefix), frozenset())

    def test_complete_coverage_required(self):
        language = tiny_language()
        tokens = language.encode(("A", "B", "help"), language.orders[0])
        with self.assertRaises(ValueError):
            language.decode(pack(tokens[:2]))

    def test_invalid_order(self):
        language = tiny_language()
        for order in (("act", "agent", "patient"), ("agent",), ("agent", "agent", "act")):
            with self.assertRaises(ValueError):
                language.encode(("A", "B", "help"), order)

    def test_invalid_schema(self):
        for schema in ({}, {"": ("x",)}, {"a": ()}, {"a": "xy"}, {"a": ("x", "x")},
                       {"a": ("",)}, {"a": (2,)}, {3: ("x",)}):
            with self.subTest(schema=schema), self.assertRaises(ValueError):
                Language(schema)

    def test_invalid_edges(self):
        for edges in ((("a", "a"),), (("a", "z"),), (("a", "b"), ("b", "a")),
                      ("ab",), (("a",),), ((1, "a"),)):
            with self.subTest(edges=edges), self.assertRaises(ValueError):
                Language({"a": ("0",), "b": ("0",)}, edges)

    def test_invalid_dictionary(self):
        for codes in ({}, {("a", "0"): 0}, {("a", "0"): "0", ("b", "0"): "1"}):
            with self.assertRaises(ValueError):
                Language({"a": ("0",)}, lexicon=codes)

    def test_invalid_messages(self):
        language = tiny_language()
        for message in ((), ("A", "B"), ("A", "B", "wrong"), "ABhelp", ("A", "B", 1)):
            with self.assertRaises(ValueError):
                language.labeled(message)

    def test_invalid_frames(self):
        for wire in ("", "{}", '"a"', "[1]", "[null]", '["a",]', 1):
            with self.assertRaises(ValueError):
                unpack(wire)
        with self.assertRaises(ValueError):
            pack("abc")
        with self.assertRaises(ValueError):
            pack((1,))

    def test_input_snapshots(self):
        domain = ["0", "1"]
        schema = {"a": domain}
        codes = {("a", "0"): "zero", ("a", "1"): "one"}
        language = Language(schema, lexicon=codes)
        domain.append("2")
        codes[("a", "0")] = "changed"
        self.assertEqual(language.messages(), (("0",), ("1",)))
        self.assertEqual(language.encode(("0",), ("a",)), ("zero",))

    def test_non_strict_shrinkage(self):
        language = Language({"x": ("only",), "y": ("0", "1")}, (("x", "y"),))
        tokens = language.encode(("only", "0"), language.orders[0])
        self.assertEqual(language.candidates(()), language.candidates(tokens[:1]))

    def test_false_observation_can_exclude_truth(self):
        language = Language({"x": ("0", "1")})
        self.assertNotIn(("0",), language.candidates(language.encode(("1",), ("x",))))

    def test_analogy_underdetermination(self):
        hypotheses = (("0", "1", "2"), ("0", "1", "4"), ("1", "2", "3"))
        remaining = version_space(hypotheses, ((0, "0"), (1, "1")))
        self.assertEqual({h[2] for h in remaining}, {"2", "4"})
        self.assertEqual(version_space((hypotheses[0], hypotheses[2]), ((0, "0"), (1, "1"))),
                         frozenset({hypotheses[0]}))

    def test_all_analogy_examples_applied(self):
        self.assertEqual(version_space((("0", "0"), ("0", "1")), ((0, "0"), (1, "1"))),
                         frozenset({("0", "1")}))

    def test_invalid_analogy_input(self):
        for hypotheses, examples in (((), ()), (((),), ()), ((("0",), ("0", "1")), ()),
                                     ((("0",),), ((True, "0"),)), ((("0",),), ((1, "0"),)),
                                     ((("0",),), ((0, 1),)), ((("0",),), ((0,),))):
            with self.assertRaises(ValueError):
                version_space(hypotheses, examples)

    def test_contradictory_examples(self):
        self.assertEqual(version_space((("0",), ("1",)), ((0, "0"), (0, "1"))), frozenset())

    def test_exhaustive_binary_schemas_through_three_features(self):
        dag_count = encoding_count = prefix_count = 0
        for n in range(1, 4):
            labels = tuple(f"f{i}" for i in range(n))
            possible_edges = tuple(itertools.permutations(labels, 2))
            for flags in itertools.product((False, True), repeat=len(possible_edges)):
                edges = tuple(edge for edge, flag in zip(possible_edges, flags) if flag)
                orders = oracle_orders(labels, edges)
                if not orders:
                    continue
                dag_count += 1
                language = Language({f: ("0", "1") for f in labels}, edges)
                self.assertEqual(set(language.orders), set(orders))
                for message in language.messages():
                    for order in orders:
                        encoding_count += 1
                        tokens = language.encode(message, order)
                        self.assertEqual(language.decode(pack(tokens)), message)
                        previous = language.candidates(())
                        for k in range(n + 1):
                            prefix_count += 1
                            current = language.candidates(tokens[:k])
                            self.assertEqual(current, oracle_candidates(language, tokens[:k]))
                            self.assertIn(message, current)
                            self.assertLessEqual(current, previous)
                            self.assertEqual(len(current), 2 ** (n - k))
                            previous = current
        self.assertEqual((dag_count, encoding_count, prefix_count), (29, 402, 1588))

    def test_exhaustive_colliding_lexicons(self):
        atoms = (("a", "0"), ("a", "1"), ("b", "0"), ("b", "1"))
        checks = 0
        for words in itertools.product(("x", "y", "z"), repeat=4):
            language = Language({"a": ("0", "1"), "b": ("0", "1")}, lexicon=dict(zip(atoms, words)))
            for k in range(4):
                for prefix in itertools.product(("x", "y", "z"), repeat=k):
                    checks += 1
                    actual = language.candidates(prefix)
                    self.assertEqual(actual, oracle_candidates(language, prefix))
                    if prefix:
                        self.assertLessEqual(actual, language.candidates(prefix[:-1]))
        self.assertEqual(checks, 3240)

    def test_heterogeneous_domain_count(self):
        language = Language({"a": ("0",), "b": ("0", "1"), "c": ("0", "1", "2")})
        for message in language.messages():
            for order in language.orders:
                tokens = language.encode(message, order)
                sizes = dict((feature, len(domain)) for feature, domain in language.schema)
                for k in range(4):
                    self.assertEqual(len(language.candidates(tokens[:k])),
                                     math.prod(sizes[feature] for feature in order[k:]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
