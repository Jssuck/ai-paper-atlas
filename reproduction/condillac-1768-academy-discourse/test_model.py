"""Finite regression and exhaustive checks, not proofs of general theorems."""
import copy
from fractions import Fraction
import itertools
import json
from pathlib import Path
import unittest

from demo import results, tree_spec, article_examples
from model import (SchemaError, UnknownInput, Tree, Lookup, RepresentationDomain,
                   Judgment, copy_judgment, distinct_origins, diffuse)


class TreeTests(unittest.TestCase):
    def test_complete_compilation_and_costs(self):
        tree = Tree(tree_spec())
        table = tree.compile()
        self.assertEqual(dict(table.table), {"a": "drop", "b": "drop", "c": "drop", "d": "keep"})
        self.assertEqual([tree.evaluate(x).predicate_tests for x in tree.domain], [1, 1, 2, 2])
        for item in tree.domain:
            self.assertEqual(tree.evaluate(item).label, table.evaluate(item).label)
            self.assertEqual(table.evaluate(item).abstract_lookups, 1)

    def test_empty_domain_and_root_leaf(self):
        spec = {"domain": [], "root": "r", "nodes": {"r": {"label": "yes"}}, "predicates": {}}
        self.assertEqual(dict(Tree(spec).compile().table), {})
        with self.assertRaises(UnknownInput):
            Tree(spec).evaluate("x")
        spec["domain"] = ["x"]
        tree = Tree(spec)
        self.assertEqual(tree.evaluate("x").predicate_tests, 0)
        self.assertEqual(tree.compile().evaluate("x").abstract_lookups, 1)
        branch = tree_spec()
        branch["domain"] = []
        branch["predicates"] = {"round": {}, "bright": {}}
        self.assertEqual(dict(Tree(branch).compile().table), {})

    def test_training_table_and_nonidentifiability(self):
        original = tree_spec()
        alternative = copy.deepcopy(original)
        # Both trees give d=keep. Their unseen c outputs disagree.
        alternative["nodes"]["u"]["label"] = "keep"
        left, right = Tree(original), Tree(alternative)
        self.assertEqual(dict(left.train_lookup(["d"]).table), dict(right.train_lookup(["d"]).table))
        self.assertNotEqual(left.evaluate("c").label, right.evaluate("c").label)
        for table in (left.train_lookup(["d"]), left.train_lookup([])):
            with self.assertRaises(UnknownInput):
                table.evaluate("c")
        with self.assertRaises(SchemaError):
            left.train_lookup(["a", "a"])
        with self.assertRaises(UnknownInput):
            left.train_lookup(["outside"])

    def test_snapshot_immutability(self):
        spec = tree_spec()
        tree = Tree(spec)
        spec["predicates"]["round"]["d"] = False
        spec["nodes"]["y"]["label"] = "changed"
        self.assertEqual(tree.evaluate("d").label, "keep")
        table = tree.compile()
        with self.assertRaises(TypeError):
            table.table["d"] = "changed"
        for obj in (tree, table):
            with self.assertRaises(AttributeError):
                obj._sealed = False
            with self.assertRaises(AttributeError):
                del obj._sealed
        raw = {"x": "yes"}
        table = Lookup(raw)
        raw["x"] = "no"
        self.assertEqual(table.evaluate("x").label, "yes")

    def test_invalid_tree_schema(self):
        bad = []
        def alter(fn):
            spec = tree_spec()
            fn(spec)
            bad.append(spec)
        bad.extend([None, [], {}, {"extra": 1}])
        alter(lambda s: s.update(extra=True))
        alter(lambda s: s.update(domain=["a", "a"]))
        alter(lambda s: s.update(domain=[1]))
        alter(lambda s: s.update(domain=("a",)))
        alter(lambda s: s.update(root="missing"))
        alter(lambda s: s.update(root=""))
        alter(lambda s: s.update(nodes={}))
        alter(lambda s: s["predicates"]["round"].pop("a"))
        alter(lambda s: s["predicates"]["round"].update(extra=True))
        alter(lambda s: s["predicates"]["round"].update(a=1))
        alter(lambda s: s["nodes"]["r"].update(predicate="unknown"))
        alter(lambda s: s["nodes"]["r"].update(false="missing"))
        alter(lambda s: s["nodes"]["r"].update(false="r"))
        alter(lambda s: s["nodes"]["r"].update(false="s"))
        alter(lambda s: s["nodes"]["y"].update(label=""))
        alter(lambda s: s["nodes"]["y"].update(extra="no"))
        alter(lambda s: s["nodes"].update(unreachable={"label": "no"}))
        alter(lambda s: s["nodes"].update(loop={"predicate": "round", "false": "loop", "true": "dangling"}, dangling={"label": "no"}))
        for spec in bad:
            with self.subTest(spec=spec), self.assertRaises(SchemaError):
                Tree(spec)
        tree = Tree(tree_spec())
        for item in (None, [], 1, True, "absent"):
            with self.subTest(item=item), self.assertRaises(UnknownInput):
                tree.evaluate(item)
            with self.assertRaises(UnknownInput):
                tree.compile().evaluate(item)

    def test_deep_tree_without_recursion_limit(self):
        nodes = {}
        depth = 1500
        for index in range(depth):
            nodes[f"n{index}"] = {"predicate": "p", "false": f"l{index}", "true": f"n{index + 1}"}
            nodes[f"l{index}"] = {"label": "no"}
        nodes[f"n{depth}"] = {"label": "yes"}
        tree = Tree({"domain": ["x"], "root": "n0", "nodes": nodes, "predicates": {"p": {"x": True}}})
        self.assertEqual(tree.evaluate("x").predicate_tests, depth)
        self.assertEqual(tree.compile().evaluate("x").label, "yes")

    def test_exhaustive_202_depth_two_trees(self):
        # Independent tuple syntax and recursive oracle on four Boolean inputs.
        leaves = ["0", "1"]
        level1 = leaves + [(p, no, yes) for p in (0, 1) for no in leaves for yes in leaves]
        trees = leaves + [(p, no, yes) for p in (0, 1) for no in level1 for yes in level1]
        self.assertEqual(len(trees), 202)
        inputs = {f"{a}{b}": (a, b) for a in (False, True) for b in (False, True)}
        def oracle(node, bits):
            if isinstance(node, str):
                return node, 0
            label, count = oracle(node[2] if bits[node[0]] else node[1], bits)
            return label, count + 1
        for abstract in trees:
            nodes = {}
            def encode(node):
                name = f"n{len(nodes)}"
                nodes[name] = None
                if isinstance(node, str):
                    nodes[name] = {"label": node}
                else:
                    nodes[name] = {"predicate": str(node[0]), "false": encode(node[1]), "true": encode(node[2])}
                return name
            root = encode(abstract)
            tree = Tree({"domain": list(inputs), "root": root, "nodes": nodes,
                         "predicates": {str(p): {name: bits[p] for name, bits in inputs.items()} for p in (0, 1)}})
            compiled = tree.compile()
            for name, bits in inputs.items():
                expected, count = oracle(abstract, bits)
                self.assertEqual((tree.evaluate(name).label, tree.evaluate(name).predicate_tests), (expected, count))
                self.assertEqual(compiled.evaluate(name).label, expected)


class RepresentationTests(unittest.TestCase):
    def spec(self):
        return {"objects": ["a", "b", "c"], "codes": {"a": "X", "b": "X", "c": "Y"},
                "labels": {"a": "yes", "b": "no", "c": "yes"}, "weights": {"a": "1/3", "b": "2/3", "c": 1}}

    def test_exact_risk_and_optimum(self):
        domain = RepresentationDomain(self.spec())
        self.assertEqual(domain.total_mass, 2)
        self.assertEqual(domain.risk({"X": "yes", "Y": "yes"}), Fraction(1, 3))
        best = domain.best_decoder()
        self.assertEqual(dict(best.decoder), {"X": "no", "Y": "yes"})
        self.assertEqual(best.error_mass, Fraction(1, 3))
        self.assertEqual(best.risk, Fraction(1, 6))
        self.assertEqual(domain.risk(best.decoder), best.risk)
        self.assertFalse(domain.sufficient())
        self.assertFalse(domain.sufficient(True))

    def test_uniform_default_and_deterministic_tie(self):
        spec = self.spec()
        spec.pop("weights")
        domain = RepresentationDomain(spec)
        self.assertEqual(domain.total_mass, 3)
        self.assertEqual(domain.best_decoder().decoder["X"], "no")
        self.assertEqual(domain.best_decoder().risk, Fraction(1, 3))
        spec["objects"].reverse()
        self.assertEqual(dict(RepresentationDomain(spec).best_decoder().decoder), dict(domain.best_decoder().decoder))

    def test_zero_mass_objects_and_fibers(self):
        spec = {"objects": ["a", "b", "c", "d"], "codes": {"a": "X", "b": "X", "c": "Z", "d": "Z"},
                "labels": {"a": "yes", "b": "no", "c": "yes", "d": "no"},
                "weights": {"a": 1, "b": 0, "c": 0, "d": 0}}
        domain = RepresentationDomain(spec)
        self.assertFalse(domain.sufficient())
        self.assertTrue(domain.sufficient(True))
        self.assertEqual(domain.best_decoder().risk, 0)
        self.assertEqual(dict(domain.best_decoder().decoder), {"X": "yes", "Z": "no"})
        self.assertEqual(domain.risk({"X": "yes", "Z": "anything"}), 0)

    def test_source_success_does_not_imply_target_success(self):
        source = {"objects": ["a", "b"], "codes": {"a": "X", "b": "Y"}, "labels": {"a": "yes", "b": "no"}}
        target = copy.deepcopy(source)
        target["labels"] = {"a": "no", "b": "yes"}
        decoder = {"X": "yes", "Y": "no"}
        self.assertEqual(RepresentationDomain(source).risk(decoder), 0)
        shifted = RepresentationDomain(target)
        self.assertTrue(shifted.sufficient())
        self.assertEqual(shifted.risk(decoder), 1)
        self.assertEqual(shifted.best_decoder().risk, 0)

    def test_representation_validation_and_snapshot(self):
        bad = [None, {}, {"objects": [], "codes": {}, "labels": {}}]
        def alter(fn):
            spec = self.spec()
            fn(spec)
            bad.append(spec)
        alter(lambda s: s.update(extra=True))
        alter(lambda s: s.update(objects=["a", "a"]))
        alter(lambda s: s["codes"].pop("a"))
        alter(lambda s: s["labels"].update(a=""))
        alter(lambda s: s["weights"].update(a=-1))
        for value in (0.25, True, "1/0", "0.1", "nan", "-1/2", {}, "1/02"):
            alter(lambda s, v=value: s["weights"].update(a=v))
        alter(lambda s: s.update(weights={"a": 0, "b": 0, "c": 0}))
        for spec in bad:
            with self.subTest(spec=spec), self.assertRaises(SchemaError):
                RepresentationDomain(spec)
        spec = self.spec()
        domain = RepresentationDomain(spec)
        spec["labels"]["a"] = "changed"
        self.assertEqual(domain.best_decoder().risk, Fraction(1, 6))
        for decoder in ({}, {"X": "yes"}, {"X": "yes", "Y": "yes", "Z": "no"}, {"X": "", "Y": "yes"}, []):
            with self.assertRaises(SchemaError):
                domain.risk(decoder)
        with self.assertRaises(SchemaError):
            domain.sufficient(1)
        with self.assertRaises(AttributeError):
            domain._mass = 100
        with self.assertRaises(AttributeError):
            del domain._sealed

    def test_exhaustive_768_populations_against_all_binary_decoders(self):
        objects = ["a", "b", "c", "d"]
        populations = 0
        for labels in itertools.product(("no", "yes"), repeat=4):
            for codes in itertools.product(("X", "Y"), repeat=4):
                for weights in ((1, 1, 1, 1), (1, 2, 3, 4), (1, 0, 0, 0)):
                    domain = RepresentationDomain({"objects": objects, "labels": dict(zip(objects, labels)),
                        "codes": dict(zip(objects, codes)), "weights": dict(zip(objects, weights))})
                    used = sorted(set(codes))
                    candidate_risks = []
                    for predictions in itertools.product(("no", "yes"), repeat=len(used)):
                        decoder = dict(zip(used, predictions))
                        direct = Fraction(sum(weight for code, label, weight in zip(codes, labels, weights)
                                              if decoder[code] != label), sum(weights))
                        self.assertEqual(domain.risk(decoder), direct)
                        candidate_risks.append(direct)
                    minimum = min(candidate_risks)
                    self.assertEqual(domain.best_decoder().risk, minimum)
                    self.assertEqual(domain.risk(domain.best_decoder().decoder), minimum)
                    self.assertEqual(domain.sufficient(True), minimum == 0)
                    pairwise = all(labels[i] == labels[j] for i in range(4) for j in range(4) if codes[i] == codes[j])
                    self.assertEqual(domain.sufficient(), pairwise)
                    populations += 1
        self.assertEqual(populations, 768)


class DiffusionTests(unittest.TestCase):
    def test_chain_shortcuts_false_claim_and_provenance(self):
        spec = {"nodes": ["A", "B", "C", "D", "I"], "edges": [["A", "B"], ["B", "C"], ["C", "D"]]}
        judgment = Judgment("2 + 2 = 5", "original")
        chain = diffuse(spec, ["A"], judgment)
        self.assertEqual([set(s) for s in chain.snapshots], [{"A"}, {"A", "B"}, {"A", "B", "C"}, {"A", "B", "C", "D"}])
        self.assertEqual(dict(chain.first_arrival), {"A": 0, "B": 1, "C": 2, "D": 3})
        spec["edges"] += [["A", "C"], ["A", "D"]]
        shortcut = diffuse(spec, ["A"], judgment)
        self.assertEqual(len(shortcut.snapshots) - 1, 1)
        self.assertEqual(shortcut.holders, chain.holders)
        self.assertEqual(shortcut.snapshots, diffuse(spec, ["A"], Judgment("2 + 2 = 4", "original")).snapshots)
        self.assertEqual(distinct_origins(copy_judgment(judgment, 100)), frozenset({"original"}))
        self.assertEqual(shortcut.origins, frozenset({"original"}))
        self.assertEqual(distinct_origins(copy_judgment(judgment, 0)), frozenset())

    def test_cycles_self_loops_empty_seeds_and_empty_graph(self):
        graph = {"nodes": ["A", "B"], "edges": [["A", "A"], ["A", "B"], ["B", "A"]]}
        j = Judgment("claim", "origin")
        self.assertEqual(diffuse(graph, ["A"], j).snapshots, (frozenset({"A"}), frozenset({"A", "B"})))
        empty = diffuse(graph, [], j)
        self.assertEqual(empty.snapshots, (frozenset(),))
        self.assertEqual(empty.origins, frozenset())
        self.assertEqual(dict(empty.first_arrival), {})
        self.assertEqual(diffuse({"nodes": [], "edges": []}, [], j).snapshots, (frozenset(),))
        all_seeds = diffuse(graph, ["A", "B"], j)
        self.assertEqual(len(all_seeds.snapshots), 1)

    def test_validation(self):
        good = {"nodes": ["A", "B"], "edges": [["A", "B"]]}
        j = Judgment("claim", "origin")
        for spec in (None, {}, {"nodes": ["A", "A"], "edges": []},
                     {"nodes": ["A"], "edges": [["A", "B"]]},
                     {"nodes": ["A"], "edges": [["A"]]},
                     {"nodes": ["A"], "edges": [["A", "A"], ["A", "A"]]},
                     {"nodes": ["A"], "edges": [("A", "A")]},
                     {"nodes": ["A"], "edges": [["A", 1]]}):
            with self.subTest(spec=spec), self.assertRaises(SchemaError):
                diffuse(spec, [], j)
        for seeds in (["unknown"], ["A", "A"], "A", [1]):
            with self.assertRaises(SchemaError):
                diffuse(good, seeds, j)
        with self.assertRaises(SchemaError):
            diffuse(good, [], "claim")
        for count in (-1, True, 1.0, "1"):
            with self.assertRaises(SchemaError):
                copy_judgment(j, count)
        with self.assertRaises(SchemaError):
            copy_judgment("claim", 1)
        with self.assertRaises(SchemaError):
            distinct_origins(["claim"])
        with self.assertRaises(SchemaError):
            distinct_origins("claim")
        for args in (("", "origin"), ("claim", 1)):
            with self.assertRaises(SchemaError):
                Judgment(*args)

    def test_exhaustive_4096_graph_seed_pairs_shortest_path_oracle(self):
        # All 512 directed graphs on three vertices, including self-loops,
        # crossed with all 8 seed sets; independent Floyd-Warshall oracle.
        nodes = ["A", "B", "C"]
        possible = list(itertools.product(range(3), repeat=2))
        count = 0
        for bits in itertools.product((False, True), repeat=9):
            edges = [edge for edge, present in zip(possible, bits) if present]
            distances = [[0 if i == j else 99 for j in range(3)] for i in range(3)]
            for i, j in edges:
                distances[i][j] = min(distances[i][j], 1)
            for k in range(3):
                for i in range(3):
                    for j in range(3):
                        distances[i][j] = min(distances[i][j], distances[i][k] + distances[k][j])
            graph = {"nodes": nodes, "edges": [[nodes[i], nodes[j]] for i, j in edges]}
            for seed_bits in itertools.product((False, True), repeat=3):
                seeds = [i for i, active in enumerate(seed_bits) if active]
                result = diffuse(graph, [nodes[i] for i in seeds], Judgment("fixed", "one"))
                oracle = {nodes[j]: min(distances[i][j] for i in seeds) for j in range(3)
                          if seeds and min(distances[i][j] for i in seeds) != 99}
                self.assertEqual(dict(result.first_arrival), oracle)
                self.assertEqual(result.holders, frozenset(oracle))
                self.assertLessEqual(len(result.snapshots), 3)
                for time, snapshot in enumerate(result.snapshots):
                    self.assertEqual(snapshot, frozenset(node for node, distance in oracle.items() if distance <= time))
                count += 1
        self.assertEqual(count, 4096)


class ExampleTests(unittest.TestCase):
    def test_article_xor_and_wrong_leaf(self):
        example = article_examples()["xor"]
        self.assertEqual(example["inputs"], ["00", "01", "10", "11"])
        self.assertEqual(example["true_labels"], ["0", "1", "1", "0"])
        self.assertEqual(example["tree_labels"], example["true_labels"])
        self.assertEqual(example["compiled_labels"], example["true_labels"])
        self.assertEqual(example["predicate_tests_per_query"], [2, 2, 2, 2])
        self.assertEqual(example["compilation_predicate_tests"], 8)
        self.assertEqual(example["stored_labels"], 4)
        self.assertEqual(example["wrong_tree_labels"], ["0", "1", "1", "1"])
        self.assertEqual(example["wrong_compiled_labels"], example["wrong_tree_labels"])
        self.assertEqual(example["wrong_tree_risk"], "1/4")
        self.assertEqual(example["wrong_compiled_risk"], "1/4")

    def test_article_uniform_transfer_weighted_tie_and_refinement(self):
        examples = article_examples()
        transfer = examples["first_bit_transfer"]
        self.assertEqual(transfer, {"source_risk": "0", "target_risk": "1/2",
            "target_structurally_sufficient": False, "minimum_target_risk": "1/2",
            "refined_minimum_target_risk": "0"})
        self.assertEqual(examples["weighted_tie_and_refinement"], {
            "total_mass": "6", "minimum_risk": "1/2", "deterministic_decoder": {"same": "0"},
            "refined_minimum_risk": "0"})

    def test_exact_demo_snapshot_and_key_counterexamples(self):
        expected = json.loads((Path(__file__).parent / "examples" / "expected_results.json").read_text())
        actual = results()
        self.assertEqual(actual, expected)
        a = actual["A_compilation"]
        self.assertEqual(a["uniform_compiled_error"], "1/4")
        self.assertEqual(a["fast_wrong_input"], "c")
        wrong = next(row for row in a["rows"] if row["input"] == "c")
        self.assertEqual((wrong["predicate_tests"], wrong["abstract_lookups"]), (2, 1))
        self.assertNotEqual(wrong["compiled_label"], wrong["true_label"])
        b = actual["B_representation"]
        self.assertEqual((b["source_risk"], b["target_risk"], b["minimum_target_risk"]), ("0", "3/8", "3/8"))
        self.assertEqual(b["shifted_transferred_risk"], "1")
        self.assertEqual(b["zero_weight_minimum_risk"], "0")


if __name__ == "__main__":
    unittest.main(verbosity=2)
