"""Execute notebook cells independently with CPython, in a disposable copy.

This deliberately does not import the author's notebook runner. It is not a
Jupyter kernel or nbformat schema validator. Prints a JSON audit to stdout.
"""
from pathlib import Path
import contextlib,hashlib,io,json,os,shutil,sys,tempfile
root=Path(__file__).resolve().parents[2]
notebook=root/'tutorial.ipynb'; data=json.loads(notebook.read_text())
assert data['nbformat']==4 and isinstance(data['cells'],list)
assert data['metadata']['kernelspec']['name']=='python3'
results=[]; saved_counts=[]
with tempfile.TemporaryDirectory(prefix='sylvester-review-') as temp:
    work=Path(temp)
    for source in root.glob('*.py'):shutil.copy2(source,work/source.name)
    shutil.copy2(notebook,work/notebook.name)
    if (root/'output').exists():shutil.copytree(root/'output',work/'output')
    previous=Path.cwd();os.chdir(work);sys.path.insert(0,str(work))
    namespace={'__name__':'__main__'}
    try:
        for index,cell in enumerate(data['cells']):
            assert isinstance(cell['source'],(list,str))
            text=''.join(cell['source']) if isinstance(cell['source'],list) else cell['source']
            if cell['cell_type']!='code':continue
            stdout,stderr=io.StringIO(),io.StringIO()
            with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr):
                exec(compile(text,f'notebook-cell-{index+1}','exec'),namespace)
            actual={'stdout':stdout.getvalue(),'stderr':stderr.getvalue()}
            expected={'stdout':'','stderr':''}; other=[]
            for out in cell['outputs']:
                if out['output_type']=='stream':expected[out['name']]+=''.join(out['text'])
                else:other.append(out['output_type'])
            assert not other,('non-stream output needs separate validation',other)
            assert actual==expected,{'cell':index+1,'actual':actual,'expected':expected}
            assert isinstance(cell['execution_count'],int) and cell['execution_count']>0
            saved_counts.append(cell['execution_count'])
            results.append({'cell':index+1,'execution_count':cell['execution_count'],
                            'stdout_matches_saved':True,'stderr_matches_saved':True})
        assert saved_counts==list(range(1,len(saved_counts)+1)),saved_counts
        assert results,'no code cells'
    finally:
        os.chdir(previous)
print(json.dumps({'status':'PASS','execution_engine':'CPython exec, shared cell namespace, fresh disposable copy',
 'not_jupyter_kernel':True,'not_official_nbformat_schema_validation':True,
 'notebook_sha256':hashlib.sha256(notebook.read_bytes()).hexdigest(),
 'code_cells_executed':len(results),'code_cells':results},indent=2))
