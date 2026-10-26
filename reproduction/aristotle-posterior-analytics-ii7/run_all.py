"""Exhaustive finite checks with an independent element-wise oracle."""
import itertools
import json
from model import (coextensive, witness_valid, transfer_witness, observations_agree,
                   binding_valid, named_witness, NameClaim, subsets)


def run():
    counts = dict(pair_models=0, equal_models=0, equal_empty_models=0,
                  transfer_premises=0, transfer_violations=0,
                  observation_models=0, sample_agreements=0,
                  sample_agrees_global_differs=0, oracle_mismatches=0)
    for n in range(5):
        u = frozenset(range(n)); sets = subsets(n)
        for p, q in itertools.product(sets, repeat=2):
            counts['pair_models'] += 1
            eq = coextensive(u,p,q)
            oracle = all((i in p) == (i in q) for i in range(n))
            counts['oracle_mismatches'] += eq != oracle
            counts['equal_models'] += eq
            counts['equal_empty_models'] += eq and not p
            for w in range(n):
                premise = transfer_witness(u,p,q,w)
                independent = oracle and (w in q)
                counts['oracle_mismatches'] += premise != independent
                counts['transfer_premises'] += premise
                counts['transfer_violations'] += premise and not witness_valid(u,p,w)
            for s in sets:
                counts['observation_models'] += 1
                agree = observations_agree(u,s,p,q)
                ind_agree = all((i in p)==(i in q) for i in range(n) if i in s)
                counts['oracle_mismatches'] += agree != ind_agree
                counts['sample_agreements'] += agree
                counts['sample_agrees_global_differs'] += agree and not eq
    names = ['circle','mountain_copper','goat_stag']
    formulas = {'inhabited':frozenset({0}), 'empty':frozenset()}
    checks=0; accepted=0
    for choices in itertools.product(formulas,repeat=3):
        lexicon=dict(zip(names,choices))
        for name in names:
            for fid in formulas:
                checks+=1
                claim=NameClaim(name,fid)
                actual=named_witness({0},formulas,lexicon,claim,0)
                expected=lexicon[name]==fid and fid=='inhabited'
                if actual != expected:
                    raise RuntimeError('name/member oracle mismatch')
                accepted+=actual
    counts['name_claim_checks']=checks
    counts['named_witnesses_accepted']=accepted
    expected = dict(pair_models=341,equal_models=31,equal_empty_models=5,
                    transfer_premises=49,transfer_violations=0,
                    observation_models=4681,sample_agreements=1555,
                    sample_agrees_global_differs=1214,oracle_mismatches=0,
                    name_claim_checks=48,named_witnesses_accepted=12)
    if counts != expected:
        raise RuntimeError((counts,expected))
    return {'scope':'n=0..4; finite interpretation only; not real existence or essence',
            'counts':counts,
            'examples':{
                'empty_equal':coextensive({0},set(),set()),
                'empty_has_witness':witness_valid({0},set(),0),
                'sample_agreement':observations_agree({0,1},{0},{0},{0,1}),
                'global_agreement':coextensive({0,1},{0},{0,1}),
                'circle_binding':binding_valid({'circle':'equidistant'},NameClaim('circle','equidistant')),
                'renamed_binding':binding_valid({'circle':'equidistant'},NameClaim('mountain_copper','equidistant'))}}

if __name__=='__main__':
    print(json.dumps(run(),ensure_ascii=False,indent=2))
