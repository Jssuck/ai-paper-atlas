"""Independent finite oracle. Run from the reproduction directory.

Uses slot-valid bit words, forward parsing, nested tuples and direct arithmetic;
never calls the author's generator/serializer/evaluator to build expected data.
All checks are explicit and remain active with -O and -OO. Standard library only.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, product
import json
from math import comb
from pathlib import Path
import platform
import sys
import types

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import model as subject
import enumerate_model as subject_census

CHECKS = 0


def check(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise RuntimeError(message)


def reject(function, expected=(TypeError, ValueError)):
    global CHECKS
    CHECKS += 1
    try:
        function()
    except expected as exc:
        return type(exc).__name__
    raise RuntimeError("invalid case was accepted or expected limit did not occur")


def raw_read(tokens, start=0):
    """Independent forward reader over already-valid, shallow reference tokens."""
    token = tokens[start]
    if token[0] == "LEAF":
        return token[1], start + 1
    left, end = raw_read(tokens, start + 1)
    right, end = raw_read(tokens, end)
    return (token[0], left, right), end


def raw_prefix(tree):
    if type(tree) is int:
        return (("LEAF", tree),)
    return ((tree[0],),) + raw_prefix(tree[1]) + raw_prefix(tree[2])


def raw_value(tree):
    if type(tree) is int:
        return tree
    left, right = raw_value(tree[1]), raw_value(tree[2])
    return left + right if tree[0] == "ADD" else left - right


def raw_leaves(tree):
    if type(tree) is int:
        return (tree,)
    return raw_leaves(tree[1]) + raw_leaves(tree[2])


def raw_display(tree):
    if type(tree) is int:
        return str(tree)
    sign = "+" if tree[0] == "ADD" else "-"
    return f"({raw_display(tree[1])} {sign} {raw_display(tree[2])})"


def make_subject(tree, module=subject):
    if type(tree) is int:
        return module.Leaf(tree)
    return module.Branch(tree[0], make_subject(tree[1], module), make_subject(tree[2], module))


def take_subject(tree, module=subject):
    if type(tree) is module.Leaf:
        return tree.value
    check(type(tree) is module.Branch, "unexpected subject node")
    return tree.op, take_subject(tree.left, module), take_subject(tree.right, module)


def shapes(n):
    """Choose internal-node positions in a 2n-1 word; filter open child slots."""
    width = 2 * n - 1
    for inner in combinations(range(width), n - 1):
        word = tuple(i in inner for i in range(width))
        slots = 1
        valid = True
        for branch in word:
            if slots == 0:
                valid = False
                break
            slots += 1 if branch else -1
        if valid and slots == 0:
            yield word


def reference_domain(n, alphabet=(0, 1, 2)):
    for shape in shapes(n):
        for operations in product(("ADD", "SUB"), repeat=n - 1):
            for values in product(alphabet, repeat=n):
                oi, vi = iter(operations), iter(values)
                prefix = tuple((next(oi),) if internal else ("LEAF", next(vi)) for internal in shape)
                raw, end = raw_read(prefix)
                check(end == len(prefix), "oracle reader did not consume generated shape")
                yield prefix, raw


def valid_word(tokens):
    slots = 1
    for token in tokens:
        if slots == 0:
            return False
        slots += -1 if token[0] == "LEAF" else 1
    return slots == 0


def minimal_pair_bruteforce(groups):
    winner = None
    best = None
    pairs = 0
    for group in groups.values():
        for a, b in combinations(group, 2):
            pairs += 1
            ar, br = (a["n"], a["prefix"]), (b["n"], b["prefix"])
            if br < ar:
                a, b, ar, br = b, a, br, ar
            rank = max(ar[0], br[0]), ar[0] + br[0], ar, br
            if best is None or rank < best:
                best, winner = rank, (a, b)
    if winner is None:
        return None, pairs
    a, b = winner
    return {
        "first": a["display"], "second": b["display"],
        "first_prefix": a["prefix"], "second_prefix": b["prefix"],
        "first_output": a["output"], "second_output": b["output"],
        "max_leaves": best[0], "sum_leaves": best[1],
    }, pairs


def normalized(value):
    return json.loads(json.dumps(value))


def finite_audit():
    records, level_counts, shape_counts = [], {}, {}
    for n in range(1, 5):
        shape_counts[str(n)] = len(tuple(shapes(n)))
        domain = tuple(reference_domain(n))
        level_counts[str(n)] = len(domain)
        expected = {raw for _, raw in domain}
        actual_trees = subject.generate_trees(n)
        actual = [take_subject(tree) for tree in actual_trees]
        check(set(actual) == expected, "author generator differs from independently generated tree set")
        check(len(actual) == len(expected), "author generator duplicates trees")
        check(len(domain) == comb(2 * n - 2, n - 1) // n * 2 ** (n - 1) * 3 ** n, "closed count mismatch")
        for prefix, raw in domain:
            tree = make_subject(raw)
            parsed = subject.parse(prefix)
            leaves = raw_leaves(raw)
            bag = tuple(sorted(leaves))
            value = raw_value(raw)
            shown = raw_display(raw)
            check(raw_prefix(raw) == prefix, "reference reader/encoder inconsistency")
            check(take_subject(parsed) == raw, "parse differs from independent forward reader")
            check(subject.serialize(tree) == prefix, "serialize differs from independent shape word")
            check(take_subject(subject.parse(subject.serialize(tree))) == raw, "tree round trip")
            check(subject.serialize(parsed) == prefix, "prefix round trip")
            check(subject.evaluate(tree) == value == subject.evaluate(parsed), "arithmetic semantics")
            check(subject.ordered_leaves(tree) == leaves, "ordered leaves")
            check(subject.leaf_bag(tree) == bag, "leaf multiset")
            check(subject.leaf_count(tree) == n, "leaf count")
            check(subject.display(tree) == shown, "display")
            check(len(prefix) == 2 * n - 1, "length lemma")
            records.append(dict(prefix=prefix, raw=raw, n=n, output=value, display=shown, leaves=leaves, bag=bag))
    stats = {}
    for name, key in (("full_prefix", "prefix"), ("ordered_leaves", "leaves"), ("leaf_bag", "bag"), ("integer_output", "output")):
        groups = defaultdict(list)
        for record in records:
            groups[record[key]].append(record)
        sizes = [len(group) for group in groups.values()]
        witness, pairs = minimal_pair_bruteforce(groups)
        check(pairs == sum(size * (size - 1) // 2 for size in sizes), "pair count mismatch")
        stats[name] = dict(classes=len(groups), singleton_classes=sizes.count(1), collision_classes=sum(size > 1 for size in sizes), colliding_unordered_pairs=pairs, largest_class=max(sizes), minimal_structural_collision=witness)
    histogram = {str(k): v for k, v in sorted(Counter(r["output"] for r in records).items())}
    live = subject_census.census()
    saved = json.loads((ROOT / "validation/census.json").read_text())
    check(normalized(live) == saved, "saved census differs from fresh author census")
    for name, value in (("leaf_counts", level_counts), ("output_histogram", histogram), ("projections", stats)):
        check(normalized(value) == normalized(live[name]), "independent census mismatch: " + name)
    check(len(records) == 3477, "domain size")
    check(shape_counts == {"1": 1, "2": 1, "3": 2, "4": 5}, "shape counts")
    # Alternate alphabet: signed, out-of-domain and large exact integers.
    alphabet = (-10 ** 100, -2, 7)
    alternate = 0
    for n in range(1, 4):
        pairs = tuple(reference_domain(n, alphabet))
        check({take_subject(t) for t in subject.generate_trees(n, alphabet)} == {r for _, r in pairs}, "alternate alphabet generation")
        for prefix, raw in pairs:
            tree = subject.parse(prefix)
            check(take_subject(tree) == raw, "alternate integer parse")
            check(subject.evaluate(tree) == raw_value(raw), "alternate integer value")
            alternate += 1
    return dict(total=len(records), shape_counts=shape_counts, leaf_counts=level_counts, projections=stats, output_histogram=histogram, alternate_integer_trees=alternate)


def grammar_audit():
    alphabet = (("ADD",), ("SUB",), ("LEAF", 0), ("LEAF", 1), ("LEAF", 2))
    accepted = rejected = 0
    for length in range(8):
        for tokens in product(alphabet, repeat=length):
            if valid_word(tokens):
                raw, end = raw_read(tokens)
                check(end == length, "forward parser whole input")
                check(take_subject(subject.parse(tokens)) == raw, "grammar membership/parse mismatch")
                accepted += 1
            else:
                reject(lambda tokens=tokens: subject.parse(tokens), (ValueError,))
                rejected += 1
    check((accepted, rejected) == (3477, 94179), "bounded grammar coverage")
    return dict(max_tokens=7, alphabet_size=5, sequences=accepted + rejected, accepted=accepted, rejected=rejected)


def malformed_audit():
    class IntSubclass(int): pass
    class StrSubclass(str): pass
    class TupleSubclass(tuple): pass
    class LeafSubclass(subject.Leaf): pass
    invalid_tokens = [(), (None,), (0,), (True,), ("NO",), ("leaf", 0), ("ADD", 0), ("SUB", 0, 1), ("LEAF",), ("LEAF", 0, 1), ("LEAF", True), ("LEAF", False), ("LEAF", 1.0), ("LEAF", "1"), ("LEAF", None), ("LEAF", IntSubclass(2)), (StrSubclass("LEAF"), 2), (StrSubclass("ADD"),), ["LEAF", 0], TupleSubclass(("LEAF", 0)), "ADD", 42, None]
    malformed = 0
    for token in invalid_tokens:
        for prefix in ((token,), (("LEAF", 0), token), (("ADD",), token, ("LEAF", 1))):
            reject(lambda prefix=prefix: subject.parse(prefix))
            malformed += 1
    for container in (None, True, "", [("LEAF", 0)], iter((("LEAF", 0),)), TupleSubclass((("LEAF", 0),))):
        reject(lambda container=container: subject.parse(container), (TypeError,))
        malformed += 1
    funcs = (subject.validate_tree, subject.serialize, subject.evaluate, subject.display, subject.ordered_leaves, subject.leaf_bag, subject.leaf_count)
    bad = [None, True, 3, ("LEAF", 0), LeafSubclass(0)]
    for value in (True, IntSubclass(2), 2.0):
        leaf = object.__new__(subject.Leaf)
        object.__setattr__(leaf, "value", value)
        bad.append(leaf)
    bad.extend((object.__new__(subject.Leaf), object.__new__(subject.Branch)))
    for field, value in (("op", "MUL"), ("op", StrSubclass("ADD")), ("left", 0), ("right", None)):
        branch = subject.Branch("ADD", subject.Leaf(1), subject.Leaf(2))
        object.__setattr__(branch, field, value)
        bad.append(branch)
    cycle = subject.Branch("ADD", subject.Leaf(0), subject.Leaf(1))
    object.__setattr__(cycle, "right", cycle)
    bad.append(cycle)
    first = subject.Branch("SUB", subject.Leaf(1), subject.Leaf(2))
    second = subject.Branch("ADD", first, first)
    object.__setattr__(first, "left", second)
    bad.append(second)
    for func in funcs:
        for tree in bad:
            reject(lambda func=func, tree=tree: func(tree))
    constructor_cases = [(lambda: subject.Leaf(True)), (lambda: subject.Leaf(IntSubclass(3))), (lambda: subject.Branch("BAD", subject.Leaf(0), subject.Leaf(1))), (lambda: subject.Branch(StrSubclass("ADD"), subject.Leaf(0), subject.Leaf(1))), (lambda: subject.Branch("ADD", LeafSubclass(0), subject.Leaf(1)))]
    for case in constructor_cases:
        reject(case)
    generator_cases = [(True, (0,)), (0, (0,)), (-1, (0,)), (1.0, (0,)), (2, [0]), (2, ()), (2, (0, 0)), (2, (True,)), (2, (IntSubclass(2),)), (2, TupleSubclass((0,)))]
    for n, alphabet in generator_cases:
        reject(lambda n=n, alphabet=alphabet: subject.generate_trees(n, alphabet))
    return dict(invalid_prefix_cases=malformed, invalid_tree_objects=len(bad), tree_entrypoints=len(funcs), invalid_tree_calls=len(bad) * len(funcs), invalid_constructor_cases=len(constructor_cases), invalid_generator_cases=len(generator_cases))


def resource_audit():
    outcomes = []
    depth = 5000
    for side in ("left", "right"):
        tree = subject.Leaf(9)
        for _ in range(depth):
            tree = subject.Branch("SUB", tree, subject.Leaf(0)) if side == "left" else subject.Branch("SUB", subject.Leaf(0), tree)
        tokens = subject.serialize(tree)
        restored = subject.parse(tokens)
        expected = 9 if side == "left" or depth % 2 == 0 else -9
        check(subject.serialize(restored) == tokens, "deep prefix round trip")
        check(subject.evaluate(restored) == expected, "deep value")
        check(subject.leaf_count(restored) == depth + 1, "deep leaf count")
        check(len(subject.display(restored)) == 1 + 6 * depth, "deep display length")
        outcomes.append(dict(side=side, branch_depth=depth, leaves=depth + 1, tokens=len(tokens), output=expected))
    equal_left, equal_right = subject.parse(tokens), subject.parse(tokens)
    equality_exception = reject(lambda: equal_left == equal_right, (RecursionError,))
    shared = subject.Leaf(1)
    for _ in range(12):
        shared = subject.Branch("ADD", shared, shared)
    check(subject.leaf_count(shared) == 4096, "shared occurrences")
    check(subject.evaluate(shared) == 4096, "shared value")
    check(len(subject.serialize(shared)) == 8191, "shared expansion")
    huge = subject.Leaf(10 ** 5000)
    check(subject.evaluate(huge) == 10 ** 5000, "large arithmetic")
    check(subject.serialize(subject.parse(subject.serialize(huge))) == subject.serialize(huge), "large integer round trip")
    digit_limit = sys.get_int_max_str_digits() if hasattr(sys, "get_int_max_str_digits") else None
    if digit_limit and digit_limit < 5001:
        display_outcome = reject(lambda: subject.display(huge), (ValueError,))
    else:
        check(len(subject.display(huge)) == 5001, "large integer display")
        display_outcome = "rendered under this runtime setting"
    return dict(deep_paths=outcomes, distinct_deep_dataclass_equality=equality_exception, shared_dag_unique_nodes=13, shared_dag_expanded_leaves=4096, integer_digits=5001, runtime_digit_limit=digit_limit, integer_display=display_outcome, note="Finite probes only; no arbitrary-size resource or performance guarantee.")


def mutation_audit():
    source = (ROOT / "model.py").read_text()
    mutation_specs = [
        ("serialize_swap_children", [("stack.extend((node.right, node.left))", "stack.extend((node.left, node.right))")], "serializer"),
        ("parse_swap_children", [("left, right = stack.pop(), stack.pop()", "right, left = stack.pop(), stack.pop()")], "parser"),
        ("paired_swaps_roundtrip_can_hide", [("stack.extend((node.right, node.left))", "stack.extend((node.left, node.right))"), ("left, right = stack.pop(), stack.pop()", "right, left = stack.pop(), stack.pop()")], "serializer"),
        ("subtraction_becomes_addition", [("left - right)", "left + right)")], "semantics"),
        ("multiset_drops_multiplicity", [("tuple(sorted(ordered_leaves(tree)))", "tuple(sorted(set(ordered_leaves(tree))))")], "bag"),
        ("ignore_surplus_expressions", [("if len(stack) != 1:", "if len(stack) < 1:")], "surplus"),
        ("leaf_payload_accepts_bool", [("type(self.value) is not int", "not isinstance(self.value, int)"), ("type(token[1]) is not int", "not isinstance(token[1], int)")], "bool"),
        ("generator_omits_split", [("range(1, size)", "range(1, size - 1)")], "generator"),
    ]
    results = []
    expected = ("SUB", 2, ("ADD", 0, 1))
    prefix = raw_prefix(expected)
    for index, (name, changes, property_name) in enumerate(mutation_specs):
        modified = source
        for old, new in changes:
            check(old in modified, "mutation target missing: " + name)
            modified = modified.replace(old, new, 1)
        module_name = "independent_mutant_" + str(index)
        module = types.ModuleType(module_name)
        sys.modules[module_name] = module
        exec(compile(modified, "<" + module_name + ">", "exec"), module.__dict__)
        if property_name == "serializer":
            detected = module.serialize(make_subject(expected, module)) != prefix
        elif property_name == "parser":
            detected = take_subject(module.parse(prefix), module) != expected
        elif property_name == "semantics":
            raw = ("SUB", 2, 1)
            detected = module.evaluate(make_subject(raw, module)) != raw_value(raw)
        elif property_name == "bag":
            detected = module.leaf_bag(make_subject(("ADD", 1, 1), module)) != (1, 1)
        elif property_name == "surplus":
            try:
                module.parse((("LEAF", 0), ("LEAF", 1)))
                detected = True
            except (TypeError, ValueError):
                detected = False
        elif property_name == "bool":
            try:
                module.parse((("LEAF", True),))
                detected = True
            except (TypeError, ValueError):
                detected = False
        else:
            detected = {take_subject(t, module) for t in module.generate_trees(2)} != {r for _, r in reference_domain(2)}
        check(detected, "targeted oracle failed to detect mutation: " + name)
        entry = dict(mutation=name, detected=detected, property=property_name)
        if name == "paired_swaps_roundtrip_can_hide":
            entry["both_roundtrips_hold_for_witness"] = (
                take_subject(module.parse(module.serialize(make_subject(expected, module))), module) == expected
                and module.serialize(module.parse(prefix)) == prefix
            )
            check(entry["both_roundtrips_hold_for_witness"], "paired-swap demonstration no longer applies")
        results.append(entry)
        del sys.modules[module_name]
    return dict(cases=results, caveat="Eight deliberately selected fault injections, not an exhaustive mutation score or proof of test completeness.")



def example_audit():
    examples = [
        ("A: retain every operation, side, and bracket", ("SUB", 2, ("ADD", 0, 1))),
        ("B: change the operation", ("ADD", 0, 1)),
        ("C: same ordered leaves as B, different output", ("SUB", 0, 1)),
        ("D: exchange C's two parts", ("SUB", 1, 0)),
        ("E: left-associated subtraction", ("SUB", ("SUB", 0, 0), 1)),
        ("F: right-associated subtraction", ("SUB", 0, ("SUB", 0, 1))),
        ("G: a bare zero", 0),
        ("H: same output as G, different parts", ("SUB", 1, 1)),
    ]
    recorded = (ROOT / "validation/demo-output.txt").read_text()
    lines = []
    for label, raw in examples:
        leaves = raw_leaves(raw)
        lines.extend((label, "  expression: " + raw_display(raw), "  full prefix: " + repr(raw_prefix(raw)),
                      "  ordered leaves: " + repr(leaves), "  leaf bag: " + repr(tuple(sorted(leaves))),
                      "  integer output: " + str(raw_value(raw)), "  exact round trip: True"))
    expected_part = "\n".join(lines) + "\n"
    check(recorded.startswith(expected_part + "STRICT PARSER REJECTIONS\n"), "demo log differs from independently computed eight examples")
    expected_outputs = [1, 1, -1, 1, -1, 1, 0, 0]
    check([raw_value(raw) for _, raw in examples] == expected_outputs, "walkthrough outputs")
    article_raw = [("SUB", 2, 1), ("SUB", 1, 2), ("SUB", ("SUB", 2, 1), 1), ("SUB", 2, ("SUB", 1, 1))]
    check([raw_value(raw) for raw in article_raw] == [1, -1, 0, 2], "article example outputs")
    return dict(demo_examples=8, walkthrough_outputs=expected_outputs, article_T1_to_T4_outputs=[1, -1, 0, 2])

def main():
    result = dict(review_kind="independent finite oracle; modern syntactic model only", python=platform.python_version(), optimize=sys.flags.optimize, oracle_sha256=sha256(Path(__file__).read_bytes()).hexdigest())
    result["finite_domain"] = finite_audit()
    result["token_grammar"] = grammar_audit()
    result["malformed"] = malformed_audit()
    result["resource_probes"] = resource_audit()
    result["targeted_mutations"] = mutation_audit()
    result["examples"] = example_audit()
    result["explicit_checks"] = CHECKS
    result["status"] = "PASS"
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
