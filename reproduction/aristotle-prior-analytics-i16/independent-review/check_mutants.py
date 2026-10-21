"""Selected literal mutations run only in isolated temporary directories."""
import json,pathlib,subprocess,sys,tempfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
source=(ROOT/'model.py').read_text()
mutations={
 'actual_zero':('world = self.actual if world is None else world','world = 0 if world is None else world'),
 'K_weak':("'K': any(signs) and not all(signs)","'K': any(signs)"),
 'Nplus_possible':("'N+': all(signs)","'N+': any(signs)"),
 'Nminus_weak':("'N-': not any(signs)","'N-': not all(signs)"),
 'some_all':("return all(answers) if quantity == 'all' else any(answers)","return all(answers)"),
 'drop_reverse_negative':("return self.modal(predicate, subject, 'N-') and self.modal(subject, predicate, 'N-')","return self.modal(predicate, subject, 'N-')"),
 'stable_only_actual':('for w in range(len(self.worlds)))\n\n    def jointly_possible','for w in (self.actual,))\n\n    def jointly_possible'),
 'accept_bool_size':('type(self.n) is not int','not isinstance(self.n, int)'),
 'E_is_I':("'E': not bool(s & p)","'E': bool(s & p)"),
}
results=[]
for name,(old,new) in mutations.items():
    if source.count(old)!=1:raise RuntimeError(('mutation site',name,source.count(old)))
    with tempfile.TemporaryDirectory(prefix='i16-mutant-') as tmp:
        p=pathlib.Path(tmp);(p/'model.py').write_text(source.replace(old,new))
        (p/'test_model.py').write_text((ROOT/'test_model.py').read_text())
        modes=[]
        for flag in ('','-O','-OO'):
            cmd=[sys.executable]+([flag] if flag else [])+['-m','unittest','-v']
            r=subprocess.run(cmd,cwd=p,text=True,capture_output=True)
            output=r.stdout+r.stderr
            if r.returncode==0 or not ('FAIL:' in output or 'ERROR:' in output):raise RuntimeError(('undetected',name,flag,output))
            if 'SyntaxError' in output or 'ImportError' in output:raise RuntimeError(('invalid mutant',name,output))
            modes.append({'mode':flag or 'normal','exit':r.returncode,'failures':[line for line in output.splitlines() if line.startswith(('FAIL:','ERROR:'))]})
        results.append({'name':name,'modes':modes})
print(json.dumps({'selected_mutants':len(results),'all_detected':True,'results':results},indent=2))
