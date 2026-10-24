"""Independent Boolean/list oracles; exhaustive ONLY over declared finite sizes."""
import json
from itertools import product
from model import every_instance, counterexample, relative_partition, broadest_adequate

def require(value, message):
    if not value: raise RuntimeError(message)

def bits(mask, width):
    return [bool((mask // (2 ** i)) % 2) for i in range(width)]

def run():
    temporal = 0
    for subject, predicate in product(range(64), repeat=2):
        s, p = bits(subject, 6), bits(predicate, 6)
        bad = [i for i in range(6) if s[i] and not p[i]]
        require(every_instance(subject, predicate, 6) == (not bad), 'inclusion oracle')
        expected = None if not bad else (bad[0] % 3, bad[0] // 3)
        require(counterexample(subject, predicate, 3, 2) == expected, 'witness oracle')
        temporal += 1
    partitions = valid = 0
    for g, a, b in product(range(8), repeat=3):
        gb, ab, bb = bits(g, 3), bits(a, 3), bits(b, 3)
        expected = all(not gb[i] or (ab[i] != bb[i]) for i in range(3))
        require(relative_partition(g, a, b, 3) == expected, 'partition oracle')
        partitions += 1
        valid += int(expected)
    hierarchies = 0
    for a, b, c, p in product(range(8), repeat=4):
        classes = dict(zip(('a', 'b', 'c'), (a, b, c)))
        sets = {name: {i for i, flag in enumerate(bits(mask, 3)) if flag}
                for name, mask in classes.items()}
        ps = {i for i, flag in enumerate(bits(p, 3)) if flag}
        good = {name: s for name, s in sets.items() if s and s <= ps}
        expected = tuple(sorted(name for name, s in good.items()
                                if not any(s < t for t in good.values())))
        require(broadest_adequate(classes, p, 3) == expected, 'candidate oracle')
        hierarchies += 1
    return {'temporal_object_time_cases': temporal, 'temporal_domain': {'objects': 3, 'times': 2},
            'partition_cases': partitions, 'valid_relative_partitions': valid,
            'three_named_class_candidate_cases': hierarchies, 'candidate_domain_objects': 3,
            'oracle_differences': 0,
            'scope': 'Finite extensional diagnostics; no inference of essence, cause, modality or scientific knowledge.'}

if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True))
