"""Isolated mutation sensitivity checks; production files are never modified."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent
MUTANTS=[
 ('A_negation','logic.py','        return not outside','        return outside','semantics'),
 ('E_negation','logic.py','        return not intersection','        return intersection','semantics'),
 ('I_negation','logic.py','        return intersection','        return not intersection','semantics'),
 ('O_negation','logic.py','    return outside\n','    return not outside\n','semantics'),
 ('ignore_nonempty_policy','logic.py','    return all(model.members(term) for term in language.required_nonempty)','    return True','semantics'),
 ('skip_support','logic.py','for support_mask in range(1, 1 << type_count):','for support_mask in range(2, 1 << type_count):','semantics'),
 ('reverse_E_conversion','proofs.py','return Prop("E", p.predicate, p.subject)','return Prop("E", p.subject, p.predicate)','rules'),
 ('wrong_I_output','proofs.py','return Prop("I", p.subject, q.predicate)','return Prop("O", p.subject, q.predicate)','rules'),
 ('wrong_O_output','proofs.py','return Prop("O", p.subject, q.predicate)','return Prop("I", p.subject, q.predicate)','rules'),
 ('allow_imported_claim','proofs.py','if step.claim != premises[premise_index]:','if False:','validation'),
 ('all_premises_dependencies','proofs.py','used = dependencies[-1]','used = frozenset(range(len(premises)))','validation'),
 ('accept_any_final_claim','proofs.py','if steps[-1].claim != conclusion:','if False:','validation'),
]
def main():
    results=[]
    before={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in ('logic.py','proofs.py')}
    for name,file,old,new,section in MUTANTS:
        with tempfile.TemporaryDirectory(prefix='i1-audit-mutant-') as work:
            work=Path(work)
            for production in ('logic.py','proofs.py'):
                shutil.copyfile(ROOT/production,work/production)
            original=(work/file).read_text()
            if original.count(old)!=1:
                raise RuntimeError(f'{name}: mutation target occurrence count {original.count(old)}')
            (work/file).write_text(original.replace(old,new,1))
            command=[sys.executable,'-B',str(OUT/'audit_checks.py'),'--module-root',str(work),'--section',section,'--quick']
            result=subprocess.run(command,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            (OUT/f'mutant-{name}.log').write_text(' '.join(command)+'\n'+result.stdout+f'\nExit code: {result.returncode}\n')
            # A detected semantic/contract mismatch must be our explicit RuntimeError.
            killed=result.returncode!=0 and 'RuntimeError:' in result.stdout and 'SyntaxError:' not in result.stdout
            results.append({'name':name,'file':file,'original':old,'replacement':new,'section':section,
                            'exit_code':result.returncode,'killed_by_independent_check':killed,
                            'failure':result.stdout.strip().splitlines()[-1],
                            'mutated_sha256':hashlib.sha256((work/file).read_bytes()).hexdigest()})
    after={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in before}
    report={'mutants':results,'killed':sum(x['killed_by_independent_check'] for x in results),
            'total':len(results),'production_unchanged':before==after,'source_hashes':before,
            'passed':all(x['killed_by_independent_check'] for x in results) and before==after}
    (OUT/'mutation-results.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,indent=2,sort_keys=True))
    return 0 if report['passed'] else 1
if __name__=='__main__':
    raise SystemExit(main())
