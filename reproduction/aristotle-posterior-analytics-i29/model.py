"""Original finite teaching models for APo I.29; no historical causality oracle."""
from itertools import product
import json


def subset(x, y):
    return x & ~y == 0


def middle(a, b, d):
    """All B is D and all D is A; empty sets allowed explicitly."""
    return subset(b, d) and subset(d, a)


def candidates(a, b, n):
    if n < 0 or any(x < 0 or x >= 1 << n for x in (a, b)):
        raise ValueError('sets must fit universe')
    return tuple(d for d in range(1 << n) if middle(a, b, d))


def pair_kind(d, h):
    if d == h:
        return 'equal'
    if subset(d, h) or subset(h, d):
        return 'comparable_distinct'
    return 'incomparable'


def paths(edges, start, end):
    """All simple directed paths in this GIVEN finite graph, not all explanations."""
    adj = {}
    for x, y in edges:
        adj.setdefault(x, set()).add(y)
    out = []
    def visit(path):
        if path[-1] == end:
            out.append(tuple(path))
            return
        for nxt in sorted(adj.get(path[-1], ())):
            if nxt not in path:
                visit(path + [nxt])
    visit([start])
    return tuple(sorted(out))


def negative_routes(a, b, d, h):
    # Celarent: E(A,D), A(D,B); Cesare: E(H,A), A(H,B).
    celarent = not (a & d) and subset(b, d)
    cesare = not (h & a) and subset(b, h)
    conclusion = not (a & b)
    return bool(celarent), bool(cesare), conclusion


def enumerate_sets(max_n=4):
    counts = dict(endpoint_pairs=0, middle_candidates=0, ordered_middle_pairs=0,
                  equal=0, comparable_distinct=0, incomparable=0,
                  nonempty_subject_pairs=0, overlap_failures=0,
                  empty_subject_disjoint_pairs=0, conclusion_failures=0,
                  candidate_count_failures=0)
    for n in range(max_n + 1):
        for a, b in product(range(1 << n), repeat=2):
            counts['endpoint_pairs'] += 1
            cs = candidates(a, b, n)
            expected = 2 ** (a & ~b).bit_count() if subset(b, a) else 0
            counts['candidate_count_failures'] += len(cs) != expected
            counts['middle_candidates'] += len(cs)
            for d, h in product(cs, repeat=2):
                counts['ordered_middle_pairs'] += 1
                counts[pair_kind(d, h)] += 1
                counts['conclusion_failures'] += not subset(b, a)
                if b:
                    counts['nonempty_subject_pairs'] += 1
                    counts['overlap_failures'] += not bool(d & h)
                elif not d & h:
                    counts['empty_subject_disjoint_pairs'] += 1
    return counts


def enumerate_negative(max_n=3):
    out = dict(assignments=0, celarent_premises=0, cesare_premises=0,
               both_routes=0, invalid_conclusions=0)
    for n in range(max_n + 1):
        for a, b, d, h in product(range(1 << n), repeat=4):
            c, s, q = negative_routes(a, b, d, h)
            out['assignments'] += 1
            out['celarent_premises'] += c
            out['cesare_premises'] += s
            out['both_routes'] += c and s
            out['invalid_conclusions'] += (c or s) and not q
    return out


def results():
    chain = [('B','C'),('C','D'),('D','Z'),('Z','A')]
    diamond = [('B','D'),('D','A'),('B','H'),('H','A')]
    return dict(set_enumeration=enumerate_sets(), negative_enumeration=enumerate_negative(),
                example=dict(A=7,B=1,D=3,H=5,kind=pair_kind(3,5),overlap=3 & 5),
                graph_examples=dict(chain_paths=paths(chain,'B','A'),
                    chain_possible_cuts=['C','D','Z'],diamond_paths=paths(diamond,'B','A')))


if __name__ == '__main__':
    print(json.dumps(results(), ensure_ascii=False, indent=2, sort_keys=True))
