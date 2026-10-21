"""Selected mutation checks of the author's unittest suite; no exhaustive claim."""
from pathlib import Path
import tempfile,subprocess,sys,json,hashlib
root=Path(__file__).resolve().parents[1]
source=(root/'model.py').read_text();tests=(root/'test_model.py').read_text()
mutants={
 'drop_final_endpoint_check':("return proof[-1].formula.predicate == major.predicate and proof[-1].formula.subject == minor.subject","return True"),
 'all_subjects_become_existential':("return subject & ~contingent == 0 if mode in ('a', 'e') else bool(subject & contingent)","return bool(subject & contingent)"),
 'possible_excludes_necessary':("return result\n    def contingent_set", "return self.contingent_set(term)\n    def contingent_set"),
 'contingency_includes_necessity':("return either & ~both","return either"),
 'wrong_base_quantity':("('a', 'i'): 'i'","('a', 'i'): 'a'"),
 'quality_swaps_terms':("return Proposition(DUAL[self.mode], self.predicate, self.subject)","return Proposition(DUAL[self.mode], self.subject, self.predicate)"),
 'ignore_actual_index':("return self.column(term)[self.actual]","return self.column(term)[0]"),
 'accept_bool_references':("type(r) is not int or not 0 <= r < i","not isinstance(r,int) or not 0 <= r < i")
}
report={'model_sha256':hashlib.sha256(source.encode()).hexdigest(),'tests_sha256':hashlib.sha256(tests.encode()).hexdigest(),'mutants':[]}
for name,(before,after) in mutants.items():
    if source.count(before)!=1:raise RuntimeError('mutation anchor not unique: '+name)
    with tempfile.TemporaryDirectory(prefix='i14-mutation-') as d:
        p=Path(d);(p/'model.py').write_text(source.replace(before,after));(p/'test_model.py').write_text(tests)
        r=subprocess.run([sys.executable,'-m','unittest','-q','test_model'],cwd=d,text=True,capture_output=True)
        report['mutants'].append({'name':name,'exit_code':r.returncode,'detected':r.returncode!=0,'stderr_tail':r.stderr[-1600:]})
print(json.dumps(report,ensure_ascii=False,indent=2))
if not all(x['detected'] for x in report['mutants']):sys.exit(1)
