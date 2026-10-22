"""Finite semantic diagnostics, not proof of ancient syllogistic completeness."""
import json
from model import Model, models, named_models, FORMS


def require(value, message):
    if not value:
        raise RuntimeError(message)


def run():
    result = {'scope':'Modern actual-subject semantics, n=1,2; two labelled worlds and both actual indices; empty term extensions allowed.',
              'configurations':0, 'checks':0, 'forward_bridge_cases':0,
              'reverse_rigid_bridge_cases':0, 'raw_rule_counterexamples':0,
              'contingent_quality_equivalences':0, 'failed_family_pairs':[], 'named':{}}
    for n in (1,2):
        for m in models(n):
            result['configurations'] += 1
            # Every universal/particular strict contingent statement is invariant under quality change.
            for p in ('A','B','C'):
                for s in ('A','B','C'):
                    for yes,no in (('A','E'),('I','O')):
                        require(m.categorical(p,s,yes,'contingent') == m.categorical(p,s,no,'contingent'), 'quality')
                        result['contingent_quality_equivalences'] += 1
            for form,conclusion in (('A','E'),('E','E'),('I','O'),('O','O')):
                premises = m.categorical('A','B','E') and m.categorical('A','C',form,'contingent')
                weak = m.categorical('B','C',conclusion,'possible')
                if premises and not weak:
                    result['raw_rule_counterexamples'] += 1
                if premises and m.persistent_exclusion('A','B'):
                    result['forward_bridge_cases'] += 1
                    require(weak, 'forward bridge')
                    result['checks'] += 1
                # Universal reverse orientation: a sufficient, deliberately strong bridge.
                reverse = m.categorical('A','C','E') and m.categorical('A','B',form,'contingent')
                if form in ('A','E') and reverse and m.persistent_exclusion('A','C') and m.rigid('B') and m.rigid('C'):
                    result['reverse_rigid_bridge_cases'] += 1
                    require(m.categorical('B','C','E','possible'), 'reverse rigid bridge')
                    result['checks'] += 1
            # Actual universal negatives can be converted without modal assumptions.
            require(m.categorical('A','B','E') == m.categorical('B','A','E'), 'actual E conversion')
            result['checks'] += 1
    # Paired endpoint models for the failed families explicitly discussed in I.18.
    # This is a transparent modern construction, not an interpretation of natural essences.
    for actual_side in ('B','C'):
        contingent_side = 'C' if actual_side == 'B' else 'B'
        for actual_form in ('A','I','O'):
            for contingent_form in FORMS:
                a0 = 0 if actual_form == 'O' else 3
                overlap = Model(2, ((a0,3,1),(3-a0,3,1)))
                separated = Model(2, ((a0,2,1),(3-a0,2,1)))
                for m in (overlap,separated):
                    require(m.categorical('A',actual_side,actual_form), 'paired actual premise')
                    require(m.categorical('A',contingent_side,contingent_form,'contingent'), 'paired Q premise')
                require(overlap.categorical('B','C','A','necessary'), 'overlap endpoint')
                require(separated.categorical('B','C','E','necessary'), 'separated endpoint')
                result['failed_family_pairs'].append({'actual_subject':actual_side,
                    'actual_form':actual_form,'contingent_form':contingent_form,
                    'overlap':overlap.as_dict(),'separated':separated.as_dict()})
    for name,m in named_models().items():
        result['named'][name] = {'model':m.as_dict(),
            'E0_A_B':m.categorical('A','B','E'), 'Q_A_C':m.categorical('A','C','A','contingent'),
            'persistent_A_B':m.persistent_exclusion('A','B'),
            'B_C':{mode:{f:m.categorical('B','C',f,mode) for f in FORMS}
                   for mode in ('actual','possible','necessary','contingent')},
            'M_notC_B':m.categorical('C','B','E','possible'),
            'joint_M_notB_C':m.jointly_possible('B','C',False)}
    return result

if __name__ == '__main__':
    print(json.dumps(run(),ensure_ascii=False,indent=2))
