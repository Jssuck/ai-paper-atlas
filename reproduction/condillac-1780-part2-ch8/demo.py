"""Deterministic, machine-readable teaching demonstrations."""
from dataclasses import asdict
from itertools import combinations
import json
import condillac_model as m
from examples import chips, query_example, selector, causal_toy, causal_run


def results():
    original, expanded, eliminated, solved, insufficient = chips()
    full, known, narrower = query_example()
    p, qs = selector()
    tree = m.minimax_tree(p, qs)
    fixed = []
    for size in range(4):
        for subset in combinations(range(3), size):
            code = m.table(p.universe, 'joint response', lambda w, subset=subset: tuple(w[i] for i in subset))
            fixed.append({'questions':[qs[i].name for i in subset], 'sufficient':m.compression(p,code).sufficient})
    toy, observations = causal_toy()
    return {
        'scope':'modern finite teaching model; not historical algorithm or empirical psychology',
        'chips': {'universe':'integers 0..10 in each hand, with both transfers feasible',
                  'before':asdict(m.analyze(insufficient)), 'after':asdict(m.analyze(original)),
                  'translation_steps':[asdict(r) for r in m.translation_chain((original, expanded, eliminated, solved))],
                  'worlds':[original.universe.worlds[i] for i in m.candidates(original)],
                  'too_small_bound_6':m.analyze(chips(6)[0]).status},
        'query_relative': {'known':asdict(m.analyze(known)),
                           'answer_preserving_but_not_world_preserving':asdict(m.compare_rewrite(known,narrower)),
                           'encode_x':asdict(m.compression(full,full.target)),
                           'encode_constant':asdict(m.compression(full,m.table(full.universe,'constant',lambda w:0)))},
        'adaptive_selector': {'tree':asdict(tree), 'fixed_subsets':fixed,
                              'replays':[{'world':w,'answer':m.follow_tree(p,qs,tree,i)[0],
                                          'questions':m.follow_tree(p,qs,tree,i)[1]} for i,w in enumerate(p.universe.worlds)]},
        'causal_toy': {'models': {'M1':'S:=U; A:=S', 'M2':'A:=U; S:=A'},
                       'natural_observations':observations[0].values,
                       'intervention_fixed_U_0_do_S_1':{label:causal_run(label,0,do_s=1) for label in ('M1','M2')},
                       'with_intervention':asdict(m.minimax_tree(toy, observations +
                          (m.table(toy.universe,'do(S=1), U=0',lambda w:causal_run(w[0],0,do_s=1)),))),
                       'analysis':asdict(m.analyze(toy)), 'plan':asdict(m.minimax_tree(toy,observations)),
                       'warning':'co-presence alone does not distinguish these stipulated causal stories'},
        'empty_universe': {'analysis':asdict(m.analyze(m.Problem(m.Universe(('x',),()),m.Table(m.Universe(('x',),()),'x',()))))}
    }


if __name__ == '__main__':
    print(json.dumps(results(), ensure_ascii=False, indent=2))
