"""Validate the restricted notebook structure and the presence of executed output."""
import json
from pathlib import Path


def validate(path='tutorial.ipynb'):
    doc=json.loads(Path(path).read_text(encoding='utf-8'))
    assert doc['nbformat']==4
    ids=[c['id'] for c in doc['cells']]
    assert len(ids)==len(set(ids))
    code=[c for c in doc['cells'] if c['cell_type']=='code']
    for i,c in enumerate(code,1):
        assert c['execution_count']==i
        assert isinstance(c['source'],list) and all(isinstance(s,str) for s in c['source'])
        compile(''.join(c['source']),f'cell-{i}','exec')
        assert c['outputs'], f'Cell {i} has no recorded demonstration output'
        assert not any(o['output_type']=='error' for o in c['outputs'])
    assert 'not a Jupyter kernel' in doc['metadata']['execution_note']
    result={'nbformat':doc['nbformat'],'nbformat_minor':doc['nbformat_minor'],
            'cells':len(doc['cells']),'code_cells':len(code),'all_executed_in_order':True,
            'error_outputs':0,'execution_mode':'CPython exec; not Jupyter kernel',
            'validation':'Restricted JSON/structure/output validation; nbformat package not installed'}
    return result


if __name__=='__main__':
    result=validate()
    print(json.dumps(result,ensure_ascii=False,indent=2))
    Path('evidence/notebook-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
