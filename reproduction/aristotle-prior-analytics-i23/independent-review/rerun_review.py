import pathlib,sys,subprocess,json,hashlib,datetime
p=pathlib.Path(__file__).resolve().parents[1]; out=p/'independent-review'
records=[]
for label,opts in [('normal',[]),('opt',['-O']),('opt2',['-OO'])]:
  lines=['UTC '+datetime.datetime.now(datetime.timezone.utc).isoformat()+'\n',sys.version+'\n']
  for script,target in [('test_model.py',None),('run_examples.py',f'author-rerun-{label}.json'),('independent-review/independent_check.py',f'results-{label}.json')]:
    cmd=[sys.executable,*opts,script];lines.append('$ '+' '.join(cmd)+'\n');r=subprocess.run(cmd,cwd=p,text=True,capture_output=True);lines.append(r.stdout+r.stderr);lines.append(f'EXIT {r.returncode}\n')
    if r.returncode: raise RuntimeError('review failed '+label+script+r.stderr)
    if target:(out/target).write_text(r.stdout)
    if script=='run_examples.py':
      old=json.loads((p/'logs'/f'results-{label}.json').read_text());new=json.loads(r.stdout)
      if old!=new:raise RuntimeError('author original mismatch')
      lines.append('AUTHOR_SAVED_JSON_EXACTLY_MATCHED\n')
  (out/f'run-{label}.log').write_text(''.join(lines))
manifest=json.loads((p/'author-manifest.json').read_text())
for name,expected in manifest['sha256'].items():
  if hashlib.sha256((p/name).read_bytes()).hexdigest()!=expected:raise RuntimeError('author manifest mismatch '+name)
print('AUTHOR_MANIFEST_11_FILES_VERIFIED')
print('ALL_THREE_MODES_PASSED')
