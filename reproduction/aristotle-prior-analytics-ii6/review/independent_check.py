import sys,itertools,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import model
# Independent truth-bit oracle: quantification over selected member types.
def oracle(types):
    a=lambda t:bool(t&4); b=lambda t:bool(t&2); c=lambda t:bool(t&1)
    all_b_a=all(not b(t) or a(t) for t in types)
    all_a_b=all(not a(t) or b(t) for t in types)
    all_c_a=all(not c(t) or a(t) for t in types)
    all_a_c=all(not a(t) or c(t) for t in types)
    ac_no=not any(a(t) and c(t) for t in types)
    ab_no=not any(a(t) and b(t) for t in types)
    bc_no=not any(b(t) and c(t) for t in types)
    c_not_a=any(c(t) and not a(t) for t in types)
    c_not_b=any(c(t) and not b(t) for t in types)
    ac_yes=any(a(t) and c(t) for t in types)
    a_not_b=any(a(t) and not b(t) for t in types)
    cover=all(b(t) or a(t) for t in types)
    return dict(camestres_forward=(all_b_a and ac_no,bc_no),cesare_forward=(ab_no and all_c_a,bc_no),baroco_forward=(all_b_a and c_not_a,c_not_b),festino_forward=(ab_no and ac_yes,c_not_b),camestres_reverse_strengthened=(all_a_b and bc_no,ac_no),cesare_reverse_strengthened=(all_a_c and bc_no,ab_no),cesare_final_E_conversion=(ab_no,ab_no),baroco_reverse_strengthened=(all_a_b and c_not_b,c_not_a),festino_complement_coverage=(cover and c_not_b,ac_yes),camestres_reverse_unstrengthened=(all_b_a and bc_no,ac_no),cesare_reverse_unstrengthened=(all_c_a and bc_no,ab_no),baroco_reverse_unstrengthened=(all_b_a and c_not_b,c_not_a),festino_simple_E_conversion=(ab_no and c_not_b,ac_yes),festino_independent_witnesses=(ab_no and a_not_b and c_not_b,ac_yes))
for mask in range(1,256):
    m=model.from_mask(mask)
    got=model.rules(m); wanted=oracle(m.universe)
    if got!=wanted:
        raise RuntimeError((mask,{k:(got[k],wanted[k]) for k in got if got[k]!=wanted[k]}))
print('PASS 255 models x 14 rules: independently quantified truth-bit oracle matches model tuples')
for flag in (False,True):
    r=model.survey(flag)
    print('model count',r['models'],'valid',sum(v['countermodels']==0 for v in r['rules'].values()),'invalid',sum(v['countermodels']>0 for v in r['rules'].values()))
# Explicit supplementary article claim: H is sufficient but not necessary.
m=model.Model(frozenset({1,2,3}),frozenset({1}),frozenset({2}),frozenset({1}))
if not (model.E(m.a,m.b) and model.O(m.b,m.c) and model.I(m.a,m.c) and not model.A(m.a,m.not_b)):
    raise RuntimeError('nonnecessity example fails')
print('PASS explicit article H-nonnecessity example')
