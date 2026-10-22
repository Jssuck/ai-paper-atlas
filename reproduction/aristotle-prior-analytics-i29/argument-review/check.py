"""Independent finite checks for the I.29 explanatory mathematics.
No author model is imported. Each object has a triple of Boolean memberships.
These finite checks do not prove an unrestricted mathematical statement.
"""
import itertools
import json


def require(value, label):
    if not value:
        raise RuntimeError(label)


def relation(rows, s, p, kind):
    if kind == 'A':
        return all(not row[s] or row[p] for row in rows)
    if kind == 'E':
        return all(not(row[s] and row[p]) for row in rows)
    if kind == 'I':
        return any(row[s] and row[p] for row in rows)
    if kind == 'O':
        return any(row[s] and not row[p] for row in rows)
    raise ValueError(kind)


def run():
    # columns 0,1,2 may be named A,B,E or A,G,E or A,M,E.
    totals = {key: 0 for key in ('models', 'negative_premises',
              'particular_premises', 'only_positive_premises',
              'only_negative_premises', 'contradictory_pairs')}
    by_n = {}
    for n in range(1, 5):
        count = 0
        for rows in itertools.product(tuple(itertools.product((False, True), repeat=3)), repeat=n):
            count += 1
            totals['models'] += 1
            for s, p in itertools.product(range(3), repeat=2):
                require(relation(rows,s,p,'A') != relation(rows,s,p,'O'), 'A/O contradiction')
                require(relation(rows,s,p,'E') != relation(rows,s,p,'I'), 'E/I contradiction')
                totals['contradictory_pairs'] += 2
            # A subset B and B disjoint E -> A disjoint E.
            if relation(rows,0,1,'A') and relation(rows,1,2,'E'):
                totals['negative_premises'] += 1
                require(relation(rows,0,2,'E'), 'negative soundness')
            # Nonempty G subset A and G subset E -> A overlap E.
            if any(row[1] for row in rows) and relation(rows,1,0,'A') and relation(rows,1,2,'A'):
                totals['particular_premises'] += 1
                require(relation(rows,0,2,'I'), 'particular soundness')
            # Includes historical M subset E, even though it is redundant for target.
            if relation(rows,1,0,'A') and relation(rows,1,2,'A') and relation(rows,2,1,'A'):
                totals['only_positive_premises'] += 1
                require(relation(rows,2,0,'A'), 'only positive soundness')
            if relation(rows,0,1,'E') and relation(rows,1,2,'A') and relation(rows,2,1,'A'):
                totals['only_negative_premises'] += 1
                require(relation(rows,0,2,'E'), 'only negative soundness')
        by_n[str(n)] = count
    # Concrete article examples, reconstructed independently as sets.
    A,B,E={1},{1,2},{3}
    require(A <= B and not B&E and not A&E and not B<=A,'negative example and failed converse')
    A,E,G={1},{2},set()
    require(G<=A and G<=E and not A&E,'missing G existence, nonempty endpoints')
    A,E,G={1,2},{2,3},{2}
    require(G<=A and G<=E and A&E=={2} and not A<=E and not E<=A,'particular example')
    A,E,M={1},{1,2},{1}
    require(M<=A and M<=E and not E<=A,'missing only positive')
    A,E,M={2},{1,2},{1}
    require(not A&M and M<=E and bool(A&E),'missing only negative')
    # Nonempty-world countermodel: all terms are nonempty in both worlds.
    worlds = [({'2'}, {'1','2'}, {'1'}), ({'2'}, {'2'}, {'1'})]
    first = [e<=b for a,b,e in worlds]
    second = [b<=a for a,b,e in worlds]
    result = [e<=a for a,b,e in worlds]
    require(all(a and b and e for a,b,e in worlds),'all world terms nonempty')
    require(any(first) and any(second) and not any(result),'different possible witnesses')
    # Semantic RAA schema: enumerate possible sets of valuations of two propositions.
    # A model class Gamma is any subset of four classical Q/R valuations.
    valuations = tuple(itertools.product((False,True), repeat=2))
    raa_classes=0
    empty_gamma_classes=0
    for selection in itertools.product((False,True), repeat=len(valuations)):
        gamma = [v for selected,v in zip(selection,valuations) if selected]
        no_not_q_model = not any(not q for q,r in gamma)
        entails_q = all(q for q,r in gamma)
        require(no_not_q_model == entails_q,'RAA semantic equivalence')
        raa_classes+=1
        empty_gamma_classes += int(not gamma)
    return {'finite_checks_only': True, 'author_code_imported':False,
            'domain_sizes':by_n,'counts':totals,'named_examples_checked':6,
            'nonempty_two_world':{'E_subset_B':first,'B_subset_A':second,'E_subset_A':result},
            'raa_valuation_classes':raa_classes,'inconsistent_gamma_classes':empty_gamma_classes,
            'status':'PASS'}

if __name__ == '__main__':
    print(json.dumps(run(),ensure_ascii=False,indent=2,sort_keys=True))
