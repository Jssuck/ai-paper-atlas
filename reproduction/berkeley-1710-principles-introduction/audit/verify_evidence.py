"""Read-only verification of frozen reviewed bytes and real execution records."""
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]


def need(condition,message):
    if not condition: raise RuntimeError(message)


def read_json(path):return json.loads(path.read_text(encoding='utf-8'))


def main():
    review=read_json(ROOT/'audit/code_review.json')
    need(review['status']=='passed' and not review['open_defects'],'review is not passing')
    seen=set()
    for item in review['reviewed_inputs']+review['evidence_files']:
        path=item['path']
        need(not Path(path).is_absolute() and path not in seen,'absolute or duplicate bound path')
        need(path!='audit/code_review.json','self-binding cycle')
        seen.add(path)
        data=(ROOT/path).read_bytes()
        data.decode('utf-8')
        need(len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256'],'byte binding failed: '+path)
    author=read_json(ROOT/'results.json');environment=read_json(ROOT/'environment.json')
    audit=read_json(ROOT/'audit/results.json')
    need(author['successful'] is True and audit['successful'] is True,'unsuccessful stored execution')
    need(author['subprocesses_run']==len(author['runs'])==6,'author command count')
    need(audit['subprocesses']==len(audit['runs'])==90,'audit command count')
    for name,digest in environment['source_sha256'].items():
        need(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,'author source changed: '+name)
    for name,digest in audit['source_sha256'].items():
        need(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,'audit source changed: '+name)
    for run in author['runs']+audit['runs']:
        for stream in ('stdout','stderr'):need(run[stream] in seen,'unbound execution stream')
        need(read_json(ROOT/run['stdout'])==run['output'],'stored output does not match real stdout')
    tests=[r for r in author['runs'] if r['script']=='test_model.py']
    need({r['mode'] for r in tests}=={'normal','O','OO'},'missing interpreter mode')
    need(all(r['returncode']==0 and r['output']['tests_run']==52 and r['output']['failures']==r['output']['errors']==r['output']['skipped']==0 and r['output']['successful'] is True for r in tests),'author suite details')
    expected_cases={'distributivity_assignments':125,'normalization_tree_assignments':1445,'simultaneous_substitution_assignments':125}
    need(all(r['output']['finite_case_groups_attempted']==expected_cases for r in tests),'author finite counts')
    need(audit['semantic_mutants_per_mode']==13 and len(audit['semantic_mutants'])==audit['semantic_detections']==39,'semantic mutation count')
    for mutant in audit['semantic_mutants']:
        need(mutant['detected_semantically'] is True,'undetected mutant')
        need(read_json(ROOT/mutant['stdout'])['status']=='semantic_failure','mutation crash mistaken for semantic failure')
    need(audit['framework_errors_correctly_classified']==3,'framework classification count')
    need(audit['stored_author_results_match'] is True and audit['example_outputs_byte_identical'] is True,'cross-run output mismatch')
    need(audit['transient_mutant_sources_removed'] is True and not (ROOT/'audit/_mutation').exists(),'transient mutation files remain')
    need(not list(ROOT.rglob('__pycache__')),'bytecode caches remain in delivery')
    print(json.dumps({'status':'passed','bound_files':len(seen),'author_subprocesses':6,'audit_subprocesses':90,'semantic_detections':39,'framework_error_probes':3,'verification':'read-only SHA-256/byte/log verification; no tests rerun'},sort_keys=True))
    return 0

if __name__=='__main__':
    try:sys.exit(main())
    except Exception as error:
        print(json.dumps({'status':'failed','error':str(error)},sort_keys=True))
        sys.exit(1)
