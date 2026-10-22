"""Independent bit-mask oracle for the declared bounded teaching semantics."""
import contextlib
import io
import json
from itertools import product
from model import Term, Inclusion, Model, chain_certificate
import run_checks


def ensure(value, message):
    if not value:
        raise RuntimeError(message)


def sub(a, b):
    return (a | b) == b


def members(mask, n):
    return tuple(i for i in range(n) if (mask // (2 ** i)) % 2)


def main():
    counts = dict(chain_models=0, chain_premise_models=0,
                  four_term_models=0, relabel_countermodels=0,
                  middle_mismatch_countermodels=0,
                  qualified_to_bare_countermodels=0,
                  bare_to_qualified_countermodels=0)
    labels = [Term('object'), Term('class'), Term('known', 'good'), Term('known', 'being')]
    api_checks = 0
    for n in range(4):
        masks = range(2 ** n)
        for c, b, a in product(masks, repeat=3):
            counts['chain_models'] += 1
            if sub(c,b) and sub(b,a):
                counts['chain_premise_models'] += 1
                ensure(sub(c,a), 'oracle transitivity failure')
        for c, b, a, r in product(masks, repeat=4):
            counts['four_term_models'] += 1
            counts['relabel_countermodels'] += int(sub(c,b) and sub(b,r) and not sub(c,a))
            counts['middle_mismatch_countermodels'] += int(sub(c,b) and sub(r,a) and not sub(c,a))
            bits = [c,b,a,r]
            m = Model(range(n), {t: members(v,n) for t,v in zip(labels,bits)})
            for i,j in product(range(4), repeat=2):
                ensure(m.holds(Inclusion(labels[i], labels[j])) == sub(bits[i], bits[j]),
                       'API differs from bit-mask oracle')
                api_checks += 1
        for a,b in product(masks,repeat=2):
            counts['qualified_to_bare_countermodels'] += int(not sub(a,b))
            counts['bare_to_qualified_countermodels'] += int(not sub(b,a))
    # Shape logic independently checked across all possible endpoint sextuples.
    shapes = 0
    for indices in product(range(4), repeat=6):
        c,b,d,a,s,p = indices
        expected = (b == d and c == s and a == p)
        got = chain_certificate(Inclusion(labels[c],labels[b]),
                                Inclusion(labels[d],labels[a]),
                                Inclusion(labels[s],labels[p]))
        ensure(got == expected, 'shape oracle mismatch')
        shapes += 1
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        run_checks.main()
    producer = json.loads(output.getvalue())
    ensure(producer['counts'] == counts, 'reported counters differ from independent oracle')
    # Equal extensions guarantee equal truth values, not true conclusions.
    m = Model({0},{labels[0]:{0},labels[2]:set(),labels[3]:set()})
    ensure(not m.holds(Inclusion(labels[0],labels[2])) and
           not m.holds(Inclusion(labels[0],labels[3])), 'equal-extension false case')
    try:
        run_checks.check(False)
    except AssertionError:
        pass
    else:
        raise RuntimeError('guard removed under optimization')
    print(json.dumps({'status':'PASS','independent_counts':counts,
                      'api_truth_comparisons':api_checks,
                      'certificate_shapes':shapes,
                      'equal_extensions_both_false':'PASS',
                      'limits':'finite independent checks, not general theorem proof'}, indent=2))


if __name__ == '__main__':
    main()
