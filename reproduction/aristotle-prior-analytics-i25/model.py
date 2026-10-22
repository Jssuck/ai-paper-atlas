"""Original teaching model for Prior Analytics I.25; not a historical formalization.

(a,b) means every a is b. Empty classes are allowed. Only transitivity is
implemented. Distinct conclusions are ordered pairs, not derivation counts.
"""
from collections.abc import Iterable


def label(value):
    if not isinstance(value, str) or not value or value.strip() != value:
        raise ValueError('labels must be nonempty strings without outer whitespace')
    return value


def pair(value):
    if not isinstance(value, (tuple, list)) or len(value) != 2:
        raise ValueError('an edge must have two labels')
    return (label(value[0]), label(value[1]))


def edge_set(edges):
    if isinstance(edges, (str, bytes)) or not isinstance(edges, Iterable):
        raise ValueError('edges must be an iterable of pairs')
    return {pair(e) for e in edges}


def closure(edges):
    """Positive-length reachability; cycles may yield (a,a), not added by fiat."""
    known = edge_set(edges)
    while True:
        more = {(a, d) for a, b in known for c, d in known if b == c}
        new = more - known
        if not new:
            return known
        known |= new


def verify_certificate(edges, steps, target):
    """Check each (a,m,b) inference using previously known (a,m),(m,b).

    A target must occur as a checked conclusion, not merely be an input edge.
    Repeated/redundant valid steps are allowed; minimality is not checked.
    Malformed inputs raise ValueError; a well-formed invalid proof returns False.
    """
    known = edge_set(edges)
    target = pair(target)
    if isinstance(steps, (str, bytes)) or not isinstance(steps, Iterable):
        raise ValueError('steps must be iterable triples')
    parsed = []
    for step in steps:
        if not isinstance(step, (tuple, list)) or len(step) != 3:
            raise ValueError('a step must have three labels')
        parsed.append(tuple(label(x) for x in step))
    produced = set()
    for a, m, b in parsed:
        if (a, m) not in known or (m, b) not in known:
            return False
        known.add((a, b))
        produced.add((a, b))
    return target in produced


def chain_report(terms):
    if not isinstance(terms, (tuple, list)) or len(terms) < 2:
        raise ValueError('a chain needs a list/tuple of at least two distinct terms')
    terms = tuple(label(t) for t in terms)
    if len(set(terms)) != len(terms):
        raise ValueError('chain labels must be distinct')
    n = len(terms)
    edges = set(zip(terms, terms[1:]))
    reached = closure(edges)
    conclusions = reached - edges
    steps = [(terms[i], terms[j-1], terms[j])
             for gap in range(2, n) for i in range(n-gap) for j in [i+gap]]
    return {'terms': list(terms), 'term_count': n,
            'premises': sorted(edges), 'premise_count': len(edges),
            'conclusions': sorted(conclusions), 'conclusion_count': len(conclusions),
            'steps': steps}


def proof_tree_stats(tree):
    """Tree syntax: ('given',a,b) or ('via',left,right).

    Checks transitivity at each internal node. A reused subtree object is counted
    on each occurrence: these are tree counts, not distinct DAG-node counts.
    Leaves are assumptions, not checked against an external database.
    Depth >200 is rejected as an implementation guard, not a logical restriction.
    """
    def walk(node, depth):
        if depth > 200:
            raise ValueError('tree depth exceeds implementation limit 200')
        if not isinstance(node, tuple) or len(node) != 3:
            raise ValueError('tree nodes must be triples')
        if node[0] == 'given':
            return pair(node[1:]), 0, 1, 1
        if node[0] != 'via':
            raise ValueError('unknown tree node kind')
        lp, lk, ll, ln = walk(node[1], depth+1)
        rp, rk, rl, rn = walk(node[2], depth+1)
        if lp[1] != rp[0]:
            raise ValueError('inference has no matching middle term')
        return (lp[0], rp[1]), lk+rk+1, ll+rl, ln+rn+1
    conclusion, k, leaves, nodes = walk(tree, 0)
    return {'conclusion': conclusion, 'inferences': k, 'leaf_occurrences': leaves,
            'premise_slots': 2*k, 'node_occurrences': nodes}
