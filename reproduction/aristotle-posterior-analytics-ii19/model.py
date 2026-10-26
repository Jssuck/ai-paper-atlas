"""Modern finite-observation teaching model; not a model of Aristotle's nous."""
from itertools import product


def normalize(domain, observations):
    """Check a finite named domain and accurate, consistent Boolean observations."""
    domain = tuple(domain)
    if any(not isinstance(x, str) or not x for x in domain):
        raise ValueError('domain objects must be nonempty strings')
    if len(set(domain)) != len(domain):
        raise ValueError('duplicate domain object')
    allowed = set(domain)
    records = list(observations)
    labels = {}
    for record in records:
        if not isinstance(record, (tuple, list)) or len(record) != 2:
            raise ValueError('observation must have object and label')
        obj, label = record
        if not isinstance(obj, str) or obj not in allowed:
            raise ValueError('observation outside domain')
        if type(label) is not bool:
            raise ValueError('label must be bool')
        if obj in labels and labels[obj] != label:
            raise ValueError('conflicting labels')
        labels[obj] = label
    return domain, records, labels


def analyse(domain, observations):
    """Exact counts over ALL Boolean functions, with no probability interpretation."""
    domain, records, labels = normalize(domain, observations)
    unseen = len(domain) - len(labels)
    compatible = 2 ** unseen
    universal_true = int(all(labels.values()))
    universal_false = compatible - universal_true
    status = ('refuted' if not universal_true else
              'certified_finite_domain' if unseen == 0 else 'underdetermined')
    return {'domain_size': len(domain), 'observation_count': len(records),
            'covered_count': len(labels), 'unseen_count': unseen,
            'compatible_count': compatible,
            'universal_true_count': universal_true,
            'universal_false_count': universal_false, 'status': status}


def compatible_explanations(domain, observations):
    """Explicit small-domain oracle interface; exponential, not meant for large data."""
    domain, _, labels = normalize(domain, observations)
    result = []
    for bits in product((False, True), repeat=len(domain)):
        explanation = dict(zip(domain, bits))
        if all(explanation[obj] == label for obj, label in labels.items()):
            result.append(explanation)
    return result


def group_memories(domain, observations, classes):
    """Group by supplied classification; does NOT discover the classes or essences."""
    domain, records, _ = normalize(domain, observations)
    if set(classes) != set(domain) or any(not isinstance(v, str) or not v for v in classes.values()):
        raise ValueError('supply exactly one nonempty class name for each domain object')
    grouped = {}
    for obj, _ in records:
        name = classes[obj]
        group = grouped.setdefault(name, {'memory_count': 0, 'objects': set()})
        group['memory_count'] += 1
        group['objects'].add(obj)
    return {name: {'memory_count': group['memory_count'], 'objects': sorted(group['objects'])}
            for name, group in sorted(grouped.items())}
