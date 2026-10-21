"""Recompute small, inspectable tables and counterexamples as JSON."""
import json
from fractions import Fraction
from itertools import product
import boole_model as m


def main():
    ship=m.truth_table(3,m.ship_example)
    identity=m.truth_table(2,m.identity_example)
    u=frozenset({0,1,2}); x=frozenset({0,1}); y=frozenset({1,2})
    cases={}
    for f0,f1 in ((0,0),(0,2),(-3,0),(1,-1),(2,2)):
        cases[f'{f0},{f1}']=list(m.endpoint_choices(f0,f1))
    cx, cy, cz = frozenset({0}), frozenset(), frozenset({1})
    cv, cvp, cxx, czz = 0, 0, 0, 1
    out={
        'semantic_policy':'pointwise rational indicators; empty classes allowed; particular claims need witnesses',
        'identity_table': [{'xy':list(a),'value':str(v)} for a,v in identity.items()],
        'identity_forbidden_atoms':[list(a) for a in sorted(m.forbidden_constituents(identity))],
        'ship_table':[{'xyz':list(a),'value':str(v)} for a,v in ship.items()],
        'ship_endpoint_choices':[{'xy':list(a),'allowed_z':list(zs)} for a,zs in m.endpoint_table(ship).items()],
        'ship_example':{'universe':sorted(u),'X':sorted(x),'Y':sorted(y),
                        'all_Z':sorted([sorted(z) for z in m.solve_last_class(ship,u,(x,y))])},
        'endpoint_cases_f0_f1':cases,
        'existence_counterexample':{'universe':[0,1],'X':[0],'Y':[],'Z':[1],
                                   'Y_subset_X':cy <= cx,'Y_subset_Z':cy <= cz,'X_intersect_Z_nonempty':bool(cx & cz)},
        'elimination_counterexample':{'v':0,'v_prime':0,'x':0,'z':1,
                                     'eliminated_equality':cv*czz == cvp*(cv-cxx),
                                     'exists_y_for_both_original_equations':any(cxx==cv*y and czz==cvp*(1-y) for y in (0,1))},
        'finite_coverage_counts':{
            'identity_class_pairs_sizes_0_through_3':sum(4**n for n in range(4)),
            'ship_X_Y_inputs_sizes_0_through_3':sum(4**n for n in range(4)),
            'ship_candidate_Z_set_checks_sizes_0_through_3':sum(8**n for n in range(4)),
            'complement_fixed_V_Y_inputs_sizes_0_through_3':sum(4**n for n in range(4)),
            'rational_two_variable_tables':3**4,
            'rational_endpoint_pairs':6**2,
            'direct_elimination_bit_assignments':2**4,
            'direct_elimination_two_element_set_assignments':4**4,
        },
        'limits':['No proof assistant or Jupyter kernel.',
                  'Finite tests do not prove general claims.',
                  'Not a reproduction of every historical syllogistic rule or the psychological claims.']
    }
    print(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True))

if __name__=='__main__': main()
