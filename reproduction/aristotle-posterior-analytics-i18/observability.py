"""Modern finite teaching model, not Aristotle's account of induction."""
import itertools
import json


def bits(values):
    """Validate and materialize a finite binary vector; bool is rejected."""
    result = tuple(values)
    if any(type(v) is not int or v not in (0, 1) for v in result):
        raise ValueError('entries must be integers 0 or 1')
    return result


def decoder(observation, target):
    """Return a decoder on the observed image, or None on a conflicting fiber.

    The domain is indices 0..n-1. Empty domain returns {}, not failure.
    Values outside the image are intentionally unspecified.
    """
    observation, target = bits(observation), bits(target)
    if len(observation) != len(target):
        raise ValueError('observation and target must have equal length')
    mapping = {}
    for observed, wanted in zip(observation, target):
        if observed in mapping and mapping[observed] != wanted:
            return None
        mapping[observed] = wanted
    return mapping


def completions(target, sample):
    """All binary target functions agreeing with a sample of domain indices."""
    target = bits(target)
    sample = tuple(sample)
    if any(type(i) is not int or not 0 <= i < len(target) for i in sample):
        raise ValueError('sample indices outside domain')
    if len(set(sample)) != len(sample):
        raise ValueError('sample indices must be distinct')
    return [candidate for candidate in itertools.product((0, 1), repeat=len(target))
            if all(candidate[i] == target[i] for i in sample)]


def run():
    rows = []
    for n in range(5):
        vectors = list(itertools.product((0, 1), repeat=n))
        good = sum(decoder(o, t) is not None for o in vectors for t in vectors)
        rows.append({'domain_size': n, 'pairs': len(vectors)**2, 'recoverable': good})
    sample_checks = 0
    ambiguous = 0
    for t in itertools.product((0, 1), repeat=4):
        for mask in itertools.product((0, 1), repeat=4):
            s = [i for i, present in enumerate(mask) if present]
            ambiguous += len(completions(t, s)) > 1
            sample_checks += 1
    # Four possible worlds: independent latent coordinates x and y.
    x, y = (0, 0, 1, 1), (0, 1, 0, 1)
    examples = {
        'missing_y_channel': decoder(x, y),
        'alternative_y_channel': decoder(y, y),
        # Restrict worlds to those satisfying the EXTRA assumption x == y.
        'restricted_background_x_equals_y': decoder((0, 1), (0, 1)),
        # Ignore the material coordinate y, retaining a shape category x.
        'abstract_shape_target': decoder(x, x),
        'one_positive_sample_all_positive_candidates': completions((1, 1), (0,)),
    }
    return {'model': 'binary finite observation fibers; modern teaching only',
            'enumeration': rows, 'total_pairs': sum(r['pairs'] for r in rows),
            'total_recoverable': sum(r['recoverable'] for r in rows),
            'sample_target_checks': sample_checks,
            'ambiguous_sample_target_checks': ambiguous, 'examples': examples}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, ensure_ascii=False))
