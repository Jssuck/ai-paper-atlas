import unittest

from enumerate_model import census
from model import Branch, Leaf, display, evaluate, generate_trees, leaf_bag, leaf_count, ordered_leaves, parse, serialize, validate_tree


class ModelTests(unittest.TestCase):
    def test_leaf_exact_integers(self):
        for value in (0, -1, 2, 10 ** 100):
            self.assertEqual(evaluate(Leaf(value)), value)
        for value in (True, False, 1.0, "1", None):
            with self.subTest(value=value), self.assertRaises(TypeError):
                Leaf(value)

    def test_branch_validation(self):
        for op in ("MUL", "add", "", "LEAF"):
            with self.subTest(op=op), self.assertRaises(ValueError):
                Branch(op, Leaf(0), Leaf(1))
        for op in (None, True, 1):
            with self.subTest(op=op), self.assertRaises(TypeError):
                Branch(op, Leaf(0), Leaf(1))
        for child in (0, ("LEAF", 0), None, [Leaf(0)]):
            with self.subTest(child=child), self.assertRaises(TypeError):
                Branch("ADD", child, Leaf(0))
            with self.subTest(child=child), self.assertRaises(TypeError):
                Branch("ADD", Leaf(0), child)

    def test_exact_round_trip_and_side_order(self):
        tree = Branch("SUB", Leaf(2), Branch("ADD", Leaf(0), Leaf(1)))
        prefix = (("SUB",), ("LEAF", 2), ("ADD",), ("LEAF", 0), ("LEAF", 1))
        self.assertEqual(serialize(tree), prefix)
        self.assertEqual(parse(prefix), tree)
        self.assertEqual(serialize(parse(prefix)), prefix)
        self.assertEqual(ordered_leaves(tree), (2, 0, 1))
        self.assertEqual(leaf_bag(tree), (0, 1, 2))
        self.assertEqual(evaluate(tree), 1)
        self.assertEqual(display(tree), "(2 - (0 + 1))")
        self.assertEqual(leaf_count(tree), 3)

    def test_operator_and_order_loss(self):
        a = Branch("ADD", Leaf(0), Leaf(1))
        b = Branch("SUB", Leaf(0), Leaf(1))
        c = Branch("SUB", Leaf(1), Leaf(0))
        self.assertEqual(ordered_leaves(a), ordered_leaves(b))
        self.assertNotEqual(evaluate(a), evaluate(b))
        self.assertEqual(leaf_bag(b), leaf_bag(c))
        self.assertNotEqual(ordered_leaves(b), ordered_leaves(c))
        self.assertEqual((evaluate(b), evaluate(c)), (-1, 1))

    def test_bracketing_loss(self):
        left = Branch("SUB", Branch("SUB", Leaf(0), Leaf(0)), Leaf(1))
        right = Branch("SUB", Leaf(0), Branch("SUB", Leaf(0), Leaf(1)))
        self.assertEqual(ordered_leaves(left), ordered_leaves(right))
        self.assertEqual((evaluate(left), evaluate(right)), (-1, 1))
        self.assertNotEqual(serialize(left), serialize(right))

    def test_equal_output_is_task_relative(self):
        a, b = Leaf(0), Branch("SUB", Leaf(1), Leaf(1))
        self.assertEqual(evaluate(a), evaluate(b))
        self.assertNotEqual(serialize(a), serialize(b))
        self.assertNotEqual(leaf_bag(a), leaf_bag(b))

    def test_bag_keeps_multiplicity(self):
        self.assertEqual(leaf_bag(Branch("ADD", Leaf(1), Leaf(1))), (1, 1))
        self.assertNotEqual(leaf_bag(Leaf(1)), (1, 1))

    def test_parser_container_and_token_types(self):
        class TupleSubclass(tuple):
            pass
        for prefix in (None, "LEAF 0", [("LEAF", 0)], iter((("LEAF", 0),)), TupleSubclass((("LEAF", 0),))):
            with self.subTest(prefix=prefix), self.assertRaises(TypeError):
                parse(prefix)
        for token in (["LEAF", 0], "ADD", 0, TupleSubclass(("LEAF", 0))):
            with self.subTest(token=token), self.assertRaises(TypeError):
                parse((token,))

    def test_parser_bad_tags_and_arities(self):
        for token in ((), (None,), (True,), (0,), ("BAD",), ("leaf", 0), ("LEAF",), ("LEAF", 0, 1), ("ADD", 0), ("SUB", 0)):
            with self.subTest(token=token), self.assertRaises(ValueError):
                parse((token,))
        for value in (True, False, 0.0, "0", None):
            with self.subTest(value=value), self.assertRaises(TypeError):
                parse((("LEAF", value),))

    def test_parser_never_coerces_subclasses(self):
        class IntSubclass(int):
            pass
        class StrSubclass(str):
            pass
        for value in (IntSubclass(1),):
            with self.assertRaises(TypeError):
                Leaf(value)
            with self.assertRaises(TypeError):
                parse((("LEAF", value),))
        with self.assertRaises(TypeError):
            Branch(StrSubclass("ADD"), Leaf(0), Leaf(0))
        with self.assertRaises(ValueError):
            parse(((StrSubclass("LEAF"), 0),))

    def test_truncated_and_surplus_prefixes(self):
        bad = ((), (("ADD",),), (("ADD",), ("LEAF", 0)),
               (("ADD",), ("LEAF", 0), ("SUB",), ("LEAF", 1)),
               (("LEAF", 0), ("LEAF", 1)),
               (("ADD",), ("LEAF", 0), ("LEAF", 1), ("LEAF", 2)),
               (("LEAF", 0), ("ADD",), ("LEAF", 1), ("LEAF", 2)))
        for prefix in bad:
            with self.subTest(prefix=prefix), self.assertRaises(ValueError):
                parse(prefix)

    def test_public_tree_functions_reject_non_nodes(self):
        for function in (validate_tree, serialize, ordered_leaves, leaf_bag, evaluate, display, leaf_count):
            for tree in (None, ("LEAF", 0), 0, True, [Leaf(0)]):
                with self.subTest(function=function.__name__, tree=tree), self.assertRaises(TypeError):
                    function(tree)

    def test_bypassed_constructor_invalid_fields_and_cycle(self):
        bad_leaf = object.__new__(Leaf)
        object.__setattr__(bad_leaf, "value", True)
        with self.assertRaises(TypeError):
            serialize(bad_leaf)
        absent_leaf = object.__new__(Leaf)
        with self.assertRaises(TypeError):
            serialize(absent_leaf)
        absent_branch = object.__new__(Branch)
        with self.assertRaises(TypeError):
            serialize(absent_branch)
        cycle = Branch("ADD", Leaf(0), Leaf(0))
        object.__setattr__(cycle, "left", cycle)
        with self.assertRaises(ValueError):
            serialize(cycle)

    def test_shared_subtree_means_two_occurrences(self):
        part = Branch("ADD", Leaf(1), Leaf(2))
        tree = Branch("SUB", part, part)
        self.assertEqual(ordered_leaves(tree), (1, 2, 1, 2))
        self.assertEqual(evaluate(tree), 0)
        restored = parse(serialize(tree))
        self.assertEqual(restored, tree)
        self.assertIsNot(restored.left, restored.right)

    def test_generator_rejects_bad_parameters(self):
        for n in (True, 1.0, "2"):
            with self.subTest(n=n), self.assertRaises(TypeError):
                generate_trees(n)
        for n in (0, -1):
            with self.subTest(n=n), self.assertRaises(ValueError):
                generate_trees(n)
        for alphabet in ([], [0, 1], None):
            with self.subTest(alphabet=alphabet), self.assertRaises(TypeError):
                generate_trees(2, alphabet)
        for alphabet in ((), (0, 0), (True,), (1.0,), ("1",)):
            with self.subTest(alphabet=alphabet), self.assertRaises(ValueError):
                generate_trees(2, alphabet)

    def test_enumeration_completeness_uniqueness_and_round_trips(self):
        result = census()
        self.assertEqual(result["leaf_counts"], {"1": 3, "2": 18, "3": 216, "4": 3240})
        self.assertEqual(result["total"], 3477)
        self.assertEqual(result["unique_full_prefixes"], 3477)
        self.assertEqual(result["tree_round_trips"], 3477)
        self.assertEqual(result["prefix_round_trips"], 3477)
        self.assertEqual(result["output_values"], list(range(-6, 9)))
        self.assertEqual({k: v["classes"] for k, v in result["projections"].items()},
                         {"full_prefix": 3477, "ordered_leaves": 120, "leaf_bag": 34, "integer_output": 15})
        self.assertIsNone(result["projections"]["full_prefix"]["minimal_structural_collision"])
        for key in ("ordered_leaves", "leaf_bag", "integer_output"):
            self.assertEqual(result["projections"][key]["minimal_structural_collision"]["max_leaves"], 2)

    def test_all_bounded_sequences_refine_bags(self):
        seen = {}
        for n in range(1, 5):
            for tree in generate_trees(n):
                sequence, bag = ordered_leaves(tree), leaf_bag(tree)
                if sequence in seen:
                    self.assertEqual(seen[sequence], bag)
                seen[sequence] = bag

    def test_iterative_prefix_path_avoids_recursion_limit(self):
        # The syntax algorithm is iterative; this is not a claim of unlimited RAM.
        prefix = (("SUB",),) * 1500 + (("LEAF", 0),) * 1501
        tree = parse(prefix)
        self.assertEqual(serialize(tree), prefix)
        self.assertEqual(evaluate(tree), 0)
        self.assertEqual(leaf_count(tree), 1501)


if __name__ == "__main__":
    unittest.main()
