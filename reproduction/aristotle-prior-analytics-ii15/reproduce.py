#!/usr/bin/env python3
"""Original teaching model for Prior Analytics II.15, not an ancient interpreter."""
import json
from itertools import product

KINDS = 'UEIO'
MOODS = {
    1: {'UUU': None, 'EUE': None, 'UII': None, 'EIO': None},
    2: {'EUE': None, 'UEE': None, 'EIO': None, 'UOO': None},
    3: {'UUI': 'M', 'IUI': None, 'UII': None, 'EUO': 'M', 'OUO': None, 'EIO': None},
}
PAIRS = ('UE', 'EU', 'UO', 'OU', 'IE', 'EI')

def proposition(kind, predicate, subject):
    if not all(isinstance(x,str) and len(x)==1 for x in (kind,predicate,subject)) or kind not in KINDS or predicate not in 'PMS' or subject not in 'PMS':
        raise ValueError('Expected U/E/I/O and single term P/M/S')
    return (kind, predicate, subject)

def premises(figure, pair):
    if type(figure) is not int or figure not in MOODS or not isinstance(pair,str) or len(pair)!=2 or any(k not in KINDS for k in pair):
        raise ValueError('Invalid figure or premise qualities')
    slots = {1:(('P','M'),('M','S')),2:(('M','P'),('M','S')),3:(('P','M'),('S','M'))}[figure]
    return tuple(proposition(k,*slot) for k,slot in zip(pair,slots))

def validate_existence(nonempty):
    if not isinstance(nonempty,(tuple,list,set,frozenset)) or any(t not in ('P','M','S') for t in nonempty):
        raise ValueError('Expected a collection of existence terms P/M/S')

def formal_conclusions(figure, pair, nonempty=()):
    """Fixed standard moods, not semantic explosion; no inferred existence."""
    premises(figure,pair)
    validate_existence(nonempty)
    return tuple(proposition(mood[2],'P','S') for mood,need in MOODS[figure].items()
                 if mood[:2]==pair and (need is None or need in nonempty))

def models():
    """Nonempty universe: each of eight unary membership types occurs 0/1 times."""
    for mask in range(1,256):
        yield {name:frozenset(t for t in range(8) if mask>>t&1 and t>>i&1)
               for i,name in enumerate('PMS')}

def holds(prop, model):
    kind,p,s=proposition(*prop)
    pred,sub=model[p],model[s]
    return {'U': sub<=pred, 'E': not(sub&pred), 'I': bool(sub&pred), 'O': bool(sub-pred)}[kind]

def encode(model):
    return {k:sorted(v) for k,v in model.items()}

def assess(assumptions, conclusion, equal_extremes=False, nonempty=()):
    validate_existence(nonempty)
    assumptions=tuple(assumptions)
    proposition(*conclusion)
    for p in assumptions: proposition(*p)
    backgrounds=[m for m in models() if (not equal_extremes or m['P']==m['S']) and all(m[t] for t in nonempty)]
    sat=[m for m in backgrounds if all(holds(p,m) for p in assumptions)]
    bad=next((m for m in sat if not holds(conclusion,m)),None)
    false_background=next((m for m in backgrounds if not holds(conclusion,m)),None)
    return {'background_models':len(backgrounds),'premise_models':len(sat),
            'semantic_entailment':bad is None,'vacuous':not sat,
            'countermodel':encode(bad) if bad else None,
            'conclusion_false_in_background':sum(not holds(conclusion,m) for m in backgrounds),
            'background_witness':encode(false_background) if false_background else None}

def routes():
    result=[]
    for figure,pair in product((2,3),PAIRS):
        ps=premises(figure,pair)
        conclusions=formal_conclusions(figure,pair,('P','M','S'))
        reversed_terms=False
        if not conclusions:
            # Figures 2/3 remain the same on exchanging their two extremes.
            conclusions=formal_conclusions(figure,pair[::-1],('P','M','S'))
            conclusions=tuple((q,'S','P') for q,_,_ in conclusions)
            reversed_terms=True
        if len(conclusions)!=1: raise RuntimeError('Each chosen route needs exactly one negative result')
        c=conclusions[0]
        need='M' if figure==3 and pair in ('UE','EU') else None
        result.append({'figure':figure,'pair':pair,'premises':ps,'conclusion':c,
                       'exchanged_extremes':reversed_terms,'existence_required':need,
                       'distinct_terms':assess(ps,c,False,(need,) if need else ()),
                       'identified_extremes':assess(ps,c,True,('P','M','S')),
                       'empty_terms_allowed':assess(ps,c,True,())})
    return result

def subset_examples():
    # Figure 2: P=science, S=medicine, M=good.
    ps=premises(2,'UE')
    c=('E','P','S')
    rows=[]
    for label,relation,exists in (
        ('no_inclusion_background',False,False),
        ('medicine_in_science_empty_allowed',True,False),
        ('medicine_in_science_nonempty',True,True)):
        bg=[m for m in models() if (not relation or m['S']<=m['P']) and (not exists or m['S'])]
        joint=[m for m in bg if all(holds(p,m) for p in ps)]
        witness=next((m for m in joint if holds(c,m) and all(m[t] for t in 'PMS')),None)
        if witness is None: witness=next((m for m in joint if holds(c,m)),None)
        rows.append({'label':label,'background_models':len(bg),'premise_models':len(joint),
                     'conclusion_false_in_background':sum(not holds(c,m) for m in bg),
                     'joint_witness':encode(witness) if witness else None})
    return rows

def run():
    checks=[]
    for figure,pair in product((1,2,3),(''.join(p) for p in product(KINDS,repeat=2))):
        for c in formal_conclusions(figure,pair,('P','M','S')):
            x=assess(premises(figure,pair),c,False,('P','M','S'))
            if not x['semantic_entailment']: raise RuntimeError('Unsound standard rule')
            checks.append({'figure':figure,'pair':pair,'conclusion':c,'premise_models':x['premise_models']})
    io=next(m for m in models() if holds(('I','P','S'),m) and holds(('O','P','S'),m))
    ue_empty=next(m for m in models() if not m['S'] and holds(('U','P','S'),m) and holds(('E','P','S'),m))
    contradictory=(('U','P','S'),('O','P','S'))
    explosion=assess(contradictory,('U','S','M'))
    return {'scope':'Finite modern unary-set model; standard mood certificates are separate from semantic entailment.',
            'models':255,'all_terms_nonempty_models':sum(all(m[t] for t in 'PMS') for m in models()),
            'standard_rule_checks':checks,'opposite_routes':routes(),'subset_examples':subset_examples(),
            'particulars_coexist':encode(io),'contraries_empty_subject':encode(ue_empty),
            'vacuous_entailment_not_a_formal_rule':explosion,
            'first_figure_direct_opposition':False,
            'first_figure_reason':'After P=S, premise pairs are P(M), M(P), not the same predicate and subject. Extra conversion is a separate step.'}

if __name__=='__main__':
    print(json.dumps(run(),ensure_ascii=False,indent=2,sort_keys=True))
