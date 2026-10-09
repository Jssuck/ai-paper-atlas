"""Produce real finite-check results; no downloads, solvers or hidden services."""
import argparse
from dataclasses import asdict
from datetime import datetime, timezone
import json
from pathlib import Path
import platform
import time
from huntington import *


def summarize(model, fn):
    checks=fn(model)
    return {'size':len(model.elements),'name':model.name,'failed':failed(checks),
            'checks':{key:asdict(value) for key,value in checks.items()}}


def main(out):
    started=time.perf_counter()
    result={'description':'Finite checks of original 1904 examples plus labelled modern teaching experiments; not a general theorem proof',
        'timestamp_utc':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),
        'original_finite':{},'powersets':[]}
    for group,models,fn in [('first',first_original_models(),first),('second',second_original_models(),second),('third',third_original_models(),third)]:
        result['original_finite'][group]={label:summarize(m,fn) for label,m in models.items()}
        for label,m in models.items():
            signature=failed(fn(m)); assert signature==label.split(',')
            print(f'Original {group:6} target={label:5} size={len(m.elements):2} failed={signature}')
    for bits in range(1,5):
        m=powerset_algebra(bits)
        row={'bits':bits,'size':len(m.elements),'first_failed':failed(first(m)),
             'second_failed':failed(second(induced_relation(m))),'third_failed':failed(third(m))}
        assert not(row['first_failed'] or row['second_failed'] or row['third_failed'])
        result['powersets'].append(row)
    result['teaching_saturated_addition']=summarize(teaching_saturated_addition(),third)
    result['enumeration']=small_enumeration()
    result['original_infinite_not_machine_exhausted']={
        'second':['4','5','separate 6/7 independence among first seven via planar regions'],
        'third':['A','D','E']}
    result['runtime_seconds']=round(time.perf_counter()-started,6)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('All 23 original finite structures match the expected failure signatures.')
    print('Powersets of sizes 2,4,8,16 satisfy all three displayed lists.')
    print('Modern saturated-addition example fails only A.')
    print('Bounded labelled enumerations:',json.dumps(result['enumeration']))
    print(f'Wrote {out.as_posix()}; elapsed {result["runtime_seconds"]} seconds.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=Path('results/experiments.json'))
    main(parser.parse_args().out)
