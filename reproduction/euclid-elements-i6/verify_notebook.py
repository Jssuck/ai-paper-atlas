"""Sequential compile/exec check, explicitly not Jupyter kernel or nbformat schema certification."""
import contextlib,io,json
from pathlib import Path

def main():
    p=Path('teaching.zh-CN.ipynb'); nb=json.loads(p.read_text());ns={};n=0; outputs=[]
    for cell in nb['cells']:
        if cell['cell_type']!='code':continue
        n+=1; out=io.StringIO()
        with contextlib.redirect_stdout(out):exec(compile(''.join(cell['source']),f'notebook-cell-{n}','exec'),ns)
        txt=out.getvalue();cell['execution_count']=n
        cell['outputs']=[dict(output_type='stream',name='stdout',text=txt.splitlines(True))] if txt else []
        outputs.append(txt)
    p.write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
    result=dict(code_cells=n,method='Python standard-library compile/exec, shared fresh namespace',jupyter_kernel=False,full_nbformat_schema_validation=False,outputs=outputs)
    Path('notebook-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
