"""Independent boolean-row oracle; no author powerset/subset implementation reused.
The checks are finite tests and do not establish a general theorem.
"""
import hashlib
import itertools
import json
from pathlib import Path
from model import Context, Proposition, check_chain, evaluate, experiments


def demand(condition, message):
    if not condition:
        raise RuntimeError(message)


def implication(a, b):
    return (not a) or b


def main():
    counts = dict(all_assignments=0, all_premises=0, all_failures=0,
                  weak_premises=0, weak_failures=0, member_assignments=0,
                  member_premises=0, member_failures=0, identities=0, identity_failures=0)
    evaluator_checks = 0
    first = None
    for n in range(4):
        for bits in itertools.product((False, True), repeat=3*n):
            # A, B, C membership is encoded row-by-row, not by author powerset.
            rows = [bits[3*i:3*i+3] for i in range(n)]
            major = all(implication(b,a) for a,b,c in rows)
            minor = all(implication(c,b) for a,b,c in rows)
            conclusion = all(implication(c,a) for a,b,c in rows)
            some = any(a and b for a,b,c in rows)
            counts['all_assignments'] += 1
            if major and minor:
                counts['all_premises'] += 1
                counts['all_failures'] += not conclusion
            if some and minor:
                counts['weak_premises'] += 1
                if not conclusion:
                    counts['weak_failures'] += 1
                    if first is None: first = n
            ext = {label: {i for i,row in enumerate(rows) if row[j]}
                   for j,label in enumerate(('A','B','C'))}
            for kind, expected in [('All',major),('Some',some)]:
                demand(evaluate(Proposition(kind,'A','B'),ext,{}) == expected, 'evaluate mismatch')
                evaluator_checks += 1
        for bits in itertools.product((False, True), repeat=2*n):
            rows = [bits[2*i:2*i+2] for i in range(n)]
            major = all(implication(b,a) for a,b in rows)
            for x in range(n):
                counts['member_assignments'] += 1
                a,b = rows[x]
                if major and b:
                    counts['member_premises'] += 1
                    counts['member_failures'] += not a
        for predicate in itertools.product((False,True), repeat=n):
            for x,y in itertools.product(range(n),repeat=2):
                if x == y:
                    counts['identities'] += 1
                    counts['identity_failures'] += predicate[x] != predicate[y]
    actual = experiments(3)
    comparisons = {
        'all_assignments': actual['all_chain']['assignments'],
        'all_premises': actual['all_chain']['premise_models'],
        'all_failures': actual['all_chain']['failures'],
        'weak_premises': actual['some_major_all_minor']['premise_models'],
        'weak_failures': actual['some_major_all_minor']['countermodels'],
        'member_assignments': actual['member_chain']['assignments'],
        'member_premises': actual['member_chain']['premise_models'],
        'member_failures': actual['member_chain']['failures'],
        'identities': actual['same_object_substitution']['equal_identity_assignments'],
        'identity_failures': actual['same_object_substitution']['failures'],
    }
    demand(counts == comparisons,'aggregate enumeration mismatch')
    demand(first == 2, 'minimal countermodel mismatch')
    saved = json.loads(Path('results.json').read_text())
    demand(saved == actual,'saved results stale')
    # Independent rule oracle: all possible labelled propositions over three names.
    props = [Proposition(k,p,s) for k in ('All','Some','Member')
             for p in ('A','B','C') for s in ('A','B','C')]
    triples = accepts = 0
    for m,n,c in itertools.product(props, repeat=3):
        oracle = any((m.kind,m.predicate,m.subject,n.kind,n.predicate,n.subject,
                      c.kind,c.predicate,c.subject) == ('All',p,b,k,b,s,k,p,s)
                     for p,b,s in itertools.product(('A','B','C'),repeat=3)
                     for k in ('All','Member'))
        result = check_chain(m,n,c)[0]
        demand(result == oracle,'certificate oracle mismatch')
        triples += 1
        accepts += result
    # Context variations must not get lost at any premise/conclusion position.
    rejected_contexts = 0
    base = [Proposition('All','A','B'),Proposition('All','B','C'),Proposition('All','A','C')]
    for position in range(3):
        for ctx in (Context('future'),Context(aspect='role')):
            candidate=base.copy(); p=candidate[position]
            candidate[position]=Proposition(p.kind,p.predicate,p.subject,ctx)
            demand(check_chain(*candidate) == (False,'context-mismatch'),'context guard failure')
            rejected_contexts += 1
    unsupported = check_chain(Proposition('All','A','B'),Proposition('Some','B','C'),Proposition('Some','A','C'))
    demand(unsupported == (False,'unsupported-minor'),'documented restricted rule mismatch')
    report = {'method':'independent per-object Boolean rows and exhaustive labelled rule oracle',
              'finite_domain_sizes':[0,1,2,3], 'counts':counts,
              'evaluate_cross_checks':evaluator_checks,
              'certificate_triples':triples, 'accepted_certificate_triples':accepts,
              'context_mismatches_rejected':rejected_contexts,
              'minimum_weak_countermodel_size':first,
              'saved_results_exact':True,
              'source_sha256':{f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
                               for f in ('model.py','test_model.py','results.json')},
              'limits':'finite testing; context labels supplied by caller; no ancient-semantic equivalence theorem'}
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
