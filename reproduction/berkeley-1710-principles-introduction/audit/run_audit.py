"""Reproduce independent audit evidence without silently rebinding the review."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/'audit'
MUTANTS={
 'linear_rhs':('Verification(combined == target, combined, tuple(dependencies))','Verification(combined.coefficients == target.coefficients, combined, tuple(dependencies))'),
 'linear_coefficients':('Verification(combined == target, combined, tuple(dependencies))','Verification(combined.rhs == target.rhs, combined, tuple(dependencies))'),
 'zero_support':('if weight != 0:', 'if True:'),
 'restriction_support':('if missing:', 'if False:'),
 'triangle_rightness':('return x + y == z','return x + y >= z'),
 'finite_coverage':('return self.denotation == frozenset(self.domain)','return bool(self.denotation)'),
 'finite_denotation':('if triangle in sign.denotation:','if True:'),
 'add_terms':('return _add_poly(normalize(expression.left), normalize(expression.right))','return normalize(expression.left)'),
 'multiply_exponents':('powers[variable] = powers.get(variable, 0) + exponent','powers[variable] = max(powers.get(variable, 0), exponent)'),
 'expr_multiplication':('return visit(node.left) * visit(node.right)','return visit(node.left) + visit(node.right)'),
 'polynomial_power':('term *= environment[variable] ** exponent','term *= environment[variable]'),
 'simultaneous_substitution':('return validated.get(node.name, node)','return visit(validated[node.name]) if node.name in validated else node'),
 'reject_boolean':('if type(value) not in (int, Fraction):','if not isinstance(value, (int, Fraction)):'),
}


def now(): return datetime.now(timezone.utc).isoformat()
def sha(data): return hashlib.sha256(data).hexdigest()
def require(condition,message):
    if not condition: raise RuntimeError(message)


def examples_check(output):
    l=output['linear_certificate']; f=output['finite_sign'];p=output['polynomial']
    require(l['valid'] is True and l['combined_coefficients']==['1','1','1','0','0'] and l['combined_rhs']=='180','linear output mismatch')
    require(l['nonzero_dependencies']==['alternate_a','alternate_c','straight_angle'] and l['after_removing_special_drawing_facts'] is True,'support output mismatch')
    require(l['right_angle_target_initially_valid'] is True and l['right_angle_dependencies']==['drawing_right'] and l['right_angle_transfer']['allowed'] is False and l['right_angle_direct_check_after_deletion'] is False,'restriction negative mismatch')
    a=l['nonright_countermodel_for_general_premises']
    require(a['a']==a['u'] and a['c']==a['v'] and a['u']+a['b']+a['v']==180 and a['b']!=90,'countermodel mismatch')
    require(f['domain_size']==3 and f['squared_side_lengths']==[[9,16,25],[4,5,5],[2,10,16]] and f['right_angle_predicate']==[True,False,False],'triangle output mismatch')
    require(f['general_sign_covers_declared_domain'] is True and f['singleton_representative_covers_declared_domain'] is False and f['counterexample_to_all_are_right']==[[0,0],[2,0],[1,2]],'finite output mismatch')
    require(p['equal_canonical_forms'] is True and p['canonical_terms']==[[[['x',1],['y',1]],'1'],[[['x',1],['z',1]],'1']],'polynomial output mismatch')
    require(p['left_value']==p['right_value']==p['normalized_value']=='29/15','polynomial value mismatch')
    require(p['simultaneous_substitution_x_to_y_plus_1_and_y_to_2']=={'result':'y+1','value_when_y_is_10':'11'},'substitution output mismatch')


def main():
    logs=AUDIT/'logs'; logs.mkdir(exist_ok=True)
    scratch=AUDIT/'_mutation'; scratch.mkdir(exist_ok=True)
    source=(ROOT/'model.py').read_text(encoding='utf-8')
    inputs=('model.py','test_model.py','examples.py','run_checks.py','audit/independent_checks.py','audit/run_audit.py')
    bindings={name:sha((ROOT/name).read_bytes()) for name in inputs}
    report={'started_utc':now(),'python':sys.version,'python_implementation':platform.python_implementation(),
            'python_executable_basename':Path(sys.executable).name,'platform':platform.platform(),
            'working_directory':'.','source_sha256':bindings,'runs':[],
            'scope':'Independent bounded tests and deliberate semantic faults; not a formal program proof or cognitive evidence.'}
    def execute(mode,options,args,label,model=None):
        env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
        if model: env['AUDIT_MODEL']=model
        else: env.pop('AUDIT_MODEL',None)
        started=now()
        completed=subprocess.run([sys.executable,*options,*args],cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8',check=False)
        prefix=f'{mode}-{label}'
        out=logs/(prefix+'.stdout.txt');err=logs/(prefix+'.stderr.txt')
        out.write_text(completed.stdout,encoding='utf-8');err.write_text(completed.stderr,encoding='utf-8')
        row={'mode':mode,'command':['python3',*options,*args],'started_utc':started,'finished_utc':now(),
             'returncode':completed.returncode,'stdout':str(out.relative_to(ROOT)),'stderr':str(err.relative_to(ROOT))}
        if model:row['model_override']=model
        try:row['output']=json.loads(completed.stdout)
        except json.JSONDecodeError:row['parse_error']='stdout is not one complete JSON value'
        report['runs'].append(row)
        return row
    errors=[]; examples=[];independent=[];authors=[];mutations=[];framework=[]
    try:
        for mode,options in (('normal',[]),('O',['-O']),('OO',['-OO'])):
            a=execute(mode,options,['test_model.py'],'author-tests');authors.append(a)
            require(a['returncode']==0 and a['output']['successful'] is True and a['output']['failures']==a['output']['errors']==a['output']['skipped']==0,'author tests failed')
            e=execute(mode,options,['examples.py'],'author-examples');examples.append(e)
            require(e['returncode']==0,'author examples failed');examples_check(e['output'])
            i=execute(mode,options,['audit/independent_checks.py'],'independent');independent.append(i)
            require(i['returncode']==0 and i['output']['status']=='passed','independent oracle failure')
            for name,(old,new) in MUTANTS.items():
                require(source.count(old)==1,'mutation anchor is not unique: '+name)
                baseline=execute(mode,options,['audit/independent_checks.py','--probe',name],'baseline-'+name)
                require(baseline['returncode']==0 and baseline['output']['status']=='passed','baseline probe failed: '+name)
                changed=source.replace(old,new)
                relative='audit/_mutation/'+name+'.py';path=ROOT/relative
                path.write_text(changed,encoding='utf-8')
                run=execute(mode,options,['audit/independent_checks.py','--probe',name],'mutant-'+name,relative)
                record={'mode':mode,'mutant':name,'mutant_sha256':sha(changed.encode('utf-8')),'old':old,'new':new,
                        'detected_semantically':run['returncode']==1 and run.get('output',{}).get('status')=='semantic_failure',
                        'stdout':run['stdout'],'stderr':run['stderr']}
                mutations.append(record)
                require(record['detected_semantically'],'mutant not semantically detected: '+name)
            probe=execute(mode,options,['audit/independent_checks.py','--probe','framework_exception'],'framework-exception')
            framework.append(probe)
            require(probe['returncode']==2 and probe['output']['status']=='framework_error','framework error was misclassified')
        require(all(i['output']['counts']==independent[0]['output']['counts'] for i in independent),'independent mode counts differ')
        require(len({(ROOT/e['stdout']).read_bytes() for e in examples})==1,'example outputs differ across modes')
        require(all(sha((ROOT/name).read_bytes())==digest for name,digest in bindings.items()),'source changed during audit')
    except Exception as error:
        errors.append(str(error))
    finally:
        shutil.rmtree(scratch)
    stored=json.loads((ROOT/'results.json').read_text(encoding='utf-8'))
    matching=all(any(r.get('script')=='test_model.py' and r.get('mode')==a['mode'] and r.get('output')==a.get('output') and r.get('returncode')==a['returncode'] for r in stored['runs']) for a in authors)
    if not matching:errors.append('author stored test results do not match audit reruns')
    report.update({'finished_utc':now(),'successful':not errors,'errors':errors,'subprocesses':len(report['runs']),
                   'author_method_counts':{r['mode']:r.get('output',{}).get('tests_run') for r in authors},
                   'independent_counts':independent[0]['output'].get('counts',{}) if independent else {},
                   'semantic_mutants':mutations,'semantic_mutants_per_mode':len(MUTANTS),
                   'semantic_detections':sum(x['detected_semantically'] for x in mutations),
                   'framework_errors_correctly_classified':len(framework),
                   'stored_author_results_match':matching,'transient_mutant_sources_removed':not scratch.exists(),
                   'example_outputs_byte_identical':len(examples)==3 and len({(ROOT/e['stdout']).read_bytes() for e in examples})==1})
    (AUDIT/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ('successful','errors','subprocesses','author_method_counts','independent_counts','semantic_detections','framework_errors_correctly_classified')},sort_keys=True))
    return 0 if report['successful'] else 1

if __name__=='__main__':sys.exit(main())
