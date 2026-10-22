"""Independent bit-mask oracle; finite audit, not a general proof."""
import json
from itertools import product
from division import FiniteModel, Step


def check(ok, message):
    if not ok:
        raise RuntimeError(message)


def rejects(call):
    try:
        call()
    except (ValueError, TypeError):
        return
    raise RuntimeError('Expected input or certificate rejection')


def run():
    counts = dict(models=0, report_fields=0, certificates=0,
                  accepted=0, missing_certificates_rejected=0,
                  renamed_models=0, definitions=0, special_checks=0)
    for n in range(1, 5):
        full = (1 << n) - 1
        subsets = [{i for i in range(n) if mask & (1 << i)} for mask in range(full + 1)]
        for a, b, c, d in product(range(full + 1), repeat=4):
            m = FiniteModel(set(range(n)), dict(zip('ABCD', [subsets[t] for t in (a,b,c,d)])))
            incl = lambda x,y: (x & (full ^ y)) == 0
            prem = incl(a,b|c) and incl(d,a)
            expected = dict(coverage=incl(a,b|c), target_in_parent=incl(d,a),
                            premises=prem, target_nonempty=d != 0,
                            disjoint_children=(b&c)==0, children_within_parent=incl(b|c,a),
                            pointwise_disjunction=incl(d,b|c), all_left=incl(d,b),
                            all_right=incl(d,c), uniform_disjunction=incl(d,b) or incl(d,c))
            check(m.division_report('A','B','C','D') == expected, 'report mismatch')
            counts['models'] += 1; counts['report_fields'] += len(expected)
            check(m.definition_report('D','B') == dict(necessary=incl(d,b), sufficient=incl(b,d), coextensive=d==b), 'definition mismatch')
            counts['definitions'] += 1
            for side, other, name in [('left',c,'B'),('right',b,'C')]:
                expected_accept = prem and (d & other) == 0
                if expected_accept:
                    check(m.select_branch('A','B','C','D',side,exclude_other=True)==name,'wrong selected name')
                    counts['accepted'] += 1
                else:
                    rejects(lambda: m.select_branch('A','B','C','D',side,exclude_other=True))
                counts['certificates'] += 1
                rejects(lambda: m.select_branch('A','B','C','D',side))
                counts['missing_certificates_rejected'] += 1
            # Independent injective rename to sparse nonnegative labels.
            if n <= 2:
                renamed = FiniteModel({17+7*i for i in range(n)}, {k:{17+7*i for i in v} for k,v in m.terms.items()})
                check(renamed.division_report('A','B','C','D')==expected,'rename changed result')
                counts['renamed_models'] += 1
    m=FiniteModel({0,1,2},{'A':{0,1,2},'B':{0,1},'C':{2},'D':{0},'E':{0},'F':{1}})
    check(m.follow_path('D',[Step('A','B','C','left',True),Step('B','E','F','left',True)])==('B','E'),'path result')
    counts['special_checks'] += 1
    cases=[lambda:m.follow_path('D',[Step('A','B','C','left',True),Step('B','E','F','left',False)]),
           lambda:m.follow_path('D',[Step('A','B','C','left',False),Step('B','E','F','left',True)]),
           lambda:m.follow_path('D',[Step('A','B','C','left',True),Step('A','B','C','left',True)]),
           lambda:m.follow_path('D',[]),lambda:m.follow_path('D',[None]),
           lambda:m.select_branch('A','B','C','D','left',exclude_other=1),
           lambda:m.select_branch('A','B','C','D',None,exclude_other=True),
           lambda:m.term('absent'),lambda:m.term(0),
           lambda:FiniteModel({0},{'A':{1}}),lambda:FiniteModel({True},{'A':set()}),
           lambda:FiniteModel({-1},{'A':set()}),lambda:FiniteModel({0.0},{'A':set()}),
           lambda:FiniteModel(set(),{'A':set()}),lambda:FiniteModel({0},{}),
           lambda:FiniteModel({0},{' A':set()}),lambda:FiniteModel([0],{'A':set()})]
    for call in cases:
        rejects(call);counts['special_checks']+=1
    return {'scope':'All four-term bit masks n=1..4; finite audit only', 'counts':counts, 'result':'PASS'}

if __name__ == '__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
