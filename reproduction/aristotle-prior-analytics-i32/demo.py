import json
from model import Prop, analyze, find_countermodel, candidate_completions, implication_chain_rows

A = lambda s, p: Prop('A', s, p)
E = lambda s, p: Prop('E', s, p)
I = lambda s, p: Prop('I', s, p)

def run():
    goal = A('S', 'P')
    examples = {
        'first_valid': ([A('M', 'P'), A('S', 'M')], goal, ()),
        'second_valid': ([E('P', 'M'), A('S', 'M')], E('S', 'P'), ()),
        'second_shape_invalid': ([A('P', 'M'), A('S', 'M')], goal, ()),
        'third_without_existence': ([A('M', 'P'), A('M', 'S')], I('S', 'P'), ()),
        'third_with_existence': ([A('M', 'P'), A('M', 'S')], I('S', 'P'), ('M',)),
    }
    out = {}
    for label, (premises, conclusion, nonempty) in examples.items():
        out[label] = {'premises': [p.as_dict() for p in premises], 'conclusion': conclusion.as_dict(),
                      'shape': analyze(premises, conclusion),
                      'finite_check': find_countermodel(premises, conclusion, nonempty=nonempty)}
    out['completion_hypotheses'] = candidate_completions(A('M', 'P'), goal,
        [A('S', 'M'), A('M', 'S'), goal, A('M', 'P')])
    out['existence_sentence_chain'] = implication_chain_rows()
    return out

if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True))
