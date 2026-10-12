"""Behavioral fault probes. Crashes/harness errors never count as mutant kills.

These are small alternative behaviors, not a claim that a source mutation tool
changed every implementation site. Expected observations are explicit witnesses.
"""
from dataclasses import dataclass, asdict
from itertools import product
import json
import condillac_model as m
from examples import chips, query_example, selector, causal_toy


def strict_equal(left, right):
    if type(left) is not type(right):
        return False
    if type(left) in (tuple,list):
        return len(left)==len(right) and all(strict_equal(a,b) for a,b in zip(left,right))
    if type(left) is dict:
        return strict_equal(tuple(left),tuple(right)) and all(strict_equal(left[k],right[k]) for k in left)
    return left==right


@dataclass(frozen=True)
class Outcome:
    status: str
    error_type: str | None = None


def classify(baseline, mutant, expected):
    try:
        actual = baseline()
    except Exception as exc:
        return Outcome('baseline_error',type(exc).__name__)
    if not strict_equal(actual,expected):
        return Outcome('invalid_baseline')
    try:
        changed = mutant()
    except Exception as exc:
        return Outcome('mutant_error',type(exc).__name__)
    return Outcome('survived' if strict_equal(changed,expected) else 'killed')


def accepts_boolean_world():
    try:
        m.Universe(('x',),((True,),))
    except (TypeError,ValueError):
        return False
    return True


def probes():
    full,known,narrow=query_example()
    original,*_=chips()
    empty=m.add_evidence(full,m.constraint(full.universe,'false',lambda w:False))
    constant=m.table(full.universe,'constant',lambda w:0)
    p,qs=selector()
    toy,oq=causal_toy()
    u=m.Universe(('a','b'),tuple(product((0,1),repeat=2)))
    xor=m.Problem(u,m.table(u,'xor',lambda w:w[0]^w[1]))
    xq=(m.table(u,'a',lambda w:w[0]),m.table(u,'b',lambda w:w[1]))
    andp=m.Problem(u,m.table(u,'and',lambda w:w[0]*w[1]))

    def check_chain():
        try: m.translation_chain((known,full,known))
        except ValueError: return False
        return True

    return [
        ('unique_world_instead_of_unique_answer',lambda:m.analyze(known).status,
         lambda:'identified' if len(m.candidates(known))==1 else 'underdetermined','identified'),
        ('empty_candidates_as_unique_answer',lambda:m.analyze(empty).status,
         lambda:'identified' if len(m.analyze(empty).answers)<=1 else 'underdetermined','inconsistent'),
        ('disjoin_instead_of_conjoin_data',lambda:len(m.candidates(original)),
         lambda:sum(any(c.mask[i] for c in original.constraints) for i in range(len(original.universe.worlds))),1),
        ('answer_identity_as_world_identity',lambda:m.compare_rewrite(known,narrow).worlds_preserved,
         lambda:set(m.analyze(known).answers)==set(m.analyze(narrow).answers),False),
        ('check_only_chain_endpoints',check_chain,
         lambda:m.compare_rewrite(known,known).worlds_preserved,False),
        ('ignore_conflicts_inside_encoding_fiber',lambda:m.compression(full,constant).sufficient,
         lambda:bool({constant.values[i]:full.target.values[i] for i in m.candidates(full)}),False),
        ('check_compression_outside_candidate_domain',lambda:m.compression(known,constant).sufficient,
         lambda:m.compression(full,constant).sufficient,True),
        ('require_observation_for_already_identified_query',lambda:m.minimax_tree(known,()).status,
         lambda:'impossible' if not () else 'measurement','identified'),
        ('force_nonadaptive_selector_schedule',lambda:m.minimax_tree(p,qs).depth,
         lambda:len(qs),2),
        ('mean_cost_instead_of_worst_case',lambda:m.minimax_tree(andp,xq).depth,
         lambda:sum(len(m.follow_tree(andp,xq,m.minimax_tree(andp,xq),i)[1]) for i in range(4))/4,2),
        ('common_presence_asserts_origin',lambda:m.minimax_tree(toy,oq).status,
         lambda:'identified' if len(set(oq[0].values))==1 else 'impossible','impossible'),
        ('boolean_as_integer_world',accepts_boolean_world,lambda:isinstance(True,int),False),
        ('only_first_measurement_signature',lambda:m.minimax_tree(xor,xq).status,
         lambda:m.minimax_tree(xor,xq[:1]).status,'measurement'),
    ]


def run():
    return {name:asdict(classify(base,mutant,expected)) for name,base,mutant,expected in probes()}


if __name__ == '__main__':
    result=run()
    print(json.dumps(result,ensure_ascii=False,indent=2))
    raise SystemExit(0 if all(r['status']=='killed' for r in result.values()) else 1)
