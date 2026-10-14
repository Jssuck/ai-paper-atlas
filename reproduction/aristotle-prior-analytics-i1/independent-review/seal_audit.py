"""Bind final audit evidence by relative paths; does not rerun the review."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RELEASE=ROOT.parents[1]
REPOSITORY=RELEASE.parent

def record(path):
    data=path.read_bytes()
    return {'path':str(path.relative_to(REPOSITORY)),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
def main():
    runs=json.loads((ROOT/'independent-review/run-results.json').read_text())
    mutation=json.loads((ROOT/'independent-review/mutation-results.json').read_text())
    if not runs['passed'] or not mutation['passed']:
        raise RuntimeError('Cannot seal failing evidence')
    for name,digest in runs['run_finished_source_hashes'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:
            raise RuntimeError('Reviewed source changed: '+name)
    production_names=('logic.py','proofs.py','demo.py','test_model.py','verify.py','README.md',
                      'WALKTHROUGH.zh-CN.md','report.json','verification.txt')
    production=[record(ROOT/name) for name in production_names]
    evidence=[record(p) for p in sorted((ROOT/'independent-review').iterdir()) if p.is_file()]
    main=RELEASE/'papers/ancient/aristotle-prior-analytics-i1.zh-CN.md'
    output={'schema':'aristotle-i1-independent-code-audit-v1',
      'sealed_at_utc':datetime.now(timezone.utc).isoformat(),
      'status':'pass_after_repair','unresolved_code_blockers':[],
      'scope':'Modern unary A/E/I/O teaching semantics and limited proof certificate implementation; not a historical algorithm or general software-correctness proof.',
      'path_base':'repository_root/','reviewed_main':record(main),'reviewed_files':production,
      'audit_report':record(ROOT/'CODE-AUDIT.zh-CN.md'),'independent_evidence':evidence,
      'audited_artifacts':[record(main),*production,record(ROOT/'CODE-AUDIT.zh-CN.md'),*evidence],
      'mode_counts':{x['mode']:x['result']['counts'] for x in runs['runs']},
      'interpreter_modes':['normal','-O','-OO'],
      'nine_report_outputs_identical':runs['all_nine_report_outputs_identical'],
      'stored_report_matches':runs['stored_report_matches'],
      'mutations_detected':mutation['killed'],'mutations_total':mutation['total'],
      'finding':{'id':'I1-CODE-01','status':'fixed_and_retested',
                 'summary':'Revalidate frozen dataclass fields at public API boundaries; reject forged negative/bool indices and incomplete objects.'},
      'limitations':['Finite independent checks are not a general proof.',
                     'Python 3.12.14 Linux was run; minimum claimed Python 3.10 was not separately run.',
                     'Three-term nondefault policies use 180 two-premise samples each, not exhaustive problems.',
                     'No hostile-runtime sandbox, proof-search completeness, natural-language truth, or historical-perfectness claim.'],
      'self_hash_policy':'This JSON intentionally does not include its own hash; parent release manifest may bind it.'}
    path=ROOT/'code-audit.json'
    path.write_text(json.dumps(output,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
    # Re-read every bound file, including docs and log evidence, after writing.
    for entry in [output['reviewed_main'],*production,output['audit_report'],*evidence]:
        fresh=record(REPOSITORY/entry['path'])
        if fresh!=entry:
            raise RuntimeError('Bytes changed during seal: '+entry['path'])
    print(json.dumps({'passed':True,'bound_files':len(production)+len(evidence)+2,
                      'main_sha256':output['reviewed_main']['sha256'],
                      'audit_json_sha256':hashlib.sha256(path.read_bytes()).hexdigest()},sort_keys=True))
if __name__=='__main__':
    main()
