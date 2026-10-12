"""Independent finite checks of definitions, not a proof or a code audit.

Run with Python standard library only. No imports from the reproduction.
Writes its JSON result to stdout; redirect as desired.
"""
from collections import Counter, defaultdict
from itertools import product, permutations
from math import prod
import hashlib
import json
from pathlib import Path
import platform
import sys


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def has_cycle(vertices, edges):
    reach = set(edges)
    for middle in vertices:
        for first in vertices:
            for last in vertices:
                if (first, middle) in reach and (middle, last) in reach:
                    reach.add((first, last))
    return any((v, v) in reach for v in vertices)


counts = Counter()
for n in range(1, 5):
    vertices = tuple(range(n))
    domains = tuple(tuple(range(k)) for k in (1, 2, 3, 2)[:n])
    messages = tuple(product(*domains))
    all_edges = tuple((a, b) for a in vertices for b in vertices if a != b)
    for bits in product((False, True), repeat=len(all_edges)):
        edges = tuple(edge for edge, present in zip(all_edges, bits) if present)
        cyclic = has_cycle(vertices, edges)
        orders = tuple(p for p in permutations(vertices)
                       if all(p.index(a) < p.index(b) for a, b in edges))
        require(bool(orders) == (not cyclic), "DAG/topological-order equivalence")
        counts["directed_graphs"] += 1
        if cyclic:
            counts["cyclic_graphs"] += 1
            continue
        counts["dags"] += 1
        counts["legal_orders"] += len(orders)
        prefixes = defaultdict(set)
        complete_pairs = {}
        for message in messages:
            for order in orders:
                # Identity atom code is injective and already token-framed.
                words = tuple((f, message[f]) for f in order)
                pair = (message, order)
                require(words not in complete_pairs or complete_pairs[words] == pair,
                        "injectivity of message/order pair")
                complete_pairs[words] = pair
                counts["complete_expressions"] += 1
                for k in range(n + 1):
                    prefixes[words[:k]].add(message)
        for prefix, candidates in prefixes.items():
            seen = {f for f, _ in prefix}
            expected = prod(len(domains[f]) for f in vertices if f not in seen)
            require(len(candidates) == expected, "product formula")
            if prefix:
                require(candidates <= prefixes[prefix[:-1]], "prefix monotonicity")
            counts["distinct_legal_prefixes"] += 1
        require(prefixes[()] == set(messages), "empty prefix")
        require(all(prefixes[words] == {pair[0]}
                    for words, pair in complete_pairs.items()), "complete recovery")

# Arbitrary colliding dictionaries, including empty word strings; all finite
# observed sequences to length three, including impossible and overlong ones.
vertices = (0, 1)
messages = tuple(product((0, 1), repeat=2))
atoms = tuple(product(vertices, (0, 1)))
word_pool = ("", "x")
for words in product(word_pool, repeat=len(atoms)):
    dictionary = dict(zip(atoms, words))
    for edges in ((), ((0, 1),), ((1, 0),)):
        orders = tuple(p for p in permutations(vertices)
                       if all(p.index(a) < p.index(b) for a, b in edges))
        streams = {m: tuple(tuple(dictionary[f, m[f]] for f in order)
                            for order in orders) for m in messages}
        def candidates(prefix):
            return {m for m, choices in streams.items()
                    if any(len(prefix) <= len(s) and s[:len(prefix)] == prefix
                           for s in choices)}
        for k in range(4):
            for prefix in product(word_pool, repeat=k):
                parent = candidates(prefix)
                for word in word_pool:
                    require(candidates(prefix + (word,)) <= parent,
                            "colliding-dictionary prefix monotonicity")
                    counts["collision_monotonicity_checks"] += 1
        counts["colliding_dictionary_context_cases"] += 1

message = ("A", "B", "help")
swapped = ("B", "A", "help")
require(Counter(message) == Counter(swapped), "unlabeled collision")
require(set(enumerate(message)) != set(enumerate(swapped)), "labels retain binding")
require("".join(("a", "bc")) == "".join(("ab", "c")), "unframed collision")
require(json.dumps(("a", "bc")) != json.dumps(("ab", "c")), "frame distinction")
hypotheses = ((0, 1, 2), (0, 1, 4), (1, 2, 3))
compatible = tuple(h for h in hypotheses if h[:2] == (0, 1))
require({h[2] for h in compatible} == {2, 4}, "underdetermination")
restricted = (hypotheses[0], hypotheses[2])
require({h[2] for h in restricted if h[:2] == (0, 1)} == {2}, "restricted predictions")
# Stronger statement would be false: a non-injective word dictionary can
# distinguish messages if the fixed positions already identify the roles.
position_dictionary = {(0, 0): "x", (0, 1): "y", (1, 0): "x", (1, 1): "y"}
position_streams = {tuple(position_dictionary[f, m[f]] for f in vertices): m
                    for m in messages}
require(len(set(position_dictionary.values())) != len(position_dictionary),
        "dictionary really noninjective")
require(len(position_streams) == len(messages), "position-based recovery counterexample")

result = {
    "scope": "Independent finite checks of the stated definitions, not general proofs, reproduction code certification, or empirical psychology",
    "python_version": platform.python_version(),
    "python_implementation": platform.python_implementation(),
    "platform": platform.platform(),
    "python_optimization": sys.flags.optimize,
    "command": sys.orig_argv,
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "domain_sizes_by_n": [[1], [1, 2], [1, 2, 3], [1, 2, 3, 2]],
    "counts": dict(counts),
    "counterexamples_passed": ["unlabeled_role_swap", "unframed_concatenation", "finite_hypothesis_underdetermination", "global_injectivity_not_necessary_with_fixed_positions"],
    "passed": True,
}
print(json.dumps(result, ensure_ascii=False, indent=2))
